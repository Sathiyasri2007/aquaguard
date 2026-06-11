from models.water_model import WaterContaminationModel
import os

def test_trained_model():
    # Load the trained model
    model = WaterContaminationModel('trained_water_model.h5')
    
    # Test with clean samples
    clean_dir = r'c:\Users\suvet\OneDrive\Documents\DT\water images\test\Clean-samples'
    print("Testing Clean Water Samples:")
    for i, img_file in enumerate(os.listdir(clean_dir)[:3]):
        if img_file.endswith('.jpg'):
            img_path = os.path.join(clean_dir, img_file)
            result = model.predict(img_path)
            print(f"{img_file}: {result['classification']} ({result['confidence']:.2f})")
    
    # Test with dirty samples  
    dirty_dir = r'c:\Users\suvet\OneDrive\Documents\DT\water images\test\Dirty-samples'
    print("\nTesting Contaminated Water Samples:")
    for i, img_file in enumerate(os.listdir(dirty_dir)[:3]):
        if img_file.endswith('.jpg'):
            img_path = os.path.join(dirty_dir, img_file)
            result = model.predict(img_path)
            print(f"{img_file}: {result['classification']} ({result['confidence']:.2f})")

if __name__ == "__main__":
    test_trained_model()