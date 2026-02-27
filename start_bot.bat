@echo off
REM TOLC Bot Başlatma Scripti (Windows)

echo 🚀 TOLC CENT@home Bot başlatılıyor...

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python yükleyin.
    pause
    exit /b 1
)

REM Sanal ortam kontrolü
if not exist "venv" (
    echo 📦 Sanal ortam oluşturuluyor...
    python -m venv venv
)

REM Sanal ortamı aktifleştir
call venv\Scripts\activate.bat

REM Bağımlılıkları yükle
echo 📥 Bağımlılıklar kontrol ediliyor...
pip install -q -r requirements.txt

REM .env kontrolü
if not exist ".env" (
    echo ❌ .env dosyası bulunamadı!
    echo 📝 Lütfen .env dosyasını oluşturun ve ayarları yapın.
    pause
    exit /b 1
)

REM Botu başlat
echo ✅ Bot başlatılıyor...
python tolc_bot.py

REM Sanal ortamdan çık
deactivate

pause
