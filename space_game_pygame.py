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
        self.current_universe_name = "uzay"
        
        # UI alanları - 3 bölümlü düzen
        self.left_width = self.screen_width // 3  # Sol bölüm
        self.right_width = self.screen_width - self.left_width  # Sağ bölüm (matris)
        
        # Sol bölüm - 2'ye bölünmüş
        self.left_top_height = self.screen_height // 2  # Sol üst (status)
        self.left_bottom_height = self.screen_height - self.left_top_height  # Sol alt (komut çıktısı)
        
        # Sağ bölüm (matris)
        self.matrix_width = self.right_width
        self.matrix_height = self.screen_height
        
        # Komut satırı yüksekliği
        self.command_height = 40
        
        # Matrix görüntü için
        self.matrix_lines = []
        self.max_matrix_lines = 20
        self.last_matrix_update = datetime.now()
        
        # Komut çıktısı için
        self.command_output_lines = []
        self.max_command_output_lines = 15
        
        # Görsel matris için
        self.matrix_size = 40  # 40x40 matris (20 eksik + 20 fazla)
        self.cell_size = min(self.matrix_width // self.matrix_size, self.matrix_height // self.matrix_size)  # Dinamik boyut
        self.matrix_x = self.left_width + (self.matrix_width - self.matrix_size * self.cell_size) // 2  # Sağ bölümde ortada
        self.matrix_y = (self.matrix_height - self.matrix_size * self.cell_size) // 2  # Dikey ortada
        
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
        """Başlık çiz - kaldırıldı"""
        pass
    
    def print_status_panel(self):
        """Sol üst durum panelini çiz"""
        if not self.mission_started or not self.ship:
            return
        
        # Sol üst bölüm arka planı
        status_rect = pygame.Rect(0, 0, self.left_width, self.left_top_height)
        pygame.draw.rect(self.screen, Colors.DARK_GRAY, status_rect)
        pygame.draw.rect(self.screen, Colors.GREEN, status_rect, 2)
        
        y_start = 20
        
        # Görev süresi (yeşil)
        mission_time = self.get_mission_time()
        mission_surface = self.font_large.render(f"GÖREV SÜRESİ: {mission_time}", True, Colors.GREEN)
        self.screen.blit(mission_surface, (10, y_start))
        
        # Hız bilgisi (yeşil)
        speed_text = f"HIZ: {self.ship.speed} dk/10 matris"
        speed_surface = self.font_large.render(speed_text, True, Colors.GREEN)
        self.screen.blit(speed_surface, (10, y_start + 40))
        
        # Enerji bilgisi (yeşil)
        energy_percent = (self.ship.energy / self.ship.max_energy) * 100
        energy_text = f"ENERJİ: {self.ship.energy}/{self.ship.max_energy} ({energy_percent:.1f}%)"
        energy_surface = self.font_large.render(energy_text, True, Colors.GREEN)
        self.screen.blit(energy_surface, (10, y_start + 80))
        
        # X koordinatı (yeşil)
        x_text = f"X: {self.ship.x}"
        x_surface = self.font_large.render(x_text, True, Colors.GREEN)
        self.screen.blit(x_surface, (10, y_start + 120))
        
        # Y koordinatı (yeşil)
        y_text = f"Y: {self.ship.y}"
        y_surface = self.font_large.render(y_text, True, Colors.GREEN)
        self.screen.blit(y_surface, (10, y_start + 160))
        
        # Durum (hareket halindeyse yeşil, duruksa kırmızı)
        status_text = "HAREKET HALİNDE" if self.ship.is_moving else "DURAK"
        status_color = Colors.GREEN if self.ship.is_moving else Colors.RED
        status_surface = self.font_large.render(status_text, True, status_color)
        self.screen.blit(status_surface, (10, y_start + 200))
    
    def print_command_output_panel(self):
        """Sol alt komut çıktısı panelini çiz"""
        # Sol alt bölüm arka planı
        output_rect = pygame.Rect(0, self.left_top_height, self.left_width, self.left_bottom_height)
        pygame.draw.rect(self.screen, Colors.BLACK, output_rect)
        pygame.draw.rect(self.screen, Colors.CYAN, output_rect, 2)
        
        # Komut çıktısı başlığı
        title_surface = self.font_medium.render("KOMUT ÇIKTISI", True, Colors.CYAN)
        self.screen.blit(title_surface, (10, self.left_top_height + 10))
        
        # Komut çıktısı satırları
        y_offset = self.left_top_height + 40
        for i, line in enumerate(self.command_output_lines[-self.max_command_output_lines:]):
            if i * 20 + y_offset < self.screen_height - 20:  # Ekran sınırları içinde
                line_surface = self.font_small.render(line, True, Colors.WHITE)
                self.screen.blit(line_surface, (10, y_offset + i * 20))
    
    def add_command_output(self, text: str, color=Colors.WHITE):
        """Komut çıktısına satır ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.command_output_lines.append(f"[{timestamp}] {text}")
        if len(self.command_output_lines) > self.max_command_output_lines:
            self.command_output_lines.pop(0)
    
    def print_matrix_display(self):
        """Sağ bölümde matrix görüntü"""
        if not self.ship:
            return
        
        # Sağ bölüm arka planı
        matrix_rect = pygame.Rect(self.left_width, 0, self.matrix_width, self.matrix_height)
        pygame.draw.rect(self.screen, Colors.BLACK, matrix_rect)
        pygame.draw.rect(self.screen, Colors.GREEN, matrix_rect, 2)
        
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
    
    def teleport_ship(self, x: int, y: int):
        """Gemi teleportasyonu"""
        # Sınır kontrolü
        if x < 0 or x >= self.universe_size or y < 0 or y >= self.universe_size:
            self.last_command_output = f"HATA: Koordinatlar evren sınırları dışında! (0-{self.universe_size-1})"
            self.add_command_output(f"HATA: Koordinatlar evren sınırları dışında! (0-{self.universe_size-1})")
            return
        
        # Enerji kontrolü
        energy_cost = int(self.ship.max_energy * 0.05)  # %5 enerji
        if self.ship.energy < energy_cost:
            self.last_command_output = f"HATA: Yetersiz enerji! Gerekli: {energy_cost}, Mevcut: {self.ship.energy}"
            self.add_command_output(f"HATA: Yetersiz enerji! Gerekli: {energy_cost}, Mevcut: {self.ship.energy}")
            return
        
        # Eski pozisyonu kaydet
        old_x, old_y = self.ship.x, self.ship.y
        
        # Enerji tüket
        self.ship.energy -= energy_cost
        
        # Pozisyonu güncelle
        self.ship.x = x
        self.ship.y = y
        
        # Matris merkezini güncelle (teleportasyon sonrası)
        self.last_matrix_center_x = x
        self.last_matrix_center_y = y
        
        # Motoru durdur (teleportasyon sonrası güvenlik)
        self.ship.is_moving = False
        
        # Başarı mesajı
        self.last_command_output = f"TELEPORTASYON BAŞARILI! ({old_x}, {old_y}) → ({x}, {y})"
        
        # Komut çıktısına ekle
        self.add_command_output(f"({x},{y}) koordinatına ışınlanıldı")
        self.add_command_output(f"Enerji tüketimi: {energy_cost} birim")
        
        # Matrix görüntüye bilgi ekle
        self.add_matrix_line(f"TELEPORTASYON: ({old_x}, {old_y}) → ({x}, {y})", Colors.MAGENTA)
        self.add_matrix_line(f"ENERJİ TÜKETİMİ: {energy_cost} birim (%5)", Colors.MAGENTA)
        self.add_matrix_line(f"MATRİS MERKEZİ: ({x}, {y})", Colors.CYAN)
        
        # Çarpışma kontrolü
        collisions = self.check_collision(x, y)
        if collisions:
            self.add_matrix_line("ALERT: Teleportasyon sonrası çarpışma!", Colors.RED)
            self.add_command_output("ALERT: Teleportasyon sonrası çarpışma!")
            for obj in collisions:
                self.add_matrix_line(f"  - {obj.name} ({obj.obj_type.value}) ile çarpışıldı!", Colors.RED)
    
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
        
        # Dinamik prompt oluştur
        if self.ship and self.mission_started:
            # Evren adını al (son yüklenen evren)
            universe_name = "unknown"
            if hasattr(self, 'current_universe_name'):
                universe_name = self.current_universe_name
            
            # Yön bilgisi
            direction_text = self.ship.direction.value.upper()
            
            # Durum bilgisi
            status_text = "HAREKET HALİNDE" if self.ship.is_moving else "DURAK"
            
            # Prompt oluştur
            prompt_text = f"{universe_name}@{direction_text}-{status_text}:$ "
        else:
            prompt_text = "uzay@başlatma:$ "
        
        # Prompt'u çiz
        prompt_surface = self.font_medium.render(prompt_text, True, Colors.GREEN)
        self.screen.blit(prompt_surface, (10, y_pos))
        
        # Yanıp sönen cursor
        current_time = datetime.now()
        if int(current_time.microsecond / 500000) % 2:  # Her 0.5 saniyede bir yanıp söner
            cursor_x = 10 + prompt_surface.get_width()
            cursor_surface = self.font_medium.render("_", True, Colors.WHITE)
            self.screen.blit(cursor_surface, (cursor_x, y_pos))
        
        # Son komut çıktısı (hata mesajları kırmızı)
        if self.last_command_output:
            # Hata mesajlarını kırmızı renkte göster
            color = Colors.RED if self.last_command_output.startswith("HATA:") else Colors.YELLOW
            output_surface = self.font_small.render(self.last_command_output, True, color)
            self.screen.blit(output_surface, (10, y_pos + 20))
    
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
            self.last_command_output = "HATA: Boş komut!"
            return
        
        cmd = parts[0].lower()
        self.last_command_output = ""
        
        if cmd == "go":
            # Parametreleri parse et
            name = None
            size = 14400  # Default boyut
            velocity = 1  # Default hız
            force_create = False  # Zorla oluştur flag'i
            
            i = 1
            while i < len(parts):
                part = parts[i]
                
                if part in ["--name", "-n"]:
                    if i + 1 < len(parts):
                        name = parts[i + 1]
                        i += 2
                    else:
                        self.last_command_output = "HATA: --name (-n) parametresi için değer gerekli!"
                        self.add_command_output("HATA: --name (-n) parametresi için değer gerekli!")
                        return
                elif part in ["--size", "-s"]:
                    if i + 1 < len(parts):
                        try:
                            size = int(parts[i + 1])
                            if size < 14400:
                                self.last_command_output = "HATA: Evren boyutu en az 14400 olmalı!"
                                self.add_command_output("HATA: Evren boyutu en az 14400 olmalı!")
                                return
                            i += 2
                        except ValueError:
                            self.last_command_output = "HATA: Geçersiz boyut değeri!"
                            self.add_command_output("HATA: Geçersiz boyut değeri!")
                            return
                    else:
                        self.last_command_output = "HATA: --size (-s) parametresi için değer gerekli!"
                        self.add_command_output("HATA: --size (-s) parametresi için değer gerekli!")
                        return
                elif part in ["--velocity", "-v"]:
                    if i + 1 < len(parts):
                        try:
                            velocity = int(parts[i + 1])
                            i += 2
                        except ValueError:
                            self.last_command_output = "HATA: Geçersiz hız değeri!"
                            self.add_command_output("HATA: Geçersiz hız değeri!")
                            return
                    else:
                        self.last_command_output = "HATA: --velocity (-v) parametresi için değer gerekli!"
                        self.add_command_output("HATA: --velocity (-v) parametresi için değer gerekli!")
                        return
                elif part in ["--create", "-c"]:
                    force_create = True
                    i += 1
                else:
                    i += 1
            
            # Name parametresi zorunlu
            if name is None:
                self.last_command_output = "HATA: --name (-n) parametresi zorunlu! Örnek: go --name myspaces"
                self.add_command_output("HATA: --name (-n) parametresi zorunlu! Örnek: go --name myspaces")
                return
            
            # Mevcut evreni kontrol et
            universe_file = f"universes/{name}.json"
            self.current_universe_name = name  # Evren adını kaydet
            
            if os.path.exists(universe_file) and not force_create:
                # Mevcut evreni yükle
                self.load_universe(universe_file)
                self.start_mission(velocity)
                self.last_command_output = f"Mevcut evren yüklendi: {name}.json ({self.universe_size}x{self.universe_size})"
                self.add_command_output(f"Evren yüklendi: {name}.json")
                self.add_command_output(f"Boyut: {self.universe_size}x{self.universe_size}")
                self.add_command_output(f"Gök cisimleri: {len(self.celestial_objects)}")
            else:
                # Yeni evren oluştur
                self.universe_size = size
                self.create_universe(name)
                self.start_mission(velocity)
                self.last_command_output = f"Yeni evren oluşturuldu: {name}.json ({self.universe_size}x{self.universe_size})"
                self.add_command_output(f"Yeni evren oluşturuldu: {name}.json")
                self.add_command_output(f"Boyut: {self.universe_size}x{self.universe_size}")
                self.add_command_output(f"Gök cisimleri: {len(self.celestial_objects)}")
        
        elif cmd in ["engine", "e"]:
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                self.add_command_output("HATA: Önce görev başlatılmalı!")
                return
            
            if len(parts) < 2:
                self.last_command_output = "HATA: Kullanım: engine on/off veya e on/off"
                self.add_command_output("HATA: Kullanım: engine on/off veya e on/off")
                return
            
            action = parts[1].lower()
            if action == "on":
                self.start_engine()
                self.last_command_output = "Engine is ON"
                self.add_command_output("Engine is ON")
            elif action == "off":
                self.stop_engine()
                self.last_command_output = "Engine is OFF"
                self.add_command_output("Engine is OFF")
            else:
                self.last_command_output = "HATA: Geçersiz parametre! 'on' veya 'off' kullanın"
                self.add_command_output("HATA: Geçersiz parametre! 'on' veya 'off' kullanın")
        
        elif cmd in ["rotate", "r"]:
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                self.add_command_output("HATA: Önce görev başlatılmalı!")
                return
            
            if len(parts) < 2:
                self.last_command_output = "HATA: Kullanım: rotate <yön> veya r <yön>"
                self.add_command_output("HATA: Kullanım: rotate <yön> veya r <yön>")
                self.add_command_output("Yönler: right/r, left/l, up/u, down/d")
                return
            
            direction = parts[1].lower()
            
            if direction in ["right", "r"]:
                self.rotate_right()
                self.last_command_output = "Sağa döndü!"
                self.add_command_output("Sağa döndü!")
            elif direction in ["left", "l"]:
                self.rotate_left()
                self.last_command_output = "Sola döndü!"
                self.add_command_output("Sola döndü!")
            elif direction in ["up", "u"]:
                self.rotate_up()
                self.last_command_output = "Yukarı döndü!"
                self.add_command_output("Yukarı döndü!")
            elif direction in ["down", "d"]:
                self.rotate_down()
                self.last_command_output = "Aşağı döndü!"
                self.add_command_output("Aşağı döndü!")
            else:
                self.last_command_output = "HATA: Geçersiz yön! Kullanım: right/r, left/l, up/u, down/d"
                self.add_command_output("HATA: Geçersiz yön! Kullanım: right/r, left/l, up/u, down/d")
        
        elif cmd == "turnback":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                self.add_command_output("HATA: Önce görev başlatılmalı!")
                return
            
            self.turn_back()
            self.last_command_output = "Geri döndü!"
            self.add_command_output("Geri döndü!")
        
        elif cmd == "scan":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                self.add_command_output("HATA: Önce görev başlatılmalı!")
                return
            
            if len(parts) < 2:
                self.last_command_output = "HATA: Kullanım: scan <x:y> (örn: scan 2303:4712)"
                self.add_command_output("HATA: Kullanım: scan <x:y> (örn: scan 2303:4712)")
                return
            
            try:
                coords = parts[1].split(":")
                x = int(coords[0])
                y = int(coords[1])
                self.scan_coordinates(x, y)
                self.add_command_output(f"Koordinat taranıyor: ({x},{y})")
            except (ValueError, IndexError):
                self.last_command_output = "HATA: Geçersiz koordinat formatı! (örn: scan 2303:4712)"
                self.add_command_output("HATA: Geçersiz koordinat formatı! (örn: scan 2303:4712)")
        
        elif cmd == "tp" or cmd == "teleportation":
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                self.add_command_output("HATA: Önce görev başlatılmalı!")
                return
            
            if len(parts) < 2:
                self.last_command_output = "HATA: Kullanım: tp <x:y> (örn: tp 2303:4716)"
                self.add_command_output("HATA: Kullanım: tp <x:y> (örn: tp 2303:4716)")
                return
            
            try:
                coords = parts[1].split(":")
                x = int(coords[0])
                y = int(coords[1])
                self.teleport_ship(x, y)
            except (ValueError, IndexError):
                self.last_command_output = "HATA: Geçersiz koordinat formatı! (örn: tp 2303:4716)"
                self.add_command_output("HATA: Geçersiz koordinat formatı! (örn: tp 2303:4716)")
        
        elif cmd in ["list", "ls"]:
            self.list_universes()
            self.add_command_output("Evren listesi gösteriliyor...")
        
        elif cmd == "test":
            self.last_command_output = "Test komutu çalışıyor!"
            self.add_matrix_line("Test komutu başarılı!", Colors.GREEN)
            self.add_command_output("Test komutu başarılı!")
        
        elif cmd in ["speed", "s"]:
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                self.add_command_output("HATA: Önce görev başlatılmalı!")
                return
            
            # Hız değiştirme kontrolü
            if len(parts) >= 2:
                try:
                    points_per_minute = int(parts[1])
                    if 10 <= points_per_minute <= 200:
                        old_speed = self.ship.speed
                        old_points_per_minute = 10 / old_speed
                        
                        # Yeni hızı hesapla (1 dakikada kaç nokta)
                        self.ship.speed = 10 / points_per_minute  # speed = 10 / points_per_minute
                        self.calculate_speed_info()
                        
                        # Enerji tüketimini güncelle (oransal)
                        # Temel enerji: 14400 (10 nokta/dk için)
                        # Yeni enerji: 14400 * (points_per_minute / 10)
                        self.ship.max_energy = int(14400 * (points_per_minute / 10))
                        self.ship.energy = self.ship.max_energy
                        
                        self.last_command_output = f"Hız değiştirildi: {old_points_per_minute:.1f} → {points_per_minute} nokta/dk"
                        self.add_command_output(f"Hız değiştirildi: {old_points_per_minute:.1f} → {points_per_minute} nokta/dk")
                        self.add_command_output(f"Enerji kapasitesi: {self.ship.max_energy}")
                        self.add_command_output(f"1 nokta: {60/points_per_minute:.1f} saniye")
                        return
                    else:
                        self.last_command_output = "HATA: Hız 10-200 arasında olmalı!"
                        self.add_command_output("HATA: Hız 10-200 arasında olmalı!")
                        return
                except ValueError:
                    self.last_command_output = "HATA: Geçersiz hız değeri!"
                    self.add_command_output("HATA: Geçersiz hız değeri!")
                    return
            
            # Hız analizi (parametre yoksa)
            points_per_minute = 10 / self.ship.speed
            seconds_per_point = 60 / points_per_minute
            points_per_hour = points_per_minute * 60
            
            speed_info = f"HIZ ANALİZİ:"
            self.add_command_output(speed_info)
            self.add_command_output(f"1 dakikada: {points_per_minute:.1f} nokta")
            self.add_command_output(f"1 nokta: {seconds_per_point:.1f} saniye")
            self.add_command_output(f"1 saatte: {points_per_hour:.1f} nokta")
            
            self.last_command_output = f"Hız analizi: 1dk={points_per_minute:.1f}pt, 1pt={seconds_per_point:.1f}sn, 1sa={points_per_hour:.1f}pt"
        
        elif cmd in ["refresh", "r"]:
            if not self.ship:
                self.last_command_output = "HATA: Önce görev başlatılmalı!"
                self.add_command_output("HATA: Önce görev başlatılmalı!")
                return
            
            # Güncelleme süresi bilgisi
            update_interval = self.seconds_per_point
            self.add_command_output(f"GÜNCELLEME SÜRESİ: {update_interval:.1f} saniye")
            self.add_command_output(f"Matris her {update_interval:.1f} saniyede bir güncellenir")
            
            self.last_command_output = f"Güncelleme süresi: {update_interval:.1f} saniye"
        
        elif cmd == "help":
            self.show_help()
            self.add_command_output("Yardım menüsü gösteriliyor...")
        
        elif cmd == "quit" or cmd == "exit":
            self.running = False
            self.last_command_output = "Oyundan çıkılıyor..."
            self.add_command_output("Oyundan çıkılıyor...")
        
        else:
            self.last_command_output = f"Bilinmeyen komut: {cmd}"
            self.add_command_output(f"Bilinmeyen komut: {cmd}")
    
    def show_help(self):
        """Yardım ekranını göster"""
        help_text = """
=== UZAY OYUNU KOMUTLARI ===

BAŞLATMA:
  go --name <isim> [--size <boyut>] [--velocity <hız>]  - Evren oluştur/yükle ve görev başlat
  Örnek: go --name myspaces --size 21000 --velocity 2
  Örnek: go -n altay -s 14400 -v 1
  Not: Mevcut evren varsa yükler, yoksa yeni oluşturur

GEMİ KONTROLÜ:
  startEngine                             - Motoru başlat
  stopEngine                              - Motoru durdur
  rotateRight/Left/Up/Down               - Yön değiştir
  turnBack                                - Geri dön

TELEPORTASYON:
  tp <x:y>                                - Işınlan (örn: tp 2303:4716)
  teleportation <x:y>                     - Işınlan (alternatif)

TARAMA:
  scan <x:y>                              - Koordinat tara (örn: scan 2303:4712)

EVREN YÖNETİMİ:
  list veya ls                            - Mevcut evrenleri listele

DİĞER:
  status                                  - Detaylı durum
  time                                    - Mevcut zaman
  help                                    - Bu yardım
  quit/exit                               - Çıkış

PARAMETRELER:
  --name, -n     : Evren adı (zorunlu)
  --size, -s     : Evren boyutu (varsayılan: 14400)
  --velocity, -v : Gemi hızı (varsayılan: 1)

NOT: Teleportasyon enerjinin %5'ini tüketir!
        """
        self.last_command_output = help_text.strip()
    
    def load_universe(self, file_path: str):
        """Mevcut evreni yükle"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.universe_size = data['size']
            self.celestial_objects = []
            
            for obj_data in data['objects']:
                obj = CelestialObject(
                    x=obj_data['x'],
                    y=obj_data['y'],
                    obj_type=CelestialType(obj_data['type']),
                    name=obj_data['name']
                )
                self.celestial_objects.append(obj)
            
            self.universe_created = True
            self.add_matrix_line(f"Evren yüklendi: {file_path} ({self.universe_size}x{self.universe_size})")
            self.add_matrix_line(f"Toplam {len(self.celestial_objects)} gök cismi yüklendi")
            # last_command_output zaten process_command'da set ediliyor
            
        except Exception as e:
            self.last_command_output = f"HATA: Evren yüklenemedi: {str(e)}"
    
    def list_universes(self):
        """Universes klasöründeki evrenleri listele"""
        try:
            # universes klasörünü oluştur
            os.makedirs("universes", exist_ok=True)
            
            # JSON dosyalarını bul
            universe_files = []
            for file in os.listdir("universes"):
                if file.endswith('.json'):
                    universe_files.append(file)
            
            if not universe_files:
                self.last_command_output = "Universes klasöründe evren bulunamadı"
                self.add_command_output("Universes klasöründe evren bulunamadı")
                return
            
            # Dosyaları listele
            universe_list = "MEVCUT EVRENLER:\n"
            for i, file in enumerate(sorted(universe_files), 1):
                name = file.replace('.json', '')
                universe_list += f"  {i}. {name}\n"
                self.add_command_output(f"{i}. {name}")
            
            self.last_command_output = universe_list.strip()
            
        except Exception as e:
            self.last_command_output = f"HATA: Evren listesi alınamadı: {str(e)}"
            self.add_command_output(f"HATA: Evren listesi alınamadı: {str(e)}")
    
    def create_universe(self, name: str):
        """Evren oluştur"""
        self.celestial_objects = []
        
        # Toplam gök cismi sayısı = evren boyutunun %0.0001'i (çok daha az)
        total_objects = max(100, int(self.universe_size * self.universe_size * 0.0001))
        
        # Gök cismi türlerini dağıt
        sun_count = max(1, int(total_objects * 0.1))  # %10 güneş
        black_hole_count = max(1, int(total_objects * 0.05))  # %5 karadelik
        asteroid_count = max(1, int(total_objects * 0.3))  # %30 asteroid
        planet_count = max(1, int(total_objects * 0.4))  # %40 gezegen
        comet_count = max(1, int(total_objects * 0.15))  # %15 kuyruklu yıldız
        
        # Güneşler
        for i in range(sun_count):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            self.celestial_objects.append(CelestialObject(x, y, CelestialType.SUN, f"Güneş-{i+1}"))
        
        # Karadelikler
        for i in range(black_hole_count):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            self.celestial_objects.append(CelestialObject(x, y, CelestialType.BLACK_HOLE, f"Karadelik-{i+1}"))
        
        # Asteroid kuşakları
        for i in range(asteroid_count):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            self.celestial_objects.append(CelestialObject(x, y, CelestialType.ASTEROID_BELT, f"Asteroid-{i+1}"))
        
        # Gezegenler
        for i in range(planet_count):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            self.celestial_objects.append(CelestialObject(x, y, CelestialType.PLANET, f"Gezegen-{i+1}"))
        
        # Kuyruklu yıldızlar
        for i in range(comet_count):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            self.celestial_objects.append(CelestialObject(x, y, CelestialType.COMET, f"Kuyruklu-{i+1}"))
        
        # JSON dosyasına kaydet
        # universes klasörünü oluştur
        os.makedirs("universes", exist_ok=True)
        
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
        
        file_path = f"universes/{name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
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
        self.add_matrix_line("Başlatma: go --name <isim> [--size <boyut>] [--velocity <hız>]")
        self.add_matrix_line("Örnek: go --name myspaces --size 21000 --velocity 2")
        self.add_matrix_line("Hareket: startEngine, stopEngine, rotateRight/Left/Up/Down, turnBack")
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
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        # Enter tuşu - komut işle
                        if self.current_command.strip():
                            self.process_command(self.current_command.strip())
                        self.current_command = ""
                    elif event.key == pygame.K_BACKSPACE:
                        # Backspace - karakter sil
                        if self.current_command:
                            self.current_command = self.current_command[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        # Escape - komutu temizle
                        self.current_command = ""
                    elif event.unicode and event.unicode.isprintable():
                        # Sadece yazdırılabilir karakterleri ekle
                        self.current_command += event.unicode
            
            # Gemi pozisyonunu güncelle
            self.update_ship_position()
            
            # Ekranı temizle
            self.clear_screen()
            
            # UI elemanlarını çiz
            self.print_header()
            self.print_status_panel()
            self.print_command_output_panel()
            self.print_matrix_display()
            self.print_command_line()
            
            # Mevcut komutu göster (prompt'un yanında)
            if self.current_command:
                y_pos = self.screen_height - self.command_height + 10
                # Prompt genişliğini hesapla
                if self.ship and self.mission_started:
                    universe_name = getattr(self, 'current_universe_name', 'unknown')
                    direction_text = self.ship.direction.value.upper()
                    status_text = "HAREKET HALİNDE" if self.ship.is_moving else "DURAK"
                    prompt_text = f"{universe_name}@{direction_text}-{status_text}:$ "
                else:
                    prompt_text = "uzay@başlatma:$ "
                
                prompt_surface = self.font_medium.render(prompt_text, True, Colors.GREEN)
                command_x = 10 + prompt_surface.get_width()
                
                command_surface = self.font_medium.render(self.current_command, True, Colors.WHITE)
                self.screen.blit(command_surface, (command_x, y_pos))
            
            # Ekranı güncelle
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SpaceGamePygame()
    game.run()
