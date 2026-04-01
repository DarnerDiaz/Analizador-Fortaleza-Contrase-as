"""
Analizador de fortaleza de contraseñas
"""

import math
import re
from typing import Dict, Tuple
import zxcvbn
from config import PASSWORD_CONFIG


class PasswordAnalyzer:
    """
    Analiza la fortaleza y características de contraseñas
    """

    @staticmethod
    def calculate_entropy(password: str) -> float:
        """
        Calcula la entropía de una contraseña

        Args:
            password: Contraseña a analizar

        Returns:
            Entropía en bits
        """
        char_set_size = 0

        if any(c.islower() for c in password):
            char_set_size += 26

        if any(c.isupper() for c in password):
            char_set_size += 26

        if any(c.isdigit() for c in password):
            char_set_size += 10

        if any(not c.isalnum() for c in password):
            char_set_size += 32  # Símbolos especiales comunes

        if char_set_size == 0:
            return 0

        entropy = len(password) * math.log2(char_set_size)
        return round(entropy, 2)

    @staticmethod
    def estimate_crack_time(entropy: float) -> str:
        """
        Estima el tiempo para crackear una contraseña

        Args:
            entropy: Entropía en bits

        Returns:
            Tiempo estimado en formato legible
        """
        # Suponemos 1 millón de intentos por segundo
        attempts_per_second = 1_000_000
        seconds_to_crack = 2 ** entropy / (2 * attempts_per_second)

        time_units = [
            (60, "segundos"),
            (60, "minutos"),
            (24, "horas"),
            (365.25, "días"),
            (1e10, "años"),
        ]

        value = seconds_to_crack
        for divisor, unit in time_units:
            if value < divisor:
                if value < 1:
                    return "< 1 " + unit
                return f"{round(value, 1)} {unit}"
            value /= divisor

        return "Prácticamente imposible"

    @staticmethod
    def analyze_password(password: str, user_inputs: list = None) -> Dict:
        """
        Análisis completo de fortaleza de una contraseña

        Args:
            password: Contraseña a analizar
            user_inputs: Datos personales del usuario para mejorar análisis

        Returns:
            Diccionario con resultados del análisis
        """
        if not password:
            return {
                "error": "Contraseña vacía",
                "score": 0,
                "feedback": "Ingresa una contraseña válida"
            }

        # Usar zxcvbn para análisis avanzado
        user_inputs = user_inputs or []
        result = zxcvbn.zxcvbn(password, user_inputs=user_inputs)

        # Calcular puntuación en escala 0-100
        score = min(100, (result['score'] + 1) * 20)

        entropy = PasswordAnalyzer.calculate_entropy(password)
        crack_time = PasswordAnalyzer.estimate_crack_time(entropy)

        # Determinar fortaleza
        strength = PasswordAnalyzer.get_strength_label(score)

        # Análisis de caracteres
        char_analysis = PasswordAnalyzer.analyze_characters(password)

        return {
            "password": password,
            "score": round(score),
            "strength": strength,
            "entropy": entropy,
            "crack_time": crack_time,
            "length": len(password),
            "character_types": char_analysis,
            "feedback": result.get('feedback', {}).get('warning', ''),
            "suggestions": result.get('feedback', {}).get('suggestions', []),
            "zxcvbn_score": result['score'],
            "guesses_log10": result['guesses_log10'],
        }

    @staticmethod
    def get_strength_label(score: int) -> str:
        """
        Obtiene etiqueta de fortaleza basada en puntuación

        Args:
            score: Puntuación 0-100

        Returns:
            Etiqueta de fortaleza
        """
        if score < 20:
            return "🔴 MUY DÉBIL"
        elif score < 40:
            return "🟠 DÉBIL"
        elif score < 60:
            return "🟡 REGULAR"
        elif score < 80:
            return "🟢 FUERTE"
        else:
            return "🟢 MUY FUERTE"

    @staticmethod
    def analyze_characters(password: str) -> Dict[str, bool]:
        """
        Analiza tipos de caracteres en la contraseña

        Args:
            password: Contraseña a analizar

        Returns:
            Diccionario con presencia de tipos de caracteres
        """
        return {
            "lowercase": bool(re.search(r'[a-z]', password)),
            "uppercase": bool(re.search(r'[A-Z]', password)),
            "digits": bool(re.search(r'[0-9]', password)),
            "special": bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password)),
        }

    @staticmethod
    def batch_analyze(passwords: list, user_inputs: list = None) -> list:
        """
        Analiza múltiples contraseñas

        Args:
            passwords: Lista de contraseñas
            user_inputs: Datos personales (opcional)

        Returns:
            Lista de análisis
        """
        results = []
        for password in passwords:
            if password.strip():  # Ignorar líneas vacías
                analysis = PasswordAnalyzer.analyze_password(password.strip(), user_inputs)
                results.append(analysis)
        return results

    @staticmethod
    def get_recommendations(analysis: Dict) -> list:
        """
        Genera recomendaciones basadas en análisis

        Args:
            analysis: Resultado del análisis

        Returns:
            Lista de recomendaciones
        """
        recommendations = []

        # Validar longitud
        if analysis['length'] < PASSWORD_CONFIG['min_length']:
            recommendations.append(f"⚠️ Aumenta la longitud a mínimo {PASSWORD_CONFIG['min_length']} caracteres")

        # Validar tipos de caracteres
        char_types = analysis['character_types']
        types_count = sum(char_types.values())

        if types_count < 3:
            recommendations.append("⚠️ Usa combinación de mayúsculas, minúsculas, números y símbolos")

        if not char_types['uppercase']:
            recommendations.append("⚠️ Añade letras mayúsculas (A-Z)")

        if not char_types['lowercase']:
            recommendations.append("⚠️ Añade letras minúsculas (a-z)")

        if not char_types['digits']:
            recommendations.append("⚠️ Añade números (0-9)")

        if not char_types['special']:
            recommendations.append("⚠️ Añade símbolos especiales (!@#$%^&*)")

        # Validar puntuación
        if analysis['score'] < PASSWORD_CONFIG['min_strength']:
            recommendations.append(
                f"⚠️ Fortaleza por debajo de lo recomendado. "
                f"Objetivo: {PASSWORD_CONFIG['min_strength']}/100 (Actual: {analysis['score']}/100)"
            )

        if not recommendations:
            recommendations.append("✅ Excelente contraseña, cumple con todos los criterios")

        return recommendations
