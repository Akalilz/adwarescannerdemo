# Android Adware Scanner - Demo 🛡️

<div align="center">

![Android Adware Scanner](https://img.shields.io/badge/Android-Adware%20Scanner-blue?style=for-the-badge&logo=android)

A demonstration web application showing static Android APK security analysis with permission-based pattern detection.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🎯 Overview

Android Adware Scanner is a **demonstration/mockup** of static malware analysis for educational purposes:
- **Permission Analysis**: Analyzes 23 critical Android permissions for suspicious patterns
- **Pattern Matching**: Detects known adware permission combinations  
- **PDF Reports**: Professional reports with detailed findings and recommendations
- **Simple Download**: Easy one-click PDF report download

**⚠️ IMPORTANT:** This is a demo/mockup application for educational and demonstration purposes only. It uses pattern matching algorithms, not actual machine learning models. For production use, implement real ML models, dynamic analysis, and behavioral monitoring.

## Features ✨

| Feature | Description |
|---------|-------------|
| 🔍 **Permission Analysis** | Analyzes 23 critical Android permissions |
| 🎯 **Pattern Detection** | Identifies suspicious permission combinations |
| 📊 **Demo Reports** | Professional PDF reports with findings |
| 📥 **Easy Download** | One-click PDF report download |
| ⚡ **Real-time Progress** | Live scanning status updates |
| 🎨 **Modern UI** | Beautiful, responsive web interface |
| 📱 **Mobile Friendly** | Works on desktop and mobile devices |

## 📋 Requirements

- Python 3.8 or higher
- Windows, macOS, or Linux

## 🚀 Quick Start

### 1. Download or Clone

```bash
git clone https://github.com/yourusername/adware-scanner-demo.git
cd adware-scanner-demo
```

### 2. Run the Application

**Windows:**
```bash
START_APP.bat
```

**Mac/Linux:**
```bash
chmod +x START_APP.sh
./START_APP.sh
```

The script will:
- ✅ Check Python installation
- ✅ Install dependencies automatically
- ✅ Start the web server
- ✅ Open your browser to http://localhost:5000

### 3. Use the Scanner

1. **Upload APK** - Click "Choose APK File" and select an Android application
2. **Start Scan** - Click "Start Static Scan" 
3. **View Results** - See permission analysis and detection results
4. **Download Report** - Get a professional PDF report

## 📦 Manual Installation

If you prefer manual installation:

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Then open http://localhost:5000 in your browser.

## 🔍 How It Works

1. **APK Upload** - User uploads an Android APK file
2. **Permission Extraction** - Androguard extracts all requested permissions
3. **Pattern Analysis** - Checks for suspicious permission combinations:
   - Internet + Location + Phone State = High risk
   - System Alert Window + Internet = Adware pattern
   - Task Manager + Internet + Storage = Suspicious
   - Install Shortcut + Internet = Adware indicator
4. **Risk Scoring** - Calculates confidence score based on patterns
5. **Report Generation** - Creates professional PDF with findings
6. **Download** - User downloads the security report

## 📊 Monitored Permissions

The scanner checks for 23 critical Android permissions:

- `INTERNET` - Network access
- `ACCESS_COARSE_LOCATION` / `ACCESS_FINE_LOCATION` - Location tracking
- `READ_PHONE_STATE` - Device identification
- `SYSTEM_ALERT_WINDOW` - Overlay other apps
- `GET_TASKS` - Monitor running apps
- `WRITE_EXTERNAL_STORAGE` - File system access
- `CAMERA` - Camera access
- And 16 more...

## 🎓 Educational Purpose

This demo shows:
- ✅ How to analyze APK files using Androguard
- ✅ Permission-based threat detection
- ✅ Pattern matching for malware detection
- ✅ PDF report generation with ReportLab
- ✅ Flask web application development
- ✅ Asynchronous task processing

**Not included (for real production):**
- ❌ Real machine learning models
- ❌ Dynamic analysis / sandbox execution
- ❌ Behavioral monitoring
- ❌ Code decompilation and analysis
- ❌ Multi-engine scanning

## 📁 Project Structure

```
adware-scanner-demo/
├── app.py                          # Flask web server
├── staticanalysismlintegrate.py    # Permission analysis (demo)
├── templates/
│   ├── index.html                  # Main upload page
│   └── result.html                 # Results page
├── static/
│   ├── css/style.css              # Styling
│   └── js/main.js                 # Frontend logic
├── requirements.txt                # Python dependencies
├── START_APP.bat                   # Windows launcher
├── START_APP.sh                    # Mac/Linux launcher
└── README.md                       # This file
```

## ⚙️ Configuration

Edit `app.py` to customize:

```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Max file size (100MB)
app.config['UPLOAD_FOLDER'] = 'uploads'                # Upload directory
app.config['REPORT_FOLDER'] = 'reports'                # Report directory
```

## 🛠️ Troubleshooting

**Issue: "Python is not installed"**
- Install Python 3.8+ from https://www.python.org/downloads/
- Make sure "Add Python to PATH" is checked during installation

**Issue: "Failed to install dependencies"**
- Try: `pip install --upgrade pip`
- Then: `pip install -r requirements.txt`

**Issue: "Cannot analyze APK"**
- Ensure the file is a valid APK
- Check file size is under 100MB
- Try with a different APK file

**Issue: Port 5000 already in use**
- Edit `app.py` and change: `app.run(debug=True, port=5000)` to a different port
- Or stop other applications using port 5000

## 📝 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This is a demonstration application for educational purposes only. The analysis results are based on pattern matching and should not be used for actual security decisions. For real malware detection:

- Use professional security tools
- Implement actual ML models trained on large datasets
- Combine static and dynamic analysis
- Use sandbox environments
- Employ behavioral monitoring
- Verify with multiple antivirus engines

## 🤝 Contributing

This is a demo project. Feel free to fork and modify for your own educational purposes!

## 📧 Contact

For questions or feedback about this demo, please open an issue on GitHub.

---

<div align="center">
Made for educational and demonstration purposes 🎓
</div>
