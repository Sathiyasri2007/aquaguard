#!/usr/bin/env python3
"""
Test script for hotspot functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.hotspot_locations import HotspotAnalyzer
from utils.geo_mapper import GeographicMapper

def test_hotspot_analyzer():
    print("Testing Hotspot Analyzer...")
    
    # Initialize analyzer
    analyzer = HotspotAnalyzer()
    
    # Get risk summary
    summary = analyzer.get_risk_summary()
    print(f"Risk Summary: {summary}")
    
    # Get high risk locations
    high_risk = analyzer.get_high_risk_locations()
    print(f"\nHigh Risk Locations ({len(high_risk)}):")
    for i, loc in enumerate(high_risk[:5]):  # Show first 5
        print(f"{i+1}. {loc['location']}, {loc['state']} (Score: {loc['risk_score']})")
    
    # Get medium risk locations
    medium_risk = analyzer.get_medium_risk_locations()
    print(f"\nMedium Risk Locations ({len(medium_risk)}):")
    for i, loc in enumerate(medium_risk[:3]):  # Show first 3
        print(f"{i+1}. {loc['location']}, {loc['state']} (Score: {loc['risk_score']})")
    
    return analyzer

def test_geo_mapper():
    print("\n" + "="*50)
    print("Testing Geographic Mapper...")
    
    # Initialize mapper
    mapper = GeographicMapper()
    
    # Create risk map
    risk_map = mapper.create_risk_map()
    
    # Save map
    map_file = mapper.save_map(risk_map, 'static/hotspot_risk_map.html')
    print(f"Risk map saved to: {map_file}")
    
    # Test filtered map (only high risk)
    high_risk_map = mapper.create_filtered_risk_map(['High Risk'])
    high_risk_file = mapper.save_map(high_risk_map, 'static/high_risk_only_map.html')
    print(f"High risk map saved to: {high_risk_file}")
    
    return mapper

def main():
    print("Water Contamination Hotspot Analysis Test")
    print("="*50)
    
    try:
        # Test hotspot analyzer
        analyzer = test_hotspot_analyzer()
        
        # Test geo mapper
        mapper = test_geo_mapper()
        
        print("\n" + "="*50)
        print("All tests completed successfully!")
        print("Check the 'static' folder for generated maps.")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()