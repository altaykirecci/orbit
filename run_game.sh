#!/bin/bash
# Uzay Oyunu Başlatma Scripti

echo "Uzay Oyunu başlatılıyor..."
echo "Python sürümü kontrol ediliyor..."

# Python sürümü kontrolü
python3 --version

if [ $? -eq 0 ]; then
    echo "Python3 bulundu. Oyun başlatılıyor..."
    python3 space_game.py
else
    echo "HATA: Python3 bulunamadı!"
    echo "Lütfen Python3'ü yükleyin."
    exit 1
fi
