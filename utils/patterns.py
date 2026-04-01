"""
Detección de patrones débiles en contraseñas
"""

import re
from datetime import datetime
from config import WEAK_PATTERNS


class PatternDetector:
    """
    Detecta patrones débiles y vulnerables en contraseñas
    """

    @staticmethod
    def detect_patterns(password: str) -> dict:
        """
        Detecta múltiples patrones débiles en una contraseña

        Args:
            password: Contraseña a analizar

        Returns:
            Diccionario con patrones detectados
        """
        patterns_found = {
            "dates": PatternDetector.detect_dates(password),
            "common_words": PatternDetector.detect_common_words(password),
            "sequences": PatternDetector.detect_sequences(password),
            "repeated_chars": PatternDetector.detect_repeated_chars(password),
            "keyboard_patterns": PatternDetector.detect_keyboard_patterns(password),
            "numbers_only": PatternDetector.detect_numbers_only(password),
        }
        return {k: v for k, v in patterns_found.items() if v}

    @staticmethod
    def detect_dates(password: str) -> list:
        """Detecta fechas comunes en la contraseña"""
        dates_found = []
        for pattern in WEAK_PATTERNS["dates"]:
            matches = re.findall(pattern, password, re.IGNORECASE)
            for match in matches:
                dates_found.append(match)
        return dates_found if dates_found else None

    @staticmethod
    def detect_common_words(password: str) -> list:
        """Detecta palabras comunes débiles"""
        words_found = []
        password_lower = password.lower()
        for word in WEAK_PATTERNS["common_words"]:
            if word.lower() in password_lower:
                words_found.append(word)
        return words_found if words_found else None

    @staticmethod
    def detect_sequences(password: str) -> list:
        """Detecta secuencias comunes (qwerty, abc, 123, etc)"""
        sequences_found = []
        for pattern in WEAK_PATTERNS["sequences"]:
            if re.search(pattern, password, re.IGNORECASE):
                sequences_found.append(pattern.replace('\\', ''))
        return sequences_found if sequences_found else None

    @staticmethod
    def detect_repeated_chars(password: str) -> dict:
        """Detecta caracteres repetidos (aaaa, 1111, etc)"""
        repeated = {}
        for char in set(password):
            pattern = char + '{3,}'
            if re.search(pattern, password):
                repeated[char] = len(re.findall(char, password))
        return repeated if repeated else None

    @staticmethod
    def detect_keyboard_patterns(password: str) -> list:
        """Detecta patrones de teclado (qwerty, asdf, etc)"""
        keyboard_patterns_list = [
            r'qwert', r'asdfg', r'zxcvb',
            r'qazwsx', r'poiuy', r'lkjhg',
        ]
        patterns_found = []
        for pattern in keyboard_patterns_list:
            if re.search(pattern, password, re.IGNORECASE):
                patterns_found.append(pattern)
        return patterns_found if patterns_found else None

    @staticmethod
    def detect_numbers_only(password: str) -> bool:
        """Detecta si es solo números"""
        return password.isdigit() if len(password) > 0 else None

    @staticmethod
    def detect_years(password: str) -> list:
        """Detecta años comunes"""
        years_found = []
        current_year = datetime.now().year
        # Buscar años entre 1900 y próximos 10 años
        for year in range(1900, current_year + 10):
            if str(year) in password:
                years_found.append(str(year))
        return years_found if years_found else None

    @staticmethod
    def get_pattern_severity(patterns: dict) -> str:
        """
        Calcula la severidad de los patrones detectados

        Args:
            patterns: Diccionario de patrones

        Returns:
            "CRÍTICO", "ALTO", "MEDIO", "BAJO" o "NINGUNO"
        """
        if not patterns:
            return "NINGUNO"

        severity_count = len(patterns)
        critical_patterns = ["numbers_only", "common_words"]

        has_critical = any(p in patterns for p in critical_patterns)

        if has_critical:
            return "CRÍTICO"
        elif severity_count >= 3:
            return "ALTO"
        elif severity_count >= 2:
            return "MEDIO"
        else:
            return "BAJO"

    @staticmethod
    def get_pattern_recommendations(patterns: dict) -> list:
        """
        Genera recomendaciones basadas en patrones detectados

        Args:
            patterns: Diccionario de patrones

        Returns:
            Lista de recomendaciones
        """
        recommendations = []

        if "dates" in patterns:
            recommendations.append("❌ Evita usar fechas (nacimiento, aniversarios). Utiliza datos personales no predecibles.")

        if "common_words" in patterns:
            recommendations.append("❌ Contiene palabras comunes débiles. Reemplazarlas con términos aleatorios.")

        if "sequences" in patterns:
            recommendations.append("❌ Detectadas secuencias de teclado. Usa combinaciones más aleatorias.")

        if "repeated_chars" in patterns:
            recommendations.append("❌ Caracteres repetidos detectados (aaaa, 1111). Varía más los caracteres.")

        if "keyboard_patterns" in patterns:
            recommendations.append("❌ Patrones de teclado detectados (qwerty, asdf). Mezcla mejor los caracteres.")

        if "numbers_only" in patterns:
            recommendations.append("❌ Solo contiene números. Añade letras mayúsculas, minúsculas y símbolos.")

        if not recommendations:
            recommendations.append("✅ No se detectaron patrones débiles significativos.")

        return recommendations
