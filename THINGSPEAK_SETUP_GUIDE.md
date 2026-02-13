# ThingSpeak Setup & Troubleshooting Guide

## 🔍 Issue Identified

The ThingSpeak channel **3245976** exists but contains **no sensor data** yet. The API returned:
```json
{
  "channel": {...},
  "feeds": [],           // ❌ Empty - no data uploaded
  "last_entry_id": null  // ❌ No entries
}
```

## ✅ Solution Implemented

The dashboard now handles this scenario gracefully:
- **With Real Data**: Displays live ThingSpeak sensor readings
- **Without Data**: Shows demo data with a warning message

---

## 📤 How to Upload Real Sensor Data to ThingSpeak

### Option 1: Use the Upload Script (Recommended for Testing)

1. **Get your Write API Key** from ThingSpeak:
   - Go to https://thingspeak.com/channels/3245976
   - Click "API Keys" tab
   - Copy the "Write API Key"

2. **Run the upload script**:
   ```bash
   python upload_sample_data.py
   ```
   
3. **Enter your Write API Key** when prompted

4. **Wait for uploads** (3 sample readings with 16-second intervals)

5. **Refresh dashboard** at http://127.0.0.1:8000/

### Option 2: Manual API Upload (Single Reading)

Using curl or browser:
```bash
https://api.thingspeak.com/update?api_key=YOUR_WRITE_KEY&field1=45.5&field2=25.0&field3=65.0
```

Replace:
- `YOUR_WRITE_KEY` - Your ThingSpeak Write API Key
- `field1` - Soil moisture (0-100%)
- `field2` - Temperature (°C)
- `field3` - Humidity (0-100%)

### Option 3: IoT Device Integration

For real IoT sensors (ESP32, Arduino, Raspberry Pi):

```cpp
// Arduino/ESP32 Example
#include <WiFi.h>
#include <HTTPClient.h>

String apiKey = "YOUR_WRITE_KEY";
String server = "http://api.thingspeak.com/update";

void uploadData(float soil, float temp, float humid) {
  HTTPClient http;
  String url = server + "?api_key=" + apiKey + 
               "&field1=" + String(soil) + 
               "&field2=" + String(temp) + 
               "&field3=" + String(humid);
  
  http.begin(url);
  int httpCode = http.GET();
  http.end();
}
```

---

## 🔑 Required Environment Variables

### Read API Key (Already Set) ✅
```env
THINGSPEAK_CHANNEL_ID=3245976
THINGSPEAK_READ_KEY=TMRSZ78KDPKVB651
```

### Write API Key (Needed for Uploads) ⚠️
You need to get this from your ThingSpeak account:
1. Login to ThingSpeak
2. Go to your channel (3245976)
3. Click "API Keys"
4. Copy "Write API Key"

---

## 📊 Field Mapping

| ThingSpeak Field | Sensor Type      | Unit  | Range    |
|-----------------|------------------|-------|----------|
| Field 1         | Soil Moisture    | %     | 0-100    |
| Field 2         | Temperature      | °C    | -50 to 60|
| Field 3         | Humidity         | %     | 0-100    |

---

## 🧪 Testing Current Setup

### Test 1: Check Environment Variables
```bash
python test_api.py
```
**Expected Output**:
```
Channel ID: 3245976
Read Key: TMRSZ78KDPKVB651
Status Code: 200
```

### Test 2: View Dashboard (Demo Mode)
1. Go to http://127.0.0.1:8000/
2. You should see:
   - ⚠️ Warning message about using demo data
   - Demo sensor readings (45% moisture, 25.5°C, 65% humidity)
   - AI soil analysis showing "Optimal" classification

### Test 3: Upload Sample Data
```bash
python upload_sample_data.py
```
Then refresh dashboard to see real data.

---

## 🐛 Common Issues & Solutions

### Issue: "Unable to fetch sensor data"
**Cause**: ThingSpeak channel is empty
**Solution**: Upload data using `upload_sample_data.py` or IoT device

### Issue: "Environment variables not set"
**Cause**: `.env` file missing or not loaded
**Solution**: 
1. Verify `.env` file exists in project root
2. Contains: `THINGSPEAK_CHANNEL_ID=3245976`
3. Django settings loads dotenv: `load_dotenv()`

### Issue: "HTTP Error 401" when uploading
**Cause**: Invalid Write API Key
**Solution**: Get correct Write API Key from ThingSpeak dashboard

### Issue: ThingSpeak Rate Limit
**Cause**: Free accounts limited to 1 update per 15 seconds
**Solution**: Wait 15+ seconds between uploads

---

## 🚀 Production Recommendations

1. **Store Historical Data**: Save ThingSpeak responses to Django database
2. **Caching**: Cache API responses (5-minute TTL) to reduce API calls
3. **Webhooks**: Use ThingSpeak webhooks instead of polling
4. **Error Monitoring**: Implement Sentry or similar for production errors
5. **Rate Limiting**: Respect ThingSpeak's API limits (free: 3M msgs/year)

---

## 📈 Next Steps

1. ✅ **Dashboard works with demo data** (Current state)
2. 🔄 **Upload sample data** using `upload_sample_data.py`
3. 🌐 **Refresh dashboard** to see real ThingSpeak data
4. 🔌 **Connect real IoT sensors** for production use
5. 📊 **Add historical charts** for trend analysis

---

## 🆘 Support

If issues persist:
1. Check [test_api.py](test_api.py) output for API connectivity
2. Verify ThingSpeak channel at https://thingspeak.com/channels/3245976
3. Ensure Write API Key is correct for data uploads
4. Check Django server logs for detailed error messages

**Note**: The dashboard now uses demo data automatically when ThingSpeak is empty, so you can test the full UI/UX immediately without real sensor data!
