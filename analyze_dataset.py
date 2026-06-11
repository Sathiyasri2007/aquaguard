import os
import cv2
import numpy as np
from pathlib import Path
import json

class DatasetAnalyzer:
    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)
        self.analysis = {}
        
    def analyze(self):
        print("Analyzing Stagnant Water and Wet Surface Dataset...")
        
        # Count images by category
        categories = {}
        total_images = 0
        
        for root, dirs, files in os.walk(self.dataset_path):
            image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            if image_files:
                category = os.path.basename(root)
                categories[category] = len(image_files)
                total_images += len(image_files)
        
        self.analysis = {
            'total_images': total_images,
            'categories': categories,
            'dataset_path': str(self.dataset_path)
        }
        
        print(f"\nDataset Analysis:")
        print(f"Total Images: {total_images}")
        print(f"\nCategories:")
        for cat, count in categories.items():
            print(f"  - {cat}: {count} images")
        
        return self.analysis
    
    def get_sample_images(self, category=None, num_samples=5):
        samples = []
        for root, dirs, files in os.walk(self.dataset_path):
            if category and category not in root:
                continue
            image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            for img_file in image_files[:num_samples]:
                samples.append(os.path.join(root, img_file))
            if len(samples) >= num_samples:
                break
        return samples
    
    def save_analysis(self, output_file='dataset_analysis.json'):
        with open(output_file, 'w') as f:
            json.dump(self.analysis, f, indent=2)
        print(f"\nAnalysis saved to {output_file}")

if __name__ == '__main__':
    dataset_path = r"c:\Users\suvet\OneDrive\Documents\DT\Stagnant water and Wet surface Dataset"
    
    analyzer = DatasetAnalyzer(dataset_path)
    analysis = analyzer.analyze()
    analyzer.save_analysis()
    
    print("\n" + "="*60)
    print("Dataset ready for training!")
    print("="*60)
