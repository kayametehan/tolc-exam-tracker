# TOLC CENT@home Takip Botu 🎓

İtalyan TOLC CENT@home sınavlarında yer açıldığında Telegram'dan bildirim gönderen profesyonel bot.

## Özellikler ✨

### Temel Özellikler
- ✅ Hem İngilizce hem İtalyanca siteleri kontrol eder
- 🔔 Anında Telegram bildirimi
- 📅 Detaylı tarih/saat bilgisi
- 🌐 Çoklu dil desteği

### Güvenilirlik
- 🔄 Otomatik yeniden deneme mekanizması (3 deneme)
- 💚 Heartbeat sistemi (bot çalışıyor mu kontrolü)
- 🛡️ Hata yönetimi ve güvenli kapanış
- 📊 Gerçek zamanlı istatistikler
- 💾 Durum kaydetme ve geri yükleme
- 📝 Sınav geçmişi takibi

### Profesyonel Özellikler
- 🔍 Başlangıç bağlantı testleri
- ⚙️ Konfigürasyon doğrulama
- 📈 Başarı oranı takibi
- 🧪 Test modu (geliştirme için)
- 🚦 Sinyal yakalama (temiz kapanış)
- 📋 Detaylı loglama sistemi

## Hızlı Başlangıç 🚀

### 1. Telegram Bot Oluşturma

1. Telegram'da [@BotFather](https://t.me/BotFather)'ı açın
2. `/newbot` komutunu gönderin
3. Bot adı ve kullanıcı adı belirleyin
4. Aldığınız token'ı kopyalayın (örn: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Chat ID Öğrenme

1. Telegram'da [@userinfobot](https://t.me/userinfobot)'u açın
2. `/start` gönderin
3. Aldığınız ID'yi kopyalayın (örn: `123456789`)

### 3. Kurulum

#### Otomatik Kurulum (Önerilen)

**Linux/Mac:**
```bash
chmod +x start_bot.sh
./start_bot.sh
```

**Windows:**
```cmd
start_bot.bat
```

#### Manuel Kurulum

```bash
# Sanal ortam oluştur (opsiyonel ama önerilen)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyasını düzenle
nano .env  # veya herhangi bir editör

# Botu çalıştır
python3 tolc_bot.py
```

### 4. Konfigürasyon

`.env` dosyasını düzenleyin:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here  # Zorunlu
TELEGRAM_CHAT_ID=your_chat_id_here      # Zorunlu
CHECK_INTERVAL=300                       # Opsiyonel
```

## Konfigürasyon ⚙️

`.env` dosyasındaki tüm ayarlar:

### Zorunlu Ayarlar
- `TELEGRAM_BOT_TOKEN`: Bot token (@BotFather'dan)
- `TELEGRAM_CHAT_ID`: Chat ID (@userinfobot'tan)

### Opsiyonel Ayarlar
- `CHECK_INTERVAL`: Kontrol aralığı saniye (varsayılan: 300 = 5 dakika)
- `HEARTBEAT_INTERVAL`: Heartbeat aralığı saniye (varsayılan: 3600 = 1 saat)
- `NOTIFICATION_SOUND`: Bildirim sesi (yes/no, varsayılan: yes)
- `VERBOSE_LOGGING`: Detaylı log (yes/no, varsayılan: no)
- `NOTIFY_ON_ERROR`: Hata bildirimi (yes/no, varsayılan: no)
- `MAX_RETRIES`: Maksimum retry sayısı (varsayılan: 3)
- `TEST_MODE`: Test modu (yes/no, varsayılan: no)

## Çalıştırma 🏃

### Normal Mod
```bash
python3 tolc_bot.py
```

### Test Modu (Tek kontrol)
```bash
# .env dosyasında TEST_MODE=yes yapın veya:
TEST_MODE=yes python3 tolc_bot.py
```

### Arka Planda Çalıştırma

**Linux/Mac (screen ile):**
```bash
screen -S tolc_bot
python3 tolc_bot.py
# Ctrl+A+D ile detach
# screen -r tolc_bot ile geri dön
```

**Linux/Mac (nohup ile):**
```bash
nohup python3 tolc_bot.py > bot.log 2>&1 &
```

**Windows (Task Scheduler ile):**
1. Task Scheduler'ı açın
2. "Create Basic Task" seçin
3. `start_bot.bat` dosyasını seçin
4. Başlangıçta çalışacak şekilde ayarlayın

Bot çalışmaya başladığında:
- ✅ Telegram'dan başlangıç mesajı gelir
- 🔍 Her kontrol sonucu loglanır
- 🎉 Yer açıldığında anında bildirim gelir
- 💚 Her saat heartbeat mesajı gelir
- 📊 İstatistikler `logs/` klasöründe saklanır
- 💾 Durum bilgisi `logs/bot_state.json` dosyasında tutulur
- 📝 Sınav geçmişi `logs/exam_history.json` dosyasında tutulur

## Loglar 📝

Loglar `logs/` klasöründe saklanır:
- `tolc_bot_YYYYMMDD.log`: Günlük log dosyası
- `bot_state.json`: Bot durumu ve son kontrol bilgisi

## Durdurma ⏹️

`Ctrl+C` ile durdurabilirsiniz. Bot durdurulduğunda:
- İstatistikler Telegram'a gönderilir
- Durum dosyası kaydedilir
- Temiz bir şekilde kapanır

## Sorun Giderme 🔧

### Bot başlamıyor
```bash
# Python versiyonunu kontrol edin (3.7+)
python3 --version

# Bağımlılıkları tekrar yükleyin
pip install -r requirements.txt --force-reinstall

# .env dosyasını kontrol edin
cat .env
```

### Bot mesaj gönderemiyor
- ✅ Token ve Chat ID'yi kontrol edin
- ✅ Bot'u Telegram'da başlattınız mı? (Bot'a `/start` gönderin)
- ✅ Internet bağlantınızı kontrol edin
- ✅ Test modu ile deneyin: `TEST_MODE=yes python3 tolc_bot.py`

### Siteye erişim sorunu
- ✅ Internet bağlantınızı kontrol edin
- ✅ VPN kullanıyorsanız kapatmayı deneyin
- ✅ Detaylı log için: `VERBOSE_LOGGING=yes`

### Detaylı log almak için
```bash
# .env dosyasında
VERBOSE_LOGGING=yes
NOTIFY_ON_ERROR=yes

# Veya direkt çalıştırırken
VERBOSE_LOGGING=yes python3 tolc_bot.py
```

### Log dosyalarını kontrol etme
```bash
# Son log dosyasını görüntüle
tail -f logs/tolc_bot_*.log

# Tüm logları görüntüle
cat logs/tolc_bot_*.log

# Hataları filtrele
grep ERROR logs/tolc_bot_*.log
```


## Güvenlik 🔒

- ⚠️ `.env` dosyasını asla paylaşmayın veya git'e eklemeyin
- ⚠️ Bot token'ınızı kimseyle paylaşmayın
- ✅ `.gitignore` dosyası `.env` dosyasını otomatik olarak hariç tutar
- ✅ Token sızdıysa @BotFather'dan yeni token alın

## Performans 📊

- Minimum kontrol aralığı: 60 saniye (önerilen: 300 saniye)
- Maksimum kontrol aralığı: 3600 saniye
- Her kontrol ~2-5 saniye sürer
- Retry mekanizması ile %99+ güvenilirlik

## Sık Sorulan Sorular ❓

**S: Bot kaç dakikada bir kontrol ediyor?**
C: Varsayılan olarak 5 dakikada bir (300 saniye). `.env` dosyasından değiştirebilirsiniz.

**S: Heartbeat nedir?**
C: Bot'un çalıştığını gösteren periyodik mesajdır. Varsayılan olarak her saat gönderilir.

**S: Test modu ne işe yarar?**
C: Tek bir kontrol yapıp çıkar. Bot'u test etmek için kullanılır.

**S: Bot çöktü mü nasıl anlarım?**
C: Heartbeat mesajları gelmiyorsa bot çökmüş olabilir. Logları kontrol edin.

**S: Birden fazla sınav türünü takip edebilir miyim?**
C: Şu anda sadece CENT@home destekleniyor. Kod üzerinde değişiklik yaparak ekleyebilirsiniz.

**S: Bot'u sunucuda çalıştırabilir miyim?**
C: Evet! VPS, AWS, Heroku gibi platformlarda çalıştırabilirsiniz.

## Katkıda Bulunma 🤝

Bu bot açık kaynak değildir ancak önerilerinizi paylaşabilirsiniz.

## Lisans 📄

Bu proje kişisel kullanım içindir.

## İletişim 📧

Sorularınız için Telegram'dan iletişime geçebilirsiniz.

---

**Not:** Bu bot CISIA'nın resmi bir ürünü değildir. Sadece bilgilendirme amaçlıdır.

Başarılar! 🎓✨
