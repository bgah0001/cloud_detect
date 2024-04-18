# Import necessary libraries
from flask import Flask, request, jsonify  # Import Flask framework for building web applications
import numpy as np  # Import NumPy library for numerical computing
import base64  # Import base64 library for encoding and decoding data
from object_detection import ObjectDetector  # Import ObjectDetector class from object_detection module
import io  # Import io module for working with streams
from PIL import Image  # Import Image module from PIL (Python Imaging Library) for image processing

# Create a Flask web application instance
app = Flask(__name__)

# Define a route for handling POST requests to '/api/v1/object/detection'
@app.route('/api/v1/object/detection', methods=['POST'])
def upload():
    try:
        # Validation: Check if 'id' and 'image' are present in the request data
        data = request.json
        if 'id' not in data or 'image' not in data:
            # If either 'id' or 'image' is missing, return an error response
            return jsonify({"error": "Both 'id' and 'image' are required."}), 400

        # Decode base64 encoded image
        encoded_image = data['image']  # Get the base64 encoded image data from the request
        im_bytes = base64.b64decode(encoded_image)  # Decode the base64 encoded image data
        im_file = io.BytesIO(im_bytes)  # Create a binary stream (BytesIO object) from the decoded image data
        img = Image.open(im_file)  # Open the image using PIL (Python Imaging Library)
        img = np.array(img)  # Convert the image to a NumPy array
        objectDetector = ObjectDetector()  # Create an instance of the ObjectDetector class
        
        # Detect objects in the image using the ObjectDetector instance
        objects = objectDetector.detectImage(img)
        
        # Return detected objects as a JSON response
        return jsonify({"id": data['id'], "objects": objects}), 200
    except Exception as e:
        # If an exception occurs during processing, return an error response
        return jsonify({"error": str(e)}), 500

# Run the Flask web application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1024, debug=True)  # Start the Flask application on host '0.0.0.0' and port 1024 in debug mode
