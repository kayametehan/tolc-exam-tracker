#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOLC CENT@home Takip Botu
Versiyon: 2.0.0
Yazar: TOLC Bot
Açıklama: İtalyan TOLC CENT@home sınavlarını takip eden gelişmiş Telegram botu
"""

import os
import sys
import time
import signal
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import hashlib

# Windows encoding fix
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Versiyon bilgisi
VERSION = "2.0.0"
BOT_NAME = "TOLC CENT@home Tracker"

# Konfigürasyon
load_dotenv()

# Zorunlu ayarlar kontrolü
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == 'your_bot_token_here':
    print("HATA: TELEGRAM_BOT_TOKEN ayarlanmamış!")
    print("Lütfen .env dosyasını düzenleyin ve bot token'ınızı girin.")
    sys.exit(1)

if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == 'your_chat_id_here':
    print("HATA: TELEGRAM_CHAT_ID ayarlanmamış!")
    print("Lütfen .env dosyasını düzenleyin ve chat ID'nizi girin.")
    sys.exit(1)

# Opsiyonel ayarlar
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '300'))
NOTIFICATION_SOUND = os.getenv('NOTIFICATION_SOUND', 'yes').lower() == 'yes'
VERBOSE_LOGGING = os.getenv('VERBOSE_LOGGING', 'no').lower() == 'yes'
NOTIFY_ON_ERROR = os.getenv('NOTIFY_ON_ERROR', 'no').lower() == 'yes'
HEARTBEAT_INTERVAL = int(os.getenv('HEARTBEAT_INTERVAL', '3600'))  # 1 saat
TEST_MODE = os.getenv('TEST_MODE', 'no').lower() == 'yes'
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))

URLS = [
    'https://testcisia.it/calendario.php?tolc=cents&lingua=inglese',  # İngilizce
    'https://testcisia.it/calendario.php?tolc=cents&lingua=italiano'  # İtalyanca
]

# Log klasörü oluştur
LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

# Logging ayarları
log_level = logging.DEBUG if VERBOSE_LOGGING else logging.INFO
log_format = '%(asctime)s - [%(levelname)s] - %(funcName)s - %(message)s'

# StreamHandler için encoding ayarı
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(log_format))

logging.basicConfig(
    level=log_level,
    format=log_format,
    handlers=[
        logging.FileHandler(
            LOG_DIR / f'tolc_bot_{datetime.now().strftime("%Y%m%d")}.log',
            encoding='utf-8'
        ),
        stream_handler
    ]
)
logger = logging.getLogger(__name__)

# Durum dosyaları
STATE_FILE = LOG_DIR / 'bot_state.json'
HISTORY_FILE = LOG_DIR / 'exam_history.json'

# Global değişkenler
shutdown_requested = False

# İstatistikler
stats = {
    'version': VERSION,
    'total_checks': 0,
    'successful_checks': 0,
    'failed_checks': 0,
    'notifications_sent': 0,
    'exams_found': 0,
    'last_available': None,
    'last_heartbeat': None,
    'start_time': datetime.now().isoformat(),
    'uptime_seconds': 0
}

def signal_handler(signum, frame):
    """Sinyal yakalayıcı - Temiz kapanış için"""
    global shutdown_requested
    logger.info(f"Sinyal alındı: {signum}. Temiz kapanış başlatılıyor...")
    shutdown_requested = True

def validate_config() -> bool:
    """Konfigürasyonu doğrula"""
    logger.info(" Konfigürasyon doğrulanıyor...")
    
    issues = []
    
    if CHECK_INTERVAL < 60:
        issues.append("CHECK_INTERVAL çok düşük (min: 60 saniye)")
    
    if CHECK_INTERVAL > 3600:
        issues.append("CHECK_INTERVAL çok yüksek (max: 3600 saniye)")
    
    if issues:
        for issue in issues:
            logger.warning(issue)
        return False
    
    logger.info(" Konfigürasyon geçerli")
    return True

def test_telegram_connection() -> bool:
    """Telegram bağlantısını test et"""
    logger.info(" Telegram bağlantısı test ediliyor...")
    
    try:
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('ok'):
            bot_info = data.get('result', {})
            logger.info(f"Telegram baglantisi basarili: @{bot_info.get('username')}")
            return True
        else:
            logger.error(f" Telegram API hatası: {data}")
            return False
            
    except Exception as e:
        logger.error(f" Telegram bağlantı hatası: {e}")
        return False

def test_website_access() -> bool:
    """Web sitelerine erişimi test et"""
    logger.info(" Web siteleri test ediliyor...")
    
    all_ok = True
    for url in URLS:
        lang = 'İngilizce' if 'inglese' in url else 'İtalyanca'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            logger.info(f"{lang} sitesi erisilebilir")
        except Exception as e:
            logger.error(f"{lang} sitesi erisilemedi: {e}")
            all_ok = False
    
    return all_ok

def load_state() -> Dict:
    """Önceki durumu yükle"""
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
                logger.info(f"Durum dosyasi yuklendi: {STATE_FILE}")
                return state
    except Exception as e:
        logger.warning(f"️ Durum dosyası yüklenemedi: {e}")
    return {}

def save_state(state: Dict) -> None:
    """Durumu kaydet"""
    try:
        state['last_update'] = datetime.now().isoformat()
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        logger.debug(f" Durum kaydedildi: {STATE_FILE}")
    except Exception as e:
        logger.error(f" Durum dosyası kaydedilemedi: {e}")

def load_history() -> List[Dict]:
    """Sınav geçmişini yükle"""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"️ Geçmiş dosyası yüklenemedi: {e}")
    return []

def save_to_history(exam: Dict) -> None:
    """Sınavı geçmişe kaydet"""
    try:
        history = load_history()
        
        # Hash ile tekrar kontrolü
        exam_hash = hashlib.md5(
            f"{exam['lang']}_{exam['date_info']}".encode()
        ).hexdigest()
        
        # Aynı sınav daha önce kaydedilmiş mi?
        if not any(h.get('hash') == exam_hash for h in history):
            exam['hash'] = exam_hash
            exam['recorded_at'] = datetime.now().isoformat()
            history.append(exam)
            
            # Son 100 kaydı tut
            history = history[-100:]
            
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Sinav gecmise kaydedildi: {exam_hash}")
    except Exception as e:
        logger.error(f" Geçmiş kaydedilemedi: {e}")

def send_telegram_message(message: str, disable_notification: bool = False, retry: int = 0) -> Optional[Dict]:
    """Telegram'a mesaj gönder (retry mekanizması ile)"""
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'disable_notification': disable_notification or not NOTIFICATION_SOUND,
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get('ok'):
            stats['notifications_sent'] += 1
            logger.info(" Telegram mesajı gönderildi")
            return result
        else:
            logger.error(f" Telegram API hatası: {result}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f" Telegram bağlantı hatası: {e}")
        
        # Retry mekanizması
        if retry < MAX_RETRIES:
            wait_time = (retry + 1) * 2
            logger.info(f"{wait_time} saniye sonra tekrar denenecek... ({retry + 1}/{MAX_RETRIES})")
            time.sleep(wait_time)
            return send_telegram_message(message, disable_notification, retry + 1)
        
        return None
    except Exception as e:
        logger.error(f" Beklenmeyen Telegram hatası: {e}")
        return None

def send_heartbeat() -> None:
    """Heartbeat mesajı gönder - Bot çalıştığını gösterir"""
    try:
        uptime = datetime.now() - datetime.fromisoformat(stats['start_time'])
        hours = int(uptime.total_seconds() // 3600)
        
        message = f"""<b>Heartbeat - Bot Aktif</b>

Çalışma süresi: {hours} saat
Toplam kontrol: {stats['total_checks']}
Başarılı: {stats['successful_checks']}
📊 Başarı oranı: {(stats['successful_checks'] / stats['total_checks'] * 100) if stats['total_checks'] > 0 else 0:.1f}%
Bulunan sınav: {stats['exams_found']}

Bot sorunsuz çalışıyor! ✨"""
        
        send_telegram_message(message, disable_notification=True)
        stats['last_heartbeat'] = datetime.now().isoformat()
        logger.info(" Heartbeat gönderildi")
        
    except Exception as e:
        logger.error(f" Heartbeat hatası: {e}")

def check_availability() -> Tuple[bool, List[Dict]]:
    """Sınav yerlerini kontrol et (gelişmiş hata yönetimi ile)"""
    all_available_exams = []
    errors = []
    
    stats['total_checks'] += 1
    check_start_time = time.time()
    
    for url in URLS:
        lang = 'İngilizce' if 'inglese' in url else 'İtalyanca'
        retry_count = 0
        
        while retry_count <= MAX_RETRIES:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                logger.debug(f" Kontrol ediliyor: {lang} - {url} (Deneme: {retry_count + 1})")
                
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                # İçerik kontrolü
                if len(response.content) < 1000:
                    raise ValueError("Sayfa içeriği çok kısa, geçersiz yanıt olabilir")
                
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Tüm sınav satırlarını kontrol et
                rows = soup.find_all('tr')
                logger.debug(f" {lang} sitesinde {len(rows)} satır bulundu")
                
                if len(rows) == 0:
                    logger.warning(f"️ {lang} sitesinde tablo bulunamadı")
                
                for row in rows:
                    text = row.get_text().lower()
                    
                    # CENT@home içeren satırları kontrol et
                    if 'cent@home' in text or 'cent @ home' in text:
                        logger.debug(f" CENT@home satırı bulundu: {text[:100]}")
                        
                        # Negatif durumları kontrol et (genişletilmiş liste)
                        negative_phrases = [
                            'artık geçerli değil',
                            'artık yer ayırtılamaz',
                            'non più valido',
                            'non è più possibile prenotare',
                            'no longer valid',
                            'no longer possible to book',
                            'scaduto',
                            'expired',
                            'completo',
                            'full',
                            'chiuso',
                            'closed',
                            'terminato',
                            'finished'
                        ]
                        
                        has_negative = any(phrase in text for phrase in negative_phrases)
                        
                        if not has_negative:
                            # Pozitif durum - yer var!
                            exam_info = row.get_text(strip=True)
                            
                            # Tarih bilgisini çıkar
                            date_info = "Tarih bilgisi bulunamadı"
                            cells = row.find_all(['td', 'th'])
                            if cells:
                                date_info = ' | '.join([cell.get_text(strip=True) for cell in cells[:3]])
                            
                            exam_data = {
                                'info': exam_info,
                                'date_info': date_info,
                                'lang': lang,
                                'url': url,
                                'found_at': datetime.now().isoformat()
                            }
                            
                            all_available_exams.append(exam_data)
                            stats['exams_found'] += 1
                            
                            # Geçmişe kaydet
                            save_to_history(exam_data)
                            
                            logger.info(f"Yer bulundu! ({lang}): {date_info}")
                
                stats['successful_checks'] += 1
                break  # Başarılı, döngüden çık
            
            except requests.exceptions.Timeout:
                error_msg = f"Zaman aşımı ({lang})"
                logger.warning(error_msg)
                retry_count += 1
                if retry_count <= MAX_RETRIES:
                    time.sleep(2 * retry_count)
                else:
                    errors.append(error_msg)
                    stats['failed_checks'] += 1
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Bağlantı hatası ({lang}): {str(e)}"
                logger.error(error_msg)
                retry_count += 1
                if retry_count <= MAX_RETRIES:
                    time.sleep(2 * retry_count)
                else:
                    errors.append(error_msg)
                    stats['failed_checks'] += 1
                    
            except Exception as e:
                error_msg = f"Kontrol hatası ({lang}): {str(e)}"
                logger.error(error_msg, exc_info=VERBOSE_LOGGING)
                retry_count += 1
                if retry_count <= MAX_RETRIES:
                    time.sleep(2 * retry_count)
                else:
                    errors.append(error_msg)
                    stats['failed_checks'] += 1
    
    check_duration = time.time() - check_start_time
    logger.debug(f"Kontrol süresi: {check_duration:.2f} saniye")
    
    # Hata bildirimi
    if errors and NOTIFY_ON_ERROR:
        error_message = f"<b>Kontrol Hatası</b>\n\n"
        error_message += f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        error_message += "\n".join(errors)
        error_message += f"\n\nSonraki kontrol: {CHECK_INTERVAL} saniye sonra"
        send_telegram_message(error_message, disable_notification=True)
    
    return len(all_available_exams) > 0, all_available_exams

def format_stats():
    """İstatistikleri formatla"""
    uptime = datetime.now() - datetime.fromisoformat(stats['start_time'])
    hours = int(uptime.total_seconds() // 3600)
    minutes = int((uptime.total_seconds() % 3600) // 60)
    
    success_rate = (stats['successful_checks'] / stats['total_checks'] * 100) if stats['total_checks'] > 0 else 0
    
    return f"""
📊 <b>İstatistikler</b>
Çalışma süresi: {hours}s {minutes}d
Toplam kontrol: {stats['total_checks']}
Başarılı: {stats['successful_checks']}
Başarısız: {stats['failed_checks']}
📨 Bildirim: {stats['notifications_sent']}
📈 Başarı oranı: {success_rate:.1f}%
"""

def format_stats() -> str:
    """İstatistikleri formatla"""
    uptime = datetime.now() - datetime.fromisoformat(stats['start_time'])
    hours = int(uptime.total_seconds() // 3600)
    minutes = int((uptime.total_seconds() % 3600) // 60)
    
    success_rate = (stats['successful_checks'] / stats['total_checks'] * 100) if stats['total_checks'] > 0 else 0
    
    return f"""
📊 <b>İstatistikler</b>
━━━━━━━━━━━━━━━━━━━━
Çalışma süresi: {hours}s {minutes}d
Toplam kontrol: {stats['total_checks']}
Başarılı: {stats['successful_checks']}
Başarısız: {stats['failed_checks']}
📨 Bildirim: {stats['notifications_sent']}
Bulunan sınav: {stats['exams_found']}
📈 Başarı oranı: {success_rate:.1f}%
━━━━━━━━━━━━━━━━━━━━
Versiyon: {VERSION}
"""

def safe_print(text: str) -> None:
    """Güvenli print - Windows encoding sorunlarını önler"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Emoji'leri kaldır ve tekrar dene
        import re
        text_no_emoji = re.sub(r'[^\x00-\x7F]+', '', text)
        print(text_no_emoji)

def main():
    """Ana döngü"""
    global shutdown_requested
    
    # Sinyal yakalayıcıları ayarla (Windows'ta SIGTERM yok)
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    
    # Banner
    safe_print("=" * 70)
    safe_print(f"{BOT_NAME} v{VERSION}")
    safe_print("=" * 70)
    
    logger.info("=" * 70)
    logger.info(f"Bot {BOT_NAME} v{VERSION} baslatildi")
    logger.info("=" * 70)
    
    # Konfigürasyon doğrulama
    if not validate_config():
        logger.warning("Konfigurasyon uyarilari var, devam ediliyor...")
    
    # Bağlantı testleri
    if not test_telegram_connection():
        logger.error("Telegram baglantisi basarisiz! Bot durduruluyor.")
        sys.exit(1)
    
    if not test_website_access():
        logger.warning("Bazi web sitelerine erisilemiyor, devam ediliyor...")
    
    # Ayarları logla
    logger.info(f"� Kontrol edilen siteler:")
    for url in URLS:
        lang = 'Ingilizce' if 'inglese' in url else 'Italyanca'
        logger.info(f"   - {lang}: {url}")
    logger.info(f"Kontrol araligi: {CHECK_INTERVAL} saniye")
    logger.info(f"Heartbeat araligi: {HEARTBEAT_INTERVAL} saniye")
    logger.info(f"Bildirim sesi: {'Acik' if NOTIFICATION_SOUND else 'Kapali'}")
    logger.info(f"Detayli log: {'Acik' if VERBOSE_LOGGING else 'Kapali'}")
    logger.info(f"Hata bildirimi: {'Acik' if NOTIFY_ON_ERROR else 'Kapali'}")
    logger.info(f"Maksimum retry: {MAX_RETRIES}")
    logger.info(f"Test modu: {'Acik' if TEST_MODE else 'Kapali'}")
    logger.info("=" * 70)
    
    # Önceki durumu yükle
    state = load_state()
    last_status = state.get('last_available', False)
    last_heartbeat_time = datetime.now()
    
    # Başlangıç mesajı
    start_msg = f"""🚀 <b>{BOT_NAME} Başlatıldı</b>

Versiyon: {VERSION}
İngilizce ve İtalyanca siteler kontrol ediliyor
Kontrol aralığı: {CHECK_INTERVAL} saniye
Heartbeat: Her {HEARTBEAT_INTERVAL // 60} dakikada bir
Bildirim: {'Açık' if NOTIFICATION_SOUND else 'Sessiz'}
� Otomatik retry: {MAX_RETRIES} deneme

✨ Bot başarıyla başlatıldı ve çalışıyor!"""
    
    send_telegram_message(start_msg, disable_notification=True)
    
    consecutive_errors = 0
    max_consecutive_errors = 5
    
    # Test modu
    if TEST_MODE:
        logger.info("TEST MODU: Tek kontrol yapilip cikilacak")
        available, exams = check_availability()
        logger.info(f"Test sonucu: {'Yer var' if available else 'Yer yok'} ({len(exams)} sinav)")
        return
    
    while not shutdown_requested:
        try:
            logger.info(f"� Kontrol başlatılıyor... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
            
            available, exams = check_availability()
            
            if available and not last_status:
                # Yeni yer açıldı!
                stats['last_available'] = datetime.now().isoformat()
                
                message = "🎉🎉🎉 <b>YER AÇILDI!</b> 🎉🎉🎉\n\n"
                message += f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                message += f"━━━━━━━━━━━━━━━━━━━━\n\n"
                message += f"<b>CENT@home sınavında {len(exams)} yer mevcut:</b>\n\n"
                
                for i, exam in enumerate(exams, 1):
                    message += f"<b>{i}. {exam['lang']}</b>\n"
                    message += f"📅 {exam['date_info']}\n"
                    message += f"🔗 <a href=\"{exam['url']}\">Hemen kayıt ol!</a>\n\n"
                
                message += "━━━━━━━━━━━━━━━━━━━━\n"
                message += "⚡ <b>Hızlı ol, yerler çabuk dolabilir!</b>"
                
                send_telegram_message(message)
                logger.info(f"Yer bulundu! {len(exams)} sinav icin bildirim gonderildi.")
                last_status = True
                consecutive_errors = 0
                
                # Durumu kaydet
                save_state({
                    'last_available': True,
                    'last_check': datetime.now().isoformat(),
                    'exams_count': len(exams)
                })
            
            elif not available and last_status:
                # Yerler doldu
                message = "<b>Yerler Doldu</b>\n\n"
                message += f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
                message += "CENT@home sınavlarında şu an yer yok.\n"
                message += "Takip devam ediyor..."
                
                send_telegram_message(message, disable_notification=True)
                last_status = False
                logger.info("Yerler doldu, takip devam ediyor.")
                
                save_state({
                    'last_available': False,
                    'last_check': datetime.now().isoformat()
                })
            
            elif available:
                logger.info(f"Hala yer mevcut ({len(exams)} sinav)")
            else:
                logger.info("Yer yok, takip devam ediyor")
            
            # Heartbeat kontrolü
            if (datetime.now() - last_heartbeat_time).total_seconds() >= HEARTBEAT_INTERVAL:
                send_heartbeat()
                last_heartbeat_time = datetime.now()
            
            consecutive_errors = 0
            
            # Bekleme
            for i in range(CHECK_INTERVAL):
                if shutdown_requested:
                    break
                time.sleep(1)
            
        except KeyboardInterrupt:
            logger.info("\n\nBot durduruldu (Kullanici istegi - Ctrl+C)")
            shutdown_requested = True
            
        except Exception as e:
            consecutive_errors += 1
            logger.error(f"Beklenmeyen hata: {e}", exc_info=True)
            
            if consecutive_errors >= max_consecutive_errors:
                error_msg = f"""🚨 <b>Kritik Hata!</b>

Art arda {max_consecutive_errors} hata oluştu.
Bot güvenlik nedeniyle durduruluyor.

Son hata: {str(e)[:200]}

{format_stats()}"""
                send_telegram_message(error_msg)
                logger.critical(f"Kritik hata limiti aşıldı, bot durduruluyor")
                break
            
            # Hata sonrası bekleme
            wait_time = min(CHECK_INTERVAL, 60 * consecutive_errors)
            logger.info(f"{wait_time} saniye bekleniyor...")
            time.sleep(wait_time)
    
    # Temiz kapanış
    logger.info("Bot kapatiliyor...")
    
    # Son istatistikler
    stats['uptime_seconds'] = (datetime.now() - datetime.fromisoformat(stats['start_time'])).total_seconds()
    
    stop_msg = f"""<b>Bot Durduruldu</b>

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

{format_stats()}

Görüşmek üzere! 👋"""
    
    send_telegram_message(stop_msg, disable_notification=True)
    
    # Son durumu kaydet
    save_state({
        'last_available': last_status,
        'last_check': datetime.now().isoformat(),
        'shutdown_time': datetime.now().isoformat(),
        'stats': stats
    })
    
    logger.info("=" * 70)
    logger.info("Bot basariyla kapatildi")
    logger.info("=" * 70)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(f"Kritik hata: {e}", exc_info=True)
        sys.exit(1)
