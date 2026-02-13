"""
Dashboard views for Smart Farming Assistant.

Handles rendering of the main dashboard with real-time sensor data
and AI-powered soil analysis.
"""
from django.shortcuts import render
from django.http import JsonResponse
from iot_integration.thingspeak_api import get_sensor_data
from agents.soil_agent import SoilAnalysisAgent


def dashboard_view(request):
    """
    Main dashboard view that displays real-time sensor data and soil analysis.
    
    Fetches data from:
    1. ThingSpeak API - sensor readings (soil moisture, temperature, humidity)
    2. SoilAnalysisAgent - AI analysis of soil conditions
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered dashboard template with context data
    """
    context = {
        'sensor_data': None,
        'soil_analysis': None,
        'error_message': None,
        'data_available': False
    }
    
    try:
        # Fetch sensor data from ThingSpeak
        sensor_data = get_sensor_data()
        
        if sensor_data is None:
            context['error_message'] = (
                "📡 DEMO MODE: Using sample data for testing. "
                "ThingSpeak channel 3245976 has no sensor data yet. "
                "To use real data, please update .env with YOUR ThingSpeak channel credentials."
            )
            # Use demo data for testing when ThingSpeak has no data
            sensor_data = {
                'soil_moisture': 45.0,
                'temperature': 25.5,
                'humidity': 65.0,
                'timestamp': 'Demo Data (Not Real-time)',
                'success': True
            }
            context['sensor_data'] = sensor_data
            context['data_available'] = True
            
            # Still analyze the demo data
            soil_analysis_agent = SoilAnalysisAgent(sensor_data['soil_moisture'])
            soil_analysis = soil_analysis_agent.analyze()
            context['soil_analysis'] = soil_analysis
            
            return render(request, 'dashboard/dashboard.html', context)
        
        # Validate sensor data structure
        if not sensor_data.get('success'):
            context['error_message'] = "Sensor data fetch returned unsuccessful status"
            return render(request, 'dashboard/dashboard.html', context)
        
        context['sensor_data'] = sensor_data
        
        # Analyze soil conditions using AI agent
        soil_analysis_agent = SoilAnalysisAgent(sensor_data['soil_moisture'])
        soil_analysis = soil_analysis_agent.analyze()
        context['soil_analysis'] = soil_analysis
        
        # Data successfully fetched and processed
        context['data_available'] = True
        
    except ValueError as e:
        # Handle validation errors
        context['error_message'] = f"Validation Error: {str(e)}"
    except Exception as e:
        # Handle unexpected errors
        context['error_message'] = f"Unexpected Error: {str(e)}"
    
    return render(request, 'dashboard/dashboard.html', context)

