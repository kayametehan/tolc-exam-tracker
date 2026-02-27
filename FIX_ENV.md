# 🔧 Environment Variable Sorunu Çözümü

## Sorun

Sistemde `TELEGRAM_BOT_TOKEN` environment variable olarak set edilmiş ve bu .env dosyasını override ediyor.

Hata mesajında görülen:
```
bot575472491  # Yanlış - başındaki 8 eksik
```

Olması gereken:
```
bot8575472491  # Doğru
```

## Çözüm

### Geçici Çözüm (Sadece bu oturum için)

**macOS/Linux:**
```bash
unset TELEGRAM_BOT_TOKEN
unset TELEGRAM_CHAT_ID
python3 tolc_bot.py
```

**Windows CMD:**
```cmd
set TELEGRAM_BOT_TOKEN=
set TELEGRAM_CHAT_ID=
python tolc_bot.py
```

**Windows PowerShell:**
```powershell
Remove-Item Env:TELEGRAM_BOT_TOKEN
Remove-Item Env:TELEGRAM_CHAT_ID
python tolc_bot.py
```

### Kalıcı Çözüm

Environment variable'ı tamamen kaldır:

**macOS/Linux:**

1. Shell config dosyanızı kontrol edin:
```bash
# Bash kullanıyorsanız
cat ~/.bashrc | grep TELEGRAM
cat ~/.bash_profile | grep TELEGRAM

# Zsh kullanıyorsanız
cat ~/.zshrc | grep TELEGRAM

# Fish kullanıyorsanız
cat ~/.config/fish/config.fish | grep TELEGRAM
```

2. Bulduğunuz satırları silin veya comment out yapın:
```bash
# Örnek: ~/.zshrc dosyasını düzenle
nano ~/.zshrc
# veya
vim ~/.zshrc

# TELEGRAM_BOT_TOKEN satırını bulup silin veya başına # ekleyin
```

3. Terminal'i yeniden başlatın veya:
```bash
source ~/.zshrc  # veya ~/.bashrc
```

**Windows:**

1. System Properties'i açın:
   - Windows tuşu + R
   - `sysdm.cpl` yazın
   - Enter

2. "Advanced" tab → "Environment Variables"

3. "User variables" ve "System variables" bölümlerinde `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` varsa silin

4. Terminal'i yeniden başlatın

### Doğrulama

Environment variable'ın temizlendiğini kontrol edin:

**macOS/Linux:**
```bash
env | grep TELEGRAM
# Hiçbir şey göstermemeli
```

**Windows CMD:**
```cmd
set | findstr TELEGRAM
REM Hiçbir şey göstermemeli
```

**Windows PowerShell:**
```powershell
Get-ChildItem Env: | Where-Object {$_.Name -like "*TELEGRAM*"}
# Hiçbir şey göstermemeli
```

### Bot'u Çalıştırma

Environment variable temizlendikten sonra:

```bash
# macOS/Linux
./start_bot.sh

# Windows
start_bot.bat
```

## Alternatif: .env Dosyasını Zorla Kullan

Eğer environment variable'ı kaldıramıyorsanız, kodu değiştirerek .env dosyasını zorla kullanabilirsiniz:

`tolc_bot.py` dosyasında, `load_dotenv()` satırını şöyle değiştirin:

```python
# Eski:
load_dotenv()

# Yeni:
load_dotenv(override=True)  # Environment variable'ları override et
```

Bu, .env dosyasındaki değerlerin environment variable'ları override etmesini sağlar.

## Test

Doğru token'ın yüklendiğini test edin:

```bash
python3 -c "
from dotenv import load_dotenv
import os

load_dotenv(override=True)
token = os.getenv('TELEGRAM_BOT_TOKEN')
print(f'Token ilk 10 karakter: {token[:10] if token else None}')
print(f'Token uzunluğu: {len(token) if token else 0}')
"
```

Çıktı şöyle olmalı:
```
Token ilk 10 karakter: 8575472491
Token uzunluğu: 46
```

---

**Not:** Token'ınızı asla paylaşmayın veya public repository'lere commit etmeyin!
