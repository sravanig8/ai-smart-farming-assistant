"""
ThingSpeak API integration module.

Fetches real-time sensor data from ThingSpeak cloud platform.
Uses environment variables for API credentials to prevent hardcoding.
"""
import os
import requests
from typing import Dict, Optional, Tuple


class ThingSpeakAPI:
    """
    Handles communication with ThingSpeak API.
    
    Attributes:
        channel_id: ThingSpeak channel ID (from environment variable)
        read_key: ThingSpeak read API key (from environment variable)
        base_url: ThingSpeak API base URL
    """
    
    BASE_URL = "https://api.thingspeak.com/channels"
    TIMEOUT = 10  # Request timeout in seconds
    
    def __init__(self):
        """Initialize ThingSpeak API client with environment variables."""
        self.channel_id = os.getenv('THINGSPEAK_CHANNEL_ID')
        self.read_key = os.getenv('THINGSPEAK_READ_KEY')
        
        if not self.channel_id or not self.read_key:
            raise ValueError(
                "Environment variables 'THINGSPEAK_CHANNEL_ID' and "
                "'THINGSPEAK_READ_KEY' must be set."
            )
    
    def fetch_latest_data(self) -> Optional[Dict]:
        """
        Fetch the latest sensor data from ThingSpeak.
        
        Returns:
            Dictionary containing parsed sensor data:
            {
                'soil_moisture': float,  # Field 1 - soil moisture percentage
                'temperature': float,    # Field 2 - temperature in Celsius
                'humidity': float,       # Field 3 - humidity percentage
                'timestamp': str,        # Data collection timestamp
                'success': bool
            }
            None if API request fails.
        """
        try:
            url = f"{self.BASE_URL}/{self.channel_id}/feeds.json"
            params = {
                'api_key': self.read_key,
                'results': 1  # Get only the latest entry
            }
            
            response = requests.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()  # Raise exception for bad status codes
            
            data = response.json()
            
            # Validate response structure
            if not data.get('feeds'):
                raise ValueError(
                    "No sensor data available from ThingSpeak channel. "
                    "The channel exists but has no data entries. "
                    "Please upload sensor data using the ThingSpeak Write API first."
                )
            
            # Parse the latest feed entry
            latest_feed = data['feeds'][0]
            
            # Extract field values with error handling
            parsed_data = self._parse_feed_fields(latest_feed)
            
            return parsed_data
        
        except requests.exceptions.Timeout:
            print("Error: ThingSpeak API request timed out")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Connection error while fetching ThingSpeak data")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            return None
        except ValueError as e:
            print(f"Data Validation Error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching ThingSpeak data: {str(e)}")
            return None
    
    @staticmethod
    def _parse_feed_fields(feed: Dict) -> Dict:
        """
        Parse ThingSpeak feed fields into sensor data.
        
        Args:
            feed: Raw feed dictionary from ThingSpeak API
            
        Returns:
            Dictionary with parsed sensor values
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        try:
            # Field mappings
            soil_moisture = feed.get('field1')
            temperature = feed.get('field2')
            humidity = feed.get('field3')
            timestamp = feed.get('created_at')
            
            # Validate that at least soil moisture exists
            if soil_moisture is None or soil_moisture == '':
                raise ValueError(
                    "Missing required sensor field (field1: soil_moisture)"
                )
            
            # Convert soil moisture to float
            soil_moisture = float(soil_moisture)
            
            # Handle optional temperature and humidity fields
            # Use default values if not available
            if temperature is None or temperature == '':
                temperature = 25.0  # Default temperature
            else:
                temperature = float(temperature)
            
            if humidity is None or humidity == '':
                humidity = 60.0  # Default humidity
            else:
                humidity = float(humidity)
            
            # Validate sensor value ranges (realistic bounds)
            if not (0 <= soil_moisture <= 100):
                raise ValueError(f"Soil moisture {soil_moisture}% out of valid range (0-100)")
            if not (-50 <= temperature <= 60):
                raise ValueError(f"Temperature {temperature}°C out of realistic range (-50 to 60)")
            if not (0 <= humidity <= 100):
                raise ValueError(f"Humidity {humidity}% out of valid range (0-100)")
            
            return {
                'soil_moisture': soil_moisture,
                'temperature': temperature,
                'humidity': humidity,
                'timestamp': timestamp,
                'success': True
            }
        
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to parse feed fields: {str(e)}")


def get_sensor_data() -> Optional[Dict]:
    """
    Convenience function to fetch sensor data from ThingSpeak.
    
    Returns:
        Dictionary with sensor data or None if fetch fails
    """
    try:
        api = ThingSpeakAPI()
        return api.fetch_latest_data()
    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
        return None
