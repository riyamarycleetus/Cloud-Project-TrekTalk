from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# AWS region
AWS_REGION = 'us-east-2'

# Initialize AWS Rekognition client
rekognition = boto3.client('rekognition', 
                           aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                           aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                           region_name=AWS_REGION)

@app.route('/', methods=['GET', 'POST'])
def detect_landmarks():
    if request.method == 'POST':
        # Get the uploaded image
        image = request.files['image']
        
        # Perform landmark detection using AWS Rekognition
        response = rekognition.detect_labels(
            Image={'Bytes': image.read()},
            MaxLabels=10,  # Adjust as needed
            MinConfidence=60  # Adjust as needed
        )
        
        # Extract landmarks from the response
        landmarks = [label['Name'] for label in response['Labels']]

        return jsonify({'landmarks': landmarks})
    
    # HTML front-end code
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Detection</title>
    </head>
    <body>
        <h1>Image Detection</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*">
            <button type="submit">Detect</button>
        </form>
        <div id="results"></div>
        <script>
            document.querySelector('form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData();
                formData.append('image', document.querySelector('input[type=file]').files[0]);
                const response = await fetch('/', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '';
                data.landmarks.forEach((landmark) => {
                    const p = document.createElement('p');
                    p.textContent = landmark;
                    resultsDiv.appendChild(p);
                });
            });
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
