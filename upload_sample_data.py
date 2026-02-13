"""
Script to upload sample sensor data to ThingSpeak channel.
This simulates IoT sensor readings for testing purposes.
"""
import os
from dotenv import load_dotenv
import requests
import time
import random

load_dotenv()

# ThingSpeak credentials
CHANNEL_ID = os.getenv('THINGSPEAK_CHANNEL_ID')
WRITE_KEY = input("Enter your THINGSPEAK_WRITE_KEY: ").strip()

if not WRITE_KEY:
    print("❌ Write key is required to upload data to ThingSpeak")
    exit(1)

BASE_URL = "https://api.thingspeak.com/update"

def upload_sample_data():
    """Upload sample sensor data to ThingSpeak."""
    
    # Simulate realistic sensor readings
    soil_moisture = round(random.uniform(25, 65), 1)  # 25-65% moisture
    temperature = round(random.uniform(18, 32), 1)    # 18-32°C
    humidity = round(random.uniform(40, 80), 1)       # 40-80% humidity
    
    params = {
        'api_key': WRITE_KEY,
        'field1': soil_moisture,
        'field2': temperature,
        'field3': humidity
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            entry_id = response.text.strip()
            if entry_id != '0':
                print(f"✅ Data uploaded successfully! Entry ID: {entry_id}")
                print(f"   Soil Moisture: {soil_moisture}%")
                print(f"   Temperature: {temperature}°C")
                print(f"   Humidity: {humidity}%")
                return True
            else:
                print("❌ Failed to upload (Entry ID = 0). Check your Write API Key.")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error uploading data: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("ThingSpeak Sample Data Uploader")
    print("=" * 60)
    print(f"Channel ID: {CHANNEL_ID}\n")
    
    # Upload 3 sample readings (ThingSpeak has 15-second rate limit)
    for i in range(3):
        print(f"\nUpload {i+1}/3:")
        upload_sample_data()
        
        if i < 2:  # Don't wait after the last upload
            print("⏳ Waiting 16 seconds (ThingSpeak rate limit)...")
            time.sleep(16)
    
    print("\n" + "=" * 60)
    print("✅ Sample data upload complete!")
    print("🌐 Refresh your dashboard at http://127.0.0.1:8000/")
    print("=" * 60)
