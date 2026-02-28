# 📱 Telegram Komutları

Bot artık Telegram'dan komutlarla kontrol edilebilir!

## 🎯 Kullanılabilir Komutlar

### `/start`
Bot'u başlatır ve hoş geldin mesajı gösterir.

**Örnek:**
```
/start
```

**Yanıt:**
- Bot bilgileri
- Mevcut komutlar listesi
- Kontrol aralığı bilgisi

---

### `/status`
Bot'un anlık durumunu ve istatistiklerini gösterir.

**Örnek:**
```
/status
```

**Gösterilen Bilgiler:**
- ✅ Bot durumu (Aktif/Pasif)
- ⏱️ Çalışma süresi
- 🔍 Toplam kontrol sayısı
- 📊 Başarı oranı
- 🎯 Bulunan sınav sayısı
- 📨 Gönderilen bildirim sayısı
- ⏰ Son kontrol zamanı
- 🔄 Sonraki kontrol zamanı

---

### `/check`
Anında manuel kontrol yapar. Normal kontrol aralığını beklemeden hemen sınavları kontrol eder.

**Örnek:**
```
/check
```

**Sonuç:**
- Yer varsa: Bulunan sınavlar ve direkt kayıt butonları
- Yer yoksa: "Yer yok" mesajı

**Kullanım Senaryoları:**
- Acil kontrol yapmak istediğinizde
- Bot'un çalışıp çalışmadığını test etmek için
- Bir arkadaşınız yer gördüğünü söylediğinde doğrulamak için

---

### `/stats`
Detaylı istatistikler ve geçmiş bilgilerini gösterir.

**Örnek:**
```
/stats
```

**Gösterilen Bilgiler:**
- 📊 Tüm istatistikler (status'tan daha detaylı)
- ⚙️ Bot ayarları
- 📝 Son bulunan 5 sınav
- 🤖 Bot versiyonu

---

### `/help`
Yardım menüsünü gösterir. Tüm komutların açıklamaları ve bot'un nasıl çalıştığı.

**Örnek:**
```
/help
```

**İçerik:**
- Komutlar listesi ve açıklamaları
- Bot nasıl çalışır?
- Özellikler
- Destek linkleri

---

### `/stop`
Bot'u durdurur. **DİKKATLİ KULLANIN!**

**Örnek:**
```
/stop
```

**Süreç:**
1. `/stop` yazarsınız
2. Bot onay ister
3. `/stop_confirm` yazarak onaylarsınız
4. Bot durur ve son istatistikleri gönderir

**Not:** Bot'u tekrar başlatmak için sunucuya erişim gerekir!

**İptal:**
```
/cancel
```

---

## 🔒 Güvenlik

- Komutlar sadece `.env` dosyasında tanımlı `TELEGRAM_CHAT_ID`'den kabul edilir
- Başka kullanıcılar komut gönderemez
- Bot sadece sizinle iletişim kurar

---

## 💡 İpuçları

### Hızlı Kontrol
```
/check
```
En hızlı şekilde sınavları kontrol eder.

### Düzenli Takip
```
/status
```
Bot'un düzgün çalışıp çalışmadığını kontrol edin.

### Sorun Giderme
```
/stats
```
Detaylı bilgi alın, başarı oranını kontrol edin.

### Acil Durum
```
/stop
/stop_confirm
```
Bot'u durdurun (sunucuya erişiminiz varsa tekrar başlatabilirsiniz).

---

## 🤖 Otomatik Özellikler

Bot komut beklerken de otomatik çalışmaya devam eder:

- ✅ Her 5 dakikada bir otomatik kontrol
- ✅ Yer açıldığında anında bildirim
- ✅ Her 1 saatte bir heartbeat mesajı
- ✅ Her 10 saniyede bir komut kontrolü

---

## 📝 Örnek Kullanım Senaryoları

### Senaryo 1: Sabah Kontrolü
```
/status
```
Bot'un gece boyunca çalıştığını ve kaç kontrol yaptığını görürsünüz.

### Senaryo 2: Acil Kontrol
Arkadaşınız "yer açıldı" dedi:
```
/check
```
Anında kontrol edersiniz.

### Senaryo 3: İstatistik Meraklısı
```
/stats
```
Bot'un performansını ve geçmişte bulduğu sınavları görürsünüz.

### Senaryo 4: Yeni Kullanıcı
```
/help
```
Tüm komutları ve bot'un nasıl çalıştığını öğrenirsiniz.

### Senaryo 5: Sınav Bitti
Sınava kayıt oldunuz, bot'a artık ihtiyacınız yok:
```
/stop
/stop_confirm
```

---

## 🔄 Komut Yanıt Süreleri

- `/start`, `/help`, `/status`, `/stats`: Anında (< 1 saniye)
- `/check`: 2-5 saniye (siteleri kontrol eder)
- `/stop`: Anında, sonra temiz kapanış (< 5 saniye)

---

## ❓ Sık Sorulan Sorular

**S: Komutlar çalışmıyor?**
C: Bot'un çalıştığından emin olun. `/status` deneyin.

**S: Başka biri bot'a komut gönderebilir mi?**
C: Hayır, sadece kayıtlı chat ID komut gönderebilir.

**S: /check çok mu sık kullanılabilir?**
C: Evet ama gereksiz yere sunucuyu yormayın. Normal kontroller yeterli.

**S: Bot durdu, nasıl başlatırım?**
C: Sunucuya SSH ile bağlanıp `python3 tolc_bot.py` çalıştırın.

**S: Komutları nereden öğrenebilirim?**
C: `/help` yazın, tüm komutlar açıklanır.

---

## 🚀 Gelişmiş Kullanım

### Komut Kombinasyonları

**Sabah Rutini:**
```
/status
/check
```

**Sorun Giderme:**
```
/stats
/check
```

**Yeni Başlangıç:**
```
/start
/help
/status
```

---

## 📊 Komut İstatistikleri

Bot her komut kullanımını loglar:
- Hangi komut kullanıldı
- Ne zaman kullanıldı
- Sonuç ne oldu

Logları görmek için:
```bash
tail -f logs/tolc_bot_*.log | grep "Komut"
```

---

## 🎓 Bot Komutları vs Web Arayüzü

| Özellik | Telegram Komutları | Web/Sunucu |
|---------|-------------------|------------|
| Erişim | Her yerden | Sadece sunucudan |
| Hız | Anında | SSH gerekir |
| Kullanım | Çok kolay | Teknik bilgi gerekir |
| Güvenlik | Chat ID ile | SSH key ile |

---

**Destek:** https://github.com/kayametehan/tolc-exam-tracker

Başarılar! 🎉
