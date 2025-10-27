#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time
import os

def test_pygame_game():
    """Pygame oyununu test et"""
    print("Pygame oyunu test ediliyor...")
    
    # Oyunu başlat
    process = subprocess.Popen(
        ["python3", "space_game_pygame.py"],
        cwd="/home/dusunenadam/Development/orbit",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Test komutları
    commands = [
        "createUniverse size=14400 name=test",
        "startMission max=1",
        "startEngine",
        "quit"
    ]
    
    # Komutları gönder
    for cmd in commands:
        print(f"Komut gönderiliyor: {cmd}")
        process.stdin.write(cmd + "\n")
        process.stdin.flush()
        time.sleep(1)  # Her komut arasında bekle
    
    # Oyunu kapat
    process.terminate()
    process.wait()
    
    print("Test tamamlandı!")

if __name__ == "__main__":
    test_pygame_game()
