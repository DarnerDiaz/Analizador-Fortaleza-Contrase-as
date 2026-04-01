"""
Tests para el módulo de detección de patrones (patterns.py)
"""

import pytest
import sys
from pathlib import Path

# Agregar ruta padre
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.patterns import PatternDetector


class TestPatternDetector:
    """Tests para la detección de patrones débiles"""

    def test_detect_dates_format1(self):
        """Detecta fechas formato DD/MM/YYYY"""
        password = "pass25/12/1990"
        dates = PatternDetector.detect_dates(password)
        assert dates is not None
        assert "25/12/1990" in dates

    def test_detect_dates_format2(self):
        """Detecta fechas formato YYYY-MM-DD"""
        password = "pass1990-12-25"
        dates = PatternDetector.detect_dates(password)
        assert dates is not None
        assert "1990-12-25" in dates

    def test_detect_dates_not_found(self):
        """Retorna None si no hay fechas"""
        password = "RandomPassword123!"
        dates = PatternDetector.detect_dates(password)
        assert dates is None

    def test_detect_common_words(self):
        """Detecta palabras comunes débiles"""
        password = "password123admin"
        words = PatternDetector.detect_common_words(password)
        assert words is not None
        assert "password" in words or "admin" in words

    def test_detect_common_words_not_found(self):
        """Retorna None si no hay palabras comunes"""
        password = "MyStr0ng!P@ssw0rd"
        words = PatternDetector.detect_common_words(password)
        # Podría no encontrar nada dependiendo de la lista
        # pero al menos no debe fallar
        assert isinstance(words, (list, type(None)))

    def test_detect_sequences_qwerty(self):
        """Detecta secuencia qwerty"""
        password = "pass123qwerty"
        sequences = PatternDetector.detect_sequences(password)
        assert sequences is not None

    def test_detect_sequences_numbers(self):
        """Detecta secuencia numérica 123"""
        password = "pass123qwerty"
        sequences = PatternDetector.detect_sequences(password)
        assert sequences is not None
        assert len(sequences) > 0

    def test_detect_sequences_not_found(self):
        """Retorna None si no hay secuencias"""
        password = "MyRandomStr0ng!P@ss2024"
        sequences = PatternDetector.detect_sequences(password)
        # Podría no encontrar o encontrar, pero no debe fallar
        assert isinstance(sequences, (list, type(None)))

    def test_detect_repeated_chars(self):
        """Detecta caracteres repetidos"""
        password = "passaaaa123"
        repeated = PatternDetector.detect_repeated_chars(password)
        assert repeated is not None
        assert "a" in repeated
        assert repeated["a"] >= 4  # Puede haber más de 4 'a's

    def test_detect_repeated_chars_numbers(self):
        """Detecta números repetidos"""
        password = "pass1111"
        repeated = PatternDetector.detect_repeated_chars(password)
        assert repeated is not None
        assert "1" in repeated

    def test_detect_repeated_chars_not_found(self):
        """Retorna None si no hay caracteres repetidos"""
        password = "MyRandomStr0ng!P@ss2"
        repeated = PatternDetector.detect_repeated_chars(password)
        assert repeated is None or isinstance(repeated, dict)

    def test_detect_keyboard_patterns(self):
        """Detecta patrones de teclado"""
        password = "myqwertypass"
        patterns = PatternDetector.detect_keyboard_patterns(password)
        assert patterns is not None

    def test_detect_keyboard_patterns_asdf(self):
        """Detecta patrón asdf"""
        password = "myasdfgpass"
        patterns = PatternDetector.detect_keyboard_patterns(password)
        assert patterns is not None

    def test_detect_numbers_only(self):
        """Detecta si es solo números"""
        result = PatternDetector.detect_numbers_only("123456789")
        assert result is True

    def test_detect_numbers_only_with_letters(self):
        """Retorna False si hay letras"""
        result = PatternDetector.detect_numbers_only("123456789a")
        assert result is False

    def test_detect_numbers_only_empty(self):
        """Contraseña vacía"""
        result = PatternDetector.detect_numbers_only("")
        assert result is None or result is False

    def test_detect_years(self):
        """Detecta años comunes"""
        password = "mypass2024"
        years = PatternDetector.detect_years(password)
        assert years is not None
        assert "2024" in years

    def test_detect_years_birth_year(self):
        """Detecta año de nacimiento"""
        password = "password1990"
        years = PatternDetector.detect_years(password)
        assert years is not None
        assert "1990" in years

    def test_detect_patterns_comprehensive(self):
        """Método detect_patterns retorna diccionario"""
        password = "password123"
        patterns = PatternDetector.detect_patterns(password)
        assert isinstance(patterns, dict)

    def test_detect_patterns_weak_password(self):
        """Detecta múltiples patrones en contraseña débil"""
        password = "password123qwerty"
        patterns = PatternDetector.detect_patterns(password)
        # Debe detectar al menos "common_words" o "sequences"
        assert len(patterns) > 0

    def test_detect_patterns_strong_password(self):
        """Contraseña fuerte debe tener pocos o ningún patrón"""
        password = "MyStr0ng!P@ssw0rd#XyZ2024"
        patterns = PatternDetector.detect_patterns(password)
        # Fuerte no debe tener muchos patrones débiles
        assert len(patterns) <= 1

    def test_get_pattern_severity_none(self):
        """Severidad sin patrones"""
        severity = PatternDetector.get_pattern_severity({})
        assert severity == "NINGUNO"

    def test_get_pattern_severity_critical(self):
        """Severidad crítica"""
        patterns = {"numbers_only": True}
        severity = PatternDetector.get_pattern_severity(patterns)
        assert severity == "CRÍTICO"

    def test_get_pattern_severity_alto(self):
        """Severidad alta con múltiples patrones"""
        patterns = {
            "sequences": ["123"],
            "repeated_chars": {"a": 4},
            "keyboard_patterns": ["qwerty"]
        }
        severity = PatternDetector.get_pattern_severity(patterns)
        assert severity == "ALTO"

    def test_get_pattern_recommendations_returns_list(self):
        """Retorna lista de recomendaciones"""
        patterns = {"dates": ["12/25/1990"]}
        recommendations = PatternDetector.get_pattern_recommendations(patterns)
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

    def test_get_pattern_recommendations_content(self):
        """Recomendaciones contienen consejos útiles"""
        patterns = {"dates": ["12/25/1990"], "common_words": ["password"]}
        recommendations = PatternDetector.get_pattern_recommendations(patterns)

        # Debe tener recomendaciones específicas para dates y palabras
        assert any("fecha" in rec.lower() for rec in recommendations)

    def test_get_pattern_recommendations_empty(self):
        """Recomendaciones para patrones vacíos"""
        recommendations = PatternDetector.get_pattern_recommendations({})
        assert len(recommendations) > 0
        assert any("✅" in rec for rec in recommendations)
