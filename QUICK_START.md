# 🚀 Hızlı Başlangıç Rehberi

## ✅ Bot Başarıyla Kuruldu!

Test sonuçları:
- ✅ Telegram bağlantısı başarılı
- ✅ Web sitelerine erişim başarılı
- ✅ Tüm bağımlılıklar yüklü
- ✅ Konfigürasyon geçerli

## 📝 Şimdi Ne Yapmalısın?

### 1. Test Modunu Kapat

`.env` dosyasında:
```bash
TEST_MODE=no  # Zaten kapalı olmalı
```

### 2. Bot'u Çalıştır

**Ön Planda (Test için):**
```bash
python3 tolc_bot.py
```
Ctrl+C ile durdurabilirsin.

**Arka Planda (Sürekli çalışması için):**

**macOS/Linux - Screen ile:**
```bash
screen -S tolc_bot
python3 tolc_bot.py
# Ctrl+A+D ile detach (arka plana al)

# Geri dönmek için:
screen -r tolc_bot
```

**macOS/Linux - nohup ile:**
```bash
nohup python3 tolc_bot.py > bot.log 2>&1 &

# Durdurmak için:
ps aux | grep tolc_bot.py
kill <PID>
```

**Windows - Başlangıçta Otomatik Çalıştır:**
1. `start_bot.bat` dosyasına sağ tıkla
2. "Kısayol Oluştur"
3. Kısayolu şuraya taşı: `shell:startup`
4. Bilgisayar açıldığında otomatik başlayacak

### 3. Bot'u İzle

**Telegram'dan:**
- Bot başladığında bildirim gelecek
- Her saat "heartbeat" mesajı gelecek
- Yer açıldığında anında bildirim gelecek

**Loglardan:**
```bash
# Son logları görüntüle
tail -f logs/tolc_bot_*.log

# Hataları filtrele
grep ERROR logs/tolc_bot_*.log
```

## 🎯 Bot Ne Yapıyor?

1. **Her 5 dakikada bir** (300 saniye) siteleri kontrol eder
2. **İngilizce ve İtalyanca** siteleri tarar
3. **CENT@home** sınavlarını arar
4. **Yer açıldığında** Telegram'dan bildirim gönderir
5. **Her saat** "bot çalışıyor" mesajı gönderir

## 📊 Beklenen Davranış

### Normal Durum (Yer Yok)
```
2026-02-28 03:02:16 - Kontrol baslatiliyor...
2026-02-28 03:02:17 - Yer yok, takip devam ediyor
```

### Yer Açıldığında
```
2026-02-28 03:02:16 - Kontrol baslatiliyor...
2026-02-28 03:02:17 - Yer bulundu! 2 sinav icin bildirim gonderildi.
```

Telegram'dan şöyle bir mesaj gelecek:
```
🎉🎉🎉 YER AÇILDI! 🎉🎉🎉

⏰ 28/02/2026 03:02:17
━━━━━━━━━━━━━━━━━━━━

CENT@home sınavında 2 yer mevcut:

1. İngilizce
📅 [Tarih bilgisi]
🔗 Hemen kayıt ol!

━━━━━━━━━━━━━━━━━━━━
⚡ Hızlı ol, yerler çabuk dolabilir!
```

## ⚙️ Ayarları Değiştir

`.env` dosyasını düzenle:

```bash
# Daha sık kontrol et (2 dakika)
CHECK_INTERVAL=120

# Heartbeat'i kapat (0 = kapalı)
HEARTBEAT_INTERVAL=0

# Bildirimleri sessiz yap
NOTIFICATION_SOUND=no

# Hata bildirimi aç
NOTIFY_ON_ERROR=yes

# Detaylı log aç (debugging için)
VERBOSE_LOGGING=yes
```

Değişiklikten sonra bot'u yeniden başlat.

## 🔧 Sorun Giderme

### Bot durdu mu?
```bash
# Process kontrolü
ps aux | grep tolc_bot.py

# Screen kontrolü
screen -ls

# Son log
tail -20 logs/tolc_bot_*.log
```

### Heartbeat gelmiyor
- Bot çökmüş olabilir, logları kontrol et
- Veya HEARTBEAT_INTERVAL çok yüksek

### Bildirim gelmiyor
- NOTIFICATION_SOUND=no ise sessiz gelir
- Bot çalışıyor mu kontrol et
- Telegram token/chat ID doğru mu kontrol et

### Çok fazla hata
```bash
# Detaylı log aç
VERBOSE_LOGGING=yes

# Hata bildirimi aç
NOTIFY_ON_ERROR=yes
```

## 📱 Telegram Komutları

Bot'a şu mesajları gönderebilirsin:
- `/start` - Bot'u başlat
- `/status` - Durum bilgisi (şu an desteklenmiyor, gelecek versiyonda)

## 🎓 Sınav Bulunduğunda

1. **Hemen** Telegram bildirimini kontrol et
2. **Linke tıkla** ve kayıt sayfasına git
3. **Hızlı ol** - yerler çabuk dolabilir
4. Bot yer dolduğunda da bildirim gönderecek

## 📈 İstatistikler

Bot durdurulduğunda şöyle bir özet gelir:

```
👋 Bot Durduruldu

⏰ 28/02/2026 15:30:00

📊 İstatistikler
━━━━━━━━━━━━━━━━━━━━
⏱️ Çalışma süresi: 12s 30d
🔍 Toplam kontrol: 3600
✅ Başarılı: 3598
❌ Başarısız: 2
📨 Bildirim: 15
🎯 Bulunan sınav: 5
📈 Başarı oranı: 99.9%
━━━━━━━━━━━━━━━━━━━━
🤖 Versiyon: 2.0.0

Görüşmek üzere! 👋
```

## 🚀 Sunucuda Çalıştırma

VPS veya cloud server'da sürekli çalıştırmak için:

**Systemd Service (Linux):**
```bash
sudo nano /etc/systemd/system/tolc-bot.service
```

Detaylar için: `DEPLOYMENT.md`

## 💡 İpuçları

1. **Kontrol aralığını çok düşük yapma** - Site'yi spam'leme
2. **Logları düzenli kontrol et** - Sorunları erken yakala
3. **Heartbeat'i aç** - Bot çalışıyor mu anlamak için
4. **Arka planda çalıştır** - Screen veya systemd kullan
5. **Yedek al** - `.env` dosyasını güvenli tut

## 📞 Destek

- GitHub Issues: https://github.com/kayametehan/tolc-exam-tracker/issues
- README: https://github.com/kayametehan/tolc-exam-tracker

---

**Başarılar! Bot artık sınavları takip ediyor! 🎓✨**

Yer açıldığında Telegram'dan bildirim alacaksın!
