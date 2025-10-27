# Uzay Oyunu - Shell Simülasyonu

Python ile geliştirilmiş, terminal tabanlı uzay simülasyon oyunu.

## Özellikler

- **14400x14400 boyutunda evren** (varsayılan, özelleştirilebilir)
- **Rastgele gök cisimleri**: Güneşler, karadelikler, astroid kuşakları, gezegenler, kuyruklu yıldızlar
- **Gemi kontrolü**: 4 yönlü hareket, dönüş, motor kontrolü
- **Enerji sistemi**: Hız ayarına göre enerji tüketimi
- **Görüş mesafesi**: 10 matris noktası içindeki objeleri tespit etme
- **Çarpışma algılama**: Rotadaki objeler için uyarı sistemi
- **Zaman sistemi**: Saat:dakika:saniye formatında gerçek zamanlı takip
- **Renkli konsol arayüzü**: Durum göstergeleri ve uyarılar

## Kurulum

```bash
# Python 3.6+ gerekli
python3 space_game.py

# Veya başlatma scripti ile
./run_game.sh
```

## Komutlar

### Evren Yönetimi
- `createUniverse size=14400 name=myspaces` - Evren oluştur
- `startMission max=1` - Görevi başlat (max=2 ile hız ayarı)

### Gemi Kontrolü
- `rotateRight` - Sağa dön
- `rotateLeft` - Sola dön
- `rotateUp` - Yukarı dön
- `rotateDown` - Aşağı dön
- `turnBack` - Geri dön

### Motor Kontrolü
- `startEngine` - Motoru başlat
- `stopEngine` - Motoru durdur

### Keşif
- `checkUp` - Yukarı kontrol et (10 matris)
- `checkDown` - Aşağı kontrol et (10 matris)
- `checkLeft` - Sola kontrol et (10 matris)
- `checkRight` - Sağa kontrol et (10 matris)

### Diğer
- `status` - Detaylı durum bilgisi
- `time` - Zaman bilgisi göster
- `save` - Oyunu kaydet
- `load <dosya>` - Oyunu yükle
- `list` - Gök cisimlerini listele
- `help` - Yardım menüsü
- `quit` / `exit` - Oyundan çık

## Oyun Mekanikleri

### Hız Sistemi
- Varsayılan: 10 matris noktası = 1 dakika
- `max=2` ile: 10 matris noktası = 2 dakika
- Hız arttıkça enerji tüketimi azalır

### Enerji Sistemi
- Başlangıç enerjisi: 14400 birim
- Hız 1: Her 10 matris için 1 enerji
- Hız 2: Her 10 matris için 7200 enerji

### Görüş Sistemi
- Gemi 10 matris noktası ileriyi görebilir
- `check` komutları ile yön kontrolü
- Çarpışma riski için uyarı sistemi

### Zaman Sistemi
- Gerçek zamanlı saat:dakika:saniye formatında takip
- Görev süresi ve hareket süresi ayrı ayrı gösterilir
- Hareket logları zaman damgası ile kaydedilir
- `time` komutu ile detaylı zaman bilgisi

## Dosya Yapısı

- `space_game.py` - Ana oyun dosyası
- `myspaces.json` - Evren verisi (otomatik oluşturulur)

## Geliştirici Notları

Oyun tamamen terminal tabanlıdır ve grafik arayüz gerektirmez. Renkli çıktılar için ANSI escape kodları kullanılır.

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
