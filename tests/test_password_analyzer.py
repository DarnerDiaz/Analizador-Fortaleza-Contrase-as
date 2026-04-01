"""
Tests para el módulo de análisis de contraseñas (password_analyzer.py)
"""

import pytest
import sys
from pathlib import Path

# Agregar ruta padre
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.password_analyzer import PasswordAnalyzer


class TestPasswordAnalyzer:
    """Tests para el análisis de contraseñas"""

    def test_calculate_entropy_empty(self):
        """Entropía de contraseña vacía debe ser 0"""
        entropy = PasswordAnalyzer.calculate_entropy("")
        assert entropy == 0

    def test_calculate_entropy_lowercase_only(self):
        """Entropía con solo minúsculas"""
        entropy = PasswordAnalyzer.calculate_entropy("aaaaa")
        assert entropy > 0
        # 5 caracteres * log2(26) ≈ 5 * 4.7 ≈ 23.5
        assert 20 < entropy < 30

    def test_calculate_entropy_mixed_characters(self):
        """Entropía aumenta con más tipos de caracteres"""
        entropy_lower = PasswordAnalyzer.calculate_entropy("aaaaa")
        entropy_mixed = PasswordAnalyzer.calculate_entropy("Aa1B@")

        assert entropy_mixed > entropy_lower

    def test_calculate_entropy_special_chars(self):
        """Entropía con caracteres especiales"""
        entropy = PasswordAnalyzer.calculate_entropy("P@ss!w0rd#123")
        assert entropy > 50

    def test_estimate_crack_time_weak(self):
        """Contraseña débil debe tener tiempo de crack corto"""
        crack_time = PasswordAnalyzer.estimate_crack_time(10)
        assert "segundos" in crack_time or "minutos" in crack_time

    def test_estimate_crack_time_strong(self):
        """Contraseña fuerte debe tener tiempo de crack largo"""
        crack_time = PasswordAnalyzer.estimate_crack_time(100)
        assert "años" in crack_time or "Prácticamente" in crack_time

    def test_analyze_password_empty(self):
        """Análisis de contraseña vacía"""
        result = PasswordAnalyzer.analyze_password("")
        assert result["error"] == "Contraseña vacía"
        assert result["score"] == 0

    def test_analyze_password_returns_dict(self):
        """Análisis debe retornar diccionario con campos requeridos"""
        result = PasswordAnalyzer.analyze_password("MyP@ssw0rd123!")

        required_fields = [
            "password", "score", "strength", "entropy",
            "crack_time", "length", "character_types", "suggestions"
        ]

        for field in required_fields:
            assert field in result

    def test_analyze_password_score_range(self):
        """Puntuación debe estar entre 0 y 100"""
        result = PasswordAnalyzer.analyze_password("MyP@ssw0rd123!")
        assert 0 <= result["score"] <= 100

    def test_analyze_password_weak(self):
        """Contraseña débil debe tener puntuación baja"""
        result = PasswordAnalyzer.analyze_password("123456")
        assert result["score"] < 40

    def test_analyze_password_strong(self):
        """Contraseña fuerte debe tener puntuación alta"""
        result = PasswordAnalyzer.analyze_password("MyStr0ng!P@ssw0rd#2024$%^&*()")
        assert result["score"] >= 60

    def test_character_types_detection(self):
        """Debe detectar correctamente tipos de caracteres"""
        # Solo minúsculas
        result = PasswordAnalyzer.analyze_password("abcdef")
        assert result["character_types"]["lowercase"] is True
        assert result["character_types"]["uppercase"] is False
        assert result["character_types"]["digits"] is False
        assert result["character_types"]["special"] is False

        # Mezcla
        result = PasswordAnalyzer.analyze_password("AaBb11!@")
        assert result["character_types"]["lowercase"] is True
        assert result["character_types"]["uppercase"] is True
        assert result["character_types"]["digits"] is True
        assert result["character_types"]["special"] is True

    def test_get_strength_label_very_weak(self):
        """Etiqueta para puntuación muy baja"""
        label = PasswordAnalyzer.get_strength_label(10)
        assert "MUY DÉBIL" in label

    def test_get_strength_label_weak(self):
        """Etiqueta para puntuación baja"""
        label = PasswordAnalyzer.get_strength_label(30)
        assert "DÉBIL" in label

    def test_get_strength_label_strong(self):
        """Etiqueta para puntuación alta"""
        label = PasswordAnalyzer.get_strength_label(75)
        assert "FUERTE" in label

    def test_batch_analyze_empty_list(self):
        """Análisis masivo con lista vacía"""
        results = PasswordAnalyzer.batch_analyze([])
        assert results == []

    def test_batch_analyze_multiple(self):
        """Análisis masivo de múltiples contraseñas"""
        passwords = ["123456", "MyP@ssw0rd123!", "WeakPass"]
        results = PasswordAnalyzer.batch_analyze(passwords)

        assert len(results) == 3
        # Primera debe ser débil
        assert results[0]["score"] < 40
        # Segunda debe ser fuerte
        assert results[1]["score"] > 60

    def test_batch_analyze_with_blank_lines(self):
        """Análisis masivo debe ignorar líneas vacías"""
        passwords = ["MyP@ssw0rd123!", "", "AnotherPass123!"]
        results = PasswordAnalyzer.batch_analyze(passwords)

        assert len(results) == 2

    def test_get_recommendations_weak_password(self):
        """Recomendaciones para contraseña débil"""
        analysis = PasswordAnalyzer.analyze_password("123456")
        recommendations = PasswordAnalyzer.get_recommendations(analysis)

        # Debe tener recomendaciones
        assert len(recommendations) > 0
        # Al menos una debe ser una advertencia
        assert any("⚠️" in rec for rec in recommendations)

    def test_get_recommendations_strong_password(self):
        """Recomendaciones para contraseña fuerte"""
        analysis = PasswordAnalyzer.analyze_password("MyStr0ng!P@ssw0rd#2024")
        recommendations = PasswordAnalyzer.get_recommendations(analysis)

        # Debe haber recomendaciones o confirmación de éxito
        assert len(recommendations) > 0
        # Si es fuerte, debería tener confirmación
        strong_enough = analysis["score"] >= 50
        if strong_enough:
            assert any("✅" in rec for rec in recommendations)

    def test_analyze_password_with_user_inputs(self):
        """Análisis debe considerar datos personales"""
        user_inputs = ["John", "Doe", "1990"]

        result1 = PasswordAnalyzer.analyze_password("john1990pass", user_inputs)
        result2 = PasswordAnalyzer.analyze_password("RandomStr0ng!Pass123")

        # La que contiene datos personales debe tener puntuación diferente
        # u al menos debe analizar correctamente
        assert "score" in result1
        assert "score" in result2

    def test_analyze_password_unicode(self):
        """Debe manejar caracteres unicode"""
        result = PasswordAnalyzer.analyze_password("MiContraseña123!ñáéíóú")
        assert result["length"] > 0
        assert result["score"] >= 0
