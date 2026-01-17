"""
PDF Report Export Module
Generates professional PDF reports with risk analysis results
"""
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from backend.utils.helpers import setup_logger

logger = setup_logger(__name__)

def add_page_number(canvas, doc):
    """Add page numbers to PDF footer."""
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(7.5*inch, 0.4*inch, text)
    canvas.restoreState()

class PDFReportGenerator:
    """Generate comprehensive professional PDF reports for crop risk analysis."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Create custom paragraph styles for professional look."""
        # Main Title
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#047857'),
            spaceAfter=12,
            spaceBefore=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=34
        ))
        
        # Subtitle
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#059669'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=18
        ))
        
        # Section Header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#047857'),
            spaceAfter=16,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderPadding=(0, 0, 8, 0),
            leading=22
        ))
        
        # Subsection
        self.styles.add(ParagraphStyle(
            name='Subsection',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#065f46'),
            spaceAfter=10,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            leading=17
        ))
        
        # Body text (custom name to avoid conflict with default BodyText)
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=14
        ))
        
        # Risk level styles
        self.styles.add(ParagraphStyle(
            name='RiskHigh',
            parent=self.styles['Normal'],
            fontSize=24,
            textColor=colors.HexColor('#dc2626'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=8
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskModerate',
            parent=self.styles['Normal'],
            fontSize=24,
            textColor=colors.HexColor('#f59e0b'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=8
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskLow',
            parent=self.styles['Normal'],
            fontSize=24,
            textColor=colors.HexColor('#16a34a'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=8
        ))
        
        # Metadata text
        self.styles.add(ParagraphStyle(
            name='Metadata',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=6,
            fontName='Helvetica',
            leading=13
        ))
        
        # Footer text
        self.styles.add(ParagraphStyle(
            name='FooterText',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#9ca3af'),
            spaceAfter=6,
            fontName='Helvetica-Oblique',
            alignment=TA_CENTER,
            leading=12
        ))
    
    def generate_report(self, prediction_data, historical_data=None):
        """
        Generate a comprehensive professional PDF report.
        
        Args:
            prediction_data: Dictionary containing prediction results
            historical_data: Optional historical trends data
        
        Returns:
            BytesIO buffer containing the PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            topMargin=0.75*inch, 
            bottomMargin=0.75*inch,
            leftMargin=0.75*inch, 
            rightMargin=0.75*inch,
            title="CFEWS Risk Analysis Report",
            author="Crop Failure Early Warning System"
        )
        
        story = []
        
        # ========== COVER PAGE ==========
        story.append(Spacer(1, 1.5*inch))
        
        # Logo/Icon placeholder (green square representing agriculture)
        story.append(Paragraph("🌾", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Main Title
        story.append(Paragraph("CROP FAILURE", self.styles['CustomTitle']))
        story.append(Paragraph("EARLY WARNING SYSTEM", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Subtitle
        story.append(Paragraph("Risk Analysis Report", self.styles['Subtitle']))
        story.append(Spacer(1, 0.5*inch))
        
        # Decorative line
        story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor('#047857'), 
                               spaceBefore=10, spaceAfter=20, hAlign='CENTER'))
        
        # Report metadata in a professional box
        metadata_data = [
            ['Report Details', ''],
            ['Generated On:', datetime.now().strftime("%B %d, %Y at %I:%M %p")],
            ['Location:', f"{prediction_data.get('district')}, {prediction_data.get('state')}"],
            ['Crop Type:', prediction_data.get('crop')],
            ['Season:', prediction_data.get('season')],
            ['Report ID:', f"CFEWS-{datetime.now().strftime('%Y%m%d%H%M')}"]
        ]
        
        metadata_table = Table(metadata_data, colWidths=[2*inch, 3.5*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#047857')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 13),
            ('SPAN', (0, 0), (1, 0)),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#d1fae5')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#065f46')),
            ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#047857')),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(metadata_table)
        
        story.append(Spacer(1, 1*inch))
        
        # Disclaimer
        story.append(Paragraph(
            "<i>This report contains AI-generated predictions based on satellite imagery, weather data, "
            "and machine learning models. Please consult local agricultural experts for final decisions.</i>",
            self.styles['FooterText']
        ))
        
        # Page break to main content
        story.append(PageBreak())
        
        # ========== EXECUTIVE SUMMARY ==========
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#d1fae5')))
        story.append(Spacer(1, 0.2*inch))
        
        risk_level = prediction_data.get('risk_level', 'Unknown')
        probability = prediction_data.get('probability', 0) * 100
        
        # Risk level box
        risk_style = 'RiskLow' if risk_level == 'Low' else 'RiskModerate' if risk_level == 'Moderate' else 'RiskHigh'
        risk_bg = colors.HexColor('#dcfce7') if risk_level == 'Low' else colors.HexColor('#fef3c7') if risk_level == 'Moderate' else colors.HexColor('#fee2e2')
        
        risk_summary_data = [
            ['Risk Assessment'],
            [Paragraph(f"<b>{risk_level.upper()} RISK</b>", self.styles[risk_style])],
            [Paragraph(f"Failure Probability: <b>{probability:.1f}%</b>", self.styles['CustomBody'])]
        ]
        
        risk_summary_table = Table(risk_summary_data, colWidths=[5.5*inch])
        risk_summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#047857')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BACKGROUND', (0, 1), (-1, -1), risk_bg),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#047857')),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(risk_summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # ========== RISK FACTORS ANALYSIS ==========
        story.append(Paragraph("Risk Factor Analysis", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#d1fae5')))
        story.append(Spacer(1, 0.15*inch))
        
        story.append(Paragraph("Top Contributing Factors", self.styles['Subsection']))
        
        explanation = prediction_data.get('explanation', {})
        top_factors = explanation.get('top_factors', [])
        
        if top_factors:
            factor_data = [['Rank', 'Risk Factor', 'Contribution (%)']]
            for idx, factor in enumerate(top_factors[:5], 1):
                contribution_pct = factor['contribution'] * 100
                # Color code based on contribution
                if contribution_pct > 12:
                    contrib_color = colors.HexColor('#dc2626')
                elif contribution_pct > 8:
                    contrib_color = colors.HexColor('#f59e0b')
                else:
                    contrib_color = colors.HexColor('#16a34a')
                
                factor_data.append([
                    str(idx),
                    factor['factor'],
                    f"{contribution_pct:.1f}%"
                ])
            
            factor_table = Table(factor_data, colWidths=[0.7*inch, 3.5*inch, 1.3*inch])
            factor_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#047857')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#065f46')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#047857')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdf4')]),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(factor_table)
        
        story.append(Spacer(1, 0.3*inch))
        
        # ========== ENVIRONMENTAL INDICATORS ==========
        story.append(Paragraph("Environmental Indicators", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#d1fae5')))
        story.append(Spacer(1, 0.15*inch))
        
        raw_features = prediction_data.get('raw_features', {})
        feature_data = [['Environmental Parameter', 'Current Value', 'Status']]
        
        # NDVI
        if 'ndvi_mean' in raw_features:
            ndvi_val = raw_features['ndvi_mean']
            ndvi_status = '✓ Healthy' if ndvi_val > 0.5 else '⚠ Stressed' if ndvi_val > 0.3 else '✗ Critical'
            feature_data.append(['NDVI (Vegetation Health)', f"{ndvi_val:.3f}", ndvi_status])
        
        # Rainfall
        if 'rainfall_deviation' in raw_features:
            rain_val = raw_features['rainfall_deviation']
            rain_status = '✓ Normal' if abs(rain_val) < 15 else '⚠ Moderate' if abs(rain_val) < 25 else '✗ Severe'
            feature_data.append(['Rainfall Deviation', f"{rain_val:.1f}%", rain_status])
        
        # Soil Moisture
        if 'soil_moisture_index' in raw_features:
            soil_val = raw_features['soil_moisture_index']
            soil_status = '✓ Adequate' if soil_val > 50 else '⚠ Low' if soil_val > 30 else '✗ Critical'
            feature_data.append(['Soil Moisture Index', f"{soil_val:.1f}%", soil_status])
        
        # Temperature
        if 'temperature_anomaly' in raw_features:
            temp_val = raw_features['temperature_anomaly']
            temp_status = '✓ Normal' if abs(temp_val) < 1.5 else '⚠ Moderate' if abs(temp_val) < 3 else '✗ Extreme'
            feature_data.append(['Temperature Anomaly', f"{temp_val:.2f}°C", temp_status])
        
        # Pest
        if 'pest_frequency' in raw_features:
            pest_val = raw_features['pest_frequency']
            pest_status = '✓ Low' if pest_val < 0.3 else '⚠ Moderate' if pest_val < 0.7 else '✗ High'
            feature_data.append(['Pest Frequency Index', f"{pest_val:.2f}", pest_status])
        
        feature_table = Table(feature_data, colWidths=[2.8*inch, 1.5*inch, 1.2*inch])
        feature_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#047857')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#065f46')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#047857')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdf4')]),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(feature_table)
        
        story.append(Spacer(1, 0.4*inch))
        
        # ========== RECOMMENDATIONS ==========
        story.append(Paragraph("Actionable Recommendations", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#d1fae5')))
        story.append(Spacer(1, 0.15*inch))
        
        recommendations = self._generate_recommendations(risk_level, raw_features)
        
        for idx, rec in enumerate(recommendations, 1):
            # Clean up the recommendation text
            clean_rec = rec.replace('<b>', '').replace('</b>', '').replace('⚠️', '').replace('⚡', '').replace('✅', '')
            bullet = '●' if idx <= 3 else '○'
            story.append(Paragraph(f"{bullet} {clean_rec}", self.styles['CustomBody']))
            story.append(Spacer(1, 0.08*inch))
        
        story.append(Spacer(1, 0.3*inch))
        
        # ========== DATA SOURCES & METHODOLOGY ==========
        story.append(Paragraph("Data Sources & Methodology", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#d1fae5')))
        story.append(Spacer(1, 0.15*inch))
        
        story.append(Paragraph("This analysis is powered by multiple authoritative data sources:", self.styles['CustomBody']))
        story.append(Spacer(1, 0.15*inch))
        
        sources_data = [
            ['Data Source', 'Purpose', 'Update Frequency'],
            ['OpenWeather API', 'Live weather data (temperature, rainfall, humidity)', 'Real-time'],
            ['NASA MODIS', 'Satellite imagery for vegetation health (NDVI)', 'Daily'],
            ['NASA GLDAS', 'Soil moisture & hydrological data', 'Daily'],
            ['NBSS&LUP', 'Soil composition & properties', 'Static'],
            ['Ministry of Agriculture', 'Historical crop yield & failure records', 'Seasonal'],
            ['State Agriculture Dept.', 'Local pest incidents & disease tracking', 'Weekly']
        ]
        
        sources_table = Table(sources_data, colWidths=[1.6*inch, 2.6*inch, 1.3*inch])
        sources_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#047857')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#047857')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f9fafb'), colors.white]),
            ('TOPPADDING', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(sources_table)
        
        story.append(Spacer(1, 0.3*inch))
        
        # Methodology
        story.append(Paragraph("Machine Learning Methodology", self.styles['Subsection']))
        story.append(Paragraph(
            "Our prediction model employs a Random Forest classifier trained on historical data encompassing "
            "satellite imagery, weather patterns, soil conditions, and pest records. The model analyzes multiple "
            "environmental parameters to assess crop failure risk with approximately 70% accuracy.",
            self.styles['CustomBody']
        ))
        
        story.append(Spacer(1, 0.5*inch))
        
        # ========== DISCLAIMER ==========
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#d1fae5')))
        story.append(Spacer(1, 0.15*inch))
        
        disclaimer_text = (
            "<b>IMPORTANT DISCLAIMER:</b> This report is generated by artificial intelligence and machine learning "
            "models based on available data sources. While we strive for accuracy, predictions should be used as "
            "guidance only and not as the sole basis for agricultural decisions. We strongly recommend consulting "
            "with local agricultural extension officers, agronomists, and experienced farmers before making final "
            "decisions regarding crop cultivation, irrigation, pest management, or other farming activities. "
            "The Crop Failure Early Warning System and its creators assume no liability for decisions made based "
            "on this report."
        )
        story.append(Paragraph(disclaimer_text, self.styles['FooterText']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Footer with contact info
        story.append(Paragraph(
            "For technical support or feedback, please contact your local agricultural department.",
            self.styles['FooterText']
        ))
        story.append(Paragraph(
            f"Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | CFEWS v1.0",
            self.styles['FooterText']
        ))
        
        # Build PDF with page numbers
        doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
        buffer.seek(0)
        
        logger.info(f"Generated professional PDF report for {prediction_data.get('district')}, {prediction_data.get('state')}")
        return buffer
    
    def _generate_recommendations(self, risk_level, raw_features):
        """Generate actionable recommendations based on risk assessment."""
        recommendations = []
        
        if risk_level == 'High':
            recommendations.append("⚠️ <b>High Risk Detected:</b> Consider postponing sowing or switching to more resilient crop varieties")
            recommendations.append("Implement intensive irrigation and soil moisture monitoring")
            recommendations.append("Apply preventive pest management measures")
            recommendations.append("Consult local agricultural extension officers for emergency support")
        elif risk_level == 'Moderate':
            recommendations.append("⚡ <b>Moderate Risk:</b> Proceed with caution and implement risk mitigation strategies")
            recommendations.append("Ensure adequate water availability through irrigation planning")
            recommendations.append("Monitor weather forecasts closely for the next 2-3 weeks")
            recommendations.append("Consider crop insurance to protect against potential losses")
        else:
            recommendations.append("✅ <b>Low Risk:</b> Favorable conditions for cultivation")
            recommendations.append("Follow standard agricultural practices for optimal yield")
            recommendations.append("Continue monitoring weather and soil conditions regularly")
            recommendations.append("Maintain proper crop nutrition and pest surveillance")
        
        # Add specific recommendations based on features
        ndvi = raw_features.get('ndvi_mean', 0)
        if ndvi < 0.3:
            recommendations.append("<b>Vegetation Stress Alert:</b> NDVI below healthy threshold - consider soil amendments and enhanced irrigation")
        
        rainfall_dev = raw_features.get('rainfall_deviation', 0)
        if abs(rainfall_dev) > 20:
            recommendations.append(f"<b>Rainfall Anomaly:</b> {abs(rainfall_dev):.0f}% deviation from normal - plan water management accordingly")
        
        return recommendations

def generate_pdf_report(prediction_data, historical_data=None):
    """Public interface to generate PDF report."""
    generator = PDFReportGenerator()
    return generator.generate_report(prediction_data, historical_data)
