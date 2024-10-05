from flask import Flask, request, jsonify, render_template
import os
from PreProcessing import preproccess
from Predicting import predict
import numpy as np
from RAG_model import run_rag_model
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variable to store uploaded file path
uploaded_file_path = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global uploaded_file_path
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    uploaded_files = request.files.getlist('file')

    if len(uploaded_files) == 0:
        return jsonify({"error": "No selected file"})

    # Save the uploaded file
    for file in uploaded_files:
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(uploaded_file_path)
        print('File saved:', uploaded_file_path)
    
    return jsonify({"message": "File uploaded successfully."})

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    user_input = request.json.get('userText', '')
    if uploaded_file_path is None:
        return jsonify({"response": "Please upload a file first."})
    
    # Process the user input and call predict if necessary
    prediction_result = process_user_input(user_input)
    return jsonify({"response": prediction_result})

def process_user_input(user_input):
    temp=preproccess(uploaded_file_path)
    prediction=predict(temp)
    # Call the predict function and return the result
    probability = run_rag_model(prediction,user_input)  # Use the uploaded file
    return f"Prediction result for '{user_input}': {probability}"

if __name__ == '__main__':
    app.run(debug=True)
