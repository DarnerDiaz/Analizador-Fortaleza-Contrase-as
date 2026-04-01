"""
Tests para el módulo generador de PDFs (pdf_generator.py)
"""

import pytest
import sys
from pathlib import Path
from io import BytesIO

# Agregar ruta padre
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.pdf_generator import PDFReportGenerator
from utils.password_analyzer import PasswordAnalyzer


class TestPDFReportGenerator:
    """Tests para la generación de reportes PDF"""

    @pytest.fixture
    def sample_analysis(self):
        """Análisis de muestra para tests"""
        return PasswordAnalyzer.analyze_password("MyP@ssw0rd123!")

    @pytest.fixture
    def sample_recommendations(self):
        """Recomendaciones de muestra"""
        return [
            "✅ Usa caracteres especiales",
            "✅ Incluye números",
            "⚠️ Aumenta la longitud"
        ]

    @pytest.fixture
    def sample_patterns(self):
        """Patrones detectados de muestra"""
        return {
            "sequences": ["123"],
            "repeated_chars": {"s": 2}
        }

    def test_generate_single_password_report_returns_bytes(self, sample_analysis, sample_recommendations):
        """Debe retornar bytes válidos"""
        pdf_bytes = PDFReportGenerator.generate_single_password_report(
            sample_analysis,
            sample_recommendations
        )

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0

    def test_generate_single_password_report_is_pdf(self, sample_analysis, sample_recommendations):
        """Los bytes deben ser un PDF válido (comienzan con %PDF)"""
        pdf_bytes = PDFReportGenerator.generate_single_password_report(
            sample_analysis,
            sample_recommendations
        )

        # Los PDFs comienzan con %PDF
        assert pdf_bytes[:4] == b'%PDF'

    def test_generate_single_password_report_with_patterns(
        self, sample_analysis, sample_recommendations, sample_patterns
    ):
        """Debe incluir patrones en el reporte"""
        pdf_bytes = PDFReportGenerator.generate_single_password_report(
            sample_analysis,
            sample_recommendations,
            sample_patterns
        )

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'

    def test_generate_batch_report_empty_list(self):
        """Reporte masivo con lista vacía"""
        pdf_bytes = PDFReportGenerator.generate_batch_report([])

        assert isinstance(pdf_bytes, bytes)
        assert pdf_bytes[:4] == b'%PDF'

    def test_generate_batch_report_single_password(self, sample_analysis):
        """Reporte masivo con una contraseña"""
        pdf_bytes = PDFReportGenerator.generate_batch_report([sample_analysis])

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'

    def test_generate_batch_report_multiple_passwords(self):
        """Reporte masivo con múltiples contraseñas"""
        analyses = [
            PasswordAnalyzer.analyze_password("123456"),
            PasswordAnalyzer.analyze_password("MyP@ssw0rd123!"),
            PasswordAnalyzer.analyze_password("WeakPass"),
        ]

        pdf_bytes = PDFReportGenerator.generate_batch_report(analyses)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'

    def test_get_color_for_score_weak(self):
        """Color para puntuación débil"""
        from reportlab.lib import colors
        color = PDFReportGenerator.get_color_for_score(20)
        assert color == colors.red

    def test_get_color_for_score_fair(self):
        """Color para puntuación regular"""
        from reportlab.lib import colors
        color = PDFReportGenerator.get_color_for_score(50)
        assert color == colors.orange

    def test_get_color_for_score_good(self):
        """Color para puntuación buena"""
        from reportlab.lib import colors
        color = PDFReportGenerator.get_color_for_score(70)
        assert color == colors.yellow

    def test_get_color_for_score_strong(self):
        """Color para puntuación fuerte"""
        from reportlab.lib import colors
        color = PDFReportGenerator.get_color_for_score(85)
        assert color == colors.green

    def test_pdf_size_increases_with_content(self, sample_analysis, sample_recommendations):
        """Reporte con más contenido debe ser más grande"""
        # Reporte sin patrones
        pdf_small = PDFReportGenerator.generate_single_password_report(
            sample_analysis,
            sample_recommendations
        )

        # Reporte con patrones
        pdf_large = PDFReportGenerator.generate_single_password_report(
            sample_analysis,
            sample_recommendations,
            {"sequences": ["123"], "repeated_chars": {"a": 4}}
        )

        # El reporte con patrones debería ser más grande
        assert len(pdf_large) >= len(pdf_small)

    def test_batch_report_more_analyses_larger_pdf(self):
        """Más análisis en reporte masivo = PDF más grande"""
        analyses_1 = [PasswordAnalyzer.analyze_password("123456")]
        analyses_3 = [
            PasswordAnalyzer.analyze_password("123456"),
            PasswordAnalyzer.analyze_password("MyP@ssw0rd123!"),
            PasswordAnalyzer.analyze_password("WeakPass"),
        ]

        pdf_1 = PDFReportGenerator.generate_batch_report(analyses_1)
        pdf_3 = PDFReportGenerator.generate_batch_report(analyses_3)

        # Más análisis = PDF más grande
        assert len(pdf_3) > len(pdf_1)
