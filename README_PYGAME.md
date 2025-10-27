# Uzay Oyunu - Pygame Versiyonu

## 🚀 Özellikler

### Linux Konsolu Görünümü
- **Üst Panel**: Sabit durum bilgileri (Enerji, Hız, Yön, Durum, Görev Süresi)
- **Orta Alan**: Matrix tarzı akışkan veri akışı
- **Alt Panel**: Komut satırı (Linux konsolu gibi)

### Oyun Mekanikleri
- **Evren Oluşturma**: `createUniverse size=14400 name=myspaces`
- **Görev Başlatma**: `startMission max=1` (hız ayarı)
- **Motor Kontrolü**: `startEngine`, `stopEngine`
- **Hareket**: `rotateRight`, `rotateLeft`, `rotateUp`, `rotateDown`, `turnBack`
- **Gerçek Zamanlı**: Her matris noktası için süre hesaplama

### Teknik Özellikler
- **Pygame**: 2D grafik arayüz
- **OS Bağımsız**: Windows, macOS, Linux
- **60 FPS**: Smooth animasyon
- **Monospace Font**: Matrix görünümü
- **Renkli Arayüz**: ANSI renk kodları yerine RGB

## 🎮 Kurulum

### 1. Virtual Environment Oluştur
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# veya
venv\Scripts\activate     # Windows
```

### 2. Pygame Kur
```bash
pip install pygame
```

### 3. Oyunu Çalıştır
```bash
python3 space_game_pygame.py
```

## 🎯 Komutlar

### Temel Komutlar
- `createUniverse size=14400 name=myspaces` - Evren oluştur
- `startMission max=1` - Görevi başlat (hız: 1 dk/10 matris)
- `startEngine` - Motoru başlat
- `stopEngine` - Motoru durdur

### Hareket Komutları
- `rotateRight` - Sağa dön
- `rotateLeft` - Sola dön
- `rotateUp` - Yukarı dön
- `rotateDown` - Aşağı dön
- `turnBack` - Geri dön

### Çıkış
- `quit` veya `exit` - Oyundan çık

## 🖥️ Ekran Düzeni

```
┌─────────────────────────────────────────────────────────┐
│                UZAY OYUNU - PYGAME SIMÜLASYONU         │
├─────────────────────────────────────────────────────────┤
│ ENERJİ: 14400/14400 (100.0%) | HIZ: 1 dk/10 matris    │
│ YÖN: UP                      | DURUM: HAREKET HALİNDE  │
│ GÖREV SÜRESİ: 00:01:23      | HAREKET SÜRESİ: 00:00:45│
├─────────────────────────────────────────────────────────┤
│ [22:35:59] 2323 4712 Rotada obje yok - güvenli seyir  │
│ [22:36:06] 2323 4711 Rotada obje yok - güvenli seyir  │
│ [22:36:12] 2323 4710 Rotada obje yok - güvenli seyir  │
│ [22:36:18] 2323 4709 ALARM 2323 474 GEZEGEN          │
│ ...                                                     │
├─────────────────────────────────────────────────────────┤
│ Komut: createUniverse size=14400 name=myspaces         │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Geliştirme

### Dosya Yapısı
```
space_game_pygame.py    # Ana oyun dosyası
test_pygame.py          # Test scripti
README_PYGAME.md        # Bu dosya
```

### Özelleştirme
- **Ekran Boyutu**: `self.screen_width`, `self.screen_height`
- **Font Boyutu**: `self.font_small`, `self.font_medium`, `self.font_large`
- **Renkler**: `Colors` sınıfı
- **Matrix Satır Sayısı**: `self.max_matrix_lines`

## 🐛 Sorun Giderme

### Pygame Kurulum Sorunu
```bash
# Virtual environment kullan
python3 -m venv venv
source venv/bin/activate
pip install pygame
```

### Font Sorunu
```bash
# Monospace font kur
sudo apt install fonts-dejavu-core  # Ubuntu/Debian
```

### Performans Sorunu
- `self.clock.tick(60)` değerini düşürün (30, 15)
- `self.max_matrix_lines` değerini azaltın

## 📝 Notlar

- Oyun gerçek zamanlı çalışır
- Matrix görüntü sürekli akar
- Komut satırı Linux konsolu gibi çalışır
- Tüm komutlar klavye ile girilir
- Enter tuşu ile komut onaylanır
