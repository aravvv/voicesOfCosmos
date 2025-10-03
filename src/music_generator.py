"""
Music generator module for creating space-inspired ambient music from telemetry data
"""
import mido
import numpy as np
from typing import Dict, Any, List
import os
import tempfile
from datetime import datetime

class SpaceMusicGenerator:
    def __init__(self):
        self.tempo = 60  # BPM for ambient space music
        self.duration = 30  # seconds
        self.ticks_per_beat = 480
        
        # Musical scales for different moods
        self.scales = {
            'peaceful': [60, 62, 64, 67, 69, 72, 74, 76],  # C major pentatonic + extensions
            'mysterious': [60, 62, 63, 67, 69, 70, 72, 75],  # C minor with augmented notes
            'cosmic': [60, 64, 67, 71, 74, 77, 81, 84],  # C major 7th extensions
            'ethereal': [60, 65, 67, 72, 74, 79, 81, 86]  # Perfect 4ths and 5ths
        }
    
    def generate_space_music(self, space_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate ambient space music from telemetry data"""
        
        telemetry = space_data.get('telemetry', {})
        iss_location = space_data.get('iss_location', {})
        
        # Map telemetry to musical parameters
        musical_params = self._map_data_to_music(telemetry, iss_location)
        
        # Generate MIDI
        midi_file = self._create_midi_composition(musical_params)
        
        # Save to temporary file
        temp_dir = tempfile.gettempdir()
        filename = f"space_music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mid"
        filepath = os.path.join(temp_dir, filename)
        
        midi_file.save(filepath)
        
        return {
            'filepath': filepath,
            'filename': filename,
            'musical_params': musical_params,
            'description': self._generate_music_description(musical_params, iss_location),
            'generated_at': datetime.now().isoformat()
        }
    
    def _map_data_to_music(self, telemetry: Dict, iss_location: Dict) -> Dict[str, Any]:
        """Map space telemetry to musical parameters"""
        
        # Extract telemetry values with defaults
        altitude = telemetry.get('altitude_km', 408)
        velocity = telemetry.get('velocity_kmh', 27600)
        temperature = telemetry.get('temperature_celsius', 0)
        cosmic_rays = telemetry.get('cosmic_ray_intensity', 1.0)
        solar_efficiency = telemetry.get('solar_panel_efficiency', 90)
        
        # Map region to scale/mood
        region = iss_location.get('region', 'Open Ocean')
        scale_type = self._get_scale_for_region(region)
        
        # Map altitude to octave (higher = higher pitch)
        base_octave = int(np.interp(altitude, [400, 430], [3, 5]))
        
        # Map velocity to rhythm density
        note_density = np.interp(velocity, [27400, 27800], [0.3, 0.8])
        
        # Map temperature to dynamics (volume)
        volume = int(np.interp(temperature, [-160, 130], [40, 100]))
        
        # Map cosmic rays to harmonic complexity
        harmony_complexity = np.interp(cosmic_rays, [0.1, 2.5], [0.2, 0.9])
        
        # Map solar efficiency to brightness (major vs minor tendencies)
        brightness = np.interp(solar_efficiency, [80, 100], [0.3, 1.0])
        
        return {
            'scale_type': scale_type,
            'base_octave': base_octave,
            'note_density': note_density,
            'volume': volume,
            'harmony_complexity': harmony_complexity,
            'brightness': brightness,
            'region': region,
            'tempo': self.tempo
        }
    
    def _get_scale_for_region(self, region: str) -> str:
        """Map Earth regions to musical scales/moods"""
        region_scales = {
            'Pacific Ocean': 'peaceful',
            'Atlantic Ocean': 'peaceful',
            'Indian Ocean': 'ethereal',
            'Arctic Ocean': 'mysterious',
            'Antarctic': 'mysterious',
            'North America': 'cosmic',
            'South America': 'ethereal',
            'Europe': 'cosmic',
            'Africa': 'cosmic',
            'Asia': 'ethereal',
            'Australia': 'peaceful'
        }
        return region_scales.get(region, 'peaceful')
    
    def _create_midi_composition(self, params: Dict[str, Any]) -> mido.MidiFile:
        """Create MIDI composition from musical parameters"""
        
        mid = mido.MidiFile(ticks_per_beat=self.ticks_per_beat)
        track = mido.MidiTrack()
        mid.tracks.append(track)
        
        # Set tempo
        tempo_microseconds = int(60000000 / params['tempo'])
        track.append(mido.MetaMessage('set_tempo', tempo=tempo_microseconds))
        
        # Get scale notes
        scale_notes = self.scales[params['scale_type']]
        base_octave_offset = (params['base_octave'] - 4) * 12
        scale_notes = [note + base_octave_offset for note in scale_notes]
        
        # Generate ambient pad layer
        self._add_ambient_pad(track, scale_notes, params)
        
        # Generate melodic layer
        self._add_melodic_layer(track, scale_notes, params)
        
        # Add some cosmic texture
        if params['harmony_complexity'] > 0.5:
            self._add_cosmic_texture(track, scale_notes, params)
        
        return mid
    
    def _add_ambient_pad(self, track: mido.MidiTrack, scale_notes: List[int], params: Dict):
        """Add sustained ambient pad sounds"""
        
        # Select chord tones
        chord_notes = [scale_notes[0], scale_notes[2], scale_notes[4]]  # Root, 3rd, 5th
        if params['brightness'] > 0.7:
            chord_notes.append(scale_notes[6])  # Add 7th for brightness
        
        volume = max(30, int(params['volume'] * 0.6))  # Softer for pad
        
        # Long sustained notes
        for note in chord_notes:
            track.append(mido.Message('note_on', channel=0, note=note, velocity=volume, time=0))
        
        # Hold for most of the duration
        hold_time = int(self.duration * 0.8 * self.ticks_per_beat * params['tempo'] / 60)
        
        for i, note in enumerate(chord_notes):
            time = hold_time if i == 0 else 0
            track.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=time))
    
    def _add_melodic_layer(self, track: mido.MidiTrack, scale_notes: List[int], params: Dict):
        """Add sparse melodic elements"""
        
        volume = int(params['volume'] * 0.8)
        note_count = int(params['note_density'] * 12)  # Max 12 notes in 30 seconds
        
        # Calculate timing between notes
        total_ticks = int(self.duration * self.ticks_per_beat * params['tempo'] / 60)
        
        current_time = 0
        for i in range(note_count):
            # Select note from scale
            note_index = int(np.random.random() * len(scale_notes))
            note = scale_notes[note_index]
            
            # Note duration (shorter for higher density)
            note_duration = int(total_ticks / (note_count * 2))
            
            # Time to next note
            time_to_note = int(total_ticks / note_count) if i == 0 else int(total_ticks / note_count)
            
            track.append(mido.Message('note_on', channel=1, note=note, velocity=volume, time=time_to_note))
            track.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=note_duration))
    
    def _add_cosmic_texture(self, track: mido.MidiTrack, scale_notes: List[int], params: Dict):
        """Add subtle cosmic texture sounds"""
        
        volume = int(params['volume'] * 0.4)  # Very subtle
        
        # High register sparkles
        high_notes = [note + 24 for note in scale_notes[:4]]  # Two octaves up
        
        texture_count = int(params['harmony_complexity'] * 8)
        total_ticks = int(self.duration * self.ticks_per_beat * params['tempo'] / 60)
        
        for i in range(texture_count):
            note = high_notes[int(np.random.random() * len(high_notes))]
            time_offset = int(np.random.random() * total_ticks)
            duration = int(self.ticks_per_beat / 4)  # Short notes
            
            if i == 0:
                track.append(mido.Message('note_on', channel=2, note=note, velocity=volume, time=time_offset))
            else:
                track.append(mido.Message('note_on', channel=2, note=note, velocity=volume, time=0))
            
            track.append(mido.Message('note_off', channel=2, note=note, velocity=0, time=duration))
    
    def _generate_music_description(self, params: Dict, iss_location: Dict) -> str:
        """Generate a poetic description of the generated music"""
        
        region = params['region']
        scale_type = params['scale_type']
        
        descriptions = {
            'peaceful': f"A serene ambient piece reflecting the tranquil passage over {region}",
            'mysterious': f"Enigmatic tones echoing the mysteries glimpsed above {region}",
            'cosmic': f"Expansive harmonies capturing the cosmic dance over {region}",
            'ethereal': f"Floating melodies inspired by the ethereal beauty of {region} from space"
        }
        
        base_desc = descriptions.get(scale_type, f"Ambient space music inspired by {region}")
        
        if params['harmony_complexity'] > 0.7:
            base_desc += ", with shimmering cosmic textures"
        
        if params['brightness'] > 0.8:
            base_desc += " and uplifting harmonies"
        elif params['brightness'] < 0.4:
            base_desc += " with contemplative, minor undertones"
        
        return base_desc + "."

if __name__ == "__main__":
    # Test with mock data
    mock_data = {
        'telemetry': {
            'altitude_km': 415.2,
            'velocity_kmh': 27580,
            'temperature_celsius': -89,
            'cosmic_ray_intensity': 1.8,
            'solar_panel_efficiency': 92
        },
        'iss_location': {
            'region': 'Pacific Ocean'
        }
    }
    
    generator = SpaceMusicGenerator()
    result = generator.generate_space_music(mock_data)
    print(f"Generated: {result['filename']}")
    print(f"Description: {result['description']}")
    print(f"Musical parameters: {result['musical_params']}")
