#!/usr/bin/env python3
"""
Uzay Oyunu Demo Scripti
"""

from space_game import SpaceGame
import time

def demo():
    """Demo oyunu çalıştır"""
    game = SpaceGame()
    
    print("=== UZAY OYUNU DEMO ===")
    print("1. Evren oluşturuluyor...")
    game.create_universe(size=14400, name="demo_universe")
    
    print("\n2. Görev başlatılıyor...")
    game.start_mission(max_speed=1)
    
    print("\n3. Gemi durumu:")
    game.show_detailed_status()
    
    print("\n4. Gök cisimleri listeleniyor...")
    game.list_celestial_objects()
    
    print("\n5. Yön kontrolü yapılıyor...")
    game.check_up()
    game.check_down()
    game.check_left()
    game.check_right()
    
    print("\n6. Motor başlatılıyor...")
    game.start_engine()
    
    print("\n7. 5 saniye hareket ediliyor...")
    for i in range(5):
        game.update_ship_position()
        time.sleep(1)
        if game.ship and game.ship.is_moving:
            print(f"Saniye {i+1}: Konum ({game.ship.x}, {game.ship.y})")
    
    print("\n8. Motor durduruluyor...")
    game.stop_engine()
    
    print("\n9. Oyun kaydediliyor...")
    game.save_game()
    
    print("\n=== DEMO TAMAMLANDI ===")

if __name__ == "__main__":
    demo()
