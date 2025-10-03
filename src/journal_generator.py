"""
Journal generator module for creating astronaut diary entries using LLM
"""
import os
from typing import Dict, Any
from datetime import datetime
import openai
from dotenv import load_dotenv

load_dotenv()

class AstronautJournalGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def generate_journal_entry(self, space_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate a poetic astronaut journal entry from space data"""
        
        # Extract key information
        iss_location = space_data.get('iss_location', {})
        telemetry = space_data.get('telemetry', {})
        astronauts = space_data.get('astronauts', {})
        
        # Create context for the LLM
        context = self._build_context_prompt(iss_location, telemetry, astronauts)
        
        try:
            # Generate journal entry
            journal_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an astronaut aboard the International Space Station writing in your personal diary. 
                        Write in first person, be poetic and contemplative, focusing on the wonder of space, Earth's beauty, 
                        and the human experience in microgravity. Keep entries between 100-200 words. 
                        Be specific about locations and technical details but make them feel personal and emotional."""
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                max_tokens=300,
                temperature=0.8
            )
            
            journal_text = journal_response.choices[0].message.content.strip()
            
            # Generate title
            title_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Create a poetic, evocative title for an astronaut's journal entry. 
                        The title should be 3-8 words and capture the essence of the experience. 
                        Examples: "Whispers Over the Pacific", "Dancing with Aurora", "Silence Above the Sahara"."""
                    },
                    {
                        "role": "user",
                        "content": f"Create a title for this journal entry: {journal_text[:200]}..."
                    }
                ],
                max_tokens=50,
                temperature=0.9
            )
            
            title = title_response.choices[0].message.content.strip().replace('"', '')
            
            return {
                'title': title,
                'journal_entry': journal_text,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating journal entry: {e}")
            return self._get_fallback_journal_entry(iss_location, telemetry)
    
    def _build_context_prompt(self, iss_location: Dict, telemetry: Dict, astronauts: Dict) -> str:
        """Build context prompt for LLM"""
        region = iss_location.get('region', 'Unknown region')
        lat = iss_location.get('latitude', 0)
        lon = iss_location.get('longitude', 0)
        altitude = telemetry.get('altitude_km', 408)
        velocity = telemetry.get('velocity_kmh', 27600)
        temperature = telemetry.get('temperature_celsius', 0)
        cosmic_rays = telemetry.get('cosmic_ray_intensity', 1.0)
        crew_count = astronauts.get('count', 7)
        
        time_of_day = self._get_time_context()
        
        prompt = f"""Current situation aboard the ISS:
        
Location: Flying over {region} at coordinates {lat:.2f}°, {lon:.2f}°
Altitude: {altitude} km above Earth
Velocity: {velocity:,} km/h
External temperature: {temperature}°C
Cosmic ray intensity: {cosmic_rays}
Crew members aboard: {crew_count}
Time context: {time_of_day}

Write a personal diary entry reflecting on this moment in space, the view of Earth below, 
the technical aspects of the mission, and the emotional experience of being in orbit."""
        
        return prompt
    
    def _get_time_context(self) -> str:
        """Get contextual time information"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Morning watch - Earth awakening below"
        elif 12 <= hour < 17:
            return "Afternoon orbit - Sun illuminating continents"
        elif 17 <= hour < 21:
            return "Evening pass - City lights beginning to twinkle"
        else:
            return "Night shift - Darkness revealing Earth's glow"
    
    def _get_fallback_journal_entry(self, iss_location: Dict, telemetry: Dict) -> Dict[str, str]:
        """Fallback journal entry if API fails"""
        region = iss_location.get('region', 'the vast ocean')
        altitude = telemetry.get('altitude_km', 408)
        
        return {
            'title': f"Reflections Above {region.title()}",
            'journal_entry': f"""Another orbit complete, another moment of wonder. 
            
            Today finds us {altitude} kilometers above {region}, moving through the cosmos at impossible speeds yet feeling perfectly still. The silence up here is profound - broken only by the gentle hum of life support systems that keep us tethered to existence.
            
            Looking down at Earth, I'm struck by how fragile and beautiful our home appears. No borders visible from this height, just the flowing blues and greens of a living world. The solar panels catch the light just right, and for a moment, everything feels perfectly aligned.
            
            These moments remind me why we're here - not just as explorers, but as witnesses to the extraordinary.""",
            'generated_at': datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Test with mock data
    mock_data = {
        'iss_location': {'region': 'Pacific Ocean', 'latitude': 25.5, 'longitude': -150.2},
        'telemetry': {'altitude_km': 415.2, 'velocity_kmh': 27580, 'temperature_celsius': -89},
        'astronauts': {'count': 7}
    }
    
    generator = AstronautJournalGenerator()
    entry = generator.generate_journal_entry(mock_data)
    print(f"Title: {entry['title']}")
    print(f"Entry: {entry['journal_entry']}")
