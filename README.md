# 🔐 OTP Anomaly Detection Demo

A real-time rule-based anomaly detection system for One-Time Password (OTP) requests. This Streamlit application demonstrates intelligent pattern recognition to identify and prevent suspicious OTP request patterns including account takeover attempts and credential stuffing attacks.

## Features

✨ **Real-time Anomaly Detection**
- Rule-based detection (no ML required)
- Multi-factor risk scoring system
- Zero-latency flagging of suspicious patterns

🎯 **Smart Pattern Recognition**
- Detects multiple OTP requests to the same phone
- Identifies single IP targeting multiple numbers
- Tracks unusual device/country changes
- Monitors consecutive failure streaks

📊 **Interactive Dashboard**
- Live metrics and analytics
- Risk score distribution charts
- Detailed flagged events viewer
- CSV export functionality

🌍 **Multi-Language Support**
- English and international language support ready
- Extensible translation framework

## Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib
- **Language**: Python 3.8+

## Installation & Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/travkkin-ui/blank-app.git
cd blank-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## How It Works

### 1. **Data Generation**
- Generates synthetic OTP request events
- Simulates normal user behavior, suspicious patterns, and abuse scenarios
- Fully configurable event counts and random seed

### 2. **Feature Engineering**
Computes meaningful features for each OTP request:
- **OTP per Phone**: Number of OTP requests to the same phone (configurable time window)
- **Phones per IP**: Unique phone numbers targeted from a single IP
- **Devices per Phone**: Unique devices used to request OTPs for a phone
- **Country Change**: Detects if a request comes from a different country than recent requests
- **Fail Streak**: Tracks consecutive failed OTP attempts

### 3. **Risk Scoring**
Rule-based scoring system (0–100) that evaluates:
- ✅ **Low Risk** (0–10): Normal user behavior
- ⚠️ **Moderate** (11–34): Some concerning patterns
- 🔴 **High** (35–69): Likely suspicious activity
- 🚨 **Critical** (70–100): Immediate action needed

### 4. **Actions**
- **Allow**: Proceed with OTP delivery
- **Throttle**: Rate-limit OTP delivery
- **Block**: Reject OTP request immediately

## Project Structure

```
blank-app/
├── streamlit_app.py       # Main application logic
├── translations.py        # Multi-language support
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── README.md             # This file
└── LICENSE               # License
```

## Configuration

### Sidebar Controls

- **Event Counts**: Adjust the number of normal, suspicious, and abuse events
- **Detection Windows**: 
  - OTP/Phone window: Time window for measuring OTP frequency per phone (default: 10 min)
  - Phones/IP window: Time window for measuring unique phones per IP (default: 10 min)
  - Devices/Phone window: Time window for unique devices per phone (default: 24 hours)
- **Random Seed**: Reproducible data generation

## Use Cases

- 🏦 **Banking & Finance**: Protect against account takeover attacks
- 🛡️ **Security Teams**: Monitor and analyze OTP fraud patterns
- 🎓 **Education**: Learn about anomaly detection techniques
- 🧪 **Testing**: Generate synthetic security incident scenarios

## Hackathon Prototype

This is a hackathon prototype (v1.0) created to demonstrate rule-based anomaly detection concepts. It's designed for rapid iteration and understanding of OTP security patterns without requiring complex machine learning models.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Version**: 1.0  
**Status**: Hackathon Prototype  
**Last Updated**: March 2026
