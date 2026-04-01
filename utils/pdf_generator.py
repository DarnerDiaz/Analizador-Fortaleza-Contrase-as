"""
Generador de reportes PDF
"""

from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas
from config import PDF_CONFIG, COLORS


class PDFReportGenerator:
    """
    Genera reportes PDF de análisis de contraseñas
    """

    @staticmethod
    def generate_single_password_report(analysis: dict, recommendations: list, patterns: dict = None) -> bytes:
        """
        Genera reporte PDF para una sola contraseña

        Args:
            analysis: Resultado del análisis
            recommendations: Lista de recomendaciones
            patterns: Diccionario de patrones detectados

        Returns:
            Bytes del PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=PDF_CONFIG['margin'],
            leftMargin=PDF_CONFIG['margin'],
            topMargin=PDF_CONFIG['margin'],
            bottomMargin=PDF_CONFIG['margin'],
        )

        # Elementos del documento
        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=PDF_CONFIG['title_size'],
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=1,  # Centrado
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=PDF_CONFIG['heading_size'],
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
        )

        # Título
        title = Paragraph("📊 Reporte de Análisis de Contraseña", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Fecha
        date_text = f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        elements.append(Paragraph(date_text, styles['Normal']))
        elements.append(Spacer(1, 20))

        # Sección de Resultados
        elements.append(Paragraph("RESULTADOS DEL ANÁLISIS", heading_style))

        # Tabla de resultados
        score = analysis['score']
        strength = analysis['strength']
        color = PDFReportGenerator.get_color_for_score(score)

        results_data = [
            ['Métrica', 'Valor'],
            ['Fortaleza', f"{strength} ({score}/100)"],
            ['Entropía', f"{analysis['entropy']} bits"],
            ['Tiempo estimado de crack', analysis['crack_time']],
            ['Longitud', f"{analysis['length']} caracteres"],
        ]

        results_table = Table(results_data, colWidths=[2.5*inch, 2.5*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))

        elements.append(results_table)
        elements.append(Spacer(1, 20))

        # Tipos de caracteres
        elements.append(Paragraph("TIPOS DE CARACTERES", heading_style))

        char_types = analysis['character_types']
        char_data = [
            ['Tipo', 'Estado'],
            ['Mayúsculas (A-Z)', '✓ Presente' if char_types['uppercase'] else '✗ No presente'],
            ['Minúsculas (a-z)', '✓ Presente' if char_types['lowercase'] else '✗ No presente'],
            ['Números (0-9)', '✓ Presente' if char_types['digits'] else '✗ No presente'],
            ['Símbolos (!@#$%^&*)', '✓ Presente' if char_types['special'] else '✗ No presente'],
        ]

        char_table = Table(char_data, colWidths=[2.5*inch, 2.5*inch])
        char_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        elements.append(char_table)
        elements.append(Spacer(1, 20))

        # Patrones detectados
        if patterns:
            elements.append(Paragraph("⚠️ PATRONES DÉBILES DETECTADOS", heading_style))
            patterns_text = "<br/>".join([f"• {p}" for p in patterns.keys()])
            elements.append(Paragraph(patterns_text, styles['Normal']))
            elements.append(Spacer(1, 20))

        # Recomendaciones
        elements.append(Paragraph("💡 RECOMENDACIONES", heading_style))
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", styles['Normal']))
            elements.append(Spacer(1, 6))

        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def generate_batch_report(analyses: list) -> bytes:
        """
        Genera reporte PDF para múltiples contraseñas

        Args:
            analyses: Lista de análisis

        Returns:
            Bytes del PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=PDF_CONFIG['margin'],
            leftMargin=PDF_CONFIG['margin'],
            topMargin=PDF_CONFIG['margin'],
            bottomMargin=PDF_CONFIG['margin'],
        )

        elements = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=PDF_CONFIG['title_size'],
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            alignment=1,
        )

        # Título
        title = Paragraph("📋 Reporte Masivo de Análisis de Contraseñas", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Fecha
        date_text = f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        elements.append(Paragraph(date_text, styles['Normal']))
        elements.append(Spacer(1, 20))

        # Resumen
        total = len(analyses)
        strong = sum(1 for a in analyses if a['score'] >= 80)
        weak = sum(1 for a in analyses if a['score'] < 40)
        average_score = round(sum(a['score'] for a in analyses) / total, 2) if total > 0 else 0

        summary_text = f"""
        <b>Resumen:</b><br/>
        • Total de contraseñas: {total}<br/>
        • Fortaleza promedio: {average_score}/100<br/>
        • Contraseñas fuertes (≥80): {strong}<br/>
        • Contraseñas débiles (<40): {weak}
        """
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 20))

        # Tabla de resultados
        table_data = [['#', 'Fortaleza', 'Entropía', 'Longitud', 'Evaluación']]

        for i, analysis in enumerate(analyses, 1):
            score = analysis['score']
            strength = "🟢 Buena" if score >= 60 else ("🟡 Regular" if score >= 40 else "🔴 Débil")
            table_data.append([
                str(i),
                f"{score}/100",
                f"{analysis['entropy']} bits",
                str(analysis['length']),
                strength,
            ])

        if table_data:
            table = Table(table_data, colWidths=[0.6*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.3*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ]))
            elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def get_color_for_score(score: int) -> str:
        """
        Retorna color RGB basado en puntuación

        Args:
            score: Puntuación 0-100

        Returns:
            Tupla RGB
        """
        if score < 40:
            return colors.red
        elif score < 60:
            return colors.orange
        elif score < 80:
            return colors.yellow
        else:
            return colors.green
