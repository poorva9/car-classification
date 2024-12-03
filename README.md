
# Car Classification API

This repository contains a FastAPI application for car classification using a custom-trained ResNet50 model. The API allows you to upload an image and get predictions about the car class.

## Requirements

- Docker
- Docker Compose (optional)

## Step-by-Step Setup and Usage

Follow the steps below to build and run the Docker container, and interact with the API via Swagger UI.

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/poorva9/car-classification
cd car-classification
```
- Download Model from https://drive.google.com/file/d/1duR13J9aXVjqdMCRfAtnjORiOUKkMrdr/view?usp=sharing , add it to the root folder (too large to be added into github repo)
- Access Dataset from https://www.kaggle.com/datasets/jessicali9530/stanford-cars-dataset 

### 2. Build the Docker Image

Make sure you are in the project directory (where the `Dockerfile` is located), then build the Docker image with the following command:

```bash
docker build -t car-classification-api .
```

This command will create a Docker image with the name `car-classification-api`.

### 3. Run the Docker Container

Once the image is built, run the following command to start the Docker container:

```bash
docker run -d -p 8000:8000 car-classification-api
```

This command will:
- Run the container in detached mode (`-d`).
- Map port `8000` from your local machine to port `8000` inside the Docker container.
- Start the FastAPI app, which will be accessible at `http://127.0.0.1:8000`.

### 4. Verify the Container is Running

To confirm the container is running, use the following command:

```bash
docker ps
```

You should see your container listed with the name `car-classification-api`.

### 5. Access the FastAPI Documentation (Swagger UI)

After the container is running, you can access the FastAPI interactive documentation at the following URL:

```
http://127.0.0.1:8000/docs
```

### 6. Generate Prediction Output

Follow these steps to generate a car classification prediction from the API:

1. Open `http://127.0.0.1:8000/docs` in your browser.
2. Scroll to the `POST /predict/` endpoint and click on it to expand.
3. Under the `Request body` section, click on `Try it out`.
4. In the `image_path` field, enter the absolute path to the image you want to classify in **Unix format** (e.g., `/app/cars_train/cars_train/08141.jpg`).

   - If your images are located inside the Docker container, ensure the `image_path` matches the container's file system.
   - Example: For an image stored in `C:/Users/poorv/Downloads/car_classification/cars_train/08141.jpg`, the corresponding path inside the container might be `/app/cars_train/cars_train/08141.jpg`.

5. Click `Execute` to send the request to the API.

The response will contain the predicted car class.

### 7. Example Response

If everything is set up correctly, you should receive a response like the following:

```json
{
  "predicted_class": "car_class_name"
}
```

Where `"car_class_name"` is the name of the predicted class for the uploaded image.

### 8. Stopping the Container

To stop the container, run the following command:

```bash
docker stop <container-id>
```

You can find the `container-id` by running `docker ps`.

### 9. Clean Up

If you no longer need the image and container, you can remove them using the following commands:

1. Stop the container:

   ```bash
   docker stop <container-id>
   ```

2. Remove the container:

   ```bash
   docker rm <container-id>
   ```

3. Remove the image:

   ```bash
   docker rmi car-classification-api
   ```

## Troubleshooting

- **Image File Not Found Error**: If you see a "file not found" error for the image in the API, make sure the path is correct, and the file is available inside the Docker container.
- **Port Conflicts**: If port `8000` is already in use on your machine, you can map the container's port to another local port by using the following command:

   ```bash
   docker run -d -p 5000:8000 car-classification-api
   ```

   This will map port `8000` inside the container to port `5000` on your local machine.

## Conclusion

You now have a working `car-classification-api` deployed in a Docker container. You can send image paths to the `POST /predict/` endpoint to get car class predictions through Swagger UI.
