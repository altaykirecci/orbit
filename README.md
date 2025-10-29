# ORBIT - Uzay Keşif Simülasyonu

**by Altay Kireççi**

Python ve Pygame ile geliştirilmiş, gelişmiş uzay keşif simülasyon oyunu. Evrenler oluşturun, gök cisimlerini keşfedin, kataloglar oluşturun ve çok dilli bir deneyim yaşayın.

## 🚀 Özellikler

### 🌌 Evren Sistemi
- **Dinamik evren oluşturma** - 200x200'den 2000x2000'e kadar özelleştirilebilir boyutlar
- **Astrofiziksel gerçekçilik** - Yıldızlar, karadelikler, gezegenler, asteroit kuşakları
- **Chunk-based yükleme** - Büyük evrenlerde performans optimizasyonu
- **Session yönetimi** - Evren bazında session'lar ve kataloglar

### 🛸 Gemi Kontrolü
- **4 yönlü hareket** - Yukarı, aşağı, sola, sağa
- **Motor kontrolü** - Motor açma/kapama
- **Hız ayarlama** - Özelleştirilebilir hareket hızı
- **Teleportasyon** - Koordinat veya katalog nesnesine ışınlanma
- **Enerji sistemi** - Evren boyutuna göre hesaplanan yakıt

### 🔍 Keşif ve Keşif
- **40x40 matris görünümü** - Gemi etrafındaki alan
- **Gök cismi tespiti** - Yıldızlar, karadelikler, gezegenler, asteroit kuşakları
- **Katalog sistemi** - Keşfedilen nesneleri kaydetme ve yönetme
- **Harita sistemi** - Mevcut chunk'ları harita olarak kaydetme

### 🌍 Çok Dilli Destek
- **6 dil desteği** - İngilizce, Türkçe, Fransızca, Almanca, İspanyolca, Japonca
- **Dinamik dil değiştirme** - Oyun içinde dil değiştirme
- **Yerelleştirilmiş arayüz** - Tüm metinler çok dilli

### 🎨 Gelişmiş Arayüz
- **Pygame tabanlı** - Modern grafik arayüz
- **Renkli matris** - Gök cismi türlerine göre renklendirme
- **Dashboard** - Gerçek zamanlı gemi durumu
- **Katalog paneli** - Keşfedilen nesnelerin istatistikleri
- **Konsol sistemi** - Komut geçmişi ve scroll desteği

## 📦 Kurulum

### Gereksinimler
- Python 3.7+
- Pygame 2.0+

### Kurulum Adımları
```bash
# Depoyu klonlayın
git clone <repository-url>
cd orbit

# Sanal ortam oluşturun
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# Gerekli paketleri yükleyin
pip install pygame

# Oyunu başlatın
python3 orbit.py
```

## 🎮 Komutlar

### 🌌 Evren Yönetimi
- `universe --name <isim> --size <boyut>` veya `u -n <isim> -s <boyut>` - Yeni evren oluştur
- `universe --name <isim> --session <session>` veya `u -n <isim> -s <session>` - Session ile evren oluştur
- `go <evren_ismi>` - Mevcut evreni yükle (deprecated, `u` kullanın)

### 🛸 Gemi Kontrolü
- `engine on/off` - Motoru aç/kapat
- `rotate up/down/left/right` - Yöne dön
- `speed <değer>` - Hız ayarla
- `tp <x> <y>` - Koordinata teleport et
- `tp --cat <nesne_ismi>` - Katalog nesnesine teleport et

### 🔍 Keşif ve Bilgi
- `info universe` veya `i u` - Evren bilgileri
- `info objects` veya `i o` - Matris'teki gök cisimleri
- `cat --save <nesne_ismi>` - Nesneyi kataloga kaydet
- `cat --list` - Katalog listesi
- `cat --all` - Tüm matris nesnelerini kaydet

### 🗺️ Harita Sistemi
- `map --save <isim> --desc <açıklama>` - Mevcut chunk'ı harita olarak kaydet
- `map --list` veya `map -ls` - Kayıtlı haritaları listele
- `map --load <isim>` veya `map -l <isim>` - Haritayı yükle
- `map --delete <isim>` veya `map -d <isim>` - Haritayı sil

### 🌍 Dil ve Arayüz
- `lang <dil_kodu>` - Dil değiştir (tr, en, fr, de, es, ja)
- `lang` - Mevcut dilleri listele
- `grid on/off` - Grid çizgilerini aç/kapat
- `help` - Yardım menüsü
- `help <komut>` - Belirli komut yardımı

### 🎯 Diğer
- `list` veya `ls` - Evren listesi
- `time` - Zaman bilgisi
- `quit` veya `exit` - Oyundan çık

## 🎮 Oyun Mekanikleri

### ⚡ Enerji Sistemi
- **Hesaplama**: Evren boyutuna göre 3 tam tur için yeterli enerji
- **Tüketim**: Her koordinat değişikliği 1 enerji
- **Görüntüleme**: Dashboard'da gerçek zamanlı enerji durumu

### 🚀 Hız Sistemi
- **Hesaplama**: 24 saatte tüm evreni keşfetmek için gerekli hız
- **Birim**: Saniye/nokta formatında
- **Ayarlama**: `speed` komutu ile özelleştirilebilir

### 🗂️ Session Sistemi
- **Yapı**: `sessions/<evren_ismi>/<session_ismi>/`
- **İçerik**: Kataloglar, haritalar, oyun verileri
- **Yönetim**: Evren bazında session'lar

### 🎨 Görsel Sistem
- **Matris boyutu**: 40x40 hücre
- **Renk kodları**:
  - 🌟 Yıldız: Sarı
  - ⚫ Karadelik: Koyu gri
  - 🪐 Gezegen: Navy
  - ☄️ Asteroit kuşağı: Açık gri
  - ☄️ Kuyruklu yıldız: Beyaz

## 📁 Dosya Yapısı

```
orbit/
├── orbit.py                 # Ana oyun dosyası
├── modules/                 # Modüler sınıflar
│   ├── __init__.py
│   ├── colors.py           # Renk tanımları
│   ├── enums.py            # Enum sınıfları
│   ├── celestial_objects.py # Gök cismi sınıfları
│   ├── ship.py             # Gemi sınıfı
│   ├── chunk_manager.py    # Chunk yönetimi
│   ├── universe_constants.py # Evren sabitleri
│   └── locale_manager.py   # Dil yönetimi
├── universes/              # Evren dosyaları
│   └── <evren_ismi>/
│       ├── metadata.json
│       └── chunk_*.json
├── sessions/               # Session verileri
│   └── <evren_ismi>/
│       └── <session_ismi>/
│           ├── cats.json   # Katalog
│           └── maps/       # Haritalar
├── loc/                    # Dil dosyaları
│   ├── en.json
│   ├── tr.json
│   ├── fr.json
│   ├── de.json
│   ├── es.json
│   └── ja.json
├── fonts/                  # Font dosyaları
│   └── orbitron-regular.ttf
└── README.md
```

## 🔧 Geliştirici Notları

### Modüler Yapı
Oyun modüler bir yapıya sahiptir. Her sınıf ayrı dosyalarda tanımlanmıştır:
- `modules/colors.py` - Renk tanımları
- `modules/enums.py` - Enum sınıfları
- `modules/celestial_objects.py` - Gök cismi sınıfları
- `modules/ship.py` - Gemi sınıfı
- `modules/chunk_manager.py` - Chunk yönetimi
- `modules/universe_constants.py` - Evren sabitleri
- `modules/locale_manager.py` - Dil yönetimi

### Chunk Sistemi
Büyük evrenlerde performans için chunk-based yükleme sistemi kullanılır. Sadece gemi etrafındaki chunk'lar yüklenir.

### Çok Dilli Destek
Tüm metinler `loc/` klasöründeki JSON dosyalarında saklanır. Yeni dil eklemek için yeni JSON dosyası oluşturun.

## 🎯 Gelecek Özellikler

- [ ] Çok oyunculu mod
- [ ] Daha fazla gök cismi türü
- [ ] Kaynak toplama sistemi
- [ ] Ticaret sistemi
- [ ] Görev sistemi
- [ ] Ses efektleri
- [ ] Animasyonlar

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 👨‍💻 Geliştirici

**Altay Kireççi**

---

*ORBIT - Uzayın derinliklerini keşfedin!* 🚀✨