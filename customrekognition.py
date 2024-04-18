from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

# AWS credentials and region
AWS_REGION = 'us-east-2'
AWS_CUSTOM_MODEL_ARN = 'arn:aws:rekognition:us-east-2:471112776544:project/PlaceRecognition/version/PlaceRecognition.2024-04-17T10.01.51/1713328320529'

# Initialize Boto3 client without credentials
rekognition = boto3.client('rekognition', region_name=AWS_REGION)

@app.route('/', methods=['GET', 'POST'])
def detect_landmarks():
    if request.method == 'POST':
        try:
            # Get the uploaded image
            image = request.files['image']
            
            # Perform landmark detection using the custom model
            response = rekognition.detect_custom_labels(
                Image={'Bytes': image.read()},
                MinConfidence=60,
                ProjectVersionArn=AWS_CUSTOM_MODEL_ARN
            )
            
            # Extract labels from the response
            labels = [label['Name'] for label in response['CustomLabels']]
            return jsonify({'labels': labels})
        except Exception as e:
            return jsonify({'error': str(e)})
    
    # HTML front-end code (unchanged)
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Landmark Detection</title>
        <link href="https://fonts.googleapis.com/css2?family=Teko&display=swap" rel="stylesheet">
        <style>
            body {
                background-color: black;
                color: white;
                font-family: 'Teko', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                margin-bottom: 30px;
                }
            h1 {
                font-size: 50px;
                margin-bottom: 30px;
            }
            .content {
                text-align: center;
                font-size:30px;
            }
        </style>
    </head>
    <body>
        <div class="content">
            <h1>Landmark Detection</h1>
            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" id="fileInput" accept="image/*">
                <button type="button" onclick="detectLandmarks()">Detect Landmarks</button>
            </form>
            <div id="results"></div>
        </div>
        <script>
            async function detectLandmarks() {
                const formData = new FormData();
                formData.append('image', document.getElementById('fileInput').files[0]);
                const response = await fetch('/', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '';
                if ('error' in data) {
                    resultsDiv.textContent = data.error;
                } else {
                    data.labels.forEach((label) => {
                        const p = document.createElement('p');
                        p.textContent = label;
                        resultsDiv.appendChild(p);
                    });
                }
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
