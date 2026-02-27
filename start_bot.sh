#!/bin/bash
# TOLC Bot Başlatma Scripti

echo "🚀 TOLC CENT@home Bot başlatılıyor..."

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı! Lütfen Python3 yükleyin."
    exit 1
fi

# Sanal ortam kontrolü
if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam oluşturuluyor..."
    python3 -m venv venv
fi

# Sanal ortamı aktifleştir
source venv/bin/activate

# Bağımlılıkları yükle
echo "📥 Bağımlılıklar kontrol ediliyor..."
pip install -q -r requirements.txt

# .env kontrolü
if [ ! -f ".env" ]; then
    echo "❌ .env dosyası bulunamadı!"
    echo "📝 Lütfen .env dosyasını oluşturun ve ayarları yapın."
    exit 1
fi

# Botu başlat
echo "✅ Bot başlatılıyor..."
python3 tolc_bot.py

# Sanal ortamdan çık
deactivate
