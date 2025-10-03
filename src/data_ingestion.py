"""
Data ingestion module for fetching ISS and space data from NASA APIs
"""
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional

class SpaceDataFetcher:
    def __init__(self):
        self.iss_api_url = "http://api.open-notify.org/iss-now.json"
        self.astronauts_api_url = "http://api.open-notify.org/astros.json"
        self.nasa_api_base = "https://api.nasa.gov"
        
    def get_iss_location(self) -> Dict[str, Any]:
        """Fetch current ISS location"""
        try:
            response = requests.get(self.iss_api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('message') == 'success':
                position = data['iss_position']
                return {
                    'latitude': float(position['latitude']),
                    'longitude': float(position['longitude']),
                    'timestamp': data['timestamp'],
                    'region': self._get_region_from_coordinates(
                        float(position['latitude']), 
                        float(position['longitude'])
                    )
                }
        except Exception as e:
            print(f"Error fetching ISS location: {e}")
            return self._get_mock_iss_data()
    
    def get_astronauts_info(self) -> Dict[str, Any]:
        """Fetch current astronauts in space"""
        try:
            response = requests.get(self.astronauts_api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('message') == 'success':
                return {
                    'count': data['number'],
                    'astronauts': data['people'],
                    'timestamp': datetime.now().timestamp()
                }
        except Exception as e:
            print(f"Error fetching astronauts info: {e}")
            return self._get_mock_astronauts_data()
    
    def get_space_telemetry(self) -> Dict[str, Any]:
        """Generate mock telemetry data for MVP"""
        import random
        
        return {
            'altitude_km': round(random.uniform(408, 420), 2),
            'velocity_kmh': round(random.uniform(27500, 27700), 2),
            'solar_panel_efficiency': round(random.uniform(85, 95), 1),
            'cosmic_ray_intensity': round(random.uniform(0.1, 2.5), 2),
            'temperature_celsius': round(random.uniform(-157, 121), 1),
            'timestamp': datetime.now().timestamp()
        }
    
    def _get_region_from_coordinates(self, lat: float, lon: float) -> str:
        """Map coordinates to Earth regions"""
        regions = {
            'Pacific Ocean': (lat > -60 and lat < 60 and lon > -180 and lon < -80),
            'Atlantic Ocean': (lat > -60 and lat < 60 and lon > -80 and lon < 20),
            'Indian Ocean': (lat > -60 and lat < 30 and lon > 20 and lon < 147),
            'Arctic Ocean': (lat > 66),
            'Antarctic': (lat < -60),
            'North America': (lat > 15 and lat < 72 and lon > -168 and lon < -52),
            'South America': (lat > -56 and lat < 15 and lon > -82 and lon < -34),
            'Europe': (lat > 35 and lat < 72 and lon > -10 and lon < 40),
            'Africa': (lat > -35 and lat < 37 and lon > -18 and lon < 52),
            'Asia': (lat > -10 and lat < 82 and lon > 26 and lon < 180),
            'Australia': (lat > -44 and lat < -10 and lon > 113 and lon < 154),
        }
        
        for region, condition in regions.items():
            if condition:
                return region
        
        return 'Open Ocean'
    
    def _get_mock_iss_data(self) -> Dict[str, Any]:
        """Fallback mock data if API fails"""
        import random
        return {
            'latitude': round(random.uniform(-51.6, 51.6), 4),
            'longitude': round(random.uniform(-180, 180), 4),
            'timestamp': datetime.now().timestamp(),
            'region': 'Pacific Ocean'
        }
    
    def _get_mock_astronauts_data(self) -> Dict[str, Any]:
        """Fallback mock astronaut data"""
        return {
            'count': 7,
            'astronauts': [
                {'name': 'Mock Astronaut', 'craft': 'ISS'}
            ],
            'timestamp': datetime.now().timestamp()
        }
    
    def get_complete_space_data(self) -> Dict[str, Any]:
        """Fetch all space data for journal entry generation"""
        return {
            'iss_location': self.get_iss_location(),
            'astronauts': self.get_astronauts_info(),
            'telemetry': self.get_space_telemetry(),
            'generated_at': datetime.now().isoformat()
        }

if __name__ == "__main__":
    fetcher = SpaceDataFetcher()
    data = fetcher.get_complete_space_data()
    print(json.dumps(data, indent=2))
