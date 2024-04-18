# Import necessary libraries
import cv2  # Library for computer vision tasks
import numpy as np  # Library for numerical computing

# Define a class called ObjectDetector
class ObjectDetector:
    def __init__(self):
        # Load classes for detection
        self.classes = self.loadClasses()
        # Load YOLO (You Only Look Once) model
        self.output_layers = self.loadYolo()

    # Method to load YOLO model
    def loadYolo(self):
        # Load YOLO model with pre-trained weights and configuration
        self.yolo = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
        # Get the names of the output layers
        layer_names = self.yolo.getLayerNames()
        # Return the names of the output layers
        return [layer_names[i - 1] for i in self.yolo.getUnconnectedOutLayers()]
      
    # Method to load classes for detection
    def loadClasses(self):
        # Open the file containing the names of the classes
        with open("coco.names", "r") as f:
            # Read lines and remove whitespace
            return [line.strip() for line in f.readlines()]
        
    # Method to load image for detection
    def loadImage(self, img):
        # Preprocess the input image for YOLO model
        return cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
       
    # Method to detect objects in an image
    def detectImage(self, img):
        # Preprocess the input image
        blob = self.loadImage(img)
        # Set the input for YOLO model
        self.yolo.setInput(blob)
        # Perform forward pass through the YOLO model
        outs = self.yolo.forward(self.output_layers)
        # Initialize a list to store detected objects
        objects = []
        # Get the dimensions of the input image
        height, width, channels = img.shape
        # Loop through the outputs of the YOLO model
        for out in outs:
            # Loop through each detection in the output
            for detection in out:
                # Extract confidence scores for each class
                scores = detection[5:]
                # Get the class ID with the highest score
                class_id = np.argmax(scores)
                # Get the confidence score for the detected class
                confidence = scores[class_id]
                # Check if the confidence score is above a threshold
                if confidence > 0:
                    # Calculate the coordinates of the bounding box
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    # Create a dictionary to store information about the detected object
                    object = {
                        "label": self.classes[class_id],  # Get the label of the detected class
                        "accuracy": float(confidence),    # Store the confidence score
                        "rectangle": [x, y, w, h]         # Store the coordinates of the bounding box
                    }
                    # Append the detected object to the list
                    objects.append(object)
        # Return the list of detected objects
        return objects
