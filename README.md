# 🌾 AI-Powered Smart Farming Assistant

A Django-based web application that integrates IoT sensor data from ThingSpeak with AI-powered soil analysis to provide real-time farming insights and recommendations.

## 🚀 Features

- **Real-time IoT Data Integration** - Fetches live sensor readings from ThingSpeak API
- **AI Soil Analysis** - Intelligent classification of soil conditions (Dry, Optimal, Overwatered)
- **Smart Recommendations** - Context-aware farming advice with urgency levels
- **Responsive Dashboard** - Beautiful gradient UI with real-time sensor cards
- **Demo Mode** - Automatic fallback to sample data for testing
- **Production-Ready** - Clean architecture, error handling, and security best practices

## 📊 Dashboard Preview

The dashboard displays:
- 💧 Soil Moisture (%)
- 🌡️ Temperature (°C)
- 💨 Humidity (%)
- 🤖 AI-powered soil condition analysis
- ⚠️ Urgency-based action recommendations

## 🛠️ Tech Stack

- **Backend:** Django 6.0.1
- **Frontend:** HTML5, CSS3 (Responsive Design)
- **IoT Platform:** ThingSpeak API
- **AI Agent:** Custom SoilAnalysisAgent
- **Environment:** Python 3.8+

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- ThingSpeak account (for IoT data)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/sravanig8/ai-smart-farming-assistant.git
   cd ai-smart-farming-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install django requests python-dotenv
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   THINGSPEAK_CHANNEL_ID=your_channel_id
   THINGSPEAK_READ_KEY=your_read_api_key
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the dashboard**
   
   Open your browser and navigate to: `http://127.0.0.1:8000/`

## 📁 Project Structure

```
ai-smart-farming-assistant/
├── ai_smart_farming_assistant/    # Django project settings
│   ├── settings.py                # Configuration
│   ├── urls.py                    # Main URL routing
│   └── wsgi.py                    # WSGI config
├── dashboard/                     # Main Django app
│   ├── views.py                   # View logic
│   ├── urls.py                    # App URLs
│   └── templates/                 # HTML templates
│       └── dashboard/
│           └── dashboard.html     # Main UI
├── iot_integration/               # IoT module
│   └── thingspeak_api.py         # ThingSpeak API client
├── agents/                        # AI agents
│   └── soil_agent.py             # Soil analysis agent
├── .env                          # Environment variables (not in repo)
├── .gitignore                    # Git ignore rules
├── manage.py                     # Django management script
└── README.md                     # This file
```

## 🔑 ThingSpeak Configuration

### Field Mapping
| Field | Sensor Type    | Unit | Range  |
|-------|---------------|------|--------|
| Field1| Soil Moisture | %    | 0-100  |
| Field2| Temperature   | °C   | -50-60 |
| Field3| Humidity      | %    | 0-100  |

### Get API Keys
1. Login to [ThingSpeak](https://thingspeak.com/)
2. Go to your channel
3. Click "API Keys" tab
4. Copy Channel ID and Read API Key

## 🤖 AI Soil Analysis

The SoilAnalysisAgent classifies soil conditions:

- **Dry** (< 30%): Irrigation needed urgently
- **Optimal** (30-60%): Ideal growing conditions
- **Overwatered** (> 60%): Reduce watering

### Urgency Levels
- **Low**: Conditions are normal
- **Medium**: Action recommended soon
- **High**: Immediate action required (< 15% or > 80% moisture)

## 🧪 Testing

Run the API test script:
```bash
python test_api.py
```

Upload sample data to ThingSpeak:
```bash
python upload_sample_data.py
```

## 🚀 Production Deployment

For production use:
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use environment variables for SECRET_KEY
4. Set up a production database (PostgreSQL)
5. Use a WSGI server (Gunicorn, uWSGI)
6. Configure static files serving
7. Enable HTTPS

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Sravani G**
- GitHub: [@sravanig8](https://github.com/sravanig8)

## 🙏 Acknowledgments

- ThingSpeak for IoT data platform
- Django community for excellent documentation
- All contributors and users of this project

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Made with ❤️ for sustainable agriculture**
