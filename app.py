import tensorflow as tf
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import scipy.io
import os
from fastapi import HTTPException


# Define the FastAPI app
app = FastAPI()

# Load the trained model
model_path = "resnet50_custom_model.h5"  # Make sure the model is in the correct path inside Docker
model = tf.keras.models.load_model(model_path)

# Load the car class names from the .mat file
mat_path = "cars_annos.mat"  # Ensure this is the correct path to your .mat file
mat_data = scipy.io.loadmat(mat_path)
class_names = mat_data['class_names'][0]  # Adjust the key if needed

# Create a class for the request body format
class CarImage(BaseModel):
    image_path: str  # Path to the image file

# Prediction function

def prepare_image(img_path):
    # Validate the file path
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail=f"Image file not found: {img_path}")

    # Load and preprocess the image
    img = image.load_img(img_path, target_size=(128, 128))  # Adjust target size as needed
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Batch size of 1
    img_array = preprocess_input(img_array)
    return img_array


@app.post("/predict/")
async def predict(car_image: CarImage):
    img_path = car_image.image_path
    
    try:
        # Preprocess the image
        img_array = prepare_image(img_path)

        # Predict class
        predictions = model.predict(img_array)
        
        # Ensure predictions have the correct shape
        if predictions.ndim != 2 or predictions.shape[1] != len(class_names):
            raise ValueError(f"Prediction output shape mismatch. Expected shape: (batch_size, {len(class_names)}), but got: {predictions.shape}")
        
        class_idx = np.argmax(predictions, axis=1)[0]  # Get index of max prediction

        # Ensure the class index is within bounds
        if class_idx >= len(class_names):
            raise ValueError(f"Class index {class_idx} out of bounds. Expected index between 0 and {len(class_names)-1}")

        # Get the predicted class name
        predicted_class_name = class_names[class_idx][0]

        # Return the predicted class name
        return {"predicted_class": predicted_class_name}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"ValueError: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
