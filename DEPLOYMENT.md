# 🚀 Deployment Guide

## GitHub Repository

**Repository:** https://github.com/kayametehan/tolc-exam-tracker

Bot başarıyla GitHub'a deploy edildi! 🎉

## Hızlı Başlangıç

### 1. Repository'yi Klonla

```bash
git clone https://github.com/kayametehan/tolc-exam-tracker.git
cd tolc-exam-tracker
```

### 2. Konfigürasyon

```bash
# .env.example dosyasını kopyala
cp .env.example .env

# .env dosyasını düzenle
nano .env  # veya herhangi bir editör
```

### 3. Çalıştır

**Otomatik (Önerilen):**
```bash
# Linux/Mac
chmod +x start_bot.sh
./start_bot.sh

# Windows
start_bot.bat
```

**Manuel:**
```bash
pip install -r requirements.txt
python3 tolc_bot.py
```

## Sunucu Deployment

### VPS/Cloud Server (Ubuntu/Debian)

```bash
# 1. Sunucuya bağlan
ssh user@your-server.com

# 2. Repository'yi klonla
git clone https://github.com/kayametehan/tolc-exam-tracker.git
cd tolc-exam-tracker

# 3. Python ve pip yükle
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# 4. Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate

# 5. Bağımlılıkları yükle
pip install -r requirements.txt

# 6. .env dosyasını yapılandır
cp .env.example .env
nano .env  # Token ve Chat ID'yi gir

# 7. Screen ile çalıştır (arka planda)
screen -S tolc_bot
python3 tolc_bot.py
# Ctrl+A+D ile detach

# 8. Screen'e geri dön
screen -r tolc_bot
```

### Systemd Service (Linux)

```bash
# 1. Service dosyası oluştur
sudo nano /etc/systemd/system/tolc-bot.service
```

```ini
[Unit]
Description=TOLC CENT@home Tracker Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/tolc-exam-tracker
Environment="PATH=/path/to/tolc-exam-tracker/venv/bin"
ExecStart=/path/to/tolc-exam-tracker/venv/bin/python3 tolc_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 2. Service'i etkinleştir ve başlat
sudo systemctl daemon-reload
sudo systemctl enable tolc-bot
sudo systemctl start tolc-bot

# 3. Durumu kontrol et
sudo systemctl status tolc-bot

# 4. Logları görüntüle
sudo journalctl -u tolc-bot -f
```

### Docker Deployment

```bash
# 1. Dockerfile oluştur
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "tolc_bot.py"]
EOF

# 2. Docker image oluştur
docker build -t tolc-bot .

# 3. Container'ı çalıştır
docker run -d \
  --name tolc-bot \
  --restart unless-stopped \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  tolc-bot

# 4. Logları görüntüle
docker logs -f tolc-bot
```

### Heroku Deployment

```bash
# 1. Heroku CLI yükle
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. App oluştur
heroku create tolc-exam-tracker

# 4. Config vars ayarla
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set TELEGRAM_CHAT_ID=your_chat_id
heroku config:set CHECK_INTERVAL=300

# 5. Procfile oluştur
echo "worker: python3 tolc_bot.py" > Procfile

# 6. Deploy
git add Procfile
git commit -m "Add Procfile for Heroku"
git push heroku main

# 7. Worker'ı başlat
heroku ps:scale worker=1

# 8. Logları görüntüle
heroku logs --tail
```

### AWS EC2 Deployment

```bash
# 1. EC2 instance oluştur (Ubuntu 22.04)
# 2. SSH ile bağlan
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Gerekli paketleri yükle
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y

# 4. Repository'yi klonla
git clone https://github.com/kayametehan/tolc-exam-tracker.git
cd tolc-exam-tracker

# 5. Kurulum ve çalıştırma
./start_bot.sh
```

## Monitoring

### Logları İzleme

```bash
# Gerçek zamanlı log
tail -f logs/tolc_bot_*.log

# Hataları filtrele
grep ERROR logs/tolc_bot_*.log

# Son 100 satır
tail -n 100 logs/tolc_bot_*.log
```

### Telegram Heartbeat

Bot her saat bir "heartbeat" mesajı gönderir. Bu mesaj gelmiyorsa bot çökmüş olabilir.

### Durum Kontrolü

```bash
# Process kontrolü
ps aux | grep tolc_bot.py

# Screen kontrolü
screen -ls

# Systemd kontrolü
sudo systemctl status tolc-bot
```

## Güncelleme

```bash
# 1. Repository'yi güncelle
git pull origin main

# 2. Bağımlılıkları güncelle
pip install -r requirements.txt --upgrade

# 3. Botu yeniden başlat
# Screen için:
screen -r tolc_bot
# Ctrl+C ile durdur, sonra tekrar başlat

# Systemd için:
sudo systemctl restart tolc-bot

# Docker için:
docker restart tolc-bot
```

## Sorun Giderme

### Bot başlamıyor
```bash
# Python versiyonu kontrol
python3 --version  # 3.7+ olmalı

# Bağımlılıkları tekrar yükle
pip install -r requirements.txt --force-reinstall

# Test modu ile dene
TEST_MODE=yes python3 tolc_bot.py
```

### Telegram mesaj gönderemiyor
```bash
# Token ve Chat ID kontrol
cat .env

# Telegram bağlantısı test
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

### Yüksek CPU/Memory kullanımı
```bash
# CHECK_INTERVAL'i artır
# .env dosyasında CHECK_INTERVAL=600 (10 dakika)

# VERBOSE_LOGGING'i kapat
# .env dosyasında VERBOSE_LOGGING=no
```

## Güvenlik

- ⚠️ `.env` dosyasını asla paylaşmayın
- ⚠️ `.env` dosyası `.gitignore`'da olmalı
- ✅ Sunucuda firewall kullanın
- ✅ SSH key authentication kullanın
- ✅ Düzenli güvenlik güncellemeleri yapın

## Destek

- 📧 Issues: https://github.com/kayametehan/tolc-exam-tracker/issues
- 📖 README: https://github.com/kayametehan/tolc-exam-tracker#readme

---

**Not:** Bu bot CISIA'nın resmi bir ürünü değildir.

Başarılar! 🎓✨
