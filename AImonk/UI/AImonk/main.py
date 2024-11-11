from flask import Flask, request, send_file, jsonify,render_template,send_from_directory
import requests
import os
from PIL import Image
import json

app = Flask(__name__)

# Set upload folder and allowed file types
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

AI_BACKEND_URL = "http://172.17.0.1:8000/detect"  # URL to AI backend service

# Check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to render the HTML form
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# Route to handle the image upload and processing
@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    image_file = request.files['image']
    if image_file.filename == '' or not allowed_file(image_file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    file_path=f"/home/files/{image_file.filename}"
    # Save the image
    img = Image.open(image_file)
    img.save(file_path)
    # sent to AI
    files={"image":file_path}
    print(AI_BACKEND_URL)
    response = requests.post(AI_BACKEND_URL, json=files)

    # Display processed image or an error if the response fails
    if response.status_code == 200:
        #Decode the byte string to a regular string
        decoded_string = response.content.decode('utf-8')
        
        data = json.loads(decoded_string)
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to process image"}), 500

# Route to handle the image upload and processing
@app.route('/home/files/<path:filename>')
def display_image(filename):
    return send_from_directory('/home/files/',filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)
