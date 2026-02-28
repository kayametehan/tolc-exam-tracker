# 🔄 Güncelleme Rehberi

## Sorun: lxml Hatası

Eğer hala "lxml" hatası alıyorsanız, eski kod çalışıyor demektir.

## Çözüm: Kodu Güncelle

### 1. Değişiklikleri Çek

```bash
git pull origin main
```

### 2. Bağımlılıkları Güncelle

```bash
pip install -r requirements.txt --upgrade
```

### 3. Eski Process'leri Durdur

Eğer bot arka planda çalışıyorsa:

**macOS/Linux:**
```bash
# Process'i bul
ps aux | grep tolc_bot.py

# Process'i durdur (PID'yi değiştir)
kill <PID>

# Veya tüm Python process'lerini durdur
pkill -f tolc_bot.py
```

**Windows:**
```cmd
# Task Manager'dan Python process'lerini durdur
# veya
taskkill /F /IM python.exe
```

### 4. Yeniden Başlat

```bash
# macOS/Linux
./start_bot.sh

# Windows
start_bot.bat
```

## Değişiklik Kontrolü

Kodun güncel olduğunu kontrol edin:

```bash
# Son commit'i kontrol et
git log -1 --oneline

# Şu çıktıyı görmelisiniz:
# 71e3c8e 🐛 Fix: Replace lxml with html.parser (built-in)
```

Veya kod içinde kontrol edin:

```bash
grep "html.parser" tolc_bot.py
# Çıktı olmalı: soup = BeautifulSoup(response.text, 'html.parser')
```

## Hala Sorun Varsa

### Manuel Güncelleme

Eğer git pull çalışmıyorsa:

```bash
# 1. Mevcut değişiklikleri kaydet
git stash

# 2. Güncellemeleri çek
git pull origin main

# 3. Değişiklikleri geri getir
git stash pop
```

### Temiz Kurulum

En son çare:

```bash
# 1. .env dosyasını yedekle
cp .env .env.backup

# 2. Repository'yi sil ve tekrar klonla
cd ..
rm -rf tolc-exam-tracker
git clone https://github.com/kayametehan/tolc-exam-tracker.git
cd tolc-exam-tracker

# 3. .env dosyasını geri getir
cp ../tolc-exam-tracker.backup/.env .env

# 4. Bağımlılıkları yükle
pip install -r requirements.txt

# 5. Çalıştır
./start_bot.sh
```

## Yeni Özellikler (v2.0.2)

✅ lxml yerine html.parser (Python built-in)
✅ Telegram butonları ile direkt kayıt linki
✅ .env dosyası öncelikli (environment variable override)
✅ Windows encoding düzeltmeleri

## Destek

Hala sorun yaşıyorsanız:
- GitHub Issues: https://github.com/kayametehan/tolc-exam-tracker/issues
- Log dosyalarını kontrol edin: `cat logs/tolc_bot_*.log`
