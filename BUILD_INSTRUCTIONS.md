# PyPI Paket Oluşturma Talimatları

## 🚀 PyPI Paketi Oluşturma

### 1. Gerekli Araçları Yükleyin
```bash
pip install build twine
```

### 2. Paket Yapısını Oluşturun
```bash
# Paket yapısını oluştur
python -m build

# Wheel ve source distribution oluşturulur
# dist/ klasöründe pyorbit_space_game-1.0.0-py3-none-any.whl
# ve pyorbit_space_game-1.0.0.tar.gz dosyaları oluşur
```

### 3. Test PyPI'ye Yükleyin (İsteğe Bağlı)
```bash
# Test PyPI'ye yükle
twine upload --repository testpypi dist/*

# Test et
pip install --index-url https://test.pypi.org/simple/ pyOrbit
```

### 4. Gerçek PyPI'ye Yükleyin
```bash
# Gerçek PyPI'ye yükle
twine upload dist/*

# Yükle
pip install pyOrbit

# Çalıştır
pyorbit
```

## 📁 Paket Yapısı

```
pyorbit/
├── __init__.py              # Ana oyun sınıfı
├── __main__.py              # Giriş noktası
├── modules/                 # Modüler sınıflar
│   ├── __init__.py
│   ├── colors.py
│   ├── enums.py
│   ├── celestial_objects.py
│   ├── ship.py
│   ├── chunk_manager.py
│   ├── universe_constants.py
│   └── locale_manager.py
├── loc/                     # Dil dosyaları
│   ├── en.json
│   ├── tr.json
│   ├── fr.json
│   ├── de.json
│   ├── es.json
│   └── ja.json
└── fonts/                   # Font dosyaları
    └── pyorbitron-regular.ttf
```

## 🔧 Konfigürasyon Dosyaları

- `setup.py` - Ana kurulum dosyası
- `pyproject.toml` - Modern Python paket konfigürasyonu
- `MANIFEST.in` - Dahil edilecek dosyalar
- `requirements.txt` - Gereksinimler
- `LICENSE` - MIT lisansı

## 🎯 Özellikler

### Otomatik Klasör Oluşturma
- `sessions/` - Session verileri
- `universes/` - Evren dosyaları
- Kullanıcının çalışma dizininde oluşturulur

### Font Yönetimi
- Orbitron font'u paket içinde
- Liberation Mono sistem font'u
- Fallback sistem font'u

### Dil Yönetimi
- 6 dil desteği
- Otomatik dil dosyası bulma
- Fallback İngilizce

### Console Script
- `pyorbit` komutu ile çalıştırma
- `python -m orbit` ile çalıştırma

## 📦 Kullanım

### PyPI'den Yükleme
```bash
pip install pyOrbit
pyorbit
```

### Manuel Kurulum
```bash
git clone <repository>
cd pyorbit
pip install -e .
pyorbit
```

## 🐛 Sorun Giderme

### Font Bulunamadı
- Orbitron font'u paket içinde
- Sistem font'u kullanılır

### Dil Dosyası Bulunamadı
- İngilizce fallback
- Uyarı mesajı gösterilir

### Klasör Oluşturma Hatası
- İzin hatası kontrol edin
- Çalışma dizini yazılabilir olmalı

## 📝 Notlar

- Paket boyutu: ~364KB
- Python 3.7+ gereklidir
- Pygame 2.0+ gereklidir
- Tüm platformlarda çalışır
