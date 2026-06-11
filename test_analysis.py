import os
import sys
sys.path.append('.')

from models.water_model import WaterContaminationModel

def test_analysis():
    # Load model
    model = WaterContaminationModel('trained_water_model.h5' if os.path.exists('trained_water_model.h5') else None)
    
    # Test on dirty samples
    dirty_dir = 'water images/test/Dirty-samples'
    clean_dir = 'water images/test/Clean-samples'
    
    print("Testing Dirty Water Samples:")
    print("-" * 40)
    
    if os.path.exists(dirty_dir):
        for img_file in os.listdir(dirty_dir)[:3]:  # Test first 3 images
            img_path = os.path.join(dirty_dir, img_file)
            result = model.predict(img_path)
            print(f"{img_file}: {result['classification']} (confidence: {result['confidence']:.2f})")
            print(f"  Indicators: {result['indicators']}")
            print(f"  Contamination Score: {result['contamination_score']:.2f}")
            print()
    
    print("Testing Clean Water Samples:")
    print("-" * 40)
    
    if os.path.exists(clean_dir):
        for img_file in os.listdir(clean_dir)[:3]:  # Test first 3 images
            img_path = os.path.join(clean_dir, img_file)
            result = model.predict(img_path)
            print(f"{img_file}: {result['classification']} (confidence: {result['confidence']:.2f})")
            print(f"  Indicators: {result['indicators']}")
            print(f"  Contamination Score: {result['contamination_score']:.2f}")
            print()

if __name__ == '__main__':
    test_analysis()