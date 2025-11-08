from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import threading
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# Try to import analysis modules (graceful degradation if dependencies missing)
try:
    from staticanalysismlintegrate import scan_single_apk
    STATIC_ANALYSIS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Static analysis not available - {e}")
    STATIC_ANALYSIS_AVAILABLE = False

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORT_FOLDER'] = 'reports'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'apk'}

# Ensure upload and report folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)

# Global variable to store scan results
scan_results = {}

def generate_pdf_report(file_name, analysis_result=None, static_result=None, save_path=None):
    """
    Generates a modern, themed PDF report for static analysis demo results.
    Matches the website's purple/blue gradient theme.
    """
    try:
        # Demo mode report
        level_name = "Static Scan (Demo Mode)"
        
        # Extract the base name without extension for the PDF file
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        if save_path is None:
            save_path = f"Static Scan ({base_name}).pdf"
        
        # Create the PDF document
        doc = SimpleDocTemplate(save_path, pagesize=letter,
                               topMargin=0.5*inch, bottomMargin=0.5*inch,
                               leftMargin=0.75*inch, rightMargin=0.75*inch)

        # Get the current date and time of the scan
        scan_datetime = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        # Define custom styles matching website theme
        styles = getSampleStyleSheet()
        
        # Title style - Purple gradient effect
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=16,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=30
        )
        
        # Subtitle style
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=24,
            spaceBefore=4,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=16
        )
        
        # Section header style
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=16,
            fontName='Helvetica-Bold',
            borderColor=colors.HexColor('#667eea'),
            borderWidth=0,
            borderPadding=5
        )
        
        # Info text style
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            spaceAfter=8,
            fontName='Helvetica'
        )
        
        # Result text style
        result_style = ParagraphStyle(
            'ResultStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=8,
            fontName='Helvetica',
            leading=16
        )
        
        # Build the report
        elements = []
        
        # Header without emoji (ReportLab doesn't render emojis well)
        elements.append(Paragraph("APK Security Analysis Report", title_style))
        elements.append(Paragraph(level_name, subtitle_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Info box with scan details (simplified to avoid overlap)
        elements.append(Paragraph(f"<b>File Name:</b> {file_name}", info_style))
        elements.append(Paragraph(f"<b>Scan Date:</b> {scan_datetime}", info_style))
        elements.append(Paragraph(f"<b>Analysis Type:</b> Permission Pattern Detection", info_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Static Analysis Results Section
        if static_result:
            elements.append(Paragraph("Analysis Results", section_style))
            
            if isinstance(static_result, dict):
                prediction = static_result.get('Prediction', 'Unknown')
                confidence = static_result.get('Confidence', 0.0)
                permissions = static_result.get('Permissions', [])
                
                # Determine result color based on prediction (no emojis - they don't render in PDF)
                if "Adware Detected" in prediction:
                    result_color = colors.HexColor('#e74c3c')
                    verdict_prefix = "[!]"
                    verdict_bg = colors.HexColor('#ffe5e5')
                elif "Error" in prediction:
                    result_color = colors.HexColor('#f39c12')
                    verdict_prefix = "[!]"
                    verdict_bg = colors.HexColor('#fff3e0')
                else:
                    result_color = colors.HexColor('#27ae60')
                    verdict_prefix = "[✓]"
                    verdict_bg = colors.HexColor('#e8f8f5')
                
                # Verdict box
                verdict_data = [[f"{verdict_prefix} {prediction}"]]
                verdict_table = Table(verdict_data, colWidths=[6.5*inch])
                verdict_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), verdict_bg),
                    ('TEXTCOLOR', (0, 0), (-1, -1), result_color),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 14),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOX', (0, 0), (-1, -1), 2, result_color),
                    ('TOPPADDING', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ]))
                elements.append(verdict_table)
                elements.append(Spacer(1, 0.15*inch))
                
                # Confidence score
                conf_text = f"<b>Confidence Score:</b> {confidence:.1%}"
                elements.append(Paragraph(conf_text, result_style))
                elements.append(Spacer(1, 0.2*inch))
                
                # Permissions section
                if permissions:
                    elements.append(Paragraph("Detected Permissions", section_style))
                    elements.append(Paragraph(
                        f"This APK requests <b>{len(permissions)}</b> permission(s):",
                        info_style
                    ))
                    elements.append(Spacer(1, 0.15*inch))
                    
                    # Create simple permissions list (no complex table)
                    perm_style = ParagraphStyle(
                        'PermStyle',
                        parent=styles['Normal'],
                        fontSize=9,
                        textColor=colors.HexColor('#2c3e50'),
                        fontName='Helvetica',
                        leftIndent=20,
                        spaceAfter=4
                    )
                    
                    # Show up to 25 permissions
                    for i, perm in enumerate(permissions[:25], 1):
                        # Shorten permission names
                        perm_display = perm.replace('android.permission.', '')
                        perm_display = perm_display.replace('com.google.android.c2dm.permission.', 'c2dm.')
                        perm_display = perm_display.replace('com.google.android.gms.permission.', 'gms.')
                        perm_display = perm_display.replace('com.android.launcher.permission.', 'launcher.')
                        perm_display = perm_display.replace('com.google.android.providers.gsf.permission.', 'gsf.')
                        
                        elements.append(Paragraph(f"{i}. {perm_display}", perm_style))
                    
                    if len(permissions) > 25:
                        elements.append(Paragraph(
                            f"... and {len(permissions) - 25} more permissions",
                            perm_style
                        ))
            else:
                elements.append(Paragraph(f"Result: {str(static_result)}", result_style))
            
            elements.append(Spacer(1, 0.3*inch))
        
        # Recommendations Section
        elements.append(Paragraph("Security Recommendations", section_style))
        elements.append(Spacer(1, 0.1*inch))
        
        recommendations = [
            ("Verify Source", "Only download APK files from trusted sources like Google Play Store or the developer's official website."),
            ("Review Permissions", "Carefully inspect all requested permissions. Avoid apps requesting excessive or unnecessary permissions."),
            ("Check Signature", "Validate the APK's digital signature to ensure it hasn't been tampered with."),
            ("Use Security Tools", "Employ reliable anti-malware tools for comprehensive analysis before installation."),
            ("Research Reviews", "Check user reviews, ratings, and feedback from trusted sources online."),
            ("Keep Backups", "Maintain regular device backups to protect against potential data loss."),
            ("Monitor Behavior", "Watch for unusual app behavior after installation (excessive battery drain, data usage)."),
            ("Update Regularly", "Keep your Android OS and apps updated with the latest security patches.")
        ]
        
        # Create recommendation style for better formatting
        rec_title_style = ParagraphStyle(
            'RecTitle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#667eea'),
            fontName='Helvetica-Bold'
        )
        
        rec_desc_style = ParagraphStyle(
            'RecDesc',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#2c3e50'),
            fontName='Helvetica'
        )
        
        rec_data = []
        for i, (title, desc) in enumerate(recommendations, 1):
            rec_data.append([
                Paragraph(f"{i}.", result_style),
                Paragraph(f"<b>{title}:</b>", rec_title_style),
                Paragraph(desc, rec_desc_style)
            ])
        
        rec_table = Table(rec_data, colWidths=[0.3*inch, 1.0*inch, 5.2*inch])
        rec_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(rec_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        elements.append(Paragraph("Important Disclaimer", section_style))
        disclaimer_text = """
        This report is generated by a <b>demonstration/mockup tool</b> for educational purposes only. 
        The analysis uses permission pattern matching and should <b>NOT</b> be used for actual security decisions. 
        For production security analysis, use professional tools with real machine learning models, 
        dynamic analysis, and behavioral monitoring. Always exercise caution when installing APK files 
        from sources outside official app stores.
        """
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            alignment=TA_JUSTIFY,
            leading=12,
            spaceAfter=12
        )
        elements.append(Paragraph(disclaimer_text, disclaimer_style))
        
        # Footer
        elements.append(Spacer(1, 0.2*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#999999'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph("Generated by Android Adware Scanner Demo • Educational Use Only", footer_style))

        # Build the PDF
        doc.build(elements)
        print(f"✅ Themed report saved as {save_path}")
        return save_path

    except Exception as e:
        print(f"Error generating PDF report: {e}")
        import traceback
        traceback.print_exc()
        return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def run_analysis(file_path, scan_id, model_path):
    """Run static analysis demo"""
    try:
        # Static Analysis Only
        scan_results[scan_id]['status'] = 'Running Static Analysis...'
        scan_results[scan_id]['progress'] = 25
        
        static_result = None
        
        if STATIC_ANALYSIS_AVAILABLE:
            try:
                static_result = scan_single_apk(file_path, model_path)
                if static_result is None:
                    static_result = {
                        "Prediction": "Analysis Error",
                        "Confidence": 0.0,
                        "Permissions": []
                    }
            except Exception as e:
                print(f"Static analysis error: {e}")
                static_result = {
                    "Prediction": f"Error: {str(e)}",
                    "Confidence": 0.0,
                    "Permissions": []
                }
        else:
            static_result = {
                "Prediction": "Static analysis unavailable",
                "Confidence": 0.0,
                "Permissions": []
            }
        
        scan_results[scan_id]['static_result'] = static_result
        scan_results[scan_id]['progress'] = 60
        
        # Determine final verdict based on static analysis only
        static_prediction = static_result.get('Prediction', 'Unknown') if isinstance(static_result, dict) else str(static_result) if static_result else 'N/A'
        
        if static_prediction == "Adware Detected!":
            final_verdict = "Adware Detected!"
            severity = "danger"
        elif "Error" in static_prediction:
            final_verdict = "Analysis Error"
            severity = "warning"
        else:
            final_verdict = "No Adware Detected"
            severity = "success"
        
        scan_results[scan_id]['final_verdict'] = final_verdict
        scan_results[scan_id]['severity'] = severity
        
        # Generate PDF report ONLY if adware is detected
        pdf_path = None
        if static_prediction == "Adware Detected!":
            scan_results[scan_id]['status'] = 'Generating PDF Report...'
            scan_results[scan_id]['progress'] = 80
            
            try:
                filename = scan_results[scan_id]['filename']
                
                if static_result:
                    pdf_path = generate_pdf_report(filename, None, static_result)
                
                if pdf_path:
                    scan_results[scan_id]['pdf_report'] = pdf_path
                    print(f"✅ PDF report generated: {pdf_path}")
            except Exception as e:
                print(f"Error generating PDF: {e}")
                import traceback
                traceback.print_exc()
        else:
            # No report for clean apps
            scan_results[scan_id]['progress'] = 90
            print(f"ℹ️ No PDF report generated - APK is clean")
        
        scan_results[scan_id]['status'] = 'Completed'
        scan_results[scan_id]['progress'] = 100
        scan_results[scan_id]['completed_at'] = datetime.now().isoformat()
        
    except Exception as e:
        print(f"Analysis error: {e}")
        import traceback
        traceback.print_exc()
        scan_results[scan_id]['status'] = f'Error: {str(e)}'
        scan_results[scan_id]['error'] = str(e)
        scan_results[scan_id]['progress'] = 100

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only APK files are allowed'}), 400
    
    try:
        # Always use static scan only
        scan_level = 'static'
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Generate scan ID
        scan_id = f"scan_{timestamp}"
        
        # Initialize scan results
        scan_results[scan_id] = {
            'filename': filename,
            'scan_level': scan_level,
            'status': 'Initializing...',
            'progress': 0,
            'started_at': datetime.now().isoformat()
        }
        
        # Get model path (you may need to adjust this)
        model_path = 'mad_droid_cnn_modelSMOTE.keras'
        
        # Start analysis in background thread
        thread = threading.Thread(target=run_analysis, args=(file_path, scan_id, model_path))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'scan_id': scan_id,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<scan_id>')
def get_status(scan_id):
    if scan_id not in scan_results:
        return jsonify({'error': 'Scan ID not found'}), 404
    
    result = scan_results[scan_id].copy()
    return jsonify(result)

@app.route('/result/<scan_id>')
def show_result(scan_id):
    if scan_id not in scan_results:
        return "Scan not found", 404
    
    result = scan_results[scan_id]
    
    if result.get('status') != 'Completed':
        return render_template('scanning.html', scan_id=scan_id)
    
    return render_template('result.html', scan_id=scan_id, result=result)

@app.route('/download-report/<scan_id>')
def download_report(scan_id):
    if scan_id not in scan_results:
        return "Scan not found", 404
    
    result = scan_results[scan_id]
    filename = result['filename']
    base_name = os.path.splitext(filename)[0]
    
    # Look for the PDF report
    pdf_path = f"Static Scan ({base_name}).pdf"
    
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return "Report not available", 404

@app.route('/api/results/<scan_id>')
def api_results(scan_id):
    """API endpoint for getting full scan results"""
    if scan_id not in scan_results:
        return jsonify({'error': 'Scan ID not found'}), 404
    
    return jsonify(scan_results[scan_id])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
