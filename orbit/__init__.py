#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ORBIT - Uzay Keşif Simülasyonu
by Altay Kireççi

Python ve Pygame ile geliştirilmiş, gelişmiş uzay keşif simülasyon oyunu.
"""

__version__ = "1.0.0"
__author__ = "Altay Kireççi"
__email__ = "altay@example.com"

import pygame
import sys
import time
import random
import json
import os
from datetime import datetime
from typing import List, Optional, Tuple
import math

# Import modules
from .modules import (
    Colors, Direction, CelestialType, StarType, BlackHoleClass,
    PlanetType, ResourceType, ResourceRichness,
    CelestialObject, Star, BlackHole, Planet, AsteroidBelt,
    Ship, ChunkManager, UniverseConstants, LocaleManager
)

# Pygame başlat
pygame.init()

# Colors class imported from modules

# Enum classes imported from modules

# All classes imported from modules

# Main game class
class SpaceGamePygame:
    def __init__(self):
        # Initialize locale manager
        self.locale = LocaleManager("en")  # Default to English
        
        # Create necessary directories in user's home or current directory
        self.setup_directories()
        
        # Pygame settings - Wider screen for new design
        self.screen_width = 1400
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.locale.get("game_title"))
        
        # Font ayarları - Orbitron + Liberation Mono
        try:
            # Font dosyalarının yolunu bul
            font_path = self.get_font_path("orbitron-regular.ttf")
            liberation_path = self.get_font_path("LiberationMono-Regular.ttf")
            
            # UI için Orbitron
            self.font_small = pygame.font.Font(font_path, 8)
            self.font_medium = pygame.font.Font(font_path, 16)
            self.font_large = pygame.font.Font(font_path, 20)
            self.font_xlarge = pygame.font.Font(font_path, 24)
            
            # Konsol için Liberation Mono
            if liberation_path and os.path.exists(liberation_path):
                self.font_mono = pygame.font.Font(liberation_path, 14)
            else:
                # Sistem varsayılan monospace font'u kullan
                self.font_mono = pygame.font.Font(None, 14)
            
            print("Orbitron + Liberation Mono font'ları yüklendi!")
        except Exception as e:
            print(f"Font yükleme hatası: {e}")
            # Sistem varsayılan font'u kullan
            self.font_small = pygame.font.Font(None, 8)
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
        self.coord_blink_timer = 0  # Koordinat yanıp sönme timer'ı
    
    def setup_directories(self):
        """Gerekli klasörleri oluştur"""
        try:
            # Mevcut çalışma dizinini al
            current_dir = os.getcwd()
            
            # Sessions klasörü oluştur
            sessions_dir = os.path.join(current_dir, "sessions")
            if not os.path.exists(sessions_dir):
                os.makedirs(sessions_dir, exist_ok=True)
                print(f"📁 Sessions klasörü oluşturuldu: {sessions_dir}")
            
            # Universes klasörü oluştur
            universes_dir = os.path.join(current_dir, "universes")
            if not os.path.exists(universes_dir):
                os.makedirs(universes_dir, exist_ok=True)
                print(f"📁 Universes klasörü oluşturuldu: {universes_dir}")
            
            # Font klasörü kontrolü
            fonts_dir = os.path.join(os.path.dirname(__file__), "fonts")
            if not os.path.exists(fonts_dir):
                print(f"⚠️  Font klasörü bulunamadı: {fonts_dir}")
                print("   Font dosyaları yüklenemeyebilir.")
            
            # Loc klasörü kontrolü
            loc_dir = os.path.join(os.path.dirname(__file__), "loc")
            if not os.path.exists(loc_dir):
                print(f"⚠️  Loc klasörü bulunamadı: {loc_dir}")
                print("   Çok dilli destek çalışmayabilir.")
                
        except Exception as e:
            print(f"❌ Klasör oluşturma hatası: {e}")
    
    def get_font_path(self, font_filename):
        """Font dosyasının yolunu bul"""
        # Önce mevcut dizinde ara
        current_dir = os.getcwd()
        font_paths = [
            os.path.join(current_dir, "fonts", font_filename),
            os.path.join(current_dir, "orbit", "fonts", font_filename),
            os.path.join(os.path.dirname(__file__), "fonts", font_filename),
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                return path
        
        # Bulunamazsa None döndür
        return None
    
    def __init__(self):
        # Initialize locale manager
        self.locale = LocaleManager("en")  # Default to English
        
        # Create necessary directories in user's home or current directory
        self.setup_directories()
        
        # Pygame settings - Wider screen for new design
        self.screen_width = 1400
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.locale.get("game_title"))
        
        # Font ayarları - Orbitron + Liberation Mono
        try:
            # Font dosyalarının yolunu bul
            font_path = self.get_font_path("orbitron-regular.ttf")
            liberation_path = self.get_font_path("LiberationMono-Regular.ttf")
            
            # UI için Orbitron
            self.font_small = pygame.font.Font(font_path, 8)
            self.font_medium = pygame.font.Font(font_path, 16)
            self.font_large = pygame.font.Font(font_path, 20)
            self.font_xlarge = pygame.font.Font(font_path, 24)
            
            # Konsol için Liberation Mono
            if liberation_path and os.path.exists(liberation_path):
                self.font_mono = pygame.font.Font(liberation_path, 14)
            else:
                # Sistem varsayılan monospace font'u kullan
                self.font_mono = pygame.font.Font(None, 14)
            
            print("Orbitron + Liberation Mono font'ları yüklendi!")
        except Exception as e:
            print(f"Font yükleme hatası: {e}")
            # Sistem varsayılan font'u kullan
            self.font_small = pygame.font.Font(None, 8)
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
        self.coord_blink_timer = 0  # Koordinat yanıp sönme timer'ı
        
        # Chunk Manager
        self.chunk_manager = ChunkManager(self.universe_size, 100)
        self.current_universe_name = "uzay"
        self.mission_started = False
        self.last_position_update = datetime.now()
        self.matrix_objects = []  # Matrix'teki gök cisimleri
        
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
        
        # Sağ bölüm - Dashboard %40, Catalog %60
        self.dashboard_height = int(self.screen_height * 0.40)  # Dashboard %40
        self.radar_height = 0  # Radar kaldırıldı
        self.probe_height = self.screen_height - self.dashboard_height - 50  # Catalog kalan %60
        
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
        self.speed_factor = 1.0  # Hız çarpanı (1.0 = normal hız)
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
    
    def add_console_line(self, text: str, color=Colors.WHITE):
        """Linux konsoluna yeni satır ekle (zaman damgası olmadan)"""
        self.console_lines.append((text, color))
        if len(self.console_lines) > self.max_console_lines * 2:
            self.console_lines = self.console_lines[-self.max_console_lines:]
    
    def add_command_line(self, command: str):
        """Komut satırını yeşil renkte ve saat ile ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_lines.append((f"[{timestamp}] > {command}", Colors.GREEN))
        if len(self.console_lines) > self.max_console_lines * 2:
            self.console_lines = self.console_lines[-self.max_console_lines:]
    
    def add_catalog_line(self, text: str, color=Colors.WHITE):
        """Catalog alanına yeni satır ekle"""
        if not hasattr(self, 'catalog_lines'):
            self.catalog_lines = []
        self.catalog_lines.append((text, color))
        if len(self.catalog_lines) > 50:  # Maksimum 50 satır
            self.catalog_lines = self.catalog_lines[-50:]
    
    def print_console(self):
        """Konsol görünümünü çiz - Text wrap ile"""
        # Konsol arka planı (siyah) - Tam yükseklik
        console_rect = pygame.Rect(0, 0, self.left_width, self.console_height)
        pygame.draw.rect(self.screen, Colors.BLACK, console_rect)
        pygame.draw.rect(self.screen, Colors.GREEN, console_rect, 2)
        
        # Konsol satırlarını çiz (scroll ile) - Text wrap ile
        y_start = 10
        
        # Scroll hesaplama - Basit ve doğru yöntem
        if len(self.console_lines) <= self.max_console_lines:
            # Eğer toplam satır sayısı max'dan az ise, scroll yok
            visible_lines = self.console_lines
        else:
            # Scroll ile gösterilecek satırları hesapla
            start_index = max(0, len(self.console_lines) - self.max_console_lines - self.console_scroll)
            end_index = len(self.console_lines) - self.console_scroll
            visible_lines = self.console_lines[start_index:end_index]
        
        line_offset = 0
        for i, (line, color) in enumerate(visible_lines):
            if y_start + (i + line_offset) * 16 < self.console_height - 60:  # Komut satırı için yer bırak
                # Text wrap için satırı böl
                max_width = self.left_width - 20  # Sağ taraftan 20px boşluk
                wrapped_lines = self.wrap_text(line, max_width)
                
                # Her wrapped satırı çiz
                for j, wrapped_line in enumerate(wrapped_lines):
                    current_y = y_start + (i + line_offset + j) * 16
                    if current_y < self.console_height - 60:
                        text_surface = self.font_mono.render(wrapped_line, True, color)
                        self.screen.blit(text_surface, (10, current_y))
                
                # Wrap text olduğunda satırlar arasında boşluk bırak
                if len(wrapped_lines) > 1:
                    line_offset += len(wrapped_lines) - 1
    
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
        if not self.ship or not self.mission_started:
            return
        
        # Orta bölüm arka planı (siyah) - Matris alanı konsol alanının bittiği yerden başlar
        # Matrix'i orta panel içinde ortalayacak şekilde hesapla
        # Koordinat sayıları için daha fazla alan bırak
        matrix_margin = 30  # Artırıldı: 15 -> 30
        
        # Önce cell size'ı hesapla (kare hücreler için)
        available_width = self.matrix_width - (2 * matrix_margin)
        available_height = self.matrix_height - (2 * matrix_margin)
        self.cell_size = min(available_width // self.matrix_size, available_height // self.matrix_size)
        
        # Matrix'in gerçek boyutlarını hesapla
        matrix_pixel_width = self.matrix_size * self.cell_size
        matrix_pixel_height = self.matrix_size * self.cell_size
        
        # Matrix'i orta panel içinde ortalayacak şekilde konumlandır
        matrix_x = self.left_width + (self.matrix_width - matrix_pixel_width) // 2
        matrix_y = (self.matrix_height - matrix_pixel_height) // 2
        
        matrix_rect = pygame.Rect(
            matrix_x,  # Ortalanmış X konumu
            matrix_y,  # Ortalanmış Y konumu
            matrix_pixel_width,  # Matrix genişliği
            matrix_pixel_height  # Matrix yüksekliği
        )
        
        pygame.draw.rect(self.screen, Colors.BLACK, matrix_rect)
        pygame.draw.rect(self.screen, Colors.GREEN, matrix_rect, 2)  # Matris alanı etrafında yeşil çizgi
        
        # Grid çizgileri - grid_enabled durumuna göre
        if self.grid_enabled:
            self.draw_grid(matrix_rect)
        
        # 40x40 görsel matris çiz
        self.draw_visual_matrix(matrix_rect)
    
    def print_dashboard_panel(self):
        """Sağ üst - Dashboard paneli"""
        if not self.mission_started:
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
        
        # Koordinatlar - Hareket durumuna göre renk ve yanıp sönme
        if not self.engine_on:
            # Engine off - Kırmızı ve yanıp sönsün
            self.coord_blink_timer += 1
            if self.coord_blink_timer > 30:  # 30 frame'de bir yanıp söner
                self.coord_blink_timer = 0
            
            if self.coord_blink_timer < 15:  # İlk 15 frame görünür
                coord_text = f"{self.ship.x} : {self.ship.y}"
                coord_surface = self.font_large.render(coord_text, True, Colors.RED)
                self.screen.blit(coord_surface, (x_start, y_start + 60))
        else:
            # Engine on - Yöne göre renk
            if self.ship.direction in [Direction.UP, Direction.DOWN]:
                # Yukarı/Aşağı - Y yeşil, X koyu gri
                x_text = f"{self.ship.x}"
                y_text = f"{self.ship.y}"
                
                x_surface = self.font_large.render(x_text, True, Colors.DARK_GRAY)
                y_surface = self.font_large.render(y_text, True, Colors.GREEN)
                
                # " : " ayırıcısı
                separator_surface = self.font_large.render(" : ", True, Colors.WHITE)
                
                # Pozisyonları hesapla
                x_width = x_surface.get_width()
                separator_width = separator_surface.get_width()
                
                self.screen.blit(x_surface, (x_start, y_start + 60))
                self.screen.blit(separator_surface, (x_start + x_width, y_start + 60))
                self.screen.blit(y_surface, (x_start + x_width + separator_width, y_start + 60))
            else:
                # Sağa/Sola - X yeşil, Y koyu gri
                x_text = f"{self.ship.x}"
                y_text = f"{self.ship.y}"
                
                x_surface = self.font_large.render(x_text, True, Colors.GREEN)
                y_surface = self.font_large.render(y_text, True, Colors.DARK_GRAY)
                
                # " : " ayırıcısı
                separator_surface = self.font_large.render(" : ", True, Colors.WHITE)
                
                # Pozisyonları hesapla
                x_width = x_surface.get_width()
                separator_width = separator_surface.get_width()
                
                self.screen.blit(x_surface, (x_start, y_start + 60))
                self.screen.blit(separator_surface, (x_start + x_width, y_start + 60))
                self.screen.blit(y_surface, (x_start + x_width + separator_width, y_start + 60))
        
        # Yön bilgisi kaldırıldı - koordinat renkleri yönü gösteriyor
        
        # Hız bilgisi (sarı) - Saniye/Nokta
        effective_speed = self.ship.speed / self.speed_factor
        speed_text = f"{effective_speed:.2f} sn/nokta"
        speed_surface = self.font_medium.render(speed_text, True, Colors.YELLOW)
        self.screen.blit(speed_surface, (x_start, y_start + 85))
        
        # 24 saat hız bilgisi (yeşil)
        if hasattr(self, 'required_24h_speed') and self.required_24h_speed > 0:
            required_speed_text = f"24h: {self.required_seconds_per_point:.2f} sn/nokta"
            required_speed_surface = self.font_medium.render(required_speed_text, True, Colors.GREEN)
            self.screen.blit(required_speed_surface, (x_start, y_start + 105))
        
        # Enerji bilgisi (sarı)
        energy_text = f"{self.ship.energy} Nokta"
        energy_surface = self.font_medium.render(energy_text, True, Colors.YELLOW)
        self.screen.blit(energy_surface, (x_start, y_start + 160))
        
        energy_percent = (self.ship.energy / self.ship.max_energy) * 100
        energy_percent_text = f"(%{energy_percent:.1f})"
        energy_percent_surface = self.font_medium.render(energy_percent_text, True, Colors.YELLOW)
        self.screen.blit(energy_percent_surface, (x_start, y_start + 180))
        
        # Alert sistemi - Dashboard'ın sonuna eklendi
        if self.radar_alarm:
            # Yanıp sönme efekti için timer
            self.alarm_blink_timer += 1
            if self.alarm_blink_timer > 30:  # 30 frame'de bir yanıp söner
                self.alarm_blink_timer = 0
            
            # Yanıp sönme kontrolü
            if self.alarm_blink_timer < 15:  # İlk 15 frame görünür
                alert_text = "[ALERT] CELESTIAL OBJECTS"
                alert_surface = self.font_medium.render(alert_text, True, Colors.RED)
                self.screen.blit(alert_surface, (x_start, y_start + 200))
    
    
    def print_probe_panel(self):
        """Sağ alt - Catalogs paneli"""
        if not self.mission_started:
            return
        
        # Catalogs arka planı (siyah) - Dashboard'ın altından başlar
        catalogs_x = self.left_width + self.center_width
        catalogs_y = self.dashboard_height
        catalogs_rect = pygame.Rect(catalogs_x, catalogs_y, self.right_width, self.probe_height)
        pygame.draw.rect(self.screen, Colors.BLACK, catalogs_rect)
        
        y_start = catalogs_y + 10
        x_start = catalogs_x + 10
        
        # Catalogs başlığı
        catalogs_title = self.font_large.render("Catalogs", True, Colors.WHITE)
        self.screen.blit(catalogs_title, (x_start, y_start))
        
        # Catalog çıktılarını göster
        if hasattr(self, 'catalog_lines') and self.catalog_lines:
            y_offset = y_start + 40
            for text, color in self.catalog_lines[-20:]:  # Son 20 satırı göster
                if y_offset > catalogs_y + self.probe_height - 20:
                    break
                text_surface = self.font_small.render(text, True, color)
                self.screen.blit(text_surface, (x_start, y_offset))
                y_offset += 16
        else:
            # Sadece "Ready" yazısı göster
            ready_text = self.locale.get("catalog.ready")
            ready_surface = self.font_medium.render(ready_text, True, Colors.GREEN)
            self.screen.blit(ready_surface, (x_start, y_start + 40))
    
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
        self.matrix_objects = self.chunk_manager.get_objects_in_area(
            self.matrix_start_x, self.matrix_start_y,
            self.matrix_start_x + self.matrix_size - 1,
            self.matrix_start_y + self.matrix_size - 1,
            self.current_universe_name
        )
        
        
        # Gök cisimlerini koordinat bazlı dictionary'ye çevir (hızlı arama)
        objects_by_coord = {}
        for obj in self.matrix_objects:
            coord_key = (obj['x'], obj['y'])
            objects_by_coord[coord_key] = obj
        
        # Radar alarm kontrolü - Matrix'te gök cismi var mı?
        self.radar_alarm = len(self.matrix_objects) > 0
        
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
                    obj = objects_by_coord[(real_x, real_y)]
                    obj_type = obj.get('type', 'unknown')
                    
                    # Gök cismi türüne göre renk belirle
                    if obj_type == 'sun':
                        color = Colors.YELLOW  # Sarı
                    elif obj_type == 'black_hole':
                        color = Colors.DARK_GRAY  # Koyu gri
                    elif obj_type == 'asteroid_belt':
                        color = Colors.LIGHT_GRAY  # Açık gri
                    elif obj_type == 'planet':
                        color = Colors.NAVY  # Navy
                    elif obj_type == 'comet':
                        color = Colors.WHITE  # Beyaz
                    else:
                        color = Colors.YELLOW  # Varsayılan
                
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
        # X ekseni etiketleri (alt) - Matrix alanının dışında
        for i in range(0, self.matrix_size, 5):  # Her 5 hücrede bir
            real_x = self.matrix_start_x + i
            label_text = str(real_x)
            label_surface = self.font_small.render(label_text, True, Colors.WHITE)
            
            # Matrix alanının dışında, alt kenarda
            x_pos = matrix_rect.left + i * self.cell_size + (self.cell_size // 2)
            y_pos = matrix_rect.bottom + 15  # Matrix alanının dışında, alt kenardan 15 pixel aşağı
            
            # Orta panel sınırları içinde kal
            if x_pos + label_surface.get_width() <= matrix_rect.right + 30:
                text_rect = label_surface.get_rect(center=(x_pos, y_pos))
                self.screen.blit(label_surface, text_rect)
        
        # Y ekseni etiketleri (sol) - Matrix alanının dışında
        for j in range(0, self.matrix_size, 5):  # Her 5 hücrede bir
            real_y = self.matrix_start_y + j
            label_text = str(real_y)
            label_surface = self.font_small.render(label_text, True, Colors.WHITE)
            
            # Matrix alanının dışında, sol kenarda
            x_pos = matrix_rect.left - 15  # Matrix alanının dışında, sol kenardan 15 pixel sola
            y_pos = matrix_rect.top + j * self.cell_size + (self.cell_size // 2)
            
            # Orta panel sınırları içinde kal
            if y_pos + label_surface.get_height() <= matrix_rect.bottom + 30:
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
            self.add_console_line(self.locale.get("errors.coordinates_out_of_bounds", max=self.universe_size-1), Colors.RED)
            return
        
        # Enerji kontrolü - Her nokta değişikliğinde 1 birim enerji
        energy_cost = 1
        if self.ship.energy < energy_cost:
            self.add_console_line(f"ERROR: Insufficient energy! Required: {energy_cost}, Available: {self.ship.energy}", Colors.RED)
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
        
        # Matrix başlangıç koordinatlarını güncelle (teleportasyon sonrası)
        half_size = self.matrix_size // 2
        self.matrix_start_x = x - half_size
        self.matrix_start_y = y - half_size
        
        # Chunk'ları güncelle (teleportasyon sonrası)
        self.chunk_manager.unload_distant_chunks(x, y)
        
        # Motoru durdur (teleportasyon sonrası güvenlik)
        self.ship.is_moving = False
        
        # Başarı mesajı
        
        # Komut çıktısına ekle
        self.add_console_line(self.locale.get("commands.teleported", x=x, y=y))
        self.add_console_line(self.locale.get("commands.energy_cost", cost=energy_cost))
        
        # Matrix görüntüye bilgi ekle
        self.add_matrix_line(f"TELEPORTASYON: ({old_x}, {old_y}) → ({x}, {y})", Colors.MAGENTA)
        self.add_matrix_line(f"ENERJİ TÜKETİMİ: {energy_cost} birim", Colors.MAGENTA)
        self.add_matrix_line(f"MATRİS MERKEZİ: ({x}, {y})", Colors.CYAN)
        self.add_matrix_line(f"MATRİS ALANI: ({self.matrix_start_x}, {self.matrix_start_y}) - ({self.matrix_start_x + self.matrix_size - 1}, {self.matrix_start_y + self.matrix_size - 1})", Colors.CYAN)
        
        # Çarpışma kontrolü
        collisions = self.check_collision(x, y)
        if collisions:
            self.add_matrix_line("ALERT: Teleportasyon sonrası çarpışma!", Colors.RED)
            self.add_console_line("ALERT: Teleportasyon sonrası çarpışma!")
            for obj in collisions:
                self.add_matrix_line(f"  - {obj.name} ({obj.obj_type.value}) ile çarpışıldı!", Colors.RED)
    
    def add_matrix_line(self, text: str, color: tuple = Colors.CYAN):
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
        
        # ship.speed artık doğrudan saniye/nokta değeri
        self.seconds_per_point = self.ship.speed
        
        # 24 saatte tüm noktalara ulaşma hesaplaması
        self.calculate_24h_speed()
    
    def calculate_24h_speed(self):
        """24 saatte tüm noktalara ulaşmak için gereken hızı hesapla"""
        if not self.ship or not hasattr(self, 'universe_size'):
            return
        
        total_points = self.universe_size * self.universe_size
        seconds_in_24h = 24 * 60 * 60  # 86400 saniye
        
        # Gerekli hız: nokta başına kaç saniye
        self.required_seconds_per_point = seconds_in_24h / total_points
        
        # Hız değeri (ship.speed formatına çevir)
        # ship.speed artık doğrudan saniye/nokta değeri
        self.required_24h_speed = self.required_seconds_per_point
    
    def save_celestial_to_catalog(self, celestial_name):
        """Save celestial object to catalog"""
        # Find celestial object in current matrix objects
        celestial_obj = None
        for obj in self.matrix_objects:
            if obj.get('name') == celestial_name:
                celestial_obj = obj
                break
        
        if not celestial_obj:
            self.add_catalog_line(f"ERROR: Celestial object '{celestial_name}' not found in matrix!", Colors.RED)
            return
        
        # Load existing catalog
        catalog = self.load_catalog()
        
        # Create catalog entry
        catalog_entry = {
            "name": celestial_obj.get('name'),
            "type": celestial_obj.get('type'),
            "x": celestial_obj.get('x'),
            "y": celestial_obj.get('y'),
            "prop": celestial_obj.get('prop'),
            "resources": celestial_obj.get('resources', {}),
            "saved_at": {
                "ship_x": self.ship.x,
                "ship_y": self.ship.y,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Add to catalog
        catalog.append(catalog_entry)
        
        # Save catalog
        self.save_catalog(catalog)
        
        self.add_catalog_line(self.locale.get("catalog.saved", name=celestial_name), Colors.CYAN)
        self.add_catalog_line(self.locale.get("catalog.saved_position", x=self.ship.x, y=self.ship.y), Colors.WHITE)
    
    def save_all_matrix_objects_to_catalog(self):
        """Save all matrix objects to catalog"""
        if not self.matrix_objects:
            self.add_catalog_line("ERROR: No celestial objects in matrix!", Colors.RED)
            return
        
        # Load existing catalog
        catalog = self.load_catalog()
        
        # Get existing names to avoid duplicates
        existing_names = {entry.get('name') for entry in catalog}
        
        saved_count = 0
        skipped_count = 0
        
        for obj in self.matrix_objects:
            obj_name = obj.get('name')
            
            # Skip if already exists
            if obj_name in existing_names:
                skipped_count += 1
                continue
            
            # Create catalog entry
            catalog_entry = {
                "name": obj.get('name'),
                "type": obj.get('type'),
                "x": obj.get('x'),
                "y": obj.get('y'),
                "prop": obj.get('prop'),
                "resources": obj.get('resources', {}),
                "saved_at": {
                    "ship_x": self.ship.x,
                    "ship_y": self.ship.y,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            # Add to catalog
            catalog.append(catalog_entry)
            existing_names.add(obj_name)
            saved_count += 1
        
        # Save catalog
        self.save_catalog(catalog)
        
        self.add_catalog_line(self.locale.get("catalog.all_saved", count=saved_count), Colors.CYAN)
    
    def list_catalog(self):
        """List catalog contents"""
        catalog = self.load_catalog()
        
        if not catalog:
            self.add_catalog_line(self.locale.get("catalog.list_empty"), Colors.CYAN)
            return
        
        self.add_catalog_line(self.locale.get("catalog.list_title"), Colors.CYAN)
        for i, entry in enumerate(catalog, 1):
            self.add_catalog_line(self.locale.get("catalog.list_item", index=i, name=entry['name'], type=entry['type']), Colors.WHITE)
            self.add_catalog_line(self.locale.get("catalog.list_position", x=entry['x'], y=entry['y']), Colors.WHITE)
            self.add_catalog_line(f"    Prop: {entry['prop']}", Colors.YELLOW)
            if entry.get('resources'):
                resources_text = ", ".join(entry['resources'].keys())
                self.add_catalog_line(self.locale.get("catalog.list_resources", resources=resources_text), Colors.CYAN)
            self.add_catalog_line(self.locale.get("catalog.list_saved_at", ship_x=entry['saved_at']['ship_x'], ship_y=entry['saved_at']['ship_y']), Colors.CYAN)
            self.add_catalog_line("", Colors.WHITE)
        self.add_catalog_line(self.locale.get("catalog.list_end"), Colors.CYAN)
    
    def show_catalog_resume(self):
        """Show catalog resume (statistics)"""
        catalog = self.load_catalog()
        
        if not catalog:
            self.add_catalog_line(self.locale.get("catalog.list_empty"), Colors.CYAN)
            return
        
        self.add_catalog_line(self.locale.get("catalog.stats_title"), Colors.CYAN)
        
        # Count by type
        type_counts = {}
        prop_counts = {}
        resource_counts = {}
        
        for entry in catalog:
            obj_type = entry.get('type', 'unknown')
            prop = entry.get('prop', 'unknown')
            
            type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
            prop_counts[prop] = prop_counts.get(prop, 0) + 1
            
            resources = entry.get('resources', {})
            for resource_type in resources.keys():
                resource_counts[resource_type] = resource_counts.get(resource_type, 0) + 1
        
        # Show type statistics
        self.add_catalog_line(self.locale.get("catalog.stats_by_type"), Colors.YELLOW)
        for obj_type, count in sorted(type_counts.items()):
            self.add_catalog_line(f"  {obj_type}: {count}", Colors.WHITE)
        
        # Show prop statistics
        self.add_catalog_line(self.locale.get("catalog.stats_by_prop"), Colors.YELLOW)
        for prop, count in sorted(prop_counts.items()):
            self.add_catalog_line(f"  {prop}: {count}", Colors.WHITE)
        
        # Show resource statistics
        if resource_counts:
            self.add_catalog_line(self.locale.get("catalog.stats_resources"), Colors.YELLOW)
            for resource_type, count in sorted(resource_counts.items()):
                self.add_catalog_line(f"  {resource_type}: {count}", Colors.WHITE)
        
        self.add_catalog_line(self.locale.get("catalog.stats_end"), Colors.CYAN)
    
    def teleport_to_catalog_object(self, celestial_name):
        """Teleport to catalog object"""
        catalog = self.load_catalog()
        
        # Find celestial object in catalog
        celestial_obj = None
        for entry in catalog:
            if entry['name'] == celestial_name:
                celestial_obj = entry
                break
        
        if not celestial_obj:
            self.add_catalog_line(self.locale.get("catalog.not_found", name=celestial_name), Colors.RED)
            return
        
        # Teleport to coordinates
        self.teleport_ship(celestial_obj['x'], celestial_obj['y'])
        self.add_catalog_line(self.locale.get("catalog.teleported", name=celestial_name, x=celestial_obj['x'], y=celestial_obj['y']), Colors.CYAN)
    
    def load_catalog(self):
        """Load catalog from session cats.json"""
        try:
            if not hasattr(self, 'current_session_name') or not self.current_session_name:
                return []
            if not hasattr(self, 'current_universe_name') or not self.current_universe_name:
                return []
            
            catalog_path = f"sessions/{self.current_universe_name}/{self.current_session_name}/cats.json"
            with open(catalog_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            self.add_console_line(f"Error loading catalog: {e}", Colors.RED)
            return []
    
    def save_catalog(self, catalog):
        """Save catalog to session cats.json"""
        try:
            if not hasattr(self, 'current_session_name') or not self.current_session_name:
                self.add_console_line("ERROR: No active session!", Colors.RED)
                return
            if not hasattr(self, 'current_universe_name') or not self.current_universe_name:
                self.add_console_line("ERROR: No active universe!", Colors.RED)
                return
            
            catalog_path = f"sessions/{self.current_universe_name}/{self.current_session_name}/cats.json"
            with open(catalog_path, 'w', encoding='utf-8') as f:
                json.dump(catalog, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.add_console_line(f"Error saving catalog: {e}", Colors.RED)
    
    def setup_session_structure(self, session_name, universe_name):
        """Create session folder structure"""
        try:
            # Create sessions folder if it doesn't exist
            sessions_dir = "sessions"
            os.makedirs(sessions_dir, exist_ok=True)
            
            # Create universe folder under sessions
            universe_dir = f"sessions/{universe_name}"
            os.makedirs(universe_dir, exist_ok=True)
            
            # Create session folder under universe
            session_dir = f"sessions/{universe_name}/{session_name}"
            os.makedirs(session_dir, exist_ok=True)
            
            # Create maps subfolder
            maps_dir = f"sessions/{universe_name}/{session_name}/maps"
            os.makedirs(maps_dir, exist_ok=True)
            
            self.add_console_line(f"Session structure created: {session_dir}", Colors.CYAN)
            
        except Exception as e:
            self.add_console_line(f"Error creating session structure: {e}", Colors.RED)
    
    def print_catalog_statistics(self, x_start, y_start):
        """Print catalog statistics"""
        catalog = self.load_catalog()
        
        if not catalog:
            # Katalog yokken hiçbir şey gösterme
            return
        
        # Evrendeki toplam gök cismi sayılarını hesapla
        total_objects = self.get_total_universe_objects()
        
        # Count by type
        type_counts = {}
        prop_counts = {}
        resource_counts = {}
        
        for entry in catalog:
            obj_type = entry.get('type', 'unknown')
            prop = entry.get('prop', 'unknown')
            
            # None değerleri 'unknown' olarak değiştir
            if obj_type is None:
                obj_type = 'unknown'
            if prop is None:
                prop = 'unknown'
            
            # Count by type
            type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
            
            # Count by prop
            prop_counts[prop] = prop_counts.get(prop, 0) + 1
            
            # Count resources
            resources = entry.get('resources', {})
            for resource_type, resource_data in resources.items():
                if isinstance(resource_data, dict):
                    resource_counts[resource_type] = resource_counts.get(resource_type, 0) + 1
        
        # Display statistics
        y_offset = y_start
        
        # 1. TİPLER (Types)
        type_title = self.font_medium.render("TYPES:", True, Colors.WHITE)
        self.screen.blit(type_title, (x_start, y_offset))
        y_offset += 25
        
        for obj_type, catalog_count in sorted(type_counts.items()):
            total_count = total_objects.get(obj_type, 0)
            percentage = (catalog_count / total_count * 100) if total_count > 0 else 0
            type_text = f"{obj_type}: {catalog_count} - {total_count} ({percentage:.1f}%)"
            type_surface = self.font_large.render(type_text, True, Colors.CYAN)
            self.screen.blit(type_surface, (x_start, y_offset))
            y_offset += 18
        
        y_offset += 15
        
        # 2. ALT TİPLER (Props)
        prop_title = self.font_medium.render("PROPS:", True, Colors.WHITE)
        self.screen.blit(prop_title, (x_start, y_offset))
        y_offset += 25
        
        for prop, catalog_count in sorted(prop_counts.items()):
            # Bu prop'un evrendeki toplam sayısını hesapla
            total_count = 0
            for chunk_coord in self.chunk_manager.loaded_chunks:
                chunk_objects = self.chunk_manager.chunks.get(chunk_coord, [])
                for obj in chunk_objects:
                    if obj.get('prop') == prop:
                        total_count += 1
            
            percentage = (catalog_count / total_count * 100) if total_count > 0 else 0
            prop_text = f"{prop}: {catalog_count} - {total_count} ({percentage:.1f}%)"
            prop_surface = self.font_large.render(prop_text, True, Colors.YELLOW)
            self.screen.blit(prop_surface, (x_start, y_offset))
            y_offset += 18
        
        y_offset += 15
        
        # 3. RESOURCES
        resource_title = self.font_medium.render("RESOURCES:", True, Colors.WHITE)
        self.screen.blit(resource_title, (x_start, y_offset))
        y_offset += 25
        
        for resource_type, catalog_count in sorted(resource_counts.items()):
            # Bu resource'un evrendeki toplam sayısını hesapla
            total_count = 0
            for chunk_coord in self.chunk_manager.loaded_chunks:
                chunk_objects = self.chunk_manager.chunks.get(chunk_coord, [])
                for obj in chunk_objects:
                    resources = obj.get('resources', {})
                    if resource_type in resources:
                        total_count += 1
            
            percentage = (catalog_count / total_count * 100) if total_count > 0 else 0
            resource_text = f"{resource_type}: {catalog_count} - {total_count} ({percentage:.1f}%)"
            resource_surface = self.font_large.render(resource_text, True, Colors.GREEN)
            self.screen.blit(resource_surface, (x_start, y_offset))
            y_offset += 18
    
    def get_total_universe_objects(self):
        """Evrendeki toplam gök cismi sayılarını hesapla"""
        total_counts = {}
        
        # Tüm yüklenmiş chunk'ları tara
        for chunk_coord in self.chunk_manager.loaded_chunks:
            chunk_objects = self.chunk_manager.chunks.get(chunk_coord, [])
            for obj in chunk_objects:
                obj_type = obj.get('type', 'unknown')
                if obj_type is None:
                    obj_type = 'unknown'
                total_counts[obj_type] = total_counts.get(obj_type, 0) + 1
        
        return total_counts
    
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
        """Gemi pozisyonunu güncelle - ship.speed saniyede bir"""
        if not self.ship or not self.ship.is_moving:
            return
        
        now = datetime.now()
        time_diff = (now - self.last_position_update).total_seconds()  # saniye cinsinden
        
        # ship.speed saniyede bir pozisyon güncelle (speed_factor ile çarpılmış)
        effective_speed = self.ship.speed / self.speed_factor
        if time_diff >= effective_speed:
            # Enerji tüketimi - Her nokta değişikliğinde 1 birim enerji
            energy_cost_per_point = 1
            self.ship.energy -= energy_cost_per_point
            
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
        
        # Komut formatını göster (yeşil renkte ve saat ile)
        self.add_command_line(command)
        
        if cmd == "go":
            # DEPRECATED: go komutu artık kullanımdan kaldırıldı
            self.add_console_line("⚠️  UYARI: 'go' komutu DEPRECATED (kullanımdan kaldırıldı)!", Colors.YELLOW)
            self.add_console_line("")
            self.add_console_line("Bunun yerine 'universe' veya 'u' komutunu kullanın:", Colors.CYAN)
            self.add_console_line("  universe --name <isim> --size <boyut>", Colors.WHITE)
            self.add_console_line("  u -n <isim> -s <boyut>", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("Örnek:", Colors.CYAN)
            self.add_console_line("  universe --name myuniverse --size 500", Colors.WHITE)
            self.add_console_line("  u -n myuniverse -s 1000", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("'go' komutu hiçbir işlem yapmıyor.", Colors.RED)
        
        elif cmd in ["engine", "e"]:
            if not self.ship:
                self.add_console_line(self.locale.get("errors.universe_required"), Colors.RED)
                return
            
            if len(parts) < 2:
                self.add_console_line("ERROR: Usage: engine on/off or e on/off", Colors.RED)
                return
            
            action = parts[1].lower()
            if action == "on":
                self.start_engine()
                self.add_console_line(self.locale.get("commands.engine_started"))
            elif action == "off":
                self.stop_engine()
                self.add_console_line(self.locale.get("commands.engine_stopped"))
            else:
                self.add_console_line("ERROR: Invalid parameter! Use 'on' or 'off'", Colors.RED)
        
        elif cmd in ["rotate", "r"]:
            if not self.ship:
                self.add_console_line(self.locale.get("errors.universe_required"), Colors.RED)
                return
            
            if len(parts) < 2:
                self.add_console_line("ERROR: Usage: rotate <direction> or r <direction>", Colors.RED)
                self.add_console_line("Directions: right/r, left/l, up/u, down/d", Colors.RED)
                return
            
            direction = parts[1].lower()
            
            if direction in ["right", "r"]:
                self.rotate_right()
                self.add_console_line(self.locale.get("commands.rotated", direction="right"))
            elif direction in ["left", "l"]:
                self.rotate_left()
                self.add_console_line(self.locale.get("commands.rotated", direction="left"))
            elif direction in ["up", "u"]:
                self.rotate_up()
                self.add_console_line(self.locale.get("commands.rotated", direction="up"))
            elif direction in ["down", "d"]:
                self.rotate_down()
                self.add_console_line(self.locale.get("commands.rotated", direction="down"))
            else:
                self.add_console_line("ERROR: Invalid direction! Usage: right/r, left/l, up/u, down/d", Colors.RED)
        
        elif cmd == "turnback":
            if not self.ship:
                self.add_console_line(self.locale.get("errors.universe_required"), Colors.RED)
                return
            
            self.turn_back()
            self.add_console_line(self.locale.get("commands.turned_back"))
        
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
                self.add_console_line("HATA: Kullanım: tp <x:y> veya tp --cat <gokcismi_adı>")
                self.add_console_line("Örnek: tp 100:200")
                self.add_console_line("Örnek: tp --cat star_50_75")
                return
            
            if parts[1] == "--cat":
                if len(parts) < 3:
                    self.add_console_line("HATA: Gök cismi adı gerekli! Kullanım: tp --cat <gokcismi_adı>", Colors.RED)
                    return
                
                celestial_name = parts[2]
                self.teleport_to_catalog_object(celestial_name)
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
        
        elif cmd == "test":
            self.add_matrix_line("Test komutu başarılı!", Colors.CYAN)
            self.add_console_line("Test komutu başarılı!", Colors.CYAN)
        
        elif cmd in ["speed", "s"]:
            if not self.ship:
                self.add_console_line("HATA: Önce görev başlatılmalı!")
                return
            
            # Hız değiştirme kontrolü
            if len(parts) >= 2:
                try:
                    seconds_per_point = float(parts[1])
                    if 0.1 <= seconds_per_point <= 60:
                        old_speed = self.ship.speed
                        
                        # Yeni hızı ayarla (saniye/nokta)
                        self.ship.speed = seconds_per_point
                        self.calculate_speed_info()
                        
                        # Enerji kapasitesi değişmez, sadece hareket hızı değişir
                        # Enerji: evrendeki tüm noktaları 3 defa ziyaret edecek kadar sabit kalır
                        
                        self.add_console_line(self.locale.get("commands.speed_set", speed=seconds_per_point))
                        self.add_console_line(f"1 nokta: {seconds_per_point:.2f} saniye")
                        return
                    else:
                        self.add_console_line("HATA: Hız 0.1-60 saniye arasında olmalı!")
                        return
                except ValueError:
                    self.add_console_line("HATA: Geçersiz hız değeri!")
                    return
            
            # Hız analizi (parametre yoksa)
            seconds_per_point = self.ship.speed
            points_per_minute = 60 / seconds_per_point
            points_per_hour = points_per_minute * 60
            
            speed_info = f"HIZ ANALİZİ:"
            self.add_console_line(speed_info)
            self.add_console_line(f"1 nokta: {seconds_per_point:.2f} saniye")
            self.add_console_line(f"1 dakikada: {points_per_minute:.1f} nokta")
            self.add_console_line(f"1 saatte: {points_per_hour:.1f} nokta")
            
        
        elif cmd in ["+", "-", "max"]:
            if not self.ship:
                self.add_console_line("HATA: Önce görev başlatılmalı!", Colors.RED)
                return
            
            if cmd == "max":
                # Maksimum hıza ayarla (1x normal hız)
                self.speed_factor = 1.0
                effective_speed = self.ship.speed / self.speed_factor
                self.add_console_line(f"Hız maksimuma ayarlandı: {effective_speed:.2f} saniye/nokta", Colors.GREEN)
                return
            
            if len(parts) < 2:
                self.add_console_line("HATA: Kullanım: + <yüzde> veya - <yüzde>", Colors.RED)
                self.add_console_line("Örnek: + 10 (hızı %10 artır), - 10 (hızı %10 azalt)", Colors.WHITE)
                return
            
            try:
                percentage = float(parts[1])
                if percentage < 0:
                    self.add_console_line("HATA: Yüzde değeri pozitif olmalı!", Colors.RED)
                    return
                
                if cmd == "+":
                    # Hız artırma - mevcut hızın yüzdesi kadar artır
                    if percentage == 0:
                        self.add_console_line("HATA: + 0 geçersiz! Hız artırmak için pozitif değer girin.", Colors.RED)
                        return
                    
                    # Mevcut hızın yüzdesi kadar artır
                    current_effective_speed = self.ship.speed / self.speed_factor
                    new_effective_speed = current_effective_speed * (1 - percentage / 100)  # Daha hızlı = daha az saniye
                    new_factor = self.ship.speed / new_effective_speed
                    
                    # Maksimum hız sınırı (1x normal hız = en hızlı)
                    if new_factor > 1.0:
                        self.add_console_line("HATA: Maksimum hız sınırına ulaşıldı! (max komutu ile kontrol edin)", Colors.RED)
                        return
                    
                    self.speed_factor = new_factor
                    self.add_console_line(f"Hız %{percentage:.1f} artırıldı. Yeni hız: {new_effective_speed:.2f} saniye/nokta", Colors.GREEN)
                
                elif cmd == "-":
                    # Hız azaltma - mevcut hızın yüzdesi kadar azalt
                    if percentage == 0:
                        # - 0 = dur
                        self.stop_engine()
                        self.add_console_line("Motor durduruldu.", Colors.YELLOW)
                        return
                    
                    # Mevcut hızın yüzdesi kadar azalt
                    current_effective_speed = self.ship.speed / self.speed_factor
                    new_effective_speed = current_effective_speed * (1 + percentage / 100)  # Daha yavaş = daha fazla saniye
                    new_factor = self.ship.speed / new_effective_speed
                    
                    # Minimum hız sınırı (10x normal hız = en yavaş)
                    if new_factor < 0.1:
                        self.add_console_line("HATA: Minimum hız sınırına ulaşıldı! (10x normal hız)", Colors.RED)
                        return
                    
                    self.speed_factor = new_factor
                    self.add_console_line(f"Hız %{percentage:.1f} azaltıldı. Yeni hız: {new_effective_speed:.2f} saniye/nokta", Colors.GREEN)
                
            except ValueError:
                self.add_console_line("HATA: Geçersiz yüzde değeri!", Colors.RED)
                return
        
        elif cmd in ["refresh", "r"]:
            if not self.ship:
                self.add_console_line("HATA: Önce görev başlatılmalı!")
                return
            
            # Güncelleme süresi bilgisi
            update_interval = self.ship.speed
            self.add_console_line(f"GÜNCELLEME SÜRESİ: {update_interval:.2f} saniye")
            self.add_console_line(f"Matris her {update_interval:.2f} saniyede bir güncellenir")
            
        
        elif cmd in ["clear", "cls"]:
            self.console_lines.clear()
            self.add_console_line("Konsol temizlendi")
        
        elif cmd == "↓" or cmd == "down":
            # Konsol aşağı scroll (eski mesajlara git)
            max_scroll = max(0, len(self.console_lines) - self.max_console_lines)
            if self.console_scroll < max_scroll:
                self.console_scroll += 1
        
        elif cmd == "↑" or cmd == "up":
            # Konsol yukarı scroll (yeni mesajlara git)
            if self.console_scroll > 0:
                self.console_scroll -= 1
        
        elif cmd == "scrollinfo":
            # Debug: Scroll bilgilerini göster
            max_scroll = max(0, len(self.console_lines) - self.max_console_lines)
            self.add_console_line(f"Toplam satır: {len(self.console_lines)}")
            self.add_console_line(f"Max gösterilecek: {self.max_console_lines}")
            self.add_console_line(f"Mevcut scroll: {self.console_scroll}")
            self.add_console_line(f"Max scroll: {max_scroll}")
        
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
        
        elif cmd in ["info", "i"]:
            if len(parts) > 1:
                sub_cmd = parts[1].lower()
                if sub_cmd == "universe" or sub_cmd == "u":
                    self.show_universe_info()
                elif sub_cmd == "objects" or sub_cmd == "o":
                    self.show_matrix_objects_info()
            else:
                self.add_console_line("HATA: Geçersiz parametre! Kullanım: info universe/objects veya i u/o", Colors.RED)
        else:
            self.add_console_line("HATA: info universe/objects kullanın veya i u/o", Colors.RED)
        
        if cmd in ["universe", "u"]:
            # Parametreleri parse et
            name = None
            size = 200  # Default boyut (dokümantasyona göre)
            force_create = False
            session_name = None
            
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
                elif part in ["--size"]:
                    if i + 1 < len(parts):
                        try:
                            size = int(parts[i + 1])
                            if size < 200 or size > 2000:
                                self.add_console_line("HATA: Evren boyutu 200-2000 arasında olmalı!")
                                return
                            i += 2
                        except ValueError:
                            self.add_console_line("HATA: Geçersiz boyut değeri!")
                            return
                    else:
                        self.add_console_line("HATA: --size parametresi için değer gerekli!", Colors.RED)
                        return
                elif part in ["--session", "-s"]:
                    if i + 1 < len(parts):
                        session_name = parts[i + 1]
                        i += 2
                    else:
                        self.add_console_line("HATA: --session (-s) parametresi için değer gerekli!", Colors.RED)
                        return
                elif part in ["--create", "-c"]:
                    force_create = True
                    i += 1
                else:
                    i += 1
            
            # Name parametresi zorunlu
            if name is None:
                self.add_console_line("HATA: --name (-n) parametresi zorunlu! Örnek: universe --name myuniverse --size 500")
                return
            
            # Session adını ayarla (default: evren adı)
            if session_name is None:
                session_name = name
            
            # Session klasör yapısını oluştur
            self.setup_session_structure(session_name, name)
            
            # Mevcut evreni kontrol et
            universe_file = f"universes/{name}.json"
            chunk_metadata_file = f"universes/{name}/metadata.json"
            self.current_universe_name = name
            self.current_session_name = session_name
            
            if (os.path.exists(universe_file) or os.path.exists(chunk_metadata_file)) and not force_create:
                # Mevcut evreni yükle
                if os.path.exists(chunk_metadata_file):
                    # Chunk-based format
                    self.load_universe(chunk_metadata_file)
                else:
                    # Eski format
                    self.load_universe(universe_file)
                
                self.start_mission(1)
                # Matrix boyutunu güncelle
                self.matrix_size = self.calculate_matrix_size()
                
                self.add_console_line(f"Evren yüklendi: {name}")
                self.add_console_line(f"Boyut: {self.universe_size}x{self.universe_size}")
                self.add_console_line(f"Matrix: {self.matrix_size}x{self.matrix_size}")
                
                # Başlangıç mesajları
                self.add_console_line("")
                self.add_console_line("=== UNIVERSE READY ===")
                self.add_console_line("Movement: engine on/off, rotate <direction>, speed <value>")
                self.add_console_line("Info: info universe/objects, scan <x:y>, tp <x:y>")
                self.add_console_line("Teleport: tp <x:y> veya tp --cat <gokcismi_adı>")
                self.add_console_line("Catalog: cat --save <name>, cat --list")
                self.add_console_line("Map: map --save/--load/--list/--delete <name>")
                self.add_console_line("Exit: quit or exit")
            else:
                # Yeni evren oluştur
                self.universe_size = size
                self.create_advanced_universe(name, size, size, "normal")
                self.start_mission(1)
                # Matrix boyutunu güncelle
                self.matrix_size = self.calculate_matrix_size()
                
                self.add_console_line(f"Yeni evren oluşturuldu: {name}")
                self.add_console_line(f"Boyut: {self.universe_size}x{self.universe_size}")
                self.add_console_line(f"Matrix: {self.matrix_size}x{self.matrix_size}")
                
                # Başlangıç mesajları
                self.add_console_line("")
                self.add_console_line("=== UNIVERSE READY ===")
                self.add_console_line("Movement: engine on/off, rotate <direction>, speed <value>")
                self.add_console_line("Info: info universe/objects, scan <x:y>, tp <x:y>")
                self.add_console_line("Teleport: tp <x:y> veya tp --cat <gokcismi_adı>")
                self.add_console_line("Catalog: cat --save <name>, cat --list")
                self.add_console_line("Map: map --save/--load/--list/--delete <name>")
                self.add_console_line("Exit: quit or exit")
        
        elif cmd == "lang":
            if len(parts) < 2:
                # List available languages
                self.add_console_line("=== AVAILABLE LANGUAGES ===", Colors.CYAN)
                languages = [
                    ("en", "English"),
                    ("tr", "Türkçe"),
                    ("fr", "Français"),
                    ("de", "Deutsch"),
                    ("es", "Español"),
                    ("ja", "日本語")
                ]
                for code, name in languages:
                    current_marker = " (current)" if code == self.locale.current_language else ""
                    self.add_console_line(f"  {code} - {name}{current_marker}", Colors.WHITE)
                self.add_console_line("", Colors.WHITE)
                self.add_console_line("Usage: lang <language_code>", Colors.CYAN)
                self.add_console_line("Example: lang tr", Colors.CYAN)
                return
            
            language = parts[1].lower()
            supported_languages = ["en", "tr", "fr", "de", "es", "ja"]
            
            if language not in supported_languages:
                self.add_console_line(self.locale.get("language.invalid"), Colors.RED)
                return
            
            self.locale.set_language(language)
            self.add_console_line(self.locale.get("language.changed", language=language.upper()), Colors.CYAN)
        
        elif cmd == "cat":
            if not self.ship:
                self.add_catalog_line("ERROR: Load a universe first!", Colors.RED)
                return
            
            if len(parts) < 2:
                self.add_catalog_line("ERROR: Usage: cat --save <name>, cat --list, cat --all, or cat --resume", Colors.RED)
                return
            
            if parts[1] == "--save" or parts[1] == "-s":
                if len(parts) < 3:
                    self.add_catalog_line(self.locale.get("catalog.name_required"), Colors.RED)
                    return
                
                celestial_name = parts[2]
                self.save_celestial_to_catalog(celestial_name)
                
            elif parts[1] == "--list" or parts[1] == "-ls":
                self.list_catalog()
                
            elif parts[1] == "--all" or parts[1] == "-a":
                self.save_all_matrix_objects_to_catalog()
                
            elif parts[1] == "--resume" or parts[1] == "-r":
                self.show_catalog_resume()
                
            else:
                self.add_catalog_line(self.locale.get("catalog.invalid_command"), Colors.RED)
        
        elif cmd == "map":
            if not self.mission_started:
                self.add_console_line("HATA: Önce bir evren yükleyin (go komutu)", Colors.RED)
                return
            
            if len(parts) < 2:
                self.add_console_line("HATA: Map komutu için parametre gerekli!", Colors.RED)
                self.add_console_line("Kullanım: map --save <isim> --desc <açıklama>")
                self.add_console_line("         map --delete <isim> veya map -d <isim>")
                self.add_console_line("         map --list veya map -ls")
                self.add_console_line("         map --load <isim> veya map -l <isim>")
                return
            
            sub_cmd = parts[1].lower()
            
            if sub_cmd == "--save":
                if len(parts) < 3:
                    self.add_console_line("HATA: Map ismi gerekli! Kullanım: map --save <isim> --desc <açıklama>", Colors.RED)
                    return
                
                map_name = parts[2]
                description = ""
                
                # Description parametresini ara
                if "--desc" in parts:
                    desc_index = parts.index("--desc")
                    if desc_index + 1 < len(parts):
                        description = " ".join(parts[desc_index + 1:])
                
                self.save_map(map_name, description)
                
            elif sub_cmd in ["--delete", "-d"]:
                if len(parts) < 3:
                    self.add_console_line("HATA: Map ismi gerekli! Kullanım: map --delete <isim> veya map -d <isim>", Colors.RED)
                    return
                
                map_name = parts[2]
                self.delete_map(map_name)
                
            elif sub_cmd in ["--list", "-ls"]:
                self.list_maps()
                
            elif sub_cmd in ["--load", "-l"]:
                if len(parts) < 3:
                    self.add_console_line("HATA: Map ismi gerekli! Kullanım: map --load <isim> veya map -l <isim>", Colors.RED)
                    return
                
                map_name = parts[2]
                self.load_map(map_name)
                
            else:
                self.add_console_line("HATA: Geçersiz map komutu!", Colors.RED)
                self.add_console_line("Kullanım: map --save/--delete/--list/--load <parametreler>")
        
        elif cmd == "help":
            if len(parts) > 1:
                # Belirli komut için yardım göster
                self.show_help(parts[1])
            else:
                # Tüm komutlar için yardım göster
                self.show_help()
        
        elif cmd == "quit" or cmd == "exit":
            self.running = False
            self.add_console_line("Oyundan çıkılıyor...", Colors.CYAN)
        
        else:
            self.add_console_line(f"Bilinmeyen komut: {cmd}", Colors.WHITE)
    
    def show_universe_info(self):
        """Evren bilgilerini göster"""
        if not self.mission_started:
            self.add_console_line("HATA: Önce bir evren yükleyin (go komutu)", Colors.RED)
            return
        
        self.add_console_line("=== EVREN BİLGİLERİ ===")
        self.add_console_line(f"Evren Adı: {self.current_universe_name}")
        self.add_console_line(f"Evren Boyutu: {self.universe_size}x{self.universe_size}")
        
        # Evren dosyasını kontrol et - chunk-based mi yoksa eski format mı?
        universe_file = f"universes/{self.current_universe_name}.json"
        metadata_file = f"universes/{self.current_universe_name}/metadata.json"
        
        total_objects = 0
        object_types = {}
        
        if os.path.exists(metadata_file):
            # Chunk-based format
            self.add_console_line("Format: Chunk-based")
            # Tüm chunk'ları yükle ve gök cisimlerini say
            for chunk_x in range(0, (self.universe_size // 100) + 1):
                for chunk_y in range(0, (self.universe_size // 100) + 1):
                    chunk_objects = self.chunk_manager.load_chunk(chunk_x, chunk_y, self.current_universe_name)
                    
                    for obj in chunk_objects:
                        total_objects += 1
                        obj_type = obj.get('type', 'unknown')
                        if obj_type in object_types:
                            object_types[obj_type] += 1
                        else:
                            object_types[obj_type] = 1
        elif os.path.exists(universe_file):
            # Eski format (tek dosya)
            self.add_console_line("Format: Eski format (tek dosya)")
            try:
                with open(universe_file, 'r', encoding='utf-8') as f:
                    universe_data = json.load(f)
                
                if 'objects' in universe_data:
                    for obj in universe_data['objects']:
                        total_objects += 1
                        obj_type = obj.get('type', 'unknown')
                        if obj_type in object_types:
                            object_types[obj_type] += 1
                        else:
                            object_types[obj_type] = 1
            except Exception as e:
                self.add_console_line(f"HATA: Evren dosyası okunamadı: {e}", Colors.RED)
                return
        else:
            self.add_console_line("HATA: Evren dosyası bulunamadı", Colors.RED)
            return
        
        self.add_console_line(f"Toplam Gök Cismi: {total_objects}")
        self.add_console_line("")
        self.add_console_line("Gök Cismi Tipleri:")
        
        # Tipleri alfabetik sıraya göre listele
        for obj_type in sorted(object_types.keys()):
            count = object_types[obj_type]
            percentage = (count / total_objects * 100) if total_objects > 0 else 0
            self.add_console_line(f"  {obj_type}: {count} adet (%{percentage:.1f})")
        
        self.add_console_line("")
        self.add_console_line("=== EVREN BİLGİLERİ SONU ===")
    
    def show_matrix_objects_info(self):
        """Matrix içerisindeki gök cisimleri hakkında detaylı bilgileri göster"""
        if not self.mission_started:
            self.add_console_line("HATA: Önce bir evren yükleyin (go komutu)", Colors.RED)
            return
        
        if not self.ship:
            self.add_console_line("HATA: Gemi bulunamadı!", Colors.RED)
            return
        
        self.add_console_line("=== MATRİS GÖK CİSİMLERİ BİLGİLERİ ===")
        self.add_console_line(f"Gemi Konumu: ({self.ship.x}, {self.ship.y})")
        self.add_console_line(f"Matris Alanı: ({self.matrix_start_x}, {self.matrix_start_y}) - ({self.matrix_start_x + self.matrix_size - 1}, {self.matrix_start_y + self.matrix_size - 1})")
        self.add_console_line(f"Matris Boyutu: {self.matrix_size}x{self.matrix_size}")
        
        # Matrix alanındaki gök cisimlerini yükle
        matrix_objects = self.chunk_manager.get_objects_in_area(
            self.matrix_start_x, self.matrix_start_y,
            self.matrix_start_x + self.matrix_size - 1,
            self.matrix_start_y + self.matrix_size - 1,
            self.current_universe_name
        )
        
        if not matrix_objects:
            self.add_console_line("")
            self.add_console_line("Matris alanında gök cismi bulunamadı.", Colors.CYAN)
            self.add_console_line("")
            self.add_console_line("=== MATRİS GÖK CİSİMLERİ BİLGİLERİ SONU ===")
            return
        
        # Gök cisimlerini mesafeye göre sırala
        objects_with_distance = []
        for obj in matrix_objects:
            distance = ((obj['x'] - self.ship.x) ** 2 + (obj['y'] - self.ship.y) ** 2) ** 0.5
            objects_with_distance.append((obj, distance))
        
        # Mesafeye göre sırala (en yakından en uzağa)
        objects_with_distance.sort(key=lambda x: x[1])
        
        self.add_console_line("")
        self.add_console_line(f"Toplam Gök Cismi: {len(matrix_objects)}")
        self.add_console_line("")
        
        # Gök cisimlerini detaylı olarak listele
        self.add_console_line("GÖK CİSİMLERİ (Mesafeye Göre Sıralı):", Colors.CYAN)
        self.add_console_line("")
        
        for i, (obj, distance) in enumerate(objects_with_distance, 1):
            obj_name = obj.get('name', 'Bilinmeyen')
            obj_type = obj.get('type', 'unknown')
            obj_x = obj['x']
            obj_y = obj['y']
            
            # Gök cismi türüne göre renk ve açıklama
            type_info = self.get_celestial_type_info(obj_type)
            
            self.add_console_line(f"{i:2d}. {obj_name}", Colors.WHITE)
            self.add_console_line(f"    Tür: {type_info['name']} ({obj_type})", type_info['color'])
            self.add_console_line(f"    Konum: ({obj_x}, {obj_y})", Colors.WHITE)
            self.add_console_line(f"    Mesafe: {distance:.1f} nokta", Colors.YELLOW)
            
            # Gök cismi türüne göre özel özellikler
            if obj_type == 'sun':
                self.add_console_line(f"    Yıldız Türü: {obj.get('prop', 'Bilinmeyen')}", Colors.YELLOW)
                self.add_console_line(f"    Yarıçap: {obj.get('radius', 'Bilinmeyen')} birim", Colors.YELLOW)
                self.add_console_line(f"    Sıcaklık: {self.get_star_temperature(obj.get('prop', 'M'))} K", Colors.YELLOW)
                self.add_console_line(f"    Parlaklık: {self.get_star_luminosity(obj.get('prop', 'M'))} L☉", Colors.YELLOW)
                
            elif obj_type == 'black_hole':
                self.add_console_line(f"    Karadelik Sınıfı: {obj.get('prop', 'Bilinmeyen')}", Colors.YELLOW)
                self.add_console_line(f"    Etki Yarıçapı: {obj.get('R_infl', 'Bilinmeyen')} birim", Colors.YELLOW)
                self.add_console_line(f"    Dışlama Yarıçapı: {obj.get('R_excl', 'Bilinmeyen')} birim", Colors.YELLOW)
                self.add_console_line(f"    Kütle: {self.get_black_hole_mass(obj.get('prop', 'stellar'))} M☉", Colors.YELLOW)
                
            elif obj_type == 'planet':
                self.add_console_line(f"    Gezegen Türü: {obj.get('prop', 'Bilinmeyen')}", Colors.YELLOW)
                self.add_console_line(f"    Yarıçap: {obj.get('radius', 'Bilinmeyen')} birim", Colors.YELLOW)
                self.add_console_line(f"    Yörünge Yarıçapı: {obj.get('orbit_radius', 'Bilinmeyen'):.1f} birim", Colors.YELLOW)
                self.add_console_line(f"    Ana Yıldız ID: {obj.get('star_id', 'Bilinmeyen')}", Colors.YELLOW)
                
                # Kaynak bilgileri
                resources = obj.get('resources', {})
                if resources:
                    self.add_console_line(f"    Kaynaklar:", Colors.CYAN)
                    for resource_type, resource_data in resources.items():
                        if isinstance(resource_data, dict):
                            richness = resource_data.get('richness', 'unknown')
                            score = resource_data.get('score', 0)
                            self.add_console_line(f"      {resource_type}: {richness} (skor: {score:.2f})", Colors.CYAN)
                
            elif obj_type == 'asteroid_belt':
                self.add_console_line(f"    Merkez Yarıçapı: {obj.get('center_radius', 'Bilinmeyen'):.1f} birim", Colors.YELLOW)
                self.add_console_line(f"    Genişlik: {obj.get('width', 'Bilinmeyen'):.1f} birim", Colors.YELLOW)
                self.add_console_line(f"    Fragment Sayısı: {obj.get('fragment_count', 'Bilinmeyen')}", Colors.YELLOW)
                self.add_console_line(f"    Ana Yıldız ID: {obj.get('star_id', 'Bilinmeyen')}", Colors.YELLOW)
                
                # Kaynak havuzu bilgileri
                resource_pool = obj.get('resource_pool', {})
                if resource_pool:
                    self.add_console_line(f"    Kaynak Havuzu:", Colors.CYAN)
                    for resource_type, resource_data in resource_pool.items():
                        if isinstance(resource_data, dict):
                            richness = resource_data.get('richness', 'unknown')
                            score = resource_data.get('score', 0)
                            self.add_console_line(f"      {resource_type}: {richness} (skor: {score:.2f})", Colors.CYAN)
            
            self.add_console_line(f"    Açıklama: {type_info['description']}", Colors.WHITE)
            self.add_console_line("")
        
        # Özet istatistikler
        self.add_console_line("ÖZET İSTATİSTİKLER:", Colors.CYAN)
        
        # Tür bazlı sayım
        type_counts = {}
        for obj in matrix_objects:
            obj_type = obj.get('type', 'unknown')
            type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
        
        for obj_type, count in sorted(type_counts.items()):
            type_info = self.get_celestial_type_info(obj_type)
            percentage = (count / len(matrix_objects) * 100)
            self.add_console_line(f"  {type_info['name']}: {count} adet (%{percentage:.1f})", type_info['color'])
        
        # Mesafe istatistikleri
        if objects_with_distance:
            min_distance = min(distance for _, distance in objects_with_distance)
            max_distance = max(distance for _, distance in objects_with_distance)
            avg_distance = sum(distance for _, distance in objects_with_distance) / len(objects_with_distance)
            
            self.add_console_line("")
            self.add_console_line("MESAFE İSTATİSTİKLERİ:", Colors.CYAN)
            self.add_console_line(f"  En yakın: {min_distance:.1f} nokta", Colors.YELLOW)
            self.add_console_line(f"  En uzak: {max_distance:.1f} nokta", Colors.RED)
            self.add_console_line(f"  Ortalama: {avg_distance:.1f} nokta", Colors.YELLOW)
        
        self.add_console_line("")
        self.add_console_line("=== MATRİS GÖK CİSİMLERİ BİLGİLERİ SONU ===")
    
    def calculate_star_count(self, width: int, height: int, preset_scale: float = 1.0) -> int:
        """Yıldız sayısını hesapla"""
        area = width * height
        S = UniverseConstants.BASE_STAR_DENOMINATOR * preset_scale
        n_stars = max(UniverseConstants.MIN_STAR_COUNT, round(area / S))
        return min(n_stars, UniverseConstants.MAX_STAR_COUNT)
    
    def calculate_minimum_star_spacing(self, width: int, height: int, n_stars: int) -> float:
        """Minimum yıldız-yıldız mesafesini hesapla"""
        area = width * height
        D = math.sqrt(area / n_stars)
        return UniverseConstants.MIN_STAR_SPACING_FACTOR * D
    
    def place_black_holes(self, width: int, height: int, area: int, max_attempts: int = 5000) -> list:
        """Karadelikleri yerleştir"""
        n_bh = max(0, round(area / UniverseConstants.BH_DENOMINATOR))
        black_holes = []
        
        for i in range(n_bh):
            placed = False
            for attempt in range(max_attempts):
                x = random.uniform(0, width)
                y = random.uniform(0, height)
                
                # Karadelik sınıfını seç
                bh_class = random.choices(
                    [BlackHoleClass.STELLAR, BlackHoleClass.INTERMEDIATE, BlackHoleClass.SUPERMASSIVE],
                    weights=[85, 14, 1]
                )[0]
                
                bh = BlackHole(x, y, bh_class, len(black_holes))
                
                # Mevcut karadeliklerle çakışma kontrolü
                collision = False
                for existing_bh in black_holes:
                    distance = math.hypot(x - existing_bh.x, y - existing_bh.y)
                    if distance < (bh.R_excl + existing_bh.R_excl):
                        collision = True
                        break
                
                if not collision:
                    black_holes.append(bh)
                    placed = True
                    break
            
            if not placed:
                # Karadelik yerleştirilemedi, devam et
                continue
        
        return black_holes
    
    def place_stars(self, width: int, height: int, n_stars: int, D_min: float, 
                   black_holes: list, max_attempts_per_star: int = 2000) -> list:
        """Yıldızları yerleştir"""
        stars = []
        
        for i in range(n_stars):
            placed = False
            for attempt in range(max_attempts_per_star):
                x = random.uniform(0, width)
                y = random.uniform(0, height)
                
                # Karadelik dışlama alanı kontrolü
                collision = False
                for bh in black_holes:
                    distance = math.hypot(x - bh.x, y - bh.y)
                    if distance < bh.R_excl:
                        collision = True
                        break
                
                if collision:
                    continue
                
                # Yıldız-yıldız mesafe kontrolü
                for star in stars:
                    distance = math.hypot(x - star.x, y - star.y)
                    if distance < D_min:
                        collision = True
                        break
                
                if collision:
                    continue
                
                # Yıldız türünü seç
                star_type = random.choices(
                    [StarType.M, StarType.K, StarType.G, StarType.HOT],
                    weights=[70, 15, 8, 7]
                )[0]
                
                # Yıldız yarıçapı
                star_radius = {"M": 5, "K": 7, "G": 9, "Hot": 12}[star_type.value]
                
                star = Star(x, y, star_type, star_radius, len(stars))
                stars.append(star)
                placed = True
                break
            
            if not placed:
                # Yıldız yerleştirilemedi, devam et
                continue
        
        return stars
    
    def place_planets_for_star(self, star: Star, width: int, height: int, 
                              existing_objects: list, mean_planets: float = 3.5) -> list:
        """Yıldız için gezegenleri yerleştir"""
        planets = []
        
        # Poisson dağılımı ile gezegen sayısı
        n_planets = max(0, int(random.gauss(mean_planets, 1)))
        n_planets = min(n_planets, 20)  # Maksimum sınır
        
        if n_planets == 0:
            return planets
        
        # İlk yörünge yarıçapı
        a = max(star.radius * 1.5, 8)
        
        for i in range(n_planets):
            # Yörünge yarıçapını artır
            r_ratio = random.uniform(*UniverseConstants.PLANET_ORBIT_RATIO_RANGE)
            a = a * r_ratio
            
            # Yörünge açısı
            theta = random.uniform(0, 2 * math.pi)
            
            # Gezegen konumu
            px = star.x + a * math.cos(theta)
            py = star.y + a * math.sin(theta)
            
            # Sınır kontrolü
            if px < 0 or px >= width or py < 0 or py >= height:
                continue
            
            # Gezegen yarıçapı tahmini
            planet_radius = max(1, int(a ** 0.3))
            
            # Çakışma kontrolü
            collision = False
            for obj in existing_objects:
                distance = math.hypot(px - obj.x, py - obj.y)
                obj_radius = getattr(obj, 'radius', 0)
                if distance < (planet_radius + obj_radius) * 1.2:
                    collision = True
                    break
            
            if collision:
                continue
            
            # Gezegen türünü belirle (mesafeye göre)
            if a < 50:
                planet_type = PlanetType.ROCKY
            elif a > 200:
                planet_type = PlanetType.GAS
            else:
                planet_type = PlanetType.ICE
            
            planet = Planet(px, py, a, theta, planet_type, planet_radius, 
                          star.star_id, len(planets))
            planets.append(planet)
        
        return planets
    
    def create_asteroid_belt(self, star: Star, planets: list, belt_id: int) -> AsteroidBelt:
        """Asteroid kuşağı oluştur"""
        # Kuşak merkez yarıçapı (gezegen yörüngeleri arasında)
        if len(planets) >= 2:
            # İkinci ve üçüncü gezegen arası
            orbit_radii = [p.orbit_radius for p in planets]
            orbit_radii.sort()
            if len(orbit_radii) >= 2:
                a_belt = random.uniform(orbit_radii[1], orbit_radii[2] if len(orbit_radii) > 2 else orbit_radii[1] * 1.5)
            else:
                a_belt = orbit_radii[0] * random.uniform(1.2, 2.5)
        else:
            # Gezegen yoksa varsayılan mesafe
            a_belt = star.radius * random.uniform(3, 8)
        
        # Kuşak genişliği
        width = random.uniform(10, 100)
        
        return AsteroidBelt(star.star_id, a_belt, width, belt_id)
    
    def assign_resources(self, body, body_type: str) -> dict:
        """Gök cismine kaynak ataması yap - Rastgele kaynak seçimi"""
        resources = {}
        
        # Kütle faktörü - radius özelliği varsa kullan, yoksa varsayılan değer
        if hasattr(body, 'radius'):
            mass_factor = max(0.5, body.radius / 5.0)
        else:
            mass_factor = 1.0  # Varsayılan kütle faktörü
        
        # Mesafe faktörü
        distance_factor = 1.0
        if body_type == "asteroid":
            distance_factor = 1.5
        elif hasattr(body, 'prop') and body.prop == "gas":
            distance_factor = 0.2
        
        # Rastgele kaynak sayısı (3-8 arası)
        num_resources = random.randint(3, 8)
        
        # Mevcut kaynak türlerini rastgele seç
        available_resources = list(UniverseConstants.BASE_RESOURCE_ABUNDANCE.keys())
        selected_resources = random.sample(available_resources, min(num_resources, len(available_resources)))
        
        # Seçilen kaynaklar için hesaplama
        for resource_type in selected_resources:
            base_val = UniverseConstants.BASE_RESOURCE_ABUNDANCE[resource_type][body_type]
            score = base_val * mass_factor * distance_factor * random.uniform(0.7, 1.3)
            
            # Zenginlik sınıflandırması
            if score > UniverseConstants.RESOURCE_THRESHOLD_HIGH:
                richness = ResourceRichness.RICH
            elif score > UniverseConstants.RESOURCE_THRESHOLD_LOW:
                richness = ResourceRichness.NORMAL
            else:
                richness = ResourceRichness.POOR
            
            resources[resource_type.value] = {
                "score": score,
                "richness": richness.value
            }
        
        return resources
    
    def get_star_temperature(self, star_type: str) -> str:
        """Yıldız türüne göre sıcaklık döndür"""
        temperatures = {
            'M': '3,000-3,500',
            'K': '3,500-5,000',
            'G': '5,000-6,000',
            'Hot': '6,000-50,000'
        }
        return temperatures.get(star_type, 'Bilinmeyen')
    
    def get_star_luminosity(self, star_type: str) -> str:
        """Yıldız türüne göre parlaklık döndür"""
        luminosities = {
            'M': '0.01-0.1',
            'K': '0.1-0.6',
            'G': '0.6-1.5',
            'Hot': '1.5-100,000'
        }
        return luminosities.get(star_type, 'Bilinmeyen')
    
    def get_black_hole_mass(self, bh_class: str) -> str:
        """Karadelik sınıfına göre kütle döndür"""
        masses = {
            'stellar': '3-20',
            'intermediate': '100-10,000',
            'super': '1,000,000-10,000,000'
        }
        return masses.get(bh_class, 'Bilinmeyen')
    
    def create_advanced_universe(self, name: str, width: int, height: int, preset: str = "normal") -> dict:
        """Gelişmiş evren oluşturma algoritması"""
        self.add_console_line(f"Evren oluşturuluyor: {name} ({width}x{height})")
        self.add_console_line(f"Preset: {preset}")
        
        # Preset ölçekleri
        preset_scales = {
            "sparse": 2.5,
            "normal": 1.0,
            "dense": 0.5,
            "empty": 10.0
        }
        preset_scale = preset_scales.get(preset, 1.0)
        
        area = width * height
        
        # 1. Yıldız sayısını hesapla
        n_stars = self.calculate_star_count(width, height, preset_scale)
        D_min = self.calculate_minimum_star_spacing(width, height, n_stars)
        
        self.add_console_line(f"Yıldız sayısı: {n_stars}")
        self.add_console_line(f"Minimum yıldız mesafesi: {D_min:.1f}")
        
        # 2. Karadelikleri yerleştir (önce)
        self.add_console_line("Karadelikler yerleştiriliyor...")
        black_holes = self.place_black_holes(width, height, area)
        self.add_console_line(f"Yerleştirilen karadelik sayısı: {len(black_holes)}")
        
        # 3. Yıldızları yerleştir
        self.add_console_line("Yıldızlar yerleştiriliyor...")
        stars = self.place_stars(width, height, n_stars, D_min, black_holes)
        self.add_console_line(f"Yerleştirilen yıldız sayısı: {len(stars)}")
        
        # 4. Her yıldıza gezegenler ekle
        all_planets = []
        all_asteroid_belts = []
        existing_objects = black_holes + stars
        
        self.add_console_line("Gezegenler yerleştiriliyor...")
        for star in stars:
            planets = self.place_planets_for_star(star, width, height, existing_objects)
            star.planets = planets
            all_planets.extend(planets)
            
            # Kaynak ataması
            for planet in planets:
                planet.resources = self.assign_resources(planet, "planet")
            
            # Asteroid kuşağı oluştur
            if random.random() < UniverseConstants.ASTEROID_BELT_PROB:
                belt = self.create_asteroid_belt(star, planets, len(all_asteroid_belts))
                belt.resource_pool = self.assign_resources(belt, "asteroid")
                star.asteroid_belts.append(belt)
                all_asteroid_belts.append(belt)
            
            # Mevcut objeleri güncelle
            existing_objects.extend(planets)
        
        self.add_console_line(f"Yerleştirilen gezegen sayısı: {len(all_planets)}")
        self.add_console_line(f"Yerleştirilen asteroid kuşağı sayısı: {len(all_asteroid_belts)}")
        
        # 5. Chunk'lara dağıt
        self.add_console_line("Chunk'lara dağıtılıyor...")
        chunk_objects = {}
        
        # Yıldızları chunk'lara dağıt
        for star in stars:
            chunk_coord = self.chunk_manager.get_chunk_coords(int(star.x), int(star.y))
            if chunk_coord not in chunk_objects:
                chunk_objects[chunk_coord] = []
            
            chunk_objects[chunk_coord].append({
                "x": int(star.x),
                "y": int(star.y),
                "type": "sun",
                "name": f"star_{int(star.x)}_{int(star.y)}",
                "prop": star.star_type.value,
                "radius": star.radius
            })
        
        # Karadelikleri chunk'lara dağıt
        for bh in black_holes:
            chunk_coord = self.chunk_manager.get_chunk_coords(int(bh.x), int(bh.y))
            if chunk_coord not in chunk_objects:
                chunk_objects[chunk_coord] = []
            
            chunk_objects[chunk_coord].append({
                "x": int(bh.x),
                "y": int(bh.y),
                "type": "black_hole",
                "name": f"blackhole_{int(bh.x)}_{int(bh.y)}",
                "prop": bh.bh_class.value,
                "R_infl": bh.R_infl,
                "R_excl": bh.R_excl
            })
        
        # Gezegenleri chunk'lara dağıt
        for planet in all_planets:
            chunk_coord = self.chunk_manager.get_chunk_coords(int(planet.x), int(planet.y))
            if chunk_coord not in chunk_objects:
                chunk_objects[chunk_coord] = []
            
            chunk_objects[chunk_coord].append({
                "x": int(planet.x),
                "y": int(planet.y),
                "type": "planet",
                "name": f"planet_{int(planet.x)}_{int(planet.y)}",
                "prop": planet.planet_type.value,
                "radius": planet.radius,
                "orbit_radius": planet.orbit_radius,
                "star_id": planet.star_id,
                "resources": planet.resources
            })
        
        # Asteroid kuşaklarını chunk'lara dağıt
        for belt in all_asteroid_belts:
            # Kuşak merkezini bul
            star = next((s for s in stars if s.star_id == belt.star_id), None)
            if star:
                chunk_coord = self.chunk_manager.get_chunk_coords(int(star.x), int(star.y))
                if chunk_coord not in chunk_objects:
                    chunk_objects[chunk_coord] = []
                
                chunk_objects[chunk_coord].append({
                    "x": int(star.x),
                    "y": int(star.y),
                    "type": "asteroid_belt",
                    "name": f"belt_{int(star.x)}_{int(star.y)}_{belt.belt_id}",
                    "center_radius": belt.center_radius,
                    "width": belt.width,
                    "fragment_count": belt.fragment_count,
                    "star_id": belt.star_id,
                    "resource_pool": belt.resource_pool
                })
        
        # 6. Chunk dosyalarını oluştur
        universe_dir = f"universes/{name}"
        os.makedirs(universe_dir, exist_ok=True)
        
        # Metadata dosyası
        metadata = {
            "name": name,
            "size": width,
            "chunk_size": 100,
            "created": datetime.now().isoformat(),
            "preset": preset,
            "statistics": {
                "stars": len(stars),
                "black_holes": len(black_holes),
                "planets": len(all_planets),
                "asteroid_belts": len(all_asteroid_belts)
            }
        }
        
        with open(f"{universe_dir}/metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Chunk dosyalarını oluştur
        for chunk_coord, objects in chunk_objects.items():
            chunk_file = self.chunk_manager.get_chunk_file_path(
                chunk_coord[0], chunk_coord[1], name
            )
            with open(chunk_file, 'w', encoding='utf-8') as f:
                json.dump(objects, f, indent=2, ensure_ascii=False)
        
        self.add_console_line(f"Evren oluşturuldu: {name}")
        self.add_console_line(f"Toplam chunk sayısı: {len(chunk_objects)}")
        
        return {
            "stars": stars,
            "black_holes": black_holes,
            "planets": all_planets,
            "asteroid_belts": all_asteroid_belts,
            "chunk_objects": chunk_objects
        }
    
    def get_celestial_type_info(self, obj_type):
        """Gök cismi türüne göre bilgi döndür"""
        type_info = {
            'sun': {
                'name': 'Güneş',
                'color': Colors.YELLOW,
                'description': 'Yıldız - Güçlü enerji kaynağı, yaklaşmayın!'
            },
            'black_hole': {
                'name': 'Kara Delik',
                'color': Colors.MAGENTA,
                'description': 'Tehlikeli - Çok güçlü çekim kuvveti, uzak durun!'
            },
            'asteroid_belt': {
                'name': 'Asteroid Kuşağı',
                'color': Colors.GRAY,
                'description': 'Orta tehlikeli - Küçük kayalar, dikkatli geçin!'
            },
            'planet': {
                'name': 'Gezegen',
                'color': Colors.BLUE,
                'description': 'Güvenli - Keşfedilebilir, iniş yapılabilir!'
            },
            'comet': {
                'name': 'Kuyruklu Yıldız',
                'color': Colors.CYAN,
                'description': 'Hareketli - Hızlı hareket eder, takip edilebilir!'
            }
        }
        
        return type_info.get(obj_type, {
            'name': 'Bilinmeyen',
            'color': Colors.WHITE,
            'description': 'Tanımlanmamış gök cismi türü'
        })
    
    def save_map(self, map_name, description=""):
        """Mevcut chunk'ı map olarak kaydet"""
        if not self.ship:
            self.add_console_line("HATA: Gemi bulunamadı!", Colors.RED)
            return
        
        # Session kontrolü
        if not hasattr(self, 'current_session_name') or not self.current_session_name:
            self.add_console_line("ERROR: No active session!", Colors.RED)
            return
        
        # Session maps klasörünü oluştur
        maps_dir = f"sessions/{self.current_universe_name}/{self.current_session_name}/maps"
        os.makedirs(maps_dir, exist_ok=True)
        
        # Map dosya yolu
        map_file = f"{maps_dir}/{map_name}.json"
        
        # Aynı isimde map var mı kontrol et
        if os.path.exists(map_file):
            self.add_console_line(f"HATA: '{map_name}' isimli map zaten mevcut!", Colors.RED)
            return
        
        # Mevcut matrix alanındaki gök cisimlerini yükle
        matrix_objects = self.chunk_manager.get_objects_in_area(
            self.matrix_start_x, self.matrix_start_y,
            self.matrix_start_x + self.matrix_size - 1,
            self.matrix_start_y + self.matrix_size - 1,
            self.current_universe_name
        )
        
        # Map verisini oluştur
        map_data = {
            "name": map_name,
            "description": description,
            "universe_name": self.current_universe_name,
            "created": datetime.now().isoformat(),
            "matrix_data": {
                "center_x": self.ship.x,
                "center_y": self.ship.y,
                "matrix_start_x": self.matrix_start_x,
                "matrix_start_y": self.matrix_start_y,
                "matrix_size": self.matrix_size,
                "celestial_objects": matrix_objects
            }
        }
        
        # Map dosyasını kaydet
        try:
            with open(map_file, 'w', encoding='utf-8') as f:
                json.dump(map_data, f, indent=2, ensure_ascii=False)
            
            self.add_console_line(f"Map kaydedildi: {map_name}")
            self.add_console_line(f"Konum: {maps_dir}/{map_name}.json")
            self.add_console_line(f"Açıklama: {description if description else 'Açıklama yok'}")
            self.add_console_line(f"Gök cismi sayısı: {len(matrix_objects)}")
            
        except Exception as e:
            self.add_console_line(f"HATA: Map kaydedilemedi: {e}", Colors.RED)
    
    def delete_map(self, map_name):
        """Map dosyasını sil"""
        if not hasattr(self, 'current_session_name') or not self.current_session_name:
            self.add_console_line("ERROR: No active session!", Colors.RED)
            return
        
        maps_dir = f"sessions/{self.current_universe_name}/{self.current_session_name}/maps"
        map_file = f"{maps_dir}/{map_name}.json"
        
        if not os.path.exists(map_file):
            self.add_console_line(f"HATA: '{map_name}' isimli map bulunamadı!", Colors.RED)
            return
        
        try:
            os.remove(map_file)
            self.add_console_line(f"Map silindi: {map_name}")
        except Exception as e:
            self.add_console_line(f"HATA: Map silinemedi: {e}", Colors.RED)
    
    def list_maps(self):
        """Kayıtlı map'leri listele"""
        if not hasattr(self, 'current_session_name') or not self.current_session_name:
            self.add_console_line("ERROR: No active session!", Colors.RED)
            return
        
        maps_dir = f"sessions/{self.current_universe_name}/{self.current_session_name}/maps"
        
        if not os.path.exists(maps_dir):
            self.add_console_line("Kayıtlı map bulunamadı.")
            return
        
        map_files = [f for f in os.listdir(maps_dir) if f.endswith('.json')]
        
        if not map_files:
            self.add_console_line("Kayıtlı map bulunamadı.")
            return
        
        self.add_console_line("=== KAYITLI MAP'LER ===")
        
        for i, map_file in enumerate(sorted(map_files), 1):
            map_name = map_file.replace('.json', '')
            map_path = os.path.join(maps_dir, map_file)
            
            try:
                with open(map_path, 'r', encoding='utf-8') as f:
                    map_data = json.load(f)
                
                description = map_data.get('description', 'Açıklama yok')
                created = map_data.get('created', 'Bilinmiyor')
                obj_count = len(map_data.get('matrix_data', {}).get('celestial_objects', []))
                
                self.add_console_line(f"{i:2d}. {map_name}")
                self.add_console_line(f"    Açıklama: {description}")
                self.add_console_line(f"    Oluşturulma: {created}")
                self.add_console_line(f"    Gök cismi sayısı: {obj_count}")
                self.add_console_line("")
                
            except Exception as e:
                self.add_console_line(f"{i:2d}. {map_name} (HATA: {e})")
        
        self.add_console_line("=== MAP LİSTESİ SONU ===")
    
    def load_map(self, map_name):
        """Map'i matrix olarak yükle"""
        if not hasattr(self, 'current_session_name') or not self.current_session_name:
            self.add_console_line("ERROR: No active session!", Colors.RED)
            return
        
        maps_dir = f"sessions/{self.current_universe_name}/{self.current_session_name}/maps"
        map_file = f"{maps_dir}/{map_name}.json"
        
        if not os.path.exists(map_file):
            self.add_console_line(f"HATA: '{map_name}' isimli map bulunamadı!", Colors.RED)
            return
        
        try:
            with open(map_file, 'r', encoding='utf-8') as f:
                map_data = json.load(f)
            
            matrix_data = map_data.get('matrix_data', {})
            
            # Matrix koordinatlarını güncelle
            self.ship.x = matrix_data.get('center_x', self.ship.x)
            self.ship.y = matrix_data.get('center_y', self.ship.y)
            self.matrix_start_x = matrix_data.get('matrix_start_x', self.matrix_start_x)
            self.matrix_start_y = matrix_data.get('matrix_start_y', self.matrix_start_y)
            self.matrix_size = matrix_data.get('matrix_size', self.matrix_size)
            
            # Matrix merkezini güncelle
            self.last_matrix_center_x = self.ship.x
            self.last_matrix_center_y = self.ship.y
            
            # Chunk'ları güncelle
            self.chunk_manager.unload_distant_chunks(self.ship.x, self.ship.y)
            
            # Motoru durdur (güvenlik)
            self.ship.is_moving = False
            self.engine_on = False
            
            # Başarı mesajı
            self.add_console_line(f"Map yüklendi: {map_name}")
            self.add_console_line(f"Gemi konumu: ({self.ship.x}, {self.ship.y})")
            self.add_console_line(f"Matrix alanı: ({self.matrix_start_x}, {self.matrix_start_y}) - ({self.matrix_start_x + self.matrix_size - 1}, {self.matrix_start_y + self.matrix_size - 1})")
            
            # Matrix görüntüye bilgi ekle
            self.add_matrix_line(f"MAP YÜKLENDİ: {map_name}", Colors.MAGENTA)
            self.add_matrix_line(f"GEMİ KONUMU: ({self.ship.x}, {self.ship.y})", Colors.CYAN)
            self.add_matrix_line(f"MATRİS ALANI: ({self.matrix_start_x}, {self.matrix_start_y}) - ({self.matrix_start_x + self.matrix_size - 1}, {self.matrix_start_y + self.matrix_size - 1})", Colors.CYAN)
            
        except Exception as e:
            self.add_console_line(f"HATA: Map yüklenemedi: {e}", Colors.RED)
    
    def show_help(self, command=None):
        """Yardım ekranını göster"""
        if command:
            # Belirli komut için yardım göster
            self.show_command_help(command)
            return
        
        self.add_console_line("=== ORBIT KOMUTLARI ===", Colors.CYAN)
        self.add_console_line("")
        
        # BAŞLATMA
        self.add_console_line("universe (u)", Colors.YELLOW)
        self.add_console_line("  --name (-n) <isim>     : Evren adı (zorunlu)", Colors.WHITE)
        self.add_console_line("  --size <boyut>         : Evren boyutu (200-2000)", Colors.WHITE)
        self.add_console_line("  --session (-s) <name>  : Session adı (varsayılan: evren adı)", Colors.WHITE)
        self.add_console_line("  --create (-c)          : Zorla yeni evren oluştur", Colors.WHITE)
        self.add_console_line("")
        
        # GEMİ KONTROLÜ
        self.add_console_line("engine (e)", Colors.YELLOW)
        self.add_console_line("  on/off                 : Motor aç/kapat", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("rotate (r)", Colors.YELLOW)
        self.add_console_line("  right/left/up/down     : Yön değiştir", Colors.WHITE)
        self.add_console_line("  r/l/u/d                : Kısa yön komutları", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("turnback", Colors.YELLOW)
        self.add_console_line("  Geri dön", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("speed (s)", Colors.YELLOW)
        self.add_console_line("  <saniye/nokta>         : Hız ayarla (0.1-60)", Colors.WHITE)
        self.add_console_line("  (parametresiz)         : Mevcut hız analizi göster", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("+ (hız artır)", Colors.YELLOW)
        self.add_console_line("  <yüzde>                : Hızı yüzde olarak artır", Colors.WHITE)
        self.add_console_line("  Örnek: + 10 (hızı %10 artır)", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("- (hız azalt/dur)", Colors.YELLOW)
        self.add_console_line("  <yüzde>                : Hızı yüzde olarak azalt", Colors.WHITE)
        self.add_console_line("  0                      : Motoru durdur", Colors.WHITE)
        self.add_console_line("  Örnek: - 10 (hızı %10 azalt), - 0 (dur)", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("max", Colors.YELLOW)
        self.add_console_line("  Hızı maksimuma ayarla (en hızlı)", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("refresh (r)", Colors.YELLOW)
        self.add_console_line("  Güncelleme süresi bilgisi", Colors.WHITE)
        self.add_console_line("")
        
        # TELEPORTASYON
        self.add_console_line("tp (teleportation)", Colors.YELLOW)
        self.add_console_line("  <x:y>                  : Koordinata ışınlan", Colors.WHITE)
        self.add_console_line("  --cat <gokcismi_adı>   : Katalog nesnesine ışınlan", Colors.WHITE)
        self.add_console_line("")
        
        # TARAMA
        self.add_console_line("scan", Colors.YELLOW)
        self.add_console_line("  <x:y>                  : Koordinat tara", Colors.WHITE)
        self.add_console_line("")
        
        # KATALOG YÖNETİMİ
        self.add_console_line("cat", Colors.YELLOW)
        self.add_console_line("  --save (-s) <name>     : Gök cismini kataloga kaydet", Colors.WHITE)
        self.add_console_line("  --list (-ls)           : Katalogu listele", Colors.WHITE)
        self.add_console_line("  --all (-a)             : Matrix'teki tüm gök cisimlerini kaydet", Colors.WHITE)
        self.add_console_line("  --resume (-r)          : Katalog istatistiklerini göster", Colors.WHITE)
        self.add_console_line("")
        
        # MAP YÖNETİMİ
        self.add_console_line("map", Colors.YELLOW)
        self.add_console_line("  --save <isim>          : Mevcut chunk'ı map olarak kaydet", Colors.WHITE)
        self.add_console_line("  --desc <açıklama>      : Map açıklaması", Colors.WHITE)
        self.add_console_line("  --delete (-d) <isim>   : Map dosyasını sil", Colors.WHITE)
        self.add_console_line("  --list (-ls)           : Kayıtlı map'leri listele", Colors.WHITE)
        self.add_console_line("  --load (-l) <isim>     : Map'i matrix olarak yükle", Colors.WHITE)
        self.add_console_line("")
        
        # BİLGİ
        self.add_console_line("info (i)", Colors.YELLOW)
        self.add_console_line("  universe (u)           : Evren bilgilerini göster", Colors.WHITE)
        self.add_console_line("  objects (o)            : Matris gök cisimleri bilgilerini göster", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("list (ls)", Colors.YELLOW)
        self.add_console_line("  Mevcut evrenleri listele", Colors.WHITE)
        self.add_console_line("")
        
        # KONSOL
        self.add_console_line("clear (cls)", Colors.YELLOW)
        self.add_console_line("  Konsolu temizle", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("↑ (up)", Colors.YELLOW)
        self.add_console_line("  Konsol scroll yukarı", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("↓ (down)", Colors.YELLOW)
        self.add_console_line("  Konsol scroll aşağı", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("scrollinfo", Colors.YELLOW)
        self.add_console_line("  Scroll debug bilgisi", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("grid", Colors.YELLOW)
        self.add_console_line("  on/off                 : Grid çizgilerini aç/kapat", Colors.WHITE)
        self.add_console_line("  (parametresiz)         : Grid durumunu göster", Colors.WHITE)
        self.add_console_line("")
        
        # DİL
        self.add_console_line("lang", Colors.YELLOW)
        self.add_console_line("  (parametresiz)         : Mevcut dilleri listele", Colors.WHITE)
        self.add_console_line("  <dil_kodu>             : Dil değiştir (en, tr, fr, de, es, ja)", Colors.WHITE)
        self.add_console_line("")
        
        # TEST VE DEBUG
        self.add_console_line("test", Colors.YELLOW)
        self.add_console_line("  Test komutu", Colors.WHITE)
        self.add_console_line("")
        
        # DİĞER
        self.add_console_line("help", Colors.YELLOW)
        self.add_console_line("  Bu yardım", Colors.WHITE)
        self.add_console_line("")
        self.add_console_line("quit (exit)", Colors.YELLOW)
        self.add_console_line("  Çıkış", Colors.WHITE)
        self.add_console_line("")
        
        # DEPRECATED
        self.add_console_line("go", Colors.YELLOW)
        self.add_console_line("  DEPRECATED             : Kullanımdan kaldırıldı (universe kullanın)", Colors.WHITE)
        self.add_console_line("")
    
    def show_command_help(self, command):
        """Belirli komut için yardım göster"""
        command = command.lower()
        
        if command in ["universe", "u"]:
            self.add_console_line("=== UNIVERSE (U) KOMUTU ===", Colors.CYAN)
            self.add_console_line("")
            self.add_console_line("universe (u)", Colors.YELLOW)
            self.add_console_line("  --name (-n) <isim>     : Evren adı (zorunlu)", Colors.WHITE)
            self.add_console_line("  --size <boyut>         : Evren boyutu (200-2000)", Colors.WHITE)
            self.add_console_line("  --session (-s) <name>  : Session adı (varsayılan: evren adı)", Colors.WHITE)
            self.add_console_line("  --create (-c)          : Zorla yeni evren oluştur", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("Örnekler:", Colors.CYAN)
            self.add_console_line("  u -n myuniverse -s 500", Colors.WHITE)
            self.add_console_line("  universe --name test --create", Colors.WHITE)
            
        elif command in ["cat"]:
            self.add_console_line("=== CAT KOMUTU ===", Colors.CYAN)
            self.add_console_line("")
            self.add_console_line("cat", Colors.YELLOW)
            self.add_console_line("  --save <name>          : Gök cismini kataloga kaydet", Colors.WHITE)
            self.add_console_line("  --list                 : Katalogu listele", Colors.WHITE)
            self.add_console_line("  --all                  : Matrix'teki tüm gök cisimlerini kaydet", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("Örnekler:", Colors.CYAN)
            self.add_console_line("  cat --save planet_123", Colors.WHITE)
            self.add_console_line("  cat --list", Colors.WHITE)
            self.add_console_line("  cat --all", Colors.WHITE)
            
        elif command in ["tp", "teleportation"]:
            self.add_console_line("=== TP (TELEPORTATION) KOMUTU ===", Colors.CYAN)
            self.add_console_line("")
            self.add_console_line("tp (teleportation)", Colors.YELLOW)
            self.add_console_line("  <x:y>                  : Koordinata ışınlan", Colors.WHITE)
            self.add_console_line("  --cat <gokcismi_adı>   : Katalog nesnesine ışınlan", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("Örnekler:", Colors.CYAN)
            self.add_console_line("  tp 100:200", Colors.WHITE)
            self.add_console_line("  tp --cat planet_123", Colors.WHITE)
            
        elif command in ["info", "i"]:
            self.add_console_line("=== INFO (I) KOMUTU ===", Colors.CYAN)
            self.add_console_line("")
            self.add_console_line("info (i)", Colors.YELLOW)
            self.add_console_line("  universe (u)           : Evren bilgilerini göster", Colors.WHITE)
            self.add_console_line("  objects (o)            : Matris gök cisimleri bilgilerini göster", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("Örnekler:", Colors.CYAN)
            self.add_console_line("  info universe", Colors.WHITE)
            self.add_console_line("  i o", Colors.WHITE)
            
        elif command in ["map"]:
            self.add_console_line("=== MAP KOMUTU ===", Colors.CYAN)
            self.add_console_line("")
            self.add_console_line("map", Colors.YELLOW)
            self.add_console_line("  --save <isim>          : Mevcut chunk'ı map olarak kaydet", Colors.WHITE)
            self.add_console_line("  --desc <açıklama>      : Map açıklaması", Colors.WHITE)
            self.add_console_line("  --delete (-d) <isim>   : Map dosyasını sil", Colors.WHITE)
            self.add_console_line("  --list (-ls)           : Kayıtlı map'leri listele", Colors.WHITE)
            self.add_console_line("  --load (-l) <isim>     : Map'i matrix olarak yükle", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("Örnekler:", Colors.CYAN)
            self.add_console_line("  map --save mymap --desc 'Güzel bir bölge'", Colors.WHITE)
            self.add_console_line("  map --list", Colors.WHITE)
            self.add_console_line("  map --load mymap", Colors.WHITE)
            
        elif command in ["engine", "e"]:
            self.add_console_line("=== ENGINE (E) KOMUTU ===", Colors.CYAN)
            self.add_console_line("")
            self.add_console_line("engine (e)", Colors.YELLOW)
            self.add_console_line("  on/off                 : Motor aç/kapat", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("Örnekler:", Colors.CYAN)
            self.add_console_line("  engine on", Colors.WHITE)
            self.add_console_line("  e off", Colors.WHITE)
            
        elif command in ["rotate", "r"]:
            self.add_console_line("=== ROTATE (R) KOMUTU ===", Colors.CYAN)
            self.add_console_line("")
            self.add_console_line("rotate (r)", Colors.YELLOW)
            self.add_console_line("  right/left/up/down     : Yön değiştir", Colors.WHITE)
            self.add_console_line("  r/l/u/d                : Kısa yön komutları", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("Örnekler:", Colors.CYAN)
            self.add_console_line("  rotate right", Colors.WHITE)
            self.add_console_line("  r u", Colors.WHITE)
            
        elif command in ["speed", "s"]:
            self.add_console_line("=== SPEED (S) KOMUTU ===", Colors.CYAN)
            self.add_console_line("")
            self.add_console_line("speed (s)", Colors.YELLOW)
            self.add_console_line("  <saniye/nokta>         : Hız ayarla (0.1-60)", Colors.WHITE)
            self.add_console_line("  (parametresiz)         : Mevcut hız analizi göster", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("Örnekler:", Colors.CYAN)
            self.add_console_line("  speed 2.5", Colors.WHITE)
            self.add_console_line("  s", Colors.WHITE)
            
        elif command in ["lang"]:
            self.add_console_line("=== LANG KOMUTU ===", Colors.CYAN)
            self.add_console_line("")
            self.add_console_line("lang", Colors.YELLOW)
            self.add_console_line("  (parametresiz)         : Mevcut dilleri listele", Colors.WHITE)
            self.add_console_line("  <dil_kodu>             : Dil değiştir (en, tr, fr, de, es, ja)", Colors.WHITE)
            self.add_console_line("")
            self.add_console_line("Örnekler:", Colors.CYAN)
            self.add_console_line("  lang", Colors.WHITE)
            self.add_console_line("  lang tr", Colors.WHITE)
            
        else:
            self.add_console_line(f"Bilinmeyen komut: {command}", Colors.RED)
            self.add_console_line("Mevcut komutlar: universe, cat, tp, info, map, engine, rotate, speed, lang", Colors.WHITE)
        
        self.add_console_line("NOT: Teleportasyon enerjinin %5'ini tüketir!", Colors.YELLOW)
    
    def load_universe(self, file_path: str):
        """Mevcut evreni yükle - Chunk-based ve eski format destekler"""
        try:
            # Chunk-based format kontrolü
            if file_path.endswith('.json') and os.path.exists(file_path.replace('.json', '/metadata.json')):
                # Chunk-based format
                metadata_file = file_path.replace('.json', '/metadata.json')
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                self.universe_size = metadata['size']
                self.celestial_objects = []  # Chunk-based'de boş bırakıyoruz, chunk'lar gerektiğinde yüklenir
                
                self.universe_created = True
                self.add_console_line(f"Chunk-based evren yüklendi: {file_path}")
                self.add_console_line(f"Boyut: {self.universe_size}x{self.universe_size}")
                self.add_console_line(f"Density: {metadata.get('density', 'normal')}")
                
            else:
                # Eski format (tek dosya)
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
                self.add_console_line(f"Eski format evren yüklendi: {file_path}")
                self.add_console_line(f"Boyut: {self.universe_size}x{self.universe_size}")
                self.add_console_line(f"Toplam {len(self.celestial_objects)} gök cismi yüklendi")
                
        except Exception as e:
            self.add_console_line(f"HATA: Evren yüklenemedi: {str(e)}", Colors.RED)
    
    def list_universes(self):
        """Universes klasöründeki evrenleri listele - hem chunk-based hem eski format"""
        try:
            # universes klasörünü oluştur
            os.makedirs("universes", exist_ok=True)
            
            # Evrenleri bul - hem chunk-based hem eski format
            universe_files = []
            chunk_dirs = []
            
            for item in os.listdir("universes"):
                item_path = os.path.join("universes", item)
                if os.path.isfile(item_path) and item.endswith('.json'):
                    # Eski format
                    universe_files.append(item)
                elif os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'metadata.json')):
                    # Chunk-based format
                    chunk_dirs.append(item)
            
            if not universe_files and not chunk_dirs:
                self.add_console_line("Universes klasöründe evren bulunamadı")
                return
            
            # Dosyaları listele - Sadece konsola yaz
            self.add_console_line("MEVCUT EVRENLER:", Colors.YELLOW)
            
            # Eski format evrenler
            for i, file in enumerate(sorted(universe_files), 1):
                name = file.replace('.json', '')
                self.add_console_line(f"{i}. {name} (Eski format)")
            
            # Chunk-based evrenler
            for i, file in enumerate(sorted(chunk_dirs), len(universe_files) + 1):
                self.add_console_line(f"{i}. {file} (Chunk-based)")
            
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
                [CelestialType.SUN, CelestialType.BLACK_HOLE, CelestialType.ASTEROID_BELT, 
                 CelestialType.PLANET, CelestialType.COMET],
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
        """Görevi başlat - Chunk-based ve eski format destekler"""
        # Chunk-based evrenlerde celestial_objects boş olabilir, bu normal
        # if not self.celestial_objects:  # Bu kontrolü kaldırdık
        #     return
        
        # Rastgele pozisyon
        x = random.randint(0, self.universe_size - 1)
        y = random.randint(0, self.universe_size - 1)
        
        # Gemi oluştur
        self.ship = Ship(x, y, self.universe_size)
        self.ship.is_moving = False
        self.ship.mission_start_time = datetime.now()
        self.mission_started = True
        
        # 24 saatte tüm noktalara ulaşmak için gereken hızı hesapla ve ayarla
        self.calculate_24h_speed()
        if hasattr(self, 'required_24h_speed') and self.required_24h_speed > 0:
            self.ship.speed = self.required_24h_speed
        else:
            self.ship.speed = max_speed
        
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
        self.add_matrix_line(f"Hız: {self.ship.speed:.2f} sn/nokta")
        self.add_matrix_line(f"Güncelleme: {self.ship.speed:.2f} saniyede bir")
        self.add_matrix_line(f"Matris merkezi: ({x}, {y}) - Her nokta değişikliğinde yenilenecek", Colors.CYAN)
    
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
        # Console initialization
        if not hasattr(self, 'console_lines'):
            self.console_lines = []
            self.max_console_lines = 50
            self.console_scroll = 0
        
        # UI layout initialization
        if not hasattr(self, 'left_width'):
            self.left_width = int(self.screen_width * 0.3)
            self.right_width = int(self.screen_width * 0.3)
            self.middle_width = self.screen_width - self.left_width - self.right_width
            self.center_width = self.middle_width
            self.console_height = self.screen_height  # Tam yükseklik (__init__ ile tutarlı)
        
        # Game state initialization
        if not hasattr(self, 'mission_started'):
            self.mission_started = False
        
        # Pygame clock initialization
        if not hasattr(self, 'clock'):
            self.clock = pygame.time.Clock()
        
        # Matrix initialization
        if not hasattr(self, 'matrix_size'):
            self.matrix_size = 20
        
        # Matrix initialization
        if not hasattr(self, 'matrix_objects'):
            self.matrix_objects = []
        
        if not hasattr(self, 'matrix_width'):
            self.matrix_width = self.center_width
        
        if not hasattr(self, 'matrix_height'):
            self.matrix_height = self.screen_height - 50
        
        if not hasattr(self, 'matrix_lines'):
            self.matrix_lines = []
            self.max_matrix_lines = 20
        
        if not hasattr(self, 'matrix_start_x'):
            self.matrix_start_x = 0
        
        if not hasattr(self, 'matrix_start_y'):
            self.matrix_start_y = 0
        
        if not hasattr(self, 'matrix_render_threshold'):
            self.matrix_render_threshold = self.calculate_render_threshold()
        
        if not hasattr(self, 'last_matrix_update'):
            self.last_matrix_update = datetime.now()
        
        if not hasattr(self, 'last_matrix_center_x'):
            self.last_matrix_center_x = 0
        
        if not hasattr(self, 'last_matrix_center_y'):
            self.last_matrix_center_y = 0
        
        if not hasattr(self, 'direction_indicator_x'):
            self.direction_indicator_x = 0
        
        if not hasattr(self, 'direction_indicator_y'):
            self.direction_indicator_y = 0
        
        if not hasattr(self, 'direction_initialized'):
            self.direction_initialized = False
        
        if not hasattr(self, 'direction_line_passed'):
            self.direction_line_passed = False
        
        # Engine and movement initialization
        if not hasattr(self, 'engine_on'):
            self.engine_on = False
        
        # Radar alarm system initialization
        if not hasattr(self, 'radar_alarm'):
            self.radar_alarm = False
        
        if not hasattr(self, 'alarm_blink_timer'):
            self.alarm_blink_timer = 0
        
        if not hasattr(self, 'coord_blink_timer'):
            self.coord_blink_timer = 0
        
        # Grid system initialization
        if not hasattr(self, 'grid_enabled'):
            self.grid_enabled = False
        
        # Movement calculation initialization
        if not hasattr(self, 'points_per_minute'):
            self.points_per_minute = 10
        
        if not hasattr(self, 'points_per_10_minutes'):
            self.points_per_10_minutes = 100
        
        if not hasattr(self, 'seconds_per_point'):
            self.seconds_per_point = 6
        
        if not hasattr(self, 'speed_factor'):
            self.speed_factor = 1.0
        
        # Command output initialization
        if not hasattr(self, 'command_output_lines'):
            self.command_output_lines = []
        
        if not hasattr(self, 'max_command_output_lines'):
            self.max_command_output_lines = 15
        
        # Startup messages - Linux console
        self.add_console_line("ORBIT", Colors.CYAN)
        self.add_console_line("by Altay Kireççi", Colors.WHITE)
        self.add_console_line("READY", Colors.CYAN)
        
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
                    elif event.key == pygame.K_DOWN:
                        # Aşağı ok tuşu - konsol scroll
                        max_scroll = max(0, len(self.console_lines) - self.max_console_lines)
                        if self.console_scroll < max_scroll:
                            self.console_scroll += 1
                    elif event.key == pygame.K_UP:
                        # Yukarı ok tuşu - konsol scroll
                        if self.console_scroll > 0:
                            self.console_scroll -= 1
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
            self.print_probe_panel()        # Sağ alt - Catalogs
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
