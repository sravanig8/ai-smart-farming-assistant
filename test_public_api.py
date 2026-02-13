import requests

# Try reading from ThingSpeak without API key (public channel)
channel_id = "3245976"
url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"

print(f"Testing PUBLIC endpoint: {url}")
response = requests.get(url, params={'results': 2}, timeout=10)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Response: {data}")

# Check if channel is public or private
print(f"\nChannel name: {data.get('channel', {}).get('name')}")
print(f"Last entry ID: {data.get('channel', {}).get('last_entry_id')}")
print(f"Number of feeds: {len(data.get('feeds', []))}")

if data.get('feeds'):
    print("\n✅ Data found!")
    for i, feed in enumerate(data['feeds'], 1):
        print(f"\nFeed {i}:")
        print(f"  Field1 (Soil): {feed.get('field1')}")
        print(f"  Field2 (Temp): {feed.get('field2')}")
        print(f"  Field3 (Humid): {feed.get('field3')}")
        print(f"  Created: {feed.get('created_at')}")
else:
    print("\n❌ No feeds found - channel is empty")
