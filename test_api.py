import os
from dotenv import load_dotenv
import requests

load_dotenv()

channel_id = os.getenv('THINGSPEAK_CHANNEL_ID')
read_key = os.getenv('THINGSPEAK_READ_KEY')

print(f"Channel ID: {channel_id}")
print(f"Read Key: {read_key}")

if channel_id and read_key:
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {
        'api_key': read_key,
        'results': 2
    }
    
    try:
        print(f"\nFetching from: {url}")
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        print(f"\nChannel Info:")
        print(f"  Name: {data.get('channel', {}).get('name')}")
        print(f"  Last Entry ID: {data.get('channel', {}).get('last_entry_id')}")
        print(f"  Field1: {data.get('channel', {}).get('field1')}")
        print(f"  Field2: {data.get('channel', {}).get('field2')}")
        print(f"  Field3: {data.get('channel', {}).get('field3')}")
        
        feeds = data.get('feeds', [])
        print(f"\nFeeds: {len(feeds)} entries found")
        
        if feeds:
            print("\n✅ Latest Data:")
            latest = feeds[-1]
            print(f"  Soil Moisture: {latest.get('field1')}%")
            print(f"  Temperature: {latest.get('field2')}°C")
            print(f"  Humidity: {latest.get('field3')}%")
            print(f"  Timestamp: {latest.get('created_at')}")
        else:
            print("\n❌ No data in channel yet")
            
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Environment variables not set!")
