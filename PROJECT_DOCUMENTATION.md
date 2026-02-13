# AI-Powered Smart Farming Assistant - Project Documentation

## Project Overview
A Django-based web application that integrates IoT sensor data from ThingSpeak with AI-powered soil analysis to provide real-time farming insights and recommendations.

---

## Project Structure

```
ai_smart_farming_assistant/
├── manage.py                          # Django management script
├── .env                              # Environment variables (API credentials)
│
├── ai_smart_farming_assistant/        # Main Django project settings
│   ├── __init__.py
│   ├── settings.py                   # Django configuration (includes .env loader)
│   ├── urls.py                       # Main URL router
│   ├── asgi.py                       # ASGI config
│   ├── wsgi.py                       # WSGI config
│   └── __pycache__/
│
├── dashboard/                         # Main Django app
│   ├── migrations/
│   ├── templates/dashboard/
│   │   └── dashboard.html            # Frontend UI template
│   ├── __init__.py
│   ├── admin.py                      # Django admin config
│   ├── apps.py                       # App configuration
│   ├── models.py                     # Database models
│   ├── tests.py                      # Unit tests
│   ├── urls.py                       # App URL routing
│   └── views.py                      # View logic (sensor data + AI analysis)
│
├── iot_integration/                   # IoT module
│   ├── __init__.py
│   └── thingspeak_api.py             # ThingSpeak API client
│
└── agents/                            # AI Agents module
    ├── __init__.py
    └── soil_agent.py                 # Soil analysis AI agent
```

---

## File Descriptions

### 1. **ai_smart_farming_assistant/settings.py**
- Django project configuration
- Loads environment variables using `python-dotenv`
- Registers the 'dashboard' app
- Configures template directories
- Enables static file serving

### 2. **ai_smart_farming_assistant/urls.py**
- Main URL router
- Routes all requests starting with `/` to the dashboard app
- Includes Django admin panel

### 3. **dashboard/views.py**
- **Main orchestrator** for the application
- Fetches sensor data from ThingSpeak API
- Passes soil moisture to SoilAnalysisAgent for AI analysis
- Renders the dashboard template with both datasets
- Handles errors gracefully with user-friendly messages

### 4. **dashboard/urls.py**
- Routes `/` (home) to the dashboard_view
- App-level URL configuration

### 5. **dashboard/templates/dashboard/dashboard.html**
- Modern, responsive HTML5 template
- Displays three sensor cards:
  - Soil Moisture (%)
  - Temperature (°C)
  - Humidity (%)
- Shows AI-powered soil analysis:
  - Soil classification (Dry, Optimal, Overwatered)
  - Urgency level (Low, Medium, High)
  - Actionable recommendation for farmers
- Handles error states and "no data" scenarios
- Mobile-responsive design with gradient background

### 6. **iot_integration/thingspeak_api.py**
**ThingSpeakAPI Class:**
- Initializes with environment variables (THINGSPEAK_CHANNEL_ID, THINGSPEAK_READ_KEY)
- **Methods:**
  - `fetch_latest_data()`: Retrieves latest sensor reading from ThingSpeak
  - `_parse_feed_fields()`: Extracts and validates field data
  
**Field Mappings:**
- Field 1 → Soil Moisture (%)
- Field 2 → Temperature (°C)
- Field 3 → Humidity (%)

**Error Handling:**
- Network timeout handling
- Connection error handling
- HTTP error handling
- Data validation for realistic sensor ranges
- Comprehensive logging

**Convenience Function:**
- `get_sensor_data()`: Wrapper function for easy access

### 7. **agents/soil_agent.py**
**SoilAnalysisAgent Class:**
- Analyzes soil moisture values
- **Thresholds:**
  - Dry: < 30%
  - Optimal: 30-60%
  - Overwatered: > 60%

**Methods:**
- `__init__(soil_moisture)`: Validates input (0-100 range)
- `analyze()`: Returns comprehensive soil analysis dictionary
- `_classify_soil()`: Determines soil condition
- `_get_recommendation()`: Provides actionable advice
- `_determine_urgency()`: Sets urgency level

**Output Dictionary:**
```python
{
    'soil_moisture': float,        # Input value
    'classification': str,         # Dry/Optimal/Overwatered
    'recommendation': str,         # Farmer-friendly advice
    'urgency': str,               # Low/Medium/High
    'status': bool                # Success indicator
}
```

**Urgency Logic:**
- Optimal conditions → Low urgency
- Extremely dry (< 15%) → High urgency
- Severely overwatered (> 80%) → High urgency
- Other cases → Medium urgency

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install django requests python-dotenv
```

### Step 2: Configure Environment Variables
Create `.env` file in project root:
```
THINGSPEAK_CHANNEL_ID=3245976
THINGSPEAK_READ_KEY=TMRSZ78KDPKVB651
```

### Step 3: Run Migrations
```bash
python manage.py migrate
```

### Step 4: Start Development Server
```bash
python manage.py runserver
```

### Step 5: Access Application
- Open browser: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

---

## API Integration

### ThingSpeak Channel
- **Channel ID**: 3245976
- **API Endpoint**: `https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json`
- **Authentication**: API Key in query parameters

### Data Flow
1. Dashboard view receives HTTP request
2. Fetches latest sensor data from ThingSpeak API
3. Parses JSON response into sensor readings
4. Passes soil_moisture to SoilAnalysisAgent
5. Agent performs AI analysis and classification
6. Both datasets rendered in HTML template

---

## Features

✅ **Real-time Sensor Data**
- Fetches latest IoT readings from ThingSpeak
- Displays soil moisture, temperature, humidity

✅ **AI-Powered Soil Analysis**
- Intelligent classification: Dry, Optimal, Overwatered
- Smart urgency assessment
- Contextual farmer recommendations

✅ **Error Handling**
- Network error resilience
- Data validation
- User-friendly error messages
- Graceful degradation

✅ **Security**
- No hardcoded API keys
- Environment variable-based configuration
- CSRF protection enabled

✅ **Production-Ready Code**
- Clean, well-commented code
- Type hints where applicable
- Comprehensive error handling
- Separation of concerns (models, views, services)

✅ **Responsive UI**
- Mobile-friendly design
- Modern gradient styling
- Intuitive card-based layout
- Color-coded classifications and urgency levels

---

## Recommended Next Steps (Production)

1. **Database Models**: Store historical sensor data
2. **User Authentication**: Add farmer accounts and dashboards
3. **Alerts**: Email/SMS notifications for critical conditions
4. **Analytics**: Track trends and historical patterns
5. **Multiple Channels**: Support multiple IoT sensors/fields
6. **API Caching**: Redis cache for API responses
7. **Testing**: Comprehensive unit and integration tests
8. **Deployment**: Docker containerization, cloud deployment (AWS/Azure)
9. **Advanced AI**: ML models for predictive analysis and recommendations
10. **Mobile App**: iOS/Android companion application

---

## Technology Stack

- **Backend**: Django 6.0.1
- **Frontend**: HTML5, CSS3, Responsive Design
- **IoT Data**: ThingSpeak API
- **Environment Management**: python-dotenv
- **HTTP Client**: Requests library

---

## Author Notes

This project demonstrates production-grade Django development practices:
- Clean code architecture
- Separation of concerns (IoT, AI, UI layers)
- Comprehensive error handling
- Environment-based configuration
- Scalable module structure for future enhancements

The AI agent provides intelligent recommendations based on soil moisture, helping farmers make data-driven irrigation decisions and optimize water usage.
