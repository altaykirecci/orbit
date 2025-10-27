#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import time
import random
import json
import os
from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple
import math

# Pygame başlat
pygame.init()

# Renkler (ANSI renk kodları yerine RGB)
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)

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

# Gök cismi sınıfı
class CelestialObject:
    def __init__(self, x: int, y: int, obj_type: CelestialType, name: str = ""):
        self.x = x
        self.y = y
        self.obj_type = obj_type
        self.name = name or f"{obj_type.value}_{random.randint(1, 1000)}"

# Gemi sınıfı
class Ship:
    def __init__(self, x: int, y: int, max_energy: int = 14400):
        self.x = x
        self.y = y
        self.direction = Direction.UP
        self.energy = max_energy
        self.max_energy = max_energy
        self.speed = 1  # dakika cinsinden
        self.is_moving = False
        self.start_time: Optional[datetime] = None
        self.mission_start_time: Optional[datetime] = None

# Ana oyun sınıfı
class SpaceGamePygame:
    def __init__(self):
        # Pygame ayarları
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Uzay Oyunu - Pygame")
        
        # Font ayarları
        self.font_small = pygame.font.Font(None, 16)
        self.font_medium = pygame.font.Font(None, 20)
        self.font_large = pygame.font.Font(None, 24)
        # Monospace font için sistem fontunu kullan
        try:
            self.font_mono = pygame.font.Font("DejaVuSansMono.ttf", 16)
        except:
            # Sistem fontunu kullan
            self.font_mono = pygame.font.Font(None, 16)
        
        # Oyun durumu
        self.running = True
        self.universe_size = 14400
        self.celestial_objects: List[CelestialObject] = []
        self.ship: Optional[Ship] = None
        self.mission_started = False
        self.last_position_update = datetime.now()
        self.last_command_output = ""
        
        # UI alanları
        self.header_height = 60
        self.status_height = 120
        self.command_height = 40
        self.matrix_height = self.screen_height - self.header_height - self.status_height - self.command_height
        
        # Matrix görüntü için
        self.matrix_lines = []
        self.max_matrix_lines = 20
        self.last_matrix_update = datetime.now()
        
        # Görsel matris için
        self.matrix_size = 40  # 40x40 matris (20 eksik + 20 fazla)
        self.cell_size = 12  # Her hücre 12x12 pixel
        self.matrix_x = (self.screen_width - self.matrix_size * self.cell_size) // 2  # Ortada
        self.matrix_y = self.header_height + self.status_height + 20  # Üst panelin altında
        
        # Matris başlangıç koordinatları
        self.matrix_start_x = 0
        self.matrix_start_y = 0
        
        # Hesaplama değişkenleri
        self.points_per_minute = 10  # 1 dakikada 10 nokta
        self.points_per_10_minutes = 100  # 10 dakikada 100 nokta
        self.seconds_per_point = 6  # 1 noktaya 6 saniye
        self.last_position_update = datetime.now()
        
        # Matris yeniden render için
        self.last_matrix_center_x = 0
        self.last_matrix_center_y = 0
        self.matrix_render_threshold = 10  # 10 nokta hareket edince matrisi yenile
        
        # Clock
        self.clock = pygame.time.Clock()
        
    def clear_screen(self):
        """Ekranı temizle"""
        self.screen.fill(Colors.BLACK)
    
    def print_header(self):
        """Başlık çiz"""
        header_text = "UZAY OYUNU - PYGAME SIMÜLASYONU"
        text_surface = self.font_large.render(header_text, True, Colors.CYAN)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.header_height // 2))
        self.screen.blit(text_surface, text_rect)
        
        # Alt çizgi
        pygame.draw.line(self.screen, Colors.CYAN, (0, self.header_height), (self.screen_width, self.header_height), 2)
    
    def print_status_panel(self):
        """Üst durum panelini çiz"""
        if not self.mission_started or not self.ship:
            return
        
        y_start = self.header_height + 10
        
        # Enerji bilgisi
        energy_percent = (self.ship.energy / self.ship.max_energy) * 100
        energy_color = Colors.GREEN if energy_percent > 50 else Colors.YELLOW if energy_percent > 25 else Colors.RED
        
        energy_text = f"ENERJİ: {self.ship.energy}/{self.ship.max_energy} ({energy_percent:.1f}%)"
        energy_surface = self.font_medium.render(energy_text, True, energy_color)
        self.screen.blit(energy_surface, (10, y_start))
        
        # Hız bilgisi
        speed_text = f"HIZ: {self.ship.speed} dk/10 matris"
        speed_surface = self.font_medium.render(speed_text, True, Colors.BLUE)
        self.screen.blit(speed_surface, (400, y_start))
        
        # Yön bilgisi
        y_start += 25
        direction_text = f"YÖN: {self.ship.direction.value.upper()}"
        direction_surface = self.font_medium.render(direction_text, True, Colors.WHITE)
        self.screen.blit(direction_surface, (10, y_start))
        
        # Durum bilgisi
        status_text = "HAREKET HALİNDE" if self.ship.is_moving else "DURAKLAMADA"
        status_color = Colors.GREEN if self.ship.is_moving else Colors.YELLOW
        status_surface = self.font_medium.render(f"DURUM: {status_text}", True, status_color)
        self.screen.blit(status_surface, (400, y_start))
        
        # Görev süresi
        y_start += 25
        mission_time = self.get_mission_time()
        mission_surface = self.font_medium.render(f"GÖREV SÜRESİ: {mission_time}", True, Colors.CYAN)
        self.screen.blit(mission_surface, (10, y_start))
        
        # Hareket süresi
        if self.ship.is_moving:
            movement_time = self.get_movement_time()
            movement_surface = self.font_medium.render(f"HAREKET SÜRESİ: {movement_time}", True, Colors.MAGENTA)
            self.screen.blit(movement_surface, (400, y_start))
        
        # Hız hesaplama bilgileri
        y_start += 25
        speed_info_text = f"HIZ HESAPLAMA: 1 dk = {self.points_per_minute} nokta, 10 dk = {self.points_per_10_minutes} nokta"
        speed_info_surface = self.font_small.render(speed_info_text, True, Colors.CYAN)
        self.screen.blit(speed_info_surface, (10, y_start))
        
        y_start += 20
        time_info_text = f"ZAMAN HESAPLAMA: 1 nokta = {self.seconds_per_point:.1f} saniye, Güncelleme = {self.seconds_per_point:.1f} saniyede bir"
        time_info_surface = self.font_small.render(time_info_text, True, Colors.CYAN)
        self.screen.blit(time_info_surface, (10, y_start))
    
    def print_matrix_display(self):
        """Matrix tarzı akışkan görüntü"""
        if not self.ship:
            return
        
        # Matrix alanını temizle
        matrix_rect = pygame.Rect(0, self.header_height + self.status_height, self.screen_width, self.matrix_height)
        pygame.draw.rect(self.screen, Colors.BLACK, matrix_rect)
        
        # 100x100 görsel matris çiz
        self.draw_visual_matrix()
        
        # Matrix çizgilerini göster (alt kısımda)
        y_offset = self.matrix_y + self.matrix_size * self.cell_size + 10
        
        for i, (line, color) in enumerate(self.matrix_lines[-self.max_matrix_lines:]):
            text_surface = self.font_mono.render(line, True, color)
            self.screen.blit(text_surface, (10, y_offset + i * 20))
    
    def draw_visual_matrix(self):
        """40x40 dinamik matris çiz"""
        if not self.ship:
            return
        
        # Matris merkezini kontrol et - 10 nokta değişti mi?
        distance_moved = ((self.ship.x - self.last_matrix_center_x) ** 2 + 
                         (self.ship.y - self.last_matrix_center_y) ** 2) ** 0.5
        
        # 10 nokta veya daha fazla hareket edildiyse matrisi yeniden render et
        if distance_moved >= self.matrix_render_threshold:
            self.last_matrix_center_x = self.ship.x
            self.last_matrix_center_y = self.ship.y
            self.add_matrix_line(f"MATRİS YENİLENDİ: Merkez ({self.ship.x}, {self.ship.y}) - {distance_moved:.1f} nokta hareket edildi", Colors.CYAN)
        
        # Matris başlangıç koordinatlarını güncelle (gemi pozisyonuna göre)
        self.matrix_start_x = self.ship.x - 20  # 20 eksik
        self.matrix_start_y = self.ship.y - 20  # 20 eksik
        
        # Matris çerçevesi
        matrix_rect = pygame.Rect(
            self.matrix_x, 
            self.matrix_y, 
            self.matrix_size * self.cell_size, 
            self.matrix_size * self.cell_size
        )
        pygame.draw.rect(self.screen, Colors.GRAY, matrix_rect, 1)
        
        # Koordinat etiketlerini çiz
        self.draw_coordinate_labels()
        
        # Her hücreyi kontrol et ve çiz
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                # Gerçek koordinatları hesapla
                real_x = self.matrix_start_x + i
                real_y = self.matrix_start_y + j
                
                # Hücre rengini belirle
                color = Colors.BLACK
                
                # Gemi pozisyonu (merkez)
                if real_x == self.ship.x and real_y == self.ship.y:
                    color = Colors.YELLOW  # Turuncu yerine sarı
                # Bir sonraki pozisyon
                elif real_x == self.ship.x + (1 if self.ship.direction == Direction.RIGHT else -1 if self.ship.direction == Direction.LEFT else 0) and \
                     real_y == self.ship.y + (1 if self.ship.direction == Direction.DOWN else -1 if self.ship.direction == Direction.UP else 0):
                    color = Colors.RED
                # 10 nokta içinde cisim var mı kontrol et
                else:
                    objects_in_range = self.get_objects_in_range(real_x, real_y, 10)
                    if objects_in_range:
                        color = Colors.RED
                
                # Hücreyi çiz
                cell_rect = pygame.Rect(
                    self.matrix_x + i * self.cell_size,
                    self.matrix_y + j * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, color, cell_rect)
                
                # Hücre sınırları
                pygame.draw.rect(self.screen, Colors.DARK_GRAY, cell_rect, 1)
    
    def draw_coordinate_labels(self):
        """Koordinat etiketlerini çiz"""
        # X ekseni etiketleri (üst)
        for i in range(0, self.matrix_size, 5):  # Her 5 hücrede bir
            real_x = self.matrix_start_x + i
            label_text = str(real_x)
            label_surface = self.font_small.render(label_text, True, Colors.WHITE)
            self.screen.blit(label_surface, (self.matrix_x + i * self.cell_size, self.matrix_y - 15))
        
        # Y ekseni etiketleri (sol)
        for j in range(0, self.matrix_size, 5):  # Her 5 hücrede bir
            real_y = self.matrix_start_y + j
            label_text = str(real_y)
            label_surface = self.font_small.render(label_text, True, Colors.WHITE)
            self.screen.blit(label_surface, (self.matrix_x - 50, self.matrix_y + j * self.cell_size))
    
    def get_objects_in_range(self, x: int, y: int, range_distance: int) -> List[CelestialObject]:
        """Belirli bir noktadan belirli mesafede olan cisimleri bul"""
        objects_in_range = []
        for obj in self.celestial_objects:
            distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
            if distance <= range_distance:
                objects_in_range.append(obj)
        return objects_in_range
    
    def scan_coordinates(self, x: int, y: int):
        """Belirli koordinatlarda cisim taraması yap"""
        objects_found = []
        
        # 10 nokta içindeki tüm cisimleri bul
        for obj in self.celestial_objects:
            distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
            if distance <= 10:
                objects_found.append((obj, distance))
        
        # Sonuçları kırmızı renkte göster
        if objects_found:
            self.add_matrix_line(f"SCAN SONUCU ({x}:{y}):", Colors.RED)
            for obj, distance in objects_found:
                obj_info = f"  {obj.name} ({obj.obj_type.value}) - Mesafe: {distance:.1f} - Konum: ({obj.x}, {obj.y})"
                self.add_matrix_line(obj_info, Colors.RED)
        else:
            self.add_matrix_line(f"SCAN SONUCU ({x}:{y}): 10 nokta içinde cisim bulunamadı", Colors.RED)
    
    def add_matrix_line(self, text: str, color: tuple = Colors.GREEN):
        """Matrix görüntüye yeni satır ekle"""
        current_time = datetime.now().strftime('%H:%M:%S')
        line = f"[{current_time}] {text}"
        self.matrix_lines.append((line, color))
        
        # Çok fazla satır varsa eski olanları sil
        if len(self.matrix_lines) > self.max_matrix_lines * 2:
            self.matrix_lines = self.matrix_lines[-self.max_matrix_lines:]
    
    def print_command_line(self):
        """Alt komut satırını çiz"""
        y_pos = self.screen_height - self.command_height + 10
        
        # Komut satırı arka planı
        command_rect = pygame.Rect(0, self.screen_height - self.command_height, self.screen_width, self.command_height)
        pygame.draw.rect(self.screen, Colors.DARK_GRAY, command_rect)
        pygame.draw.line(self.screen, Colors.GRAY, (0, y_pos - 10), (self.screen_width, y_pos - 10), 1)
        
        # Komut prompt'u
        prompt_text = "Komut: "
        prompt_surface = self.font_medium.render(prompt_text, True, Colors.WHITE)
        self.screen.blit(prompt_surface, (10, y_pos))
        
        # Son komut çıktısı
        if self.last_command_output:
            output_surface = self.font_small.render(self.last_command_output, True, Colors.YELLOW)
            self.screen.blit(output_surface, (100, y_pos))
    
    def get_mission_time(self) -> str:
        """Görev süresini hesapla"""
        if not self.ship or not self.ship.mission_start_time:
            return "00:00:00"
        
        elapsed = (datetime.now() - self.ship.mission_start_time).total_seconds()
        return self.format_time(elapsed)
    
    def get_movement_time(self) -> str:
        """Hareket süresini hesapla"""
        if not self.ship or not self.ship.start_time:
            return "00:00:00"
        
        elapsed = (datetime.now() - self.ship.start_time).total_seconds()
        return self.format_time(elapsed)
    
    def format_time(self, total_seconds: float) -> str:
        """Saniyeyi saat:dakika:saniye formatına çevir"""
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def calculate_speed_info(self):
        """Hız bilgilerini hesapla"""
        if not self.ship:
            return
        
        # 1 dakikada 10 nokta, 10 dakikada 100 nokta
        self.points_per_minute = 10
        self.points_per_10_minutes = self.points_per_minute * 10  # 100 nokta
        
        # 1 noktaya kaç saniyede gidiyor
        self.seconds_per_point = 60 / self.points_per_minute  # 6 saniye
    
    def get_next_position(self):
        """Bir sonraki pozisyonu hesapla"""
        if not self.ship or not self.ship.is_moving:
            return self.ship.x, self.ship.y if self.ship else (0, 0)
        
        # Mevcut pozisyon
        x, y = self.ship.x, self.ship.y
        
        # Yöne göre bir sonraki pozisyon
        if self.ship.direction == Direction.UP:
            y -= 1
        elif self.ship.direction == Direction.DOWN:
            y += 1
        elif self.ship.direction == Direction.LEFT:
            x -= 1
        else:  # RIGHT
            x += 1
        
        return x, y
    
    def update_ship_position(self):
        """Gemi pozisyonunu güncelle - 6 saniyede bir"""
        if not self.ship or not self.ship.is_moving:
            return
        
        now = datetime.now()
        time_diff = (now - self.last_position_update).total_seconds()  # saniye cinsinden
        
        # 6 saniyede bir pozisyon güncelle
        if time_diff >= self.seconds_per_point:
            # Enerji tüketimi
            energy_cost_per_point = 1 if self.ship.speed == 1 else self.ship.max_energy / (self.ship.speed * 10)
            self.ship.energy -= int(energy_cost_per_point)
            
            if self.ship.energy <= 0:
                self.add_matrix_line("ALERT: Enerji bitti! Motor durduruldu.")
                self.stop_engine()
                return
            
            # Pozisyon güncelleme
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
                self.add_matrix_line("ALERT: Evren sınırına ulaşıldı!")
                self.ship.x = max(0, min(self.ship.x, self.universe_size - 1))
                self.ship.y = max(0, min(self.ship.y, self.universe_size - 1))
                self.stop_engine()
                return
            
            # Çarpışma kontrolü
            collisions = self.check_collision(self.ship.x, self.ship.y)
            if collisions:
                self.add_matrix_line("ALERT: Çarpışma!")
                for obj in collisions:
                    self.add_matrix_line(f"  - {obj.name} ({obj.obj_type.value}) ile çarpışıldı!")
                self.stop_engine()
                return
            
            # Pozisyon güncelleme zamanını sıfırla
            self.last_position_update = now
            
            # Matrix görüntüye pozisyon bilgisi ekle
            self.add_matrix_line(f"{self.ship.x} {self.ship.y} Pozisyon güncellendi - {self.ship.direction.value.upper()}")
    
    def check_collision(self, x: int, y: int) -> List[CelestialObject]:
        """Çarpışma kontrolü"""
        collisions = []
        for obj in self.celestial_objects:
            if obj.x == x and obj.y == y:
                collisions.append(obj)
        return collisions
    
    def process_command(self, command: str):
        """Komutu işle"""
        parts = command.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        self.last_command_output = ""
        
        if cmd == "createuniverse":
            if len(parts) < 3:
                self.last_command_output = "HATA: createUniverse size=<sayı> name=<isim> formatında kullanın"
                return
            
            try:
                size = int(parts[1].split('=')[1])
                name = parts[2].split('=')[1]
                
                if size < 14400:
                    self.last_command_output = "HATA: Evren boyutu en az 14400 olmalı"
                    return
                
                self.universe_size = size
                self.create_universe(name)
                self.last_command_output = f"Evren oluşturuldu: {name}.json ({size}x{size})"
                
            except (ValueError, IndexError):
                self.last_command_output = "HATA: Geçersiz parametreler"
        
        elif cmd == "startmission":
            if not self.celestial_objects:
                self.last_command_output = "HATA: Önce evren oluşturulmalı!"
                return
            
            max_speed = 1
            if len(parts) > 1 and parts[1].startswith('max='):
                try:
                    max_speed = int(parts[1].split('=')[1])
                except ValueError:
                    pass
            
            self.start_mission(max_speed)
            self.last_command_output = f"Görev başlatıldı! Hız: {max_speed} dk/10 matris"
        
        elif cmd == "startengine":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                return
            
            self.start_engine()
            self.last_command_output = "Motor başlatıldı!"
        
        elif cmd == "stopengine":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                return
            
            self.stop_engine()
            self.last_command_output = "Motor durduruldu!"
        
        elif cmd == "rotateright":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                return
            
            self.rotate_right()
            self.last_command_output = "Sağa döndü!"
        
        elif cmd == "rotateleft":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                return
            
            self.rotate_left()
            self.last_command_output = "Sola döndü!"
        
        elif cmd == "rotateup":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                return
            
            self.rotate_up()
            self.last_command_output = "Yukarı döndü!"
        
        elif cmd == "rotatedown":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                return
            
            self.rotate_down()
            self.last_command_output = "Aşağı döndü!"
        
        elif cmd == "turnback":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                return
            
            self.turn_back()
            self.last_command_output = "Geri döndü!"
        
        elif cmd == "scan":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                return
            
            if len(parts) < 2:
                self.last_command_output = "HATA: Kullanım: scan <x:y> (örn: scan 2303:4712)"
                return
            
            try:
                coords = parts[1].split(":")
                x = int(coords[0])
                y = int(coords[1])
                self.scan_coordinates(x, y)
            except (ValueError, IndexError):
                self.last_command_output = "HATA: Geçersiz koordinat formatı! (örn: scan 2303:4712)"
        
        elif cmd == "quit" or cmd == "exit":
            self.running = False
            self.last_command_output = "Oyundan çıkılıyor..."
        
        else:
            self.last_command_output = f"Bilinmeyen komut: {cmd}"
    
    def create_universe(self, name: str):
        """Evren oluştur"""
        self.celestial_objects = []
        
        # Rastgele gök cisimleri oluştur
        num_objects = random.randint(50, 200)
        
        for _ in range(num_objects):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            obj_type = random.choice(list(CelestialType))
            obj = CelestialObject(x, y, obj_type)
            self.celestial_objects.append(obj)
        
        # JSON dosyasına kaydet
        universe_data = {
            "size": self.universe_size,
            "objects": [
                {
                    "x": obj.x,
                    "y": obj.y,
                    "type": obj.obj_type.value,
                    "name": obj.name
                }
                for obj in self.celestial_objects
            ]
        }
        
        with open(f"{name}.json", "w", encoding="utf-8") as f:
            json.dump(universe_data, f, indent=2, ensure_ascii=False)
    
    def start_mission(self, max_speed: int = 1):
        """Görevi başlat"""
        if not self.celestial_objects:
            return
        
        # Rastgele pozisyon
        x = random.randint(0, self.universe_size - 1)
        y = random.randint(0, self.universe_size - 1)
        
        self.ship = Ship(x, y)
        self.ship.speed = max_speed
        self.ship.mission_start_time = datetime.now()
        self.mission_started = True
        
        # Hız bilgilerini hesapla
        self.calculate_speed_info()
        
        # Matris merkezini başlat
        self.last_matrix_center_x = x
        self.last_matrix_center_y = y
        
        self.add_matrix_line(f"Görev başlatıldı! Konum: ({x}, {y})")
        self.add_matrix_line(f"Hız: {max_speed} dk/10 matris = {self.points_per_minute} nokta/dk")
        self.add_matrix_line(f"Güncelleme: {self.seconds_per_point:.1f} saniyede bir")
        self.add_matrix_line(f"Matris merkezi: ({x}, {y}) - 10 nokta hareket edildiğinde yenilenecek", Colors.CYAN)
    
    def start_engine(self):
        """Motoru başlat"""
        if self.ship:
            self.ship.is_moving = True
            self.ship.start_time = datetime.now()
            self.last_position_update = datetime.now()
    
    def stop_engine(self):
        """Motoru durdur"""
        if self.ship:
            self.ship.is_moving = False
    
    def rotate_right(self):
        """Sağa dön"""
        if self.ship:
            if self.ship.direction == Direction.UP:
                self.ship.direction = Direction.RIGHT
            elif self.ship.direction == Direction.RIGHT:
                self.ship.direction = Direction.DOWN
            elif self.ship.direction == Direction.DOWN:
                self.ship.direction = Direction.LEFT
            else:  # LEFT
                self.ship.direction = Direction.UP
    
    def rotate_left(self):
        """Sola dön"""
        if self.ship:
            if self.ship.direction == Direction.UP:
                self.ship.direction = Direction.LEFT
            elif self.ship.direction == Direction.LEFT:
                self.ship.direction = Direction.DOWN
            elif self.ship.direction == Direction.DOWN:
                self.ship.direction = Direction.RIGHT
            else:  # RIGHT
                self.ship.direction = Direction.UP
    
    def rotate_up(self):
        """Yukarı dön"""
        if self.ship:
            self.ship.direction = Direction.UP
    
    def rotate_down(self):
        """Aşağı dön"""
        if self.ship:
            self.ship.direction = Direction.DOWN
    
    def turn_back(self):
        """Geri dön"""
        if self.ship:
            if self.ship.direction == Direction.UP:
                self.ship.direction = Direction.DOWN
            elif self.ship.direction == Direction.DOWN:
                self.ship.direction = Direction.UP
            elif self.ship.direction == Direction.LEFT:
                self.ship.direction = Direction.RIGHT
            else:  # RIGHT
                self.ship.direction = Direction.LEFT
    
    def run(self):
        """Ana oyun döngüsü"""
        # Başlangıç mesajları
        self.add_matrix_line("Uzay Oyunu başlatıldı!")
        self.add_matrix_line("Komutlar: createUniverse, startMission, startEngine, stopEngine")
        self.add_matrix_line("Hareket: rotateRight, rotateLeft, rotateUp, rotateDown, turnBack")
        self.add_matrix_line("Çıkış: quit veya exit")
        
        # Komut satırı için
        self.current_command = ""
        
        # Ana oyun döngüsü
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Enter tuşu - komut işle
                        if self.current_command:
                            self.process_command(self.current_command)
                            self.current_command = ""
                    elif event.key == pygame.K_BACKSPACE:
                        # Backspace - karakter sil
                        if self.current_command:
                            self.current_command = self.current_command[:-1]
                    else:
                        # Karakter ekle
                        self.current_command += event.unicode
            
            # Gemi pozisyonunu güncelle
            self.update_ship_position()
            
            # Ekranı temizle
            self.clear_screen()
            
            # UI elemanlarını çiz
            self.print_header()
            self.print_status_panel()
            self.print_matrix_display()
            self.print_command_line()
            
            # Mevcut komutu göster
            y_pos = self.screen_height - self.command_height + 10
            command_text = f"Komut: {self.current_command}_"
            command_surface = self.font_medium.render(command_text, True, Colors.WHITE)
            self.screen.blit(command_surface, (10, y_pos))
            
            # Ekranı güncelle
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SpaceGamePygame()
    game.run()
