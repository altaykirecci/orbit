import json
import os

class LocaleManager:
    def __init__(self, default_language="en"):
        self.current_language = default_language
        self.translations = {}
        self.load_language(default_language)
    
    def get_locale_path(self, language_code):
        """Get locale file path"""
        # Önce mevcut dizinde ara
        current_dir = os.getcwd()
        locale_paths = [
            os.path.join(current_dir, "loc", f"{language_code}.json"),
            os.path.join(current_dir, "orbit", "loc", f"{language_code}.json"),
            os.path.join(os.path.dirname(__file__), "..", "loc", f"{language_code}.json"),
        ]
        
        for path in locale_paths:
            if os.path.exists(path):
                return path
        
        # Bulunamazsa None döndür
        return None
    
    def load_language(self, language_code):
        """Load language file"""
        try:
            locale_path = self.get_locale_path(language_code)
            if locale_path:
                with open(locale_path, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
                    self.current_language = language_code
            else:
                print(f"Language file not found: {language_code}.json")
                # Fallback to English
                if language_code != "en":
                    self.load_language("en")
        except Exception as e:
            print(f"Error loading language {language_code}: {e}")
            if language_code != "en":
                self.load_language("en")
    
    def get(self, key, **kwargs):
        """Get translated string with optional formatting"""
        try:
            # Navigate through nested keys (e.g., "help.title")
            keys = key.split('.')
            value = self.translations
            for k in keys:
                value = value[k]
            
            # Format string if kwargs provided
            if kwargs:
                return value.format(**kwargs)
            return value
        except (KeyError, TypeError):
            # Return key if translation not found
            return key
    
    def set_language(self, language_code):
        """Change language"""
        self.load_language(language_code)
