# train_model.py
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Ensure the models directory exists
os.makedirs("models", exist_ok=True)

# --- Step 1: Prepare a Synthetic Dataset ---
# For demonstration, we simulate a dataset.
# Let's assume each signal is represented by 10 features, and we have 5 classes.
num_samples = 1000
num_features = 10
num_classes = 5

# Generate synthetic feature data (values between 0 and 1)
X = np.random.rand(num_samples, num_features).astype(np.float32)

# Generate synthetic labels (integer classes between 0 and 4)
y = np.random.randint(0, num_classes, size=(num_samples,))
y = keras.utils.to_categorical(y, num_classes)  # One-hot encode the labels

# --- Step 2: Define and Train a Simple Model ---
model = keras.Sequential([
    layers.Input(shape=(num_features,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print("Starting model training...")
model.fit(X, y, epochs=20, batch_size=32, validation_split=0.2)

# Evaluate the model (optional)
loss, accuracy = model.evaluate(X, y)
print("Training complete. Model accuracy: {:.2f}%".format(accuracy * 100))

# --- Step 3: Save the Trained Keras Model ---
keras_model_path = "models/signal_classifier.h5"
model.save(keras_model_path)
print("Keras model saved to:", keras_model_path)

# --- Step 4: Convert the Keras Model to TFLite ---
converter = tf.lite.TFLiteConverter.from_keras_model(model)
# Optionally, enable optimizations:
# converter.optimizations = [tf.lite.Optimize.DEFAULT]

tflite_model = converter.convert()
tflite_model_path = "models/signal_classifier.tflite"
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)
print("TFLite model saved to:", tflite_model_path)
