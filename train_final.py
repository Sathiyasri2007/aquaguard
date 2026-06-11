import tensorflow as tf
import numpy as np
import os
import cv2
from sklearn.utils.class_weight import compute_class_weight

def load_balanced_data():
    train_dir = r'c:\Users\suvet\OneDrive\Documents\DT\water images\train'
    test_dir = r'c:\Users\suvet\OneDrive\Documents\DT\water images\test'
    
    X_train, y_train = [], []
    X_test, y_test = [], []
    
    # Load training data
    for class_idx, folder in enumerate(['Clean-samples', 'Dirty-samples']):
        folder_path = os.path.join(train_dir, folder)
        for img_file in os.listdir(folder_path):
            if img_file.endswith('.jpg'):
                img = cv2.imread(os.path.join(folder_path, img_file))
                img = cv2.resize(img, (224, 224)) / 255.0
                X_train.append(img)
                y_train.append(class_idx)
    
    # Load test data
    for class_idx, folder in enumerate(['Clean-samples', 'Dirty-samples']):
        folder_path = os.path.join(test_dir, folder)
        for img_file in os.listdir(folder_path):
            if img_file.endswith('.jpg'):
                img = cv2.imread(os.path.join(folder_path, img_file))
                img = cv2.resize(img, (224, 224)) / 255.0
                X_test.append(img)
                y_test.append(class_idx)
    
    return np.array(X_train), np.array(y_train), np.array(X_test), np.array(y_test)

def train_proper_model():
    X_train, y_train, X_test, y_test = load_balanced_data()
    
    # Convert to categorical
    y_train_cat = tf.keras.utils.to_categorical(y_train, 2)
    y_test_cat = tf.keras.utils.to_categorical(y_test, 2)
    
    # Calculate class weights for balanced training
    class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
    class_weight_dict = {i: class_weights[i] for i in range(len(class_weights))}
    
    # Build model
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(2, activation='softmax')
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train with class weights
    model.fit(
        X_train, y_train_cat,
        epochs=50,
        batch_size=8,
        validation_data=(X_test, y_test_cat),
        class_weight=class_weight_dict
    )
    
    model.save('trained_water_model.h5')
    print("Model trained and saved!")

if __name__ == "__main__":
    train_proper_model()