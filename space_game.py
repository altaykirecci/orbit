#!/usr/bin/env python3
"""
Uzay Oyunu - Shell Tabanlı Uzay Simülasyonu
Geliştirici: AI Assistant
"""

import os
import sys
import time
import random
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Renk kodları
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Yön enum'u
class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

# Gök cismi türleri
class CelestialType(Enum):
    SUN = "sun"
    BLACK_HOLE = "black_hole"
    ASTEROID_BELT = "asteroid_belt"
    PLANET = "planet"
    COMET = "comet"

@dataclass
class CelestialObject:
    x: int
    y: int
    obj_type: CelestialType
    name: str
    size: int = 1

@dataclass
class Ship:
    x: int
    y: int
    direction: Direction
    speed: int  # 10 matris noktası için geçen dakika
    energy: int
    max_energy: int
    is_moving: bool = False
    start_time: Optional[datetime] = None
    mission_start_time: Optional[datetime] = None

class SpaceGame:
    def __init__(self):
        self.universe_size = 14400
        self.universe_name = "default"
        self.celestial_objects: List[CelestialObject] = []
        self.ship: Optional[Ship] = None
        self.universe_created = False
        self.mission_started = False
        self.running = True
        
        # Ekran boyutları (terminal için)
        self.terminal_width = 80
        self.terminal_height = 24
        
        # Oyun durumu
        self.last_position_update = datetime.now()
        
        # Komut çıktıları için
        self.last_command_output = ""
        
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        """Oyun başlığını yazdır"""
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*self.terminal_width}")
        print(f"{'UZAY OYUNU - SHELL SIMÜLASYONU':^{self.terminal_width}}")
        print(f"{'='*self.terminal_width}{Colors.END}")
        print()
    
    def format_time(self, total_seconds: float) -> str:
        """Saniyeyi saat:dakika:saniye formatına çevir"""
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_mission_time(self) -> str:
        """Görev süresini saat:dakika:saniye formatında döndür"""
        if not self.ship or not self.ship.mission_start_time:
            return "00:00:00"
        
        elapsed = (datetime.now() - self.ship.mission_start_time).total_seconds()
        return self.format_time(elapsed)
    
    def get_movement_time(self) -> str:
        """Hareket süresini saat:dakika:saniye formatında döndür"""
        if not self.ship or not self.ship.start_time:
            return "00:00:00"
        
        elapsed = (datetime.now() - self.ship.start_time).total_seconds()
        return self.format_time(elapsed)
    
    def print_status_panel(self):
        """Üst durum panelini yazdır - sabit üst panel"""
        if not self.mission_started or not self.ship:
            return
        
        # Sabit üst panel - sadece temel bilgiler
        energy_percent = (self.ship.energy / self.ship.max_energy) * 100
        energy_color = Colors.GREEN if energy_percent > 50 else Colors.YELLOW if energy_percent > 25 else Colors.RED
        
        print(f"{Colors.BOLD}ENERJİ: {energy_color}{self.ship.energy}/{self.ship.max_energy} ({energy_percent:.1f}%){Colors.END} | {Colors.BOLD}HIZ: {Colors.BLUE}{self.ship.speed} dk/10 matris{Colors.END}")
        print(f"{Colors.BOLD}YÖN: {self.ship.direction.value.upper()}{Colors.END}")
        
        status_text = "HAREKET HALİNDE" if self.ship.is_moving else "DURAKLAMADA"
        status_color = Colors.GREEN if self.ship.is_moving else Colors.YELLOW
        mission_time = self.get_mission_time()
        
        print(f"{Colors.BOLD}DURUM: {status_color}{status_text}{Colors.END} | {Colors.BOLD}GÖREV SÜRESİ: {Colors.CYAN}{mission_time}{Colors.END}")
        
        if self.ship.is_moving:
            movement_time = self.get_movement_time()
            print(f"{Colors.BOLD}HAREKET SÜRESİ: {Colors.MAGENTA}{movement_time}{Colors.END}")
        
        print()
    
    def print_matrix_display(self):
        """Matrix tarzı akışkan görüntü - sürekli akan bilgiler"""
        if not self.ship:
            return
        
        # Matrix tarzı akışkan bilgi
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # 10 nokta ilerisindeki objeleri kontrol et
        objects_ahead = self.check_direction(self.ship.direction)
        
        if objects_ahead:
            # Obje tespit edildi
            for obj, distance in objects_ahead:
                obj_color = self.get_object_color(obj.obj_type)
                obj_type_name = self.get_object_type_name(obj.obj_type)
                print(f"{Colors.CYAN}[{current_time}] {self.ship.x} {self.ship.y} {Colors.YELLOW}ALARM {obj.x} {obj.y} {obj_color}{obj_type_name}{Colors.END}")
        else:
            # Güvenli seyir
            print(f"{Colors.CYAN}[{current_time}] {self.ship.x} {self.ship.y} {Colors.GREEN}Rotada obje yok - güvenli seyir{Colors.END}")
    
    def get_object_type_name(self, obj_type: CelestialType) -> str:
        """Gök cismi türüne göre Türkçe isim döndür"""
        type_map = {
            CelestialType.SUN: "GÜNEŞ",
            CelestialType.BLACK_HOLE: "KARADELİK",
            CelestialType.ASTEROID_BELT: "ASTEROİD",
            CelestialType.PLANET: "GEZEGEN",
            CelestialType.COMET: "KUYRUKLU YILDIZ"
        }
        return type_map.get(obj_type, "BİLİNMEYEN")
    
    def get_object_color(self, obj_type: CelestialType) -> str:
        """Gök cismi türüne göre renk döndür"""
        color_map = {
            CelestialType.SUN: Colors.YELLOW,
            CelestialType.BLACK_HOLE: Colors.RED,
            CelestialType.ASTEROID_BELT: Colors.WHITE,
            CelestialType.PLANET: Colors.BLUE,
            CelestialType.COMET: Colors.CYAN
        }
        return color_map.get(obj_type, Colors.WHITE)
    
    def print_universe_info(self):
        """Evren bilgilerini yazdır"""
        if not self.universe_created:
            return
            
        print(f"{Colors.MAGENTA}EVREN: {self.universe_name} ({self.universe_size}x{self.universe_size}){Colors.END}")
        print(f"{Colors.MAGENTA}GÖK CİSİMLERİ: {len(self.celestial_objects)} adet{Colors.END}")
        print()
    
    def print_command_prompt(self):
        """Komut satırını yazdır"""
        print(f"{Colors.WHITE}{Colors.BOLD}Komut: {Colors.END}", end="", flush=True)
    
    def create_universe(self, size: int = 14400, name: str = "myspaces"):
        """Evren oluştur"""
        self.universe_size = max(size, 14400)
        self.universe_name = name
        self.celestial_objects = []
        
        print(f"{Colors.GREEN}Evren oluşturuluyor... ({self.universe_size}x{self.universe_size}){Colors.END}")
        
        # Güneşler (evrenin %0.1'i)
        sun_count = max(1, self.universe_size // 10000)
        for i in range(sun_count):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            self.celestial_objects.append(CelestialObject(
                x, y, CelestialType.SUN, f"Sun_{i+1}", random.randint(5, 15)
            ))
        
        # Karadelikler (evrenin %0.05'i)
        black_hole_count = max(1, self.universe_size // 20000)
        for i in range(black_hole_count):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            self.celestial_objects.append(CelestialObject(
                x, y, CelestialType.BLACK_HOLE, f"BlackHole_{i+1}", random.randint(3, 8)
            ))
        
        # Astroid kuşakları (evrenin %0.2'i)
        asteroid_count = max(5, self.universe_size // 5000)
        for i in range(asteroid_count):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            self.celestial_objects.append(CelestialObject(
                x, y, CelestialType.ASTEROID_BELT, f"AsteroidBelt_{i+1}", random.randint(2, 6)
            ))
        
        # Gezegenler (evrenin %0.3'i)
        planet_count = max(10, self.universe_size // 3000)
        for i in range(planet_count):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            self.celestial_objects.append(CelestialObject(
                x, y, CelestialType.PLANET, f"Planet_{i+1}", random.randint(2, 10)
            ))
        
        # Kuyruklu yıldızlar (evrenin %0.1'i)
        comet_count = max(3, self.universe_size // 10000)
        for i in range(comet_count):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            self.celestial_objects.append(CelestialObject(
                x, y, CelestialType.COMET, f"Comet_{i+1}", random.randint(1, 4)
            ))
        
        self.universe_created = True
        
        # Dosyaya kaydet
        self.save_universe()
        
        print(f"{Colors.GREEN}Evren başarıyla oluşturuldu!{Colors.END}")
        print(f"{Colors.GREEN}Toplam {len(self.celestial_objects)} gök cismi oluşturuldu.{Colors.END}")
    
    def save_universe(self):
        """Evreni dosyaya kaydet"""
        universe_data = {
            "name": self.universe_name,
            "size": self.universe_size,
            "celestial_objects": [
                {
                    "x": obj.x,
                    "y": obj.y,
                    "type": obj.obj_type.value,
                    "name": obj.name,
                    "size": obj.size
                }
                for obj in self.celestial_objects
            ],
            "created_at": datetime.now().isoformat()
        }
        
        filename = f"{self.universe_name}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(universe_data, f, indent=2, ensure_ascii=False)
        
        print(f"{Colors.BLUE}Evren '{filename}' dosyasına kaydedildi.{Colors.END}")
    
    def start_mission(self, max_speed: int = 1):
        """Görevi başlat"""
        if not self.universe_created:
            print(f"{Colors.RED}HATA: Önce evren oluşturulmalı!{Colors.END}")
            return
        
        # Gemi oluştur
        ship_x = random.randint(0, self.universe_size - 1)
        ship_y = random.randint(0, self.universe_size - 1)
        mission_start_time = datetime.now()
        
        self.ship = Ship(
            x=ship_x,
            y=ship_y,
            direction=Direction.RIGHT,
            speed=max_speed,
            energy=14400,
            max_energy=14400,
            is_moving=False,
            mission_start_time=mission_start_time
        )
        
        
        self.mission_started = True
        self.last_position_update = datetime.now()
        
        print(f"{Colors.GREEN}Görev başlatıldı!{Colors.END}")
        print(f"{Colors.GREEN}Gemi konumu: ({ship_x}, {ship_y}){Colors.END}")
        print(f"{Colors.GREEN}Hız ayarı: {max_speed} dakika/10 matris{Colors.END}")
        print(f"{Colors.GREEN}Görev başlangıç zamanı: {mission_start_time.strftime('%H:%M:%S')}{Colors.END}")
    
    def rotate_right(self):
        """Sağa dön"""
        if not self.ship:
            return
        
        direction_map = {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP
        }
        self.ship.direction = direction_map[self.ship.direction]
        print(f"{Colors.BLUE}Gemi sağa döndü. Yeni yön: {self.ship.direction.value.upper()}{Colors.END}")
    
    def rotate_left(self):
        """Sola dön"""
        if not self.ship:
            return
        
        direction_map = {
            Direction.UP: Direction.LEFT,
            Direction.LEFT: Direction.DOWN,
            Direction.DOWN: Direction.RIGHT,
            Direction.RIGHT: Direction.UP
        }
        self.ship.direction = direction_map[self.ship.direction]
        print(f"{Colors.BLUE}Gemi sola döndü. Yeni yön: {self.ship.direction.value.upper()}{Colors.END}")
    
    def rotate_up(self):
        """Yukarı dön"""
        if not self.ship:
            return
        
        self.ship.direction = Direction.UP
        print(f"{Colors.BLUE}Gemi yukarı döndü. Yeni yön: {self.ship.direction.value.upper()}{Colors.END}")
    
    def rotate_down(self):
        """Aşağı dön"""
        if not self.ship:
            return
        
        self.ship.direction = Direction.DOWN
        print(f"{Colors.BLUE}Gemi aşağı döndü. Yeni yön: {self.ship.direction.value.upper()}{Colors.END}")
    
    def turn_back(self):
        """Geri dön"""
        if not self.ship:
            return
        
        direction_map = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        self.ship.direction = direction_map[self.ship.direction]
        print(f"{Colors.BLUE}Gemi geri döndü. Yeni yön: {self.ship.direction.value.upper()}{Colors.END}")
    
    def start_engine(self):
        """Motoru başlat"""
        if not self.ship:
            return
        
        self.ship.is_moving = True
        self.ship.start_time = datetime.now()
        self.last_position_update = datetime.now()
        print(f"{Colors.GREEN}Motor başlatıldı! Gemi hareket ediyor...{Colors.END}")
    
    def stop_engine(self):
        """Motoru durdur"""
        if not self.ship:
            return
        
        self.ship.is_moving = False
        self.ship.start_time = None
        print(f"{Colors.YELLOW}Motor durduruldu! Gemi durdu.{Colors.END}")
    
    def check_collision(self, x: int, y: int) -> List[CelestialObject]:
        """Belirtilen koordinatta çarpışma kontrolü"""
        collisions = []
        for obj in self.celestial_objects:
            distance = math.sqrt((obj.x - x)**2 + (obj.y - y)**2)
            if distance <= obj.size:
                collisions.append(obj)
        return collisions
    
    def check_direction(self, direction: Direction) -> List[CelestialObject]:
        """Belirtilen yönde 10 matris noktası içindeki objeleri kontrol et"""
        if not self.ship:
            return []
        
        x, y = self.ship.x, self.ship.y
        objects_in_range = []
        
        for i in range(1, 11):  # 1-10 matris noktası
            if direction == Direction.UP:
                check_x, check_y = x, y - i
            elif direction == Direction.DOWN:
                check_x, check_y = x, y + i
            elif direction == Direction.LEFT:
                check_x, check_y = x - i, y
            else:  # RIGHT
                check_x, check_y = x + i, y
            
            # Sınır kontrolü
            if check_x < 0 or check_x >= self.universe_size or check_y < 0 or check_y >= self.universe_size:
                break
            
            # Obje kontrolü
            for obj in self.celestial_objects:
                distance = math.sqrt((obj.x - check_x)**2 + (obj.y - check_y)**2)
                if distance <= obj.size:
                    objects_in_range.append((obj, i))
        
        return objects_in_range
    
    def check_up(self):
        """Yukarı kontrol et"""
        objects = self.check_direction(Direction.UP)
        if objects:
            print(f"{Colors.YELLOW}ALERT: Yukarıda {len(objects)} obje tespit edildi!{Colors.END}")
            for obj, distance in objects:
                print(f"{Colors.YELLOW}  - {obj.name} ({obj.obj_type.value}) {distance} matris uzaklıkta{Colors.END}")
        else:
            print(f"{Colors.GREEN}Yukarıda obje yok.{Colors.END}")
    
    def check_down(self):
        """Aşağı kontrol et"""
        objects = self.check_direction(Direction.DOWN)
        if objects:
            print(f"{Colors.YELLOW}ALERT: Aşağıda {len(objects)} obje tespit edildi!{Colors.END}")
            for obj, distance in objects:
                print(f"{Colors.YELLOW}  - {obj.name} ({obj.obj_type.value}) {distance} matris uzaklıkta{Colors.END}")
        else:
            print(f"{Colors.GREEN}Aşağıda obje yok.{Colors.END}")
    
    def check_left(self):
        """Sola kontrol et"""
        objects = self.check_direction(Direction.LEFT)
        if objects:
            print(f"{Colors.YELLOW}ALERT: Solda {len(objects)} obje tespit edildi!{Colors.END}")
            for obj, distance in objects:
                print(f"{Colors.YELLOW}  - {obj.name} ({obj.obj_type.value}) {distance} matris uzaklıkta{Colors.END}")
        else:
            print(f"{Colors.GREEN}Solda obje yok.{Colors.END}")
    
    def check_right(self):
        """Sağa kontrol et"""
        objects = self.check_direction(Direction.RIGHT)
        if objects:
            print(f"{Colors.YELLOW}ALERT: Sağda {len(objects)} obje tespit edildi!{Colors.END}")
            for obj, distance in objects:
                print(f"{Colors.YELLOW}  - {obj.name} ({obj.obj_type.value}) {distance} matris uzaklıkta{Colors.END}")
        else:
            print(f"{Colors.GREEN}Sağda obje yok.{Colors.END}")
    
    def update_ship_position(self):
        """Gemi pozisyonunu güncelle"""
        if not self.ship or not self.ship.is_moving:
            return
        
        now = datetime.now()
        time_diff = (now - self.last_position_update).total_seconds() / 60  # dakika cinsinden
        
        # Her matris noktası için geçen süre hesapla
        # speed = 1 ise 10 matris noktası için 1 dakika = 0.1 dakika/matris
        # speed = 2 ise 10 matris noktası için 2 dakika = 0.2 dakika/matris
        time_per_matrix = self.ship.speed / 10  # dakika/matris
        
        if time_diff >= time_per_matrix:  # Her matris noktası için geçen süre
            # Enerji tüketimi - her matris noktası için
            energy_cost_per_matrix = 1 if self.ship.speed == 1 else self.ship.max_energy / (self.ship.speed * 10)
            self.ship.energy -= int(energy_cost_per_matrix)
            
            if self.ship.energy <= 0:
                print(f"{Colors.RED}ALERT: Enerji bitti! Motor durduruldu.{Colors.END}")
                self.stop_engine()
                return
            
            # Pozisyon güncelleme - 1 matris noktası
            old_x, old_y = self.ship.x, self.ship.y
            
            if self.ship.direction == Direction.UP:
                self.ship.y -= 1
            elif self.ship.direction == Direction.DOWN:
                self.ship.y += 1
            elif self.ship.direction == Direction.LEFT:
                self.ship.x -= 1
            else:  # RIGHT
                self.ship.x += 1
            
            # Sınır kontrolü
            if (self.ship.x < 0 or self.ship.x >= self.universe_size or 
                self.ship.y < 0 or self.ship.y >= self.universe_size):
                print(f"{Colors.RED}ALERT: Evren sınırına ulaşıldı!{Colors.END}")
                self.ship.x = max(0, min(self.ship.x, self.universe_size - 1))
                self.ship.y = max(0, min(self.ship.y, self.universe_size - 1))
                self.stop_engine()
                return
            
            # Çarpışma kontrolü
            collisions = self.check_collision(self.ship.x, self.ship.y)
            if collisions:
                print(f"{Colors.RED}ALERT: Çarpışma!{Colors.END}")
                for obj in collisions:
                    print(f"{Colors.RED}  - {obj.name} ({obj.obj_type.value}) ile çarpışıldı!{Colors.END}")
                self.stop_engine()
                return
            
            # Pozisyon güncelleme zamanını sıfırla
            self.last_position_update = now
    
    def process_command(self, command: str):
        """Komutu işle"""
        parts = command.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        
        # Komut çıktısını temizle
        self.last_command_output = ""
        
        if cmd == "createuniverse":
            size = 14400
            name = "myspaces"
            
            for i in range(1, len(parts)):
                if parts[i].startswith("size="):
                    size = int(parts[i].split("=")[1])
                elif parts[i].startswith("name="):
                    name = parts[i].split("=")[1]
            
            self.create_universe(size, name)
            self.last_command_output = f"{Colors.GREEN}Evren oluşturuldu! Şimdi 'startMission' komutunu kullanın.{Colors.END}"
        
        elif cmd == "startmission":
            max_speed = 1
            for i in range(1, len(parts)):
                if parts[i].startswith("max="):
                    max_speed = int(parts[i].split("=")[1])
            
            self.start_mission(max_speed)
            self.last_command_output = f"{Colors.GREEN}Görev başlatıldı! Gemi hazır.{Colors.END}"
        
        elif cmd == "rotateright":
            self.rotate_right()
            self.last_command_output = f"{Colors.BLUE}Gemi sağa döndü.{Colors.END}"
        
        elif cmd == "rotateleft":
            self.rotate_left()
            self.last_command_output = f"{Colors.BLUE}Gemi sola döndü.{Colors.END}"
        
        elif cmd == "rotateup":
            self.rotate_up()
            self.last_command_output = f"{Colors.BLUE}Gemi yukarı döndü.{Colors.END}"
        
        elif cmd == "rotatedown":
            self.rotate_down()
            self.last_command_output = f"{Colors.BLUE}Gemi aşağı döndü.{Colors.END}"
        
        elif cmd == "turnback":
            self.turn_back()
            self.last_command_output = f"{Colors.BLUE}Gemi geri döndü.{Colors.END}"
        
        elif cmd == "startengine":
            self.start_engine()
            self.last_command_output = f"{Colors.GREEN}Motor başlatıldı!{Colors.END}"
        
        elif cmd == "stopengine":
            self.stop_engine()
            self.last_command_output = f"{Colors.YELLOW}Motor durduruldu!{Colors.END}"
        
        elif cmd == "checkup":
            self.check_up()
            self.last_command_output = f"{Colors.CYAN}Yukarı kontrol edildi.{Colors.END}"
        
        elif cmd == "checkdown":
            self.check_down()
            self.last_command_output = f"{Colors.CYAN}Aşağı kontrol edildi.{Colors.END}"
        
        elif cmd == "checkleft":
            self.check_left()
            self.last_command_output = f"{Colors.CYAN}Sola kontrol edildi.{Colors.END}"
        
        elif cmd == "checkright":
            self.check_right()
            self.last_command_output = f"{Colors.CYAN}Sağa kontrol edildi.{Colors.END}"
        
        elif cmd == "quit" or cmd == "exit":
            self.running = False
        
        elif cmd == "help":
            self.show_help()
            self.last_command_output = f"{Colors.CYAN}Yardım menüsü gösterildi.{Colors.END}"
        
        elif cmd == "status":
            self.show_detailed_status()
            self.last_command_output = f"{Colors.CYAN}Detaylı durum gösterildi.{Colors.END}"
        
        elif cmd == "save":
            self.save_game()
            self.last_command_output = f"{Colors.GREEN}Oyun kaydedildi.{Colors.END}"
        
        elif cmd == "load":
            if len(parts) > 1:
                self.load_game(parts[1])
                self.last_command_output = f"{Colors.GREEN}Oyun yüklendi.{Colors.END}"
            else:
                self.last_command_output = f"{Colors.RED}Kullanım: load <dosya_adı>{Colors.END}"
        
        elif cmd == "list":
            self.list_celestial_objects()
            self.last_command_output = f"{Colors.CYAN}Gök cisimleri listelendi.{Colors.END}"
        
        elif cmd == "time":
            self.show_current_time()
            self.last_command_output = f"{Colors.CYAN}Zaman bilgisi gösterildi.{Colors.END}"
        
        else:
            self.last_command_output = f"{Colors.RED}Bilinmeyen komut: {cmd}{Colors.END}\n{Colors.YELLOW}'help' yazarak komutları görebilirsiniz.{Colors.END}"
    
    def show_detailed_status(self):
        """Detaylı durum bilgisi göster"""
        if not self.ship:
            print(f"{Colors.RED}Gemi bulunamadı!{Colors.END}")
            return
        
        print(f"{Colors.CYAN}{Colors.BOLD}=== DETAYLI DURUM ==={Colors.END}")
        print(f"{Colors.WHITE}Gemi Konumu: ({self.ship.x}, {self.ship.y}){Colors.END}")
        print(f"{Colors.WHITE}Yön: {self.ship.direction.value.upper()}{Colors.END}")
        print(f"{Colors.WHITE}Hız: {self.ship.speed} dakika/10 matris{Colors.END}")
        print(f"{Colors.WHITE}Enerji: {self.ship.energy}/{self.ship.max_energy} ({self.ship.energy/self.ship.max_energy*100:.1f}%){Colors.END}")
        print(f"{Colors.WHITE}Durum: {'HAREKET HALİNDE' if self.ship.is_moving else 'DURAKLAMADA'}{Colors.END}")
        
        # Zaman bilgileri
        mission_time = self.get_mission_time()
        print(f"{Colors.WHITE}Görev Süresi: {mission_time}{Colors.END}")
        
        if self.ship.is_moving and self.ship.start_time:
            movement_time = self.get_movement_time()
            print(f"{Colors.WHITE}Hareket Süresi: {movement_time}{Colors.END}")
        
        # Görev başlangıç zamanı
        if self.ship.mission_start_time:
            start_time_str = self.ship.mission_start_time.strftime('%H:%M:%S')
            print(f"{Colors.WHITE}Görev Başlangıcı: {start_time_str}{Colors.END}")
        
        print()
    
    def save_game(self):
        """Oyunu kaydet"""
        if not self.ship:
            print(f"{Colors.RED}Kaydedilecek gemi bulunamadı!{Colors.END}")
            return
        
        game_data = {
            "universe_name": self.universe_name,
            "universe_size": self.universe_size,
            "ship": {
                "x": self.ship.x,
                "y": self.ship.y,
                "direction": self.ship.direction.value,
                "speed": self.ship.speed,
                "energy": self.ship.energy,
                "max_energy": self.ship.max_energy,
                "is_moving": self.ship.is_moving,
                "mission_start_time": self.ship.mission_start_time.isoformat() if self.ship.mission_start_time else None,
                "start_time": self.ship.start_time.isoformat() if self.ship.start_time else None
            },
            "saved_at": datetime.now().isoformat()
        }
        
        filename = f"save_{self.universe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(game_data, f, indent=2, ensure_ascii=False)
        
        print(f"{Colors.GREEN}Oyun '{filename}' dosyasına kaydedildi.{Colors.END}")
    
    def load_game(self, filename: str):
        """Oyunu yükle"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                game_data = json.load(f)
            
            # Evren bilgilerini yükle
            self.universe_name = game_data["universe_name"]
            self.universe_size = game_data["universe_size"]
            
            # Evren dosyasını yükle
            universe_file = f"{self.universe_name}.json"
            if os.path.exists(universe_file):
                with open(universe_file, 'r', encoding='utf-8') as f:
                    universe_data = json.load(f)
                
                self.celestial_objects = []
                for obj_data in universe_data["celestial_objects"]:
                    obj = CelestialObject(
                        x=obj_data["x"],
                        y=obj_data["y"],
                        obj_type=CelestialType(obj_data["type"]),
                        name=obj_data["name"],
                        size=obj_data["size"]
                    )
                    self.celestial_objects.append(obj)
                
                self.universe_created = True
            
            # Gemi bilgilerini yükle
            ship_data = game_data["ship"]
            
            # Zaman bilgilerini parse et
            mission_start_time = None
            start_time = None
            
            if ship_data.get("mission_start_time"):
                mission_start_time = datetime.fromisoformat(ship_data["mission_start_time"])
            if ship_data.get("start_time"):
                start_time = datetime.fromisoformat(ship_data["start_time"])
            
            self.ship = Ship(
                x=ship_data["x"],
                y=ship_data["y"],
                direction=Direction(ship_data["direction"]),
                speed=ship_data["speed"],
                energy=ship_data["energy"],
                max_energy=ship_data["max_energy"],
                is_moving=ship_data["is_moving"],
                mission_start_time=mission_start_time,
                start_time=start_time
            )
            
            self.mission_started = True
            self.last_position_update = datetime.now()
            
            print(f"{Colors.GREEN}Oyun '{filename}' dosyasından yüklendi.{Colors.END}")
            
        except FileNotFoundError:
            print(f"{Colors.RED}Dosya bulunamadı: {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Yükleme hatası: {e}{Colors.END}")
    
    def list_celestial_objects(self):
        """Gök cisimlerini listele"""
        if not self.celestial_objects:
            print(f"{Colors.YELLOW}Gök cismi bulunamadı!{Colors.END}")
            return
        
        print(f"{Colors.CYAN}{Colors.BOLD}=== GÖK CİSİMLERİ ==={Colors.END}")
        
        # Türlere göre grupla
        by_type = {}
        for obj in self.celestial_objects:
            if obj.obj_type not in by_type:
                by_type[obj.obj_type] = []
            by_type[obj.obj_type].append(obj)
        
        for obj_type, objects in by_type.items():
            print(f"{Colors.WHITE}{obj_type.value.upper()}: {len(objects)} adet{Colors.END}")
            for obj in objects[:5]:  # İlk 5 tanesini göster
                print(f"  - {obj.name} ({obj.x}, {obj.y})")
            if len(objects) > 5:
                print(f"  ... ve {len(objects) - 5} tane daha")
            print()
    
    def show_current_time(self):
        """Mevcut zamanı göster"""
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        current_date = now.strftime('%Y-%m-%d')
        
        print(f"{Colors.CYAN}{Colors.BOLD}=== ZAMAN BİLGİSİ ==={Colors.END}")
        print(f"{Colors.WHITE}Mevcut Zaman: {current_time}{Colors.END}")
        print(f"{Colors.WHITE}Mevcut Tarih: {current_date}{Colors.END}")
        
        if self.ship and self.ship.mission_start_time:
            mission_time = self.get_mission_time()
            print(f"{Colors.WHITE}Görev Süresi: {mission_time}{Colors.END}")
            
            if self.ship.is_moving and self.ship.start_time:
                movement_time = self.get_movement_time()
                print(f"{Colors.WHITE}Hareket Süresi: {movement_time}{Colors.END}")
        
        print()
    
    def show_help(self):
        """Yardım menüsünü göster"""
        self.clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*self.terminal_width}")
        print(f"{'YARDIM MENÜSÜ':^{self.terminal_width}}")
        print(f"{'='*self.terminal_width}{Colors.END}")
        print()
        print(f"{Colors.CYAN}{Colors.BOLD}KOMUTLAR:{Colors.END}")
        print(f"{Colors.WHITE}  createUniverse size=14400 name=myspaces{Colors.END} - Evren oluştur")
        print(f"{Colors.WHITE}  startMission max=1{Colors.END} - Görevi başlat")
        print(f"{Colors.WHITE}  rotateRight/Left/Up/Down{Colors.END} - Yön değiştir")
        print(f"{Colors.WHITE}  turnBack{Colors.END} - Geri dön")
        print(f"{Colors.WHITE}  startEngine/stopEngine{Colors.END} - Motor kontrolü")
        print(f"{Colors.WHITE}  checkUp/Down/Left/Right{Colors.END} - Yön kontrolü")
        print(f"{Colors.WHITE}  status{Colors.END} - Detaylı durum bilgisi")
        print(f"{Colors.WHITE}  time{Colors.END} - Zaman bilgisi göster")
        print(f"{Colors.WHITE}  save{Colors.END} - Oyunu kaydet")
        print(f"{Colors.WHITE}  load <dosya>{Colors.END} - Oyunu yükle")
        print(f"{Colors.WHITE}  list{Colors.END} - Gök cisimlerini listele")
        print(f"{Colors.WHITE}  help{Colors.END} - Bu yardım menüsü")
        print(f"{Colors.WHITE}  quit/exit{Colors.END} - Oyundan çık")
        print()
        print(f"{Colors.YELLOW}Devam etmek için herhangi bir tuşa basın...{Colors.END}")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass
    
    def print_command_output(self):
        """Komut çıktılarını göster"""
        if self.last_command_output:
            print(f"{Colors.YELLOW}{Colors.BOLD}=== KOMUT ÇIKTISI ==={Colors.END}")
            print(self.last_command_output)
            print(f"{Colors.YELLOW}{Colors.BOLD}{'='*self.terminal_width}{Colors.END}")
            print()
    
    def print_command_line(self):
        """Alt komut satırını yazdır - sabit alt panel"""
        print(f"{Colors.WHITE}{Colors.BOLD}Komut: {Colors.END}", end="", flush=True)
    
    def run(self):
        """Ana oyun döngüsü - sürekli akan matrix görüntü"""
        self.clear_screen()
        self.print_header()
        self.show_help()
        
        print(f"{Colors.CYAN}Oyunu başlatmak için 'createUniverse' komutunu kullanın.{Colors.END}")
        print(f"{Colors.CYAN}Yardım için 'help' yazın.{Colors.END}")
        print()
        
        # Ana oyun döngüsü - sürekli akan matrix görüntü
        while self.running:
            # Gemi pozisyonunu güncelle
            self.update_ship_position()
            
            # Ekranı temizle
            self.clear_screen()
            
            # Üst panel - sabit durum bilgileri
            self.print_status_panel()
            
            # Orta alan - matrix görüntü (sadece gemi varsa)
            if self.ship:
                self.print_matrix_display()
            else:
                print(f"{Colors.CYAN}Gemi bulunamadı. Önce 'startMission' komutunu kullanın.{Colors.END}")
                print()
            
            # Alt komut satırı
            self.print_command_line()
            
            # Basit input sistemi
            try:
                command = input()
                
                # Komutu işle
                if command.strip():
                    self.process_command(command)
                    
                    # Komut işlendikten sonra kısa bir bekleme
                    if not command.startswith('quit') and not command.startswith('exit'):
                        time.sleep(0.5)
                        
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Oyundan çıkılıyor...{Colors.END}")
                break
            except EOFError:
                break
        
        print(f"{Colors.GREEN}Oyun sona erdi. İyi oyunlar!{Colors.END}")

if __name__ == "__main__":
    game = SpaceGame()
    game.run()
