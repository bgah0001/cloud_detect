from locust import HttpUser, task, between
import base64
import os
import uuid
import base64
import random

class APILoadTest(HttpUser):
    wait_time = between(1, 3)  # Random wait time between requests

    @task
    def access_api(self):
        # Read images from a directory
        image_dir = "../images"
        images = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, img))]

        if images:
            # Select a random image
            image_path = random.choice(images)
            encoded_image = ""
            # Convert the image to base64
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
           
            quid = str(uuid.uuid4())
            
            # Send the image to the API
            json_data = {
                "id": quid,
                "image": encoded_image
            }
            headers = {'Content-Type': 'application/json'}
            response = self.client.post("/upload", json=json_data, headers=headers)
    

    def on_start(self):
        print("Starting load test")
