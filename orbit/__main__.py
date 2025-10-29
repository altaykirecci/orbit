#!/usr/bin/env python3
"""
ORBIT - Uzay Keşif Simülasyonu
Ana giriş noktası

Kullanım:
    python -m orbit
    veya
    orbit
"""

import sys
import os
from pathlib import Path

def main():
    """Ana giriş noktası"""
    try:
        # Orbit paketinin yolunu bul
        orbit_package_path = Path(__file__).parent
        orbit_root = orbit_package_path.parent
        
        # Python path'e ekle
        if str(orbit_root) not in sys.path:
            sys.path.insert(0, str(orbit_root))
        
        # Ana oyun dosyasını import et ve çalıştır
        from orbit import SpaceGamePygame
        
        print("🚀 ORBIT - Uzay Keşif Simülasyonu")
        print("by Altay Kireççi")
        print("")
        
        # Oyunu başlat
        game = SpaceGamePygame()
        game.run()
        
    except ImportError as e:
        print(f"❌ HATA: Gerekli modüller yüklenemedi: {e}")
        print("Lütfen 'pip install -r requirements.txt' komutunu çalıştırın.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ HATA: Oyun başlatılamadı: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
