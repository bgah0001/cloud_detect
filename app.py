from flask import Flask, request, jsonify
import numpy as np
import base64
from object_detection import ObjectDetector
import io
from PIL import Image

app = Flask(__name__)


@app.route('/api/v1/object/detection', methods=['POST'])
def upload():
    try:
        # validation
        data = request.json
        if 'id' not in data or 'image' not in data:
            return jsonify({"error": "Both 'id' and 'image' are required."}), 400

        # Decode base64 image
        encoded_image = data['image']
        im_bytes = base64.b64decode(encoded_image)  
        im_file = io.BytesIO(im_bytes)  
        img = Image.open(im_file)
        img = np.array(img)
        objectDetector = ObjectDetector()
        
        objects = objectDetector.detectImage(img)
        # Return detected objects
        return jsonify({"id": data['id'], "objects": objects}), 200
    except Exception as e:
         return jsonify({"error": str(e)}), 500

   



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=1024, debug=True)
