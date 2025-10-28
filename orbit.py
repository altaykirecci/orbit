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
    TURQUOISE = (64, 224, 208)  # Turkuaz rengi

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

# Chunk Manager sınıfı
class ChunkManager:
    def __init__(self, universe_size, chunk_size=100):
        self.universe_size = universe_size
        self.chunk_size = chunk_size
        self.chunks = {}  # Yüklenen chunk'lar
        self.loaded_chunks = set()
        self.max_loaded_chunks = 25  # Maksimum 5x5 alan (500x500)
    
    def get_chunk_coords(self, x, y):
        """Koordinatları chunk koordinatlarına çevir"""
        return (x // self.chunk_size, y // self.chunk_size)
    
    def get_chunk_file_path(self, chunk_x, chunk_y, universe_name):
        """Chunk dosya yolunu oluştur"""
        return f"universes/{universe_name}/chunk_{chunk_x}_{chunk_y}.json"
    
    def load_chunk(self, chunk_x, chunk_y, universe_name):
        """Chunk'ı yükle"""
        if (chunk_x, chunk_y) in self.loaded_chunks:
            return self.chunks.get((chunk_x, chunk_y), [])
        
        chunk_file = self.get_chunk_file_path(chunk_x, chunk_y, universe_name)
        if os.path.exists(chunk_file):
            try:
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunk_data = json.load(f)
                self.chunks[(chunk_x, chunk_y)] = chunk_data
                self.loaded_chunks.add((chunk_x, chunk_y))
                return chunk_data
            except Exception as e:
                print(f"Chunk yükleme hatası: {e}")
                return []
        return []
    
    def unload_distant_chunks(self, ship_x, ship_y, max_distance=2):
        """Uzak chunk'ları bellekten çıkar"""
        ship_chunk = self.get_chunk_coords(ship_x, ship_y)
        chunks_to_remove = []
        
        for chunk_coord in self.loaded_chunks:
            distance = max(abs(chunk_coord[0] - ship_chunk[0]), 
                          abs(chunk_coord[1] - ship_chunk[1]))
            if distance > max_distance:
                chunks_to_remove.append(chunk_coord)
        
        for chunk_coord in chunks_to_remove:
            if chunk_coord in self.chunks:
                del self.chunks[chunk_coord]
            self.loaded_chunks.remove(chunk_coord)
    
    def get_objects_in_area(self, min_x, min_y, max_x, max_y, universe_name):
        """Belirtilen alandaki objeleri getir"""
        objects = []
        
        # Bu alanı kapsayan chunk'ları hesapla
        min_chunk_x = min_x // self.chunk_size
        max_chunk_x = max_x // self.chunk_size
        min_chunk_y = min_y // self.chunk_size
        max_chunk_y = max_y // self.chunk_size
        
        # Her chunk'ı yükle
        for chunk_x in range(min_chunk_x, max_chunk_x + 1):
            for chunk_y in range(min_chunk_y, max_chunk_y + 1):
                chunk_objects = self.load_chunk(chunk_x, chunk_y, universe_name)
                
                # Chunk içindeki objeleri filtrele
                for obj in chunk_objects:
                    if (min_x <= obj['x'] <= max_x and 
                        min_y <= obj['y'] <= max_y):
                        objects.append(obj)
        
        return objects

# Ana oyun sınıfı
class SpaceGamePygame:
    def __init__(self):
        # Pygame ayarları - Yeni tasarım için daha geniş ekran
        self.screen_width = 1400
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Orbit - Space Game")
        
        # Font ayarları - Orbitron + Liberation Mono
        try:
            # UI için Orbitron
            self.font_small = pygame.font.Font("fonts/orbitron-regular.ttf", 14)
            self.font_medium = pygame.font.Font("fonts/orbitron-regular.ttf", 16)
            self.font_large = pygame.font.Font("fonts/orbitron-regular.ttf", 20)
            self.font_xlarge = pygame.font.Font("fonts/orbitron-regular.ttf", 24)
            # Konsol için Liberation Mono
            self.font_mono = pygame.font.Font("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 12)
            print("Orbitron + Liberation Mono font'ları yüklendi!")
        except Exception as e:
            print(f"Font yükleme hatası: {e}")
            # Sistem varsayılan font'u kullan
            self.font_small = pygame.font.Font(None, 14)
            self.font_medium = pygame.font.Font(None, 16)
            self.font_large = pygame.font.Font(None, 20)
            self.font_xlarge = pygame.font.Font(None, 24)
            self.font_mono = pygame.font.Font(None, 12)
            print("Sistem font'u kullanılıyor!")
        
        # Oyun durumu
        self.running = True
        self.universe_size = 500
        self.celestial_objects: List[CelestialObject] = []
        self.ship: Optional[Ship] = None
        
        # Grid durumu
        self.grid_enabled = False  # Varsayılan olarak kapalı
        
        # Radar alarm sistemi
        self.radar_alarm = False  # Gök cismi alarmı
        self.alarm_blink_timer = 0  # Yanıp sönme timer'ı
        
        # Chunk Manager
        self.chunk_manager = ChunkManager(self.universe_size, 100)
        self.current_universe_name = "uzay"
        self.mission_started = False
        self.last_position_update = datetime.now()
        
        # UI alanları - Yeni 3 bölümlü düzen
        self.left_width = int(self.screen_width * 0.30)      # Sol %30 - Linux konsolu
        remaining_width = self.screen_width - self.left_width  # Kalan alan
        self.center_width = int(remaining_width * 0.60)       # Orta - Kalan alanın %60'ı
        self.right_width = remaining_width - self.center_width # Sağ - Kalan alan
        
        # Sol bölüm - Sadece konsol (tam yükseklik)
        self.console_height = self.screen_height  # Tam yükseklik
        
        # Orta bölüm (grid) - 20x20 sabit
        self.matrix_width = self.center_width
        self.matrix_height = self.screen_height - 50
        
        # Sağ bölüm - 3'e bölünmüş
        self.dashboard_height = int(self.screen_height * 0.25)  # Dashboard %25
        self.radar_height = int(self.screen_height * 0.15)      # Radar %15
        self.probe_height = self.screen_height - self.dashboard_height - self.radar_height - 50  # Sonda kalan
        
        # Komut satırı yüksekliği
        self.command_height = 50
        
        # Konsol için
        self.console_lines = []
        self.max_console_lines = 50  # Daha fazla satır
        self.console_scroll = 0
        
        # Matrix görüntü için
        self.matrix_lines = []
        self.max_matrix_lines = 20
        self.last_matrix_update = datetime.now()
        
        # Matrix başlangıç koordinatları (gemi yokken)
        self.matrix_start_x = 0
        self.matrix_start_y = 0
        
        # Komut çıktısı için
        self.command_output_lines = []
        self.max_command_output_lines = 15
        
        # Görsel matris için - Evren boyutuna göre dinamik
        self.matrix_size = self.calculate_matrix_size()  # Evren boyutuna göre hesapla
        
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
        
        # Yön göstergesi için
        self.direction_indicator_x = 0
        self.direction_indicator_y = 0
        self.direction_initialized = False
        self.direction_line_passed = False  # Yön hattı geçildi mi?
        self.engine_on = False  # Motor açık mı?
        self.matrix_render_threshold = self.calculate_render_threshold()  # Evren boyutuna göre hesapla
        
        # Clock
        self.clock = pygame.time.Clock()
        
    def clear_screen(self):
        """Ekranı temizle - Yeni tasarım için"""
        self.screen.fill(Colors.BLACK)
        
        # Sol panel arka planı (siyah - Linux konsolu)
        left_rect = pygame.Rect(0, 0, self.left_width, self.screen_height)
        pygame.draw.rect(self.screen, Colors.BLACK, left_rect)
        
        # Orta panel arka planı (siyah - Grid)
        center_rect = pygame.Rect(self.left_width, 0, self.center_width, self.screen_height)
        pygame.draw.rect(self.screen, Colors.BLACK, center_rect)
        
        # Sağ panel arka planı (siyah - Dashboard/Radar/Sonda)
        right_rect = pygame.Rect(self.left_width + self.center_width, 0, self.right_width, self.screen_height)
        pygame.draw.rect(self.screen, Colors.BLACK, right_rect)
    
    def print_header(self):
        """Başlık çiz - kaldırıldı"""
        pass
    
    
    
    def add_command_output(self, text: str, color=Colors.WHITE):
        """Komut çıktısına satır ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.command_output_lines.append(f"[{timestamp}] {text}")
        if len(self.command_output_lines) > self.max_command_output_lines:
            self.command_output_lines.pop(0)
    
    def add_console_line(self, text: str, color=Colors.GREEN):
        """Linux konsoluna yeni satır ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_lines.append((f"[{timestamp}] {text}", color))
        if len(self.console_lines) > self.max_console_lines * 2:
            self.console_lines = self.console_lines[-self.max_console_lines:]
    
    def print_console(self):
        """Konsol görünümünü çiz - Text wrap ile"""
        # Konsol arka planı (siyah) - Tam yükseklik
        console_rect = pygame.Rect(0, 0, self.left_width, self.console_height)
        pygame.draw.rect(self.screen, Colors.BLACK, console_rect)
        pygame.draw.rect(self.screen, Colors.GREEN, console_rect, 2)
        
        # Konsol satırlarını çiz (scroll ile) - Text wrap ile
        y_start = 10
        visible_lines = self.console_lines[-self.max_console_lines:]
        
        for i, (line, color) in enumerate(visible_lines):
            if y_start + i * 16 < self.console_height - 60:  # Komut satırı için yer bırak
                # Text wrap için satırı böl
                max_width = self.left_width - 20  # Sağ taraftan 20px boşluk
                wrapped_lines = self.wrap_text(line, max_width)
                
                # Her wrapped satırı çiz
                for j, wrapped_line in enumerate(wrapped_lines):
                    if y_start + (i + j) * 16 < self.console_height - 60:
                        text_surface = self.font_mono.render(wrapped_line, True, color)
                        self.screen.blit(text_surface, (10, y_start + (i + j) * 16))
    
    def wrap_text(self, text, max_width):
        """Text'i belirtilen genişliğe göre wrap yap"""
        if not text:
            return [""]
        
        # Font ile text genişliğini hesapla
        test_surface = self.font_mono.render(text, True, Colors.WHITE)
        if test_surface.get_width() <= max_width:
            return [text]
        
        # Text'i wrap yap
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            test_surface = self.font_mono.render(test_line, True, Colors.WHITE)
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def print_matrix_display(self):
        """Orta bölümde matrix görüntü"""
        if not self.ship:
            return
        
        # Orta bölüm arka planı (siyah) - Matris alanı konsol alanının bittiği yerden başlar
        # Matrix'i orta panel içinde 15 pixel margin ile çiz
        matrix_margin = 15
        matrix_rect = pygame.Rect(
            self.left_width + matrix_margin,  # Sol margin
            matrix_margin,  # Üst margin
            self.matrix_width - (2 * matrix_margin),  # Genişlik - iki yan margin
            self.matrix_height - (2 * matrix_margin)  # Yükseklik - üst ve alt margin
        )
        
        # Cell size'ı matrix_rect boyutlarına göre hesapla
        self.cell_size = min(matrix_rect.width // self.matrix_size, matrix_rect.height // self.matrix_size)
        
        pygame.draw.rect(self.screen, Colors.BLACK, matrix_rect)
        pygame.draw.rect(self.screen, Colors.GREEN, matrix_rect, 2)  # Matris alanı etrafında yeşil çizgi
        
        # Grid çizgileri - grid_enabled durumuna göre
        if self.grid_enabled:
            self.draw_grid(matrix_rect)
        
        # 40x40 görsel matris çiz
        self.draw_visual_matrix(matrix_rect)
    
    def print_dashboard_panel(self):
        """Sağ üst - Dashboard paneli"""
        if not self.mission_started or not self.ship:
            return
        
        # Dashboard arka planı (siyah) - Matrix alanının bittiği yerden başlar
        dashboard_x = self.left_width + self.center_width
        dashboard_rect = pygame.Rect(dashboard_x, 0, self.right_width, self.dashboard_height)
        pygame.draw.rect(self.screen, Colors.BLACK, dashboard_rect)
        
        y_start = 10
        x_start = dashboard_x + 10
        
        # Zaman ve Dashboard başlığı
        mission_time = self.get_mission_time()
        time_surface = self.font_xlarge.render(mission_time, True, Colors.WHITE)
        self.screen.blit(time_surface, (x_start, y_start))
        
        dashboard_title = self.font_large.render("DashBoard", True, Colors.WHITE)
        self.screen.blit(dashboard_title, (x_start, y_start + 30))
        
        # Koordinatlar - Hareket durumuna göre renk
        x_color, y_color = self.get_coordinate_colors()
        
        # X koordinatı
        x_text = f"X: {self.ship.x}"
        x_surface = self.font_large.render(x_text, True, x_color)
        self.screen.blit(x_surface, (x_start, y_start + 60))
        
        # Y koordinatı
        y_text = f"Y: {self.ship.y}"
        y_surface = self.font_large.render(y_text, True, y_color)
        self.screen.blit(y_surface, (x_start, y_start + 85))
        
        # Yön bilgisi kaldırıldı - koordinat renkleri yönü gösteriyor
        
        # Hız bilgisi (sarı)
        points_per_minute = 10 / self.ship.speed
        speed_text = f"{points_per_minute:.0f} Nokta/dk"
        speed_surface = self.font_medium.render(speed_text, True, Colors.YELLOW)
        self.screen.blit(speed_surface, (x_start, y_start + 110))
        
        # Enerji bilgisi (sarı)
        energy_text = f"{self.ship.energy} Nokta"
        energy_surface = self.font_medium.render(energy_text, True, Colors.YELLOW)
        self.screen.blit(energy_surface, (x_start, y_start + 140))
        
        energy_percent = (self.ship.energy / self.ship.max_energy) * 100
        energy_percent_text = f"(%{energy_percent:.1f})"
        energy_percent_surface = self.font_medium.render(energy_percent_text, True, Colors.YELLOW)
        self.screen.blit(energy_percent_surface, (x_start, y_start + 160))
    
    def print_radar_panel(self):
        """Sağ orta - Radar paneli"""
        if not self.mission_started or not self.ship:
            return
        
        # Radar arka planı (siyah) - Matrix alanının bittiği yerden başlar
        radar_x = self.left_width + self.center_width
        radar_y = self.dashboard_height
        radar_rect = pygame.Rect(radar_x, radar_y, self.right_width, self.radar_height)
        pygame.draw.rect(self.screen, Colors.BLACK, radar_rect)
        
        y_start = radar_y + 10
        x_start = radar_x + 10
        
        # Radar başlığı
        radar_title = self.font_large.render("Radar", True, Colors.WHITE)
        self.screen.blit(radar_title, (x_start, y_start))
        
        # Radar menzili
        radar_range = self.font_medium.render("20 Nokta", True, Colors.WHITE)
        self.screen.blit(radar_range, (x_start, y_start + 30))
        
        # Radar alarm sistemi - Gök cismi varsa yanıp sönen alarm
        if self.radar_alarm:
            # Yanıp sönme efekti için timer
            self.alarm_blink_timer += 1
            if self.alarm_blink_timer > 30:  # 30 frame'de bir yanıp söner
                self.alarm_blink_timer = 0
            
            # Yanıp sönme kontrolü
            if self.alarm_blink_timer < 15:  # İlk 15 frame görünür
                alarm_text = "[ALARM] GÖK CİSİMLERİ"
                radar_alert = self.font_medium.render(alarm_text, True, Colors.RED)
                self.screen.blit(radar_alert, (x_start, y_start + 60))
    
    def print_probe_panel(self):
        """Sağ alt - Sonda paneli"""
        if not self.mission_started or not self.ship:
            return
        
        # Sonda arka planı (siyah) - Matrix alanının bittiği yerden başlar
        probe_x = self.left_width + self.center_width
        probe_y = self.dashboard_height + self.radar_height
        probe_rect = pygame.Rect(probe_x, probe_y, self.right_width, self.probe_height)
        pygame.draw.rect(self.screen, Colors.BLACK, probe_rect)
        
        y_start = probe_y + 10
        x_start = probe_x + 10
        
        # Sonda başlığı
        probe_title = self.font_large.render("Sonda Durumu", True, Colors.WHITE)
        self.screen.blit(probe_title, (x_start, y_start))
        
        # Sonda durumları (şimdilik sabit)
        probe_states = [
            "[1] Hazır",
            "[2] Hazır", 
            "[3] Keşif",
            "[4] Hazır"
        ]
        
        probe_colors = [Colors.WHITE, Colors.WHITE, Colors.GREEN, Colors.WHITE]
        
        for i, (state, color) in enumerate(zip(probe_states, probe_colors)):
            probe_surface = self.font_medium.render(state, True, color)
            self.screen.blit(probe_surface, (x_start, y_start + 30 + (i * 25)))
        
        # Sonda koordinat ve hız bilgileri
        probe_coords = f"{self.ship.x} {self.ship.y}"
        probe_coords_surface = self.font_small.render(probe_coords, True, Colors.WHITE)
        self.screen.blit(probe_coords_surface, (x_start, y_start + 140))
        
        points_per_minute = 10 / self.ship.speed
        probe_speed = f"{points_per_minute:.0f} Nokta/dk"
        probe_speed_surface = self.font_small.render(probe_speed, True, Colors.WHITE)
        self.screen.blit(probe_speed_surface, (x_start, y_start + 160))
        
        probe_energy = f"{self.ship.energy} Nokta"
        probe_energy_surface = self.font_small.render(probe_energy, True, Colors.WHITE)
        self.screen.blit(probe_energy_surface, (x_start, y_start + 180))
    
    def get_direction_text(self):
        """Yön bilgisini Türkçe metin olarak döndür"""
        if not self.ship:
            return "Bilinmiyor"
        
        direction_map = {
            Direction.UP: "Yukarı",
            Direction.DOWN: "Aşağı", 
            Direction.LEFT: "Sol",
            Direction.RIGHT: "Sağ"
        }
        return direction_map.get(self.ship.direction, "Bilinmiyor")
    
    def get_coordinate_colors(self):
        """Koordinat renklerini hareket durumuna göre hesapla"""
        if not self.ship or not self.engine_on:
            # Motor çalışmıyorsa her ikisi de kırmızı
            return Colors.RED, Colors.RED
        
        # Motor çalışıyorsa yön bazlı renk
        if self.ship.direction in [Direction.LEFT, Direction.RIGHT]:
            # X ekseninde hareket - X yeşil, Y turkuaz
            return Colors.GREEN, Colors.TURQUOISE
        elif self.ship.direction in [Direction.UP, Direction.DOWN]:
            # Y ekseninde hareket - X turkuaz, Y yeşil
            return Colors.TURQUOISE, Colors.GREEN
        else:
            # Bilinmeyen durum - her ikisi de kırmızı
            return Colors.RED, Colors.RED
    
    def calculate_matrix_size(self):
        """Evren boyutuna göre matrix boyutunu hesapla"""
        if self.universe_size < 1000:
            return 20  # 100-999 arası evrenler için 20x20
        elif self.universe_size < 10000:
            return 50  # 1000-9999 arası evrenler için 50x50
        else:
            return 100  # 10000+ evrenler için 100x100
    
    def calculate_render_threshold(self):
        """Evren boyutuna göre render threshold hesapla"""
        if self.universe_size < 1000:
            return 5  # 20x20 için 5 nokta
        elif self.universe_size < 10000:
            return 10  # 50x50 için 10 nokta
        else:
            return 20  # 100x100 için 20 nokta
    
    def calculate_direction_indicator(self):
        """Gemi'nin yönüne göre matrix'in son hücresini hesapla"""
        half_size = self.matrix_size // 2
        
        if self.ship.direction == Direction.UP:
            # Yukarı - Aynı X, en küçük Y (üst)
            self.direction_indicator_x = self.ship.x
            self.direction_indicator_y = self.matrix_start_y
        elif self.ship.direction == Direction.DOWN:
            # Aşağı - Aynı X, en büyük Y (alt)
            self.direction_indicator_x = self.ship.x
            self.direction_indicator_y = self.matrix_start_y + self.matrix_size - 1
        elif self.ship.direction == Direction.LEFT:
            # Sol - En küçük X (sol), aynı Y
            self.direction_indicator_x = self.matrix_start_x
            self.direction_indicator_y = self.ship.y
        elif self.ship.direction == Direction.RIGHT:
            # Sağ - En büyük X (sağ), aynı Y
            self.direction_indicator_x = self.matrix_start_x + self.matrix_size - 1
            self.direction_indicator_y = self.ship.y
    
    def get_direction_line_cells(self):
        """Gemi'nin yönündeki tüm hücreleri döndür"""
        cells = []
        
        if self.ship.direction in [Direction.UP, Direction.DOWN]:
            # Yukarı/Aşağı - En üstteki aynı Y'deki tüm X'ler (yatay çizgi)
            for x in range(self.matrix_start_x, self.matrix_start_x + self.matrix_size):
                cells.append((x, self.direction_indicator_y))
        elif self.ship.direction == Direction.RIGHT:
            # Sağa - Aynı X'deki tüm Y'ler (dikey çizgi - sağ kenar)
            for y in range(self.matrix_start_y, self.matrix_start_y + self.matrix_size):
                cells.append((self.direction_indicator_x, y))
        elif self.ship.direction == Direction.LEFT:
            # Sola - Aynı X'deki tüm Y'ler (dikey çizgi - sol kenar)
            for y in range(self.matrix_start_y, self.matrix_start_y + self.matrix_size):
                cells.append((self.direction_indicator_x, y))
        
        return cells
    
    def draw_grid(self, matrix_rect):
        """Grid çizgilerini çiz - grid_enabled durumuna göre"""
        if not self.grid_enabled:
            return
            
        # Dikey çizgiler
        for i in range(1, self.matrix_size):
            x_pos = matrix_rect.left + i * self.cell_size
            pygame.draw.line(self.screen, Colors.LIGHT_GRAY, 
                           (x_pos, matrix_rect.top), 
                           (x_pos, matrix_rect.bottom), 1)
        
        # Yatay çizgiler
        for j in range(1, self.matrix_size):
            y_pos = matrix_rect.top + j * self.cell_size
            pygame.draw.line(self.screen, Colors.LIGHT_GRAY, 
                           (matrix_rect.left, y_pos), 
                           (matrix_rect.right, y_pos), 1)
    
    def draw_visual_matrix(self, matrix_rect):
        """Chunk-based dinamik matris çiz"""
        if not self.ship:
            return
        
        # Matrix güncelleme - Her hareket ettiğinde
        distance_moved = ((self.ship.x - self.last_matrix_center_x) ** 2 + 
                         (self.ship.y - self.last_matrix_center_y) ** 2) ** 0.5
        
        # Her hareket ettiğinde matrix'i güncelle
        if distance_moved >= 1:  # 1 nokta hareket ettiyse
            self.last_matrix_center_x = self.ship.x
            self.last_matrix_center_y = self.ship.y
            
            # Matrix başlangıç koordinatlarını güncelle
            half_size = self.matrix_size // 2
            self.matrix_start_x = self.ship.x - half_size
            self.matrix_start_y = self.ship.y - half_size
            
            # Chunk'ları güncelle
            self.chunk_manager.unload_distant_chunks(self.ship.x, self.ship.y)
        
        # Yön göstergesini hesapla - Sadece engine on ise
        if self.engine_on:
            if not self.direction_initialized:
                # İlk kez hesapla
                self.calculate_direction_indicator()
                self.direction_initialized = True
                self.direction_line_passed = False
            elif (self.direction_indicator_x == self.ship.x and 
                  self.direction_indicator_y == self.ship.y):
                # Gemi yön göstergesi ile aynı koordinatta ise yeni yön hesapla
                self.calculate_direction_indicator()
                self.direction_line_passed = True  # Hattı geçti
        
        # Koordinat etiketlerini çiz
        self.draw_coordinate_labels(matrix_rect)
        
        # Matrix alanındaki tüm gök cisimlerini bir seferde yükle (verimli)
        matrix_objects = self.chunk_manager.get_objects_in_area(
            self.matrix_start_x, self.matrix_start_y,
            self.matrix_start_x + self.matrix_size - 1,
            self.matrix_start_y + self.matrix_size - 1,
            self.current_universe_name
        )
        
        # Gök cisimlerini koordinat bazlı dictionary'ye çevir (hızlı arama)
        objects_by_coord = {}
        for obj in matrix_objects:
            coord_key = (obj['x'], obj['y'])
            objects_by_coord[coord_key] = obj
        
        # Radar alarm kontrolü - Matrix'te gök cismi var mı?
        self.radar_alarm = len(matrix_objects) > 0
        
        # Her hücreyi kontrol et ve çiz
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                # Gerçek koordinatları hesapla (i=yatay=X, j=dikey=Y)
                real_x = self.matrix_start_x + i  # i = yatay = X ekseni
                real_y = self.matrix_start_y + j  # j = dikey = Y ekseni
                
                # Hücre rengini belirle
                color = Colors.BLACK
                border_color = Colors.DARK_GRAY
                bottom_line_color = Colors.DARK_GRAY
                
                # Gemi pozisyonu (merkez) - kırmızı dolu
                if real_x == self.ship.x and real_y == self.ship.y:
                    color = Colors.RED  # İçini tamamen kırmızı doldur
                    border_color = Colors.RED
                    bottom_line_color = Colors.RED
                # Yön hattındaki hücreler - sadece engine on ise
                elif self.engine_on and (real_x, real_y) in self.get_direction_line_cells():
                    if not self.direction_line_passed:
                        bottom_line_color = Colors.GREEN  # Henüz geçilmedi - yeşil
                    else:
                        bottom_line_color = Colors.TURQUOISE  # Geçildi - turkuaz
                # Bu hücrede gök cismi var mı kontrol et (hızlı dictionary arama)
                elif (real_x, real_y) in objects_by_coord:
                    color = Colors.YELLOW
                
                # Hücreyi çiz
                cell_rect = pygame.Rect(
                    matrix_rect.left + i * self.cell_size,
                    matrix_rect.top + j * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, color, cell_rect)
                
                # Hücre sınırları kaldırıldı - sadece siyah ekran
                
                # Yön hattı çizgisi - Yön bazlı
                if bottom_line_color != Colors.DARK_GRAY:
                    if self.ship.direction in [Direction.UP, Direction.DOWN]:
                        # Yukarı/Aşağı - Yatay çizgi (alt kenar)
                        pygame.draw.line(self.screen, bottom_line_color, 
                                       (cell_rect.left, cell_rect.bottom-1), 
                                       (cell_rect.right, cell_rect.bottom-1), 2)
                    elif self.ship.direction == Direction.RIGHT:
                        # Sağa - Dikey çizgi (sağ kenar)
                        pygame.draw.line(self.screen, bottom_line_color, 
                                       (cell_rect.right-1, cell_rect.top), 
                                       (cell_rect.right-1, cell_rect.bottom), 2)
                    elif self.ship.direction == Direction.LEFT:
                        # Sola - Dikey çizgi (sol kenar)
                        pygame.draw.line(self.screen, bottom_line_color, 
                                       (cell_rect.left, cell_rect.top), 
                                       (cell_rect.left, cell_rect.bottom), 2)
                
                # Yön göstergesi için + işareti çiz (sadece engine on ve son hücrede)
                if self.engine_on and real_x == self.direction_indicator_x and real_y == self.direction_indicator_y:
                    center_x = cell_rect.centerx
                    center_y = cell_rect.centery
                    cross_size = self.cell_size // 4
                    
                    # + işareti çiz (yeşil)
                    pygame.draw.line(self.screen, Colors.GREEN, 
                                   (center_x - cross_size, center_y), 
                                   (center_x + cross_size, center_y), 3)
                    pygame.draw.line(self.screen, Colors.GREEN, 
                                   (center_x, center_y - cross_size), 
                                   (center_x, center_y + cross_size), 3)
    
    def draw_coordinate_labels(self, matrix_rect):
        """Koordinat etiketlerini orta alana fit ederek çiz"""
        # X ekseni etiketleri (alt) - Orta alana fit
        for i in range(0, self.matrix_size, 5):  # Her 5 hücrede bir
            real_x = self.matrix_start_x + i
            label_text = str(real_x)
            label_surface = self.font_small.render(label_text, True, Colors.WHITE)
            
            # Matrix alanının içinde kalacak şekilde pozisyonla
            x_pos = matrix_rect.left + i * self.cell_size + (self.cell_size // 2)
            y_pos = matrix_rect.bottom - 10  # Matrix alanının içinde, alt kenardan 10 pixel yukarı
            
            # Matrix alanının sınırları içinde kal
            if x_pos + label_surface.get_width() <= matrix_rect.right:
                text_rect = label_surface.get_rect(center=(x_pos, y_pos))
                self.screen.blit(label_surface, text_rect)
        
        # Y ekseni etiketleri (sol) - Matris alanının solunda
        for j in range(0, self.matrix_size, 5):  # Her 5 hücrede bir
            real_y = self.matrix_start_y + j
            label_text = str(real_y)
            label_surface = self.font_small.render(label_text, True, Colors.WHITE)
            
            # Matrix alanının içinde, sol kenarda
            x_pos = matrix_rect.left + 10  # Matrix alanının içinde, sol kenardan 10 pixel içeride
            y_pos = matrix_rect.top + j * self.cell_size + (self.cell_size // 2)
            
            # Matrix alanının sınırları içinde kal
            if y_pos + label_surface.get_height() <= matrix_rect.bottom:
                text_rect = label_surface.get_rect(right=x_pos, centery=y_pos)
                self.screen.blit(label_surface, text_rect)
    
    def get_objects_in_range(self, x: int, y: int, range_distance: int) -> List[dict]:
        """Chunk-based: Belirli bir noktadan belirli mesafede olan cisimleri bul"""
        # Chunk-based arama
        min_x = int(x - range_distance)
        max_x = int(x + range_distance)
        min_y = int(y - range_distance)
        max_y = int(y + range_distance)
        
        view_objects = self.chunk_manager.get_objects_in_area(
            min_x, min_y, max_x, max_y, self.current_universe_name
        )
        
        # Mesafe kontrolü
        objects_in_range = []
        for obj in view_objects:
            distance = ((obj['x'] - x) ** 2 + (obj['y'] - y) ** 2) ** 0.5
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
            self.add_console_line(f"HATA: Koordinatlar evren sınırları dışında! (0-{self.universe_size-1})", Colors.RED)
            return
        
        # Enerji kontrolü
        energy_cost = int(self.ship.max_energy * 0.05)  # %5 enerji
        if self.ship.energy < energy_cost:
            self.add_console_line(f"HATA: Yetersiz enerji! Gerekli: {energy_cost}, Mevcut: {self.ship.energy}", Colors.RED)
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
        
        # Komut çıktısına ekle
        self.add_console_line(f"({x},{y}) koordinatına ışınlanıldı")
        self.add_console_line(f"Enerji tüketimi: {energy_cost} birim")
        
        # Matrix görüntüye bilgi ekle
        self.add_matrix_line(f"TELEPORTASYON: ({old_x}, {old_y}) → ({x}, {y})", Colors.MAGENTA)
        self.add_matrix_line(f"ENERJİ TÜKETİMİ: {energy_cost} birim (%5)", Colors.MAGENTA)
        self.add_matrix_line(f"MATRİS MERKEZİ: ({x}, {y})", Colors.CYAN)
        
        # Çarpışma kontrolü
        collisions = self.check_collision(x, y)
        if collisions:
            self.add_matrix_line("ALERT: Teleportasyon sonrası çarpışma!", Colors.RED)
            self.add_console_line("ALERT: Teleportasyon sonrası çarpışma!")
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
        """Alt komut satırını çiz - Sabit konum"""
        y_pos = self.screen_height - 35  # Sabit konum
        
        # Komut satırı arka planı (tüm genişlik)
        command_rect = pygame.Rect(0, self.screen_height - 50, self.screen_width, 50)
        pygame.draw.rect(self.screen, Colors.DARK_GRAY, command_rect)
        
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
            prompt_text = "orbit@başlatma:$ "
        
        # Prompt'u çiz
        prompt_surface = self.font_medium.render(prompt_text, True, Colors.GREEN)
        self.screen.blit(prompt_surface, (10, y_pos))
        
        # Yanıp sönen cursor
        current_time = datetime.now()
        if int(current_time.microsecond / 500000) % 2:  # Her 0.5 saniyede bir yanıp söner
            cursor_x = 10 + prompt_surface.get_width()
            cursor_surface = self.font_medium.render("_", True, Colors.WHITE)
            self.screen.blit(cursor_surface, (cursor_x, y_pos))
        
    
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
        
        if cmd == "go":
            # Parametreleri parse et
            name = None
            size = 500  # Default boyut
            velocity = 1  # Default hız
            force_create = False  # Zorla oluştur flag'i
            preset = "normal"  # Default preset
            
            i = 1
            while i < len(parts):
                part = parts[i]
                
                if part in ["--name", "-n"]:
                    if i + 1 < len(parts):
                        name = parts[i + 1]
                        i += 2
                    else:
                        self.add_console_line("HATA: --name (-n) parametresi için değer gerekli!", Colors.RED)
                        return
                elif part in ["--size", "-s"]:
                    if i + 1 < len(parts):
                        try:
                            size = int(parts[i + 1])
                            if size < 100 or size > 1000:
                                self.add_console_line("HATA: Evren boyutu 100-1000 arasında olmalı!")
                                return
                            i += 2
                        except ValueError:
                            self.add_console_line("HATA: Geçersiz boyut değeri!")
                            return
                    else:
                        self.add_console_line("HATA: --size (-s) parametresi için değer gerekli!")
                        return
                elif part in ["--velocity", "-v"]:
                    if i + 1 < len(parts):
                        try:
                            velocity = int(parts[i + 1])
                            i += 2
                        except ValueError:
                            self.add_console_line("HATA: Geçersiz hız değeri!")
                            return
                    else:
                        self.add_console_line("HATA: --velocity (-v) parametresi için değer gerekli!")
                        return
                elif part in ["--create", "-c"]:
                    force_create = True
                    i += 1
                elif part in ["--preset", "-p"]:
                    if i + 1 < len(parts):
                        preset = parts[i + 1].lower()
                        i += 2
                    else:
                        self.add_console_line("HATA: --preset (-p) parametresi için değer gerekli!")
                        self.add_console_line("Kullanılabilir preset'ler: normal, sparse, dense, empty")
                        return
                else:
                    i += 1
            
            # Name parametresi zorunlu
            if name is None:
                self.add_console_line("HATA: --name (-n) parametresi zorunlu! Örnek: go --name myspaces")
                return
            
            # Mevcut evreni kontrol et
            universe_file = f"universes/{name}.json"
            self.current_universe_name = name  # Evren adını kaydet
            
            if os.path.exists(universe_file) and not force_create:
                # Mevcut evreni yükle
                self.load_universe(universe_file)
                self.start_mission(velocity)
                # Matrix boyutunu güncelle
                self.matrix_size = self.calculate_matrix_size()
                
                self.add_console_line(f"Evren yüklendi: {name}.json")
                self.add_console_line(f"Boyut: {self.universe_size}x{self.universe_size}")
                self.add_console_line(f"Matrix: {self.matrix_size}x{self.matrix_size}")
                self.add_console_line(f"Gök cisimleri: {len(self.celestial_objects)}")
            else:
                # Yeni evren oluştur
                self.universe_size = size
                self.create_universe(name, preset)
                self.start_mission(velocity)
                # Matrix boyutunu güncelle
                self.matrix_size = self.calculate_matrix_size()
                
                self.add_console_line(f"Yeni evren oluşturuldu: {name}.json")
                self.add_console_line(f"Boyut: {self.universe_size}x{self.universe_size}")
                self.add_console_line(f"Matrix: {self.matrix_size}x{self.matrix_size}")
                self.add_console_line(f"Gök cisimleri: {len(self.celestial_objects)}")
        
        elif cmd in ["engine", "e"]:
            if not self.ship:
                self.add_console_line("HATA: Önce görev başlatılmalı!")
                return
            
            if len(parts) < 2:
                self.add_console_line("HATA: Kullanım: engine on/off veya e on/off")
                return
            
            action = parts[1].lower()
            if action == "on":
                self.start_engine()
                self.add_console_line("Engine is ON")
            elif action == "off":
                self.stop_engine()
                self.add_console_line("Engine is OFF")
            else:
                self.add_console_line("HATA: Geçersiz parametre! 'on' veya 'off' kullanın")
        
        elif cmd in ["rotate", "r"]:
            if not self.ship:
                self.add_console_line("HATA: Önce görev başlatılmalı!")
                return
            
            if len(parts) < 2:
                self.add_console_line("HATA: Kullanım: rotate <yön> veya r <yön>")
                self.add_console_line("Yönler: right/r, left/l, up/u, down/d")
                return
            
            direction = parts[1].lower()
            
            if direction in ["right", "r"]:
                self.rotate_right()
                self.add_console_line("Sağa döndü!")
            elif direction in ["left", "l"]:
                self.rotate_left()
                self.add_console_line("Sola döndü!")
            elif direction in ["up", "u"]:
                self.rotate_up()
                self.add_console_line("Yukarı döndü!")
            elif direction in ["down", "d"]:
                self.rotate_down()
                self.add_console_line("Aşağı döndü!")
            else:
                self.add_console_line("HATA: Geçersiz yön! Kullanım: right/r, left/l, up/u, down/d")
        
        elif cmd == "turnback":
            if not self.ship:
                self.add_console_line("HATA: Önce görev başlatılmalı!")
                return
            
            self.turn_back()
            self.add_console_line("Geri döndü!")
        
        elif cmd == "scan":
            if not self.ship:
                self.add_console_line("HATA: Önce görev başlatılmalı!")
                return
            
            if len(parts) < 2:
                self.add_console_line("HATA: Kullanım: scan <x:y> (örn: scan 2303:4712)")
                return
            
            try:
                coords = parts[1].split(":")
                x = int(coords[0])
                y = int(coords[1])
                self.scan_coordinates(x, y)
                self.add_console_line(f"Koordinat taranıyor: ({x},{y})")
            except (ValueError, IndexError):
                self.add_console_line("HATA: Geçersiz koordinat formatı! (örn: scan 2303:4712)")
        
        elif cmd == "tp" or cmd == "teleportation":
            if not self.ship:
                self.add_console_line("HATA: Önce görev başlatılmalı!")
                return
            
            if len(parts) < 2:
                self.add_console_line("HATA: Kullanım: tp <x:y> (örn: tp 2303:4716)")
                return
            
            try:
                coords = parts[1].split(":")
                x = int(coords[0])
                y = int(coords[1])
                self.teleport_ship(x, y)
            except (ValueError, IndexError):
                self.add_console_line("HATA: Geçersiz koordinat formatı! (örn: tp 2303:4716)")
        
        elif cmd in ["list", "ls"]:
            self.list_universes()
            self.add_console_line("Evren listesi gösteriliyor...")
        
        elif cmd == "test":
            self.add_matrix_line("Test komutu başarılı!", Colors.GREEN)
            self.add_console_line("Test komutu başarılı!")
        
        elif cmd in ["speed", "s"]:
            if not self.ship:
                self.add_console_line("HATA: Önce görev başlatılmalı!")
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
                        
                        self.add_console_line(f"Hız değiştirildi: {old_points_per_minute:.1f} → {points_per_minute} nokta/dk")
                        self.add_console_line(f"Enerji kapasitesi: {self.ship.max_energy}")
                        self.add_console_line(f"1 nokta: {60/points_per_minute:.1f} saniye")
                        return
                    else:
                        self.add_console_line("HATA: Hız 10-200 arasında olmalı!")
                        return
                except ValueError:
                    self.add_console_line("HATA: Geçersiz hız değeri!")
                    return
            
            # Hız analizi (parametre yoksa)
            points_per_minute = 10 / self.ship.speed
            seconds_per_point = 60 / points_per_minute
            points_per_hour = points_per_minute * 60
            
            speed_info = f"HIZ ANALİZİ:"
            self.add_console_line(speed_info)
            self.add_console_line(f"1 dakikada: {points_per_minute:.1f} nokta")
            self.add_console_line(f"1 nokta: {seconds_per_point:.1f} saniye")
            self.add_console_line(f"1 saatte: {points_per_hour:.1f} nokta")
            
        
        elif cmd in ["refresh", "r"]:
            if not self.ship:
                self.add_console_line("HATA: Önce görev başlatılmalı!")
                return
            
            # Güncelleme süresi bilgisi
            update_interval = self.seconds_per_point
            self.add_console_line(f"GÜNCELLEME SÜRESİ: {update_interval:.1f} saniye")
            self.add_console_line(f"Matris her {update_interval:.1f} saniyede bir güncellenir")
            
        
        elif cmd in ["clear", "cls"]:
            self.console_lines.clear()
            self.add_console_line("Konsol temizlendi")
        
        elif cmd == "grid":
            if len(parts) > 1:
                sub_cmd = parts[1].lower()
                if sub_cmd == "on":
                    self.grid_enabled = True
                    self.add_console_line("Grid çizgileri açıldı")
                elif sub_cmd == "off":
                    self.grid_enabled = False
                    self.add_console_line("Grid çizgileri kapatıldı")
                else:
                    self.add_console_line("HATA: grid on veya grid off kullanın", Colors.RED)
            else:
                status = "açık" if self.grid_enabled else "kapalı"
                self.add_console_line(f"Grid durumu: {status}")
        
        elif cmd == "help":
            self.show_help()
            self.add_console_line("Yardım menüsü gösteriliyor...")
        
        elif cmd == "quit" or cmd == "exit":
            self.running = False
            self.add_console_line("Oyundan çıkılıyor...")
        
        else:
            self.add_console_line(f"Bilinmeyen komut: {cmd}")
    
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
  grid on/off                             - Grid çizgilerini aç/kapat
  clear/cls                               - Konsolu temizle
  help                                    - Bu yardım
  quit/exit                               - Çıkış

PARAMETRELER:
  --name, -n     : Evren adı (zorunlu)
  --size, -s     : Evren boyutu (varsayılan: 500, 100-1000 arası)
  --velocity, -v : Gemi hızı (varsayılan: 1)

NOT: Teleportasyon enerjinin %5'ini tüketir!
        """
        # Yardım metnini konsola yaz
        self.add_console_line("=== UZAY OYUNU KOMUTLARI ===", Colors.YELLOW)
        self.add_console_line("")
        self.add_console_line("BAŞLATMA:", Colors.CYAN)
        self.add_console_line("  go --name <isim> [--size <boyut>] [--velocity <hız>]")
        self.add_console_line("  Örnek: go --name myspaces --size 21000 --velocity 2")
        self.add_console_line("  Örnek: go -n altay -s 500 -v 1")
        self.add_console_line("")
        self.add_console_line("GEMİ KONTROLÜ:", Colors.CYAN)
        self.add_console_line("  startEngine, stopEngine")
        self.add_console_line("  rotate right/left/up/down")
        self.add_console_line("  turnBack")
        self.add_console_line("")
        self.add_console_line("HAREKET:", Colors.CYAN)
        self.add_console_line("  engine on/off, e on/off")
        self.add_console_line("  speed <1-5>, sp <1-5>")
        self.add_console_line("")
        self.add_console_line("BİLGİ:", Colors.CYAN)
        self.add_console_line("  checkUp/Down/Left/Right")
        self.add_console_line("  scan <x>:<y>, tp <x>:<y>")
        self.add_console_line("  status, time, help, quit/exit")
        self.add_console_line("")
        self.add_console_line("KONSOL:", Colors.CYAN)
        self.add_console_line("  clear, cls - Konsolu temizle")
    
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
            
        except Exception as e:
            self.add_console_line(f"HATA: Evren yüklenemedi: {str(e)}")
    
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
                self.add_console_line("Universes klasöründe evren bulunamadı")
                return
            
            # Dosyaları listele - Sadece konsola yaz
            self.add_console_line("MEVCUT EVRENLER:", Colors.YELLOW)
            for i, file in enumerate(sorted(universe_files), 1):
                name = file.replace('.json', '')
                self.add_console_line(f"{i}. {name}")
            
        except Exception as e:
            self.add_console_line(f"HATA: Evren listesi alınamadı: {str(e)}")
    
    def create_universe(self, name: str, preset: str = "normal"):
        """Evren oluştur - Chunk-based with presets"""
        self.celestial_objects = []
        
        # Chunk klasörünü oluştur
        universe_dir = f"universes/{name}"
        os.makedirs(universe_dir, exist_ok=True)
        
        # Metadata dosyası oluştur
        metadata = {
            "name": name,
            "size": self.universe_size,
            "chunk_size": 100,
            "created": datetime.now().isoformat()
        }
        
        with open(f"{universe_dir}/metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        # Preset'e göre gök cismi yoğunluğunu belirle
        density_multipliers = {
            "empty": 0.00001,    # Çok az (0.001%)
            "sparse": 0.0001,    # Az (0.01%)
            "normal": 0.001,     # Normal (0.1%)
            "dense": 0.01,       # Yoğun (1%)
            "ultra": 0.1         # Çok yoğun (10%)
        }
        
        density = density_multipliers.get(preset, 0.001)  # Default normal
        total_objects = max(10, int(self.universe_size * self.universe_size * density))
        
        self.add_console_line(f"Preset: {preset.upper()} (Yoğunluk: {density*100:.3f}%)")
        
        # Chunk'lara göre gök cisimlerini dağıt
        chunk_objects = {}  # chunk_coord -> [objects]
        
        for i in range(total_objects):
            x = random.randint(0, self.universe_size - 1)
            y = random.randint(0, self.universe_size - 1)
            
            # Chunk koordinatlarını hesapla
            chunk_coord = self.chunk_manager.get_chunk_coords(x, y)
            
            if chunk_coord not in chunk_objects:
                chunk_objects[chunk_coord] = []
            
                # Gök cismi türlerini dağıt
            obj_type = random.choices(
                [ObjectType.SUN, ObjectType.BLACK_HOLE, ObjectType.ASTEROID, 
                 ObjectType.PLANET, ObjectType.COMET],
                weights=[0.1, 0.05, 0.3, 0.4, 0.15]
            )[0]
            
            obj_name = f"{obj_type.value}_{i+1}"
            
            # Chunk'a ekle
            chunk_objects[chunk_coord].append({
                "x": x,
                "y": y,
                "type": obj_type.value,
                "name": obj_name
            })
        
        # Chunk dosyalarını oluştur
        for chunk_coord, objects in chunk_objects.items():
            chunk_file = self.chunk_manager.get_chunk_file_path(
                chunk_coord[0], chunk_coord[1], name
            )
            with open(chunk_file, 'w', encoding='utf-8') as f:
                json.dump(objects, f, indent=2)
        
        self.add_console_line(f"Chunk-based evren oluşturuldu: {name}")
        self.add_console_line(f"Toplam {total_objects} gök cismi, {len(chunk_objects)} chunk")
    
    def start_mission(self, max_speed: int = 1):
        """Görevi başlat"""
        if not self.celestial_objects:
            return
        
        # Rastgele pozisyon
        x = random.randint(0, self.universe_size - 1)
        y = random.randint(0, self.universe_size - 1)
        
        # Gemi oluştur
        self.ship = Ship(x, y, 14400)
        self.ship.speed = max_speed
        self.ship.is_moving = False
        self.ship.mission_start_time = datetime.now()
        self.mission_started = True
        
        # Matrix başlangıç koordinatlarını gemi pozisyonuna ayarla
        half_size = self.matrix_size // 2
        self.matrix_start_x = self.ship.x - half_size
        self.matrix_start_y = self.ship.y - half_size
        self.last_matrix_center_x = self.ship.x
        self.last_matrix_center_y = self.ship.y
        
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
            self.engine_on = True
            # Yön hattını hesapla
            self.calculate_direction_indicator()
            self.direction_initialized = True
            self.direction_line_passed = False
    
    def stop_engine(self):
        """Motoru durdur"""
        if self.ship:
            self.ship.is_moving = False
            self.engine_on = False
    
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
            
            # Yön hattını yeniden hesapla
            self.direction_initialized = False
    
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
            
            # Yön hattını yeniden hesapla
            self.direction_initialized = False
    
    def rotate_up(self):
        """Yukarı dön"""
        if self.ship:
            self.ship.direction = Direction.UP
            # Yön hattını yeniden hesapla
            self.direction_initialized = False
    
    def rotate_down(self):
        """Aşağı dön"""
        if self.ship:
            self.ship.direction = Direction.DOWN
            # Yön hattını yeniden hesapla
            self.direction_initialized = False
    
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
        # Başlangıç mesajları - Linux konsoluna
        self.add_console_line("Orbit - Space Game başlatıldı!")
        self.add_console_line("Başlatma: go --name <isim> [--size <boyut>] [--velocity <hız>]")
        self.add_console_line("Örnek: go --name myspaces --size 21000 --velocity 2")
        self.add_console_line("Hareket: engine on/off, rotate <direction>, speed <value>")
        self.add_console_line("Çıkış: quit veya exit")
        
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
            
            # UI elemanlarını çiz - Yeni tasarım
            self.print_console()            # Sol %25 - Konsol (wrap ile)
            self.print_matrix_display()     # Orta %50 - Grid
            self.print_dashboard_panel()    # Sağ üst - Dashboard
            self.print_radar_panel()        # Sağ orta - Radar
            self.print_probe_panel()        # Sağ alt - Sonda
            self.print_command_line()       # Alt - Komut satırı
            
            # Mevcut komutu göster (prompt'un yanında) - Sabit konum
            if self.current_command:
                y_pos = self.screen_height - 35  # Sabit konum
                # Prompt genişliğini hesapla
                if self.ship and self.mission_started:
                    universe_name = getattr(self, 'current_universe_name', 'unknown')
                    direction_text = self.ship.direction.value.upper()
                    status_text = "HAREKET HALİNDE" if self.ship.is_moving else "DURAK"
                    prompt_text = f"{universe_name}@{direction_text}-{status_text}:$ "
                else:
                    prompt_text = "orbit@başlatma:$ "
                
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
