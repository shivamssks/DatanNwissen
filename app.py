from flask import Flask, request
from flask_restful import Api, Resource
import os
from ultralytics import YOLO
import numpy as np

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = YOLO('best.pt')
clsss = {0: 'Car', 1: 'Person'}
def allowed_file(filename):
    """
    Function to check if a file has an allowed extension
    """
    # Function to check if a file has an allowed extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ImageUpload(Resource):
    def post(self):
        """
        Function to handle POST requests for image upload
        """
        # Function to handle POST requests for image upload
        if 'file' not in request.files:
            print("No file part in request.files")
            return {'error': 'No file part'}

        file = request.files['file']

        if file.filename == '':
            print("No selected file")
            return {'error': 'No selected file'}, 400

        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            class_name, prob = classify_image(filename)
            name = clsss[class_name]


            return {'filename': filename, 'class_name': name, 'probability': prob}

        return {'error': 'Invalid file extension'}, 400

class Img(Resource):
    def post(self):
        file = request.files['file']
        return {'e': 'file '}



class HelloWorld(Resource):
    def get(self):
        """
        Get method to retrieve a message 'Hello, World!'.
        """
        return {'message': 'Hello, World!'}

        
def classify_image(filename):
    """
    Function to classify an uploaded image

    Parameters:
    filename (str): The name of the file to be classified

    Returns:
    tuple: A tuple containing the classified image's class name and the rounded probability
    """
    # Function to classify an uploaded image
    results = model(filename)
    prob = results[0].probs
    class_name = prob.top1
    val = prob.top1conf
    prob = np.array(val).item()
    return class_name, round(prob, 3)

api.add_resource(ImageUpload, '/upload')
api.add_resource(Img, '/up')
api.add_resource(HelloWorld, '/hello')

if __name__ == '__main__':
    app.run(debug=True,port=5000)

