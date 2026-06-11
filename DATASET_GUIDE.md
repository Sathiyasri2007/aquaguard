# Using Your Stagnant Water and Wet Surface Dataset

## Dataset Location
`c:\Users\suvet\OneDrive\Documents\DT\Stagnant water and Wet surface Dataset`

## Quick Start

### 1. Analyze Dataset
```bash
python analyze_dataset.py
```
This will:
- Count total images
- Show categories
- Save analysis to `dataset_analysis.json`

### 2. Train Model with Your Dataset
```bash
python train_model.py
```
This will:
- Load images from your dataset
- Train CNN model (20 epochs)
- Save trained model as `trained_water_model.h5`
- Takes 30-60 minutes depending on dataset size

### 3. Use Trained Model
The backend automatically uses `trained_water_model.h5` if it exists.

```bash
python backend/app.py
```

## Dataset Structure Expected

The trainer automatically maps folders to contamination levels:
- **Stagnant/Contaminated** → Contaminated (Class 2)
- **Wet/Moderate** → Possibly Contaminated (Class 1)
- **Clean/Safe** → Safe (Class 0)

## Training Parameters

Edit `train_model.py` to adjust:
- `epochs=20` - Number of training iterations
- `batch_size=32` - Images per batch
- `max_per_category=500` - Max images per category

## Model Performance

After training, the model will:
- Show training/validation accuracy
- Save best weights
- Be ready for real-time predictions

## Integration with System

Once trained, the model is automatically used by:
- `backend/app.py` - API server
- `test_system.py` - Testing script
- `frontend/index.html` - Dashboard

## Quick Commands

```bash
# Analyze dataset
python analyze_dataset.py

# Train model (takes time!)
python train_model.py

# Test with trained model
python test_system.py

# Start backend with trained model
python backend/app.py
```

## Notes

- Training requires TensorFlow and sufficient RAM
- First run will take longer (loading images)
- Model improves with more training epochs
- Validation accuracy shows real performance
