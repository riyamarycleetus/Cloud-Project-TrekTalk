from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

# Initialize AWS Translate client
translate = boto3.client('translate', region_name='us-west-2')  

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Language Translation</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Teko&display=swap" rel="stylesheet">
        <style>
            body {
                background-color: black;
                color: white;
                font-family: 'Teko', sans-serif;
                height: 100vh;
                margin: ;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                letter-spacing: 1px;
                background-image: url("");
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;                 
            }

            h1 {
                font-size: 52px;
                margin-bottom: 20px;
                letter-spacing: 2px;
            }

            .input-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 20px;
                letter-spacing: 1px;
            }

            textarea, input {
                font-family: 'Teko', sans-serif;
                font-size: 22px;
                padding: 10px;
                width: 400px;
                border-radius: 5px;
                border: none;
                letter-spacing: 1px;
            }

            button {
                background-color: gray;
                color: black;
                border: none;
                padding: 15px 30px;
                font-size: 26px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                letter-spacing: 1px;
                border-radius: 5px;
                font-family: 'Teko';
                letter-spacing: 1px;
            }

            button:hover {
                background-color:  rgba(104, 104, 104, 0.5);
            }
            
            .languages-container {
                position: absolute;
                right: 20px;
                top: 50px;
                bottom: 50px;
                overflow-y: auto;
                padding: 20px;
                border-left: 1px solid white;
                border-top: 1px solid white;
                border-right: 1px solid white;
                border-bottom: 1px solid white;
            }

            .languages-container ul {
                list-style-type: none;
                padding: 0;
            }

            .languages-container li {
                margin-bottom: 10px;
            }
            .translated-container {
                margin-top: 20px;
                font-size: 24px;
                padding: 15px;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.9);
                max-width: 800px;
                text-align: center;
                height:26px;
                color:black;
                margin-bottom: 20px;

            }

        </style>
    </head>
    <body>
        <h1>Language Translation</h1>

        <div class="input-container">
            <textarea id="inputText" placeholder="Enter text to translate..."></textarea>
            <input type="text" id="sourceLang" placeholder="Source Language (e.g., en)">
            <input type="text" id="targetLang" placeholder="Target Language (e.g., es)">
            <button onclick="translateText()">Translate</button>
        </div>

        <div class="translated-container" id="translatedText" style="margin-top: 20px;"></div>
        
            <div class="languages-container">

        <h2>Languages</h2>
        <ul>
            <li>Arabic - ar</li>
            <li>Chinese (Simplified) - zh</li>
            <li>Chinese (Traditional) - zh-TW</li>
            <li>Czech - cs</li>
            <li>Danish - da</li>
            <li>Dutch - nl</li>
            <li>English - en</li>
            <li>Finnish - fi</li>
            <li>French - fr</li>
            <li>German - de</li>
            <li>Greek - el</li>
            <li>Hebrew - he</li>
            <li>Hindi - hi</li>
            <li>Hungarian - hu</li>
            <li>Indonesian - id</li>
            <li>Italian - it</li>
            <li>Japanese - ja</li>
            <li>Korean - ko</li>
            <li>Malay - ms</li>
            <li>Norwegian - no</li>
            <li>Polish - pl</li>
            <li>Portuguese - pt</li>
            <li>Romanian - ro</li>
            <li>Russian - ru</li>
            <li>Spanish - es</li>
            <li>Swedish - sv</li>
            <li>Turkish - tr</li>
            <li>Ukrainian - uk</li>
            <li>Vietnamese - vi</li>
        </ul>
    </div>
    
    <button onclick="speakText()">Speak</button>
    </div>
       <script>
    async function translateText() {
        const inputText = document.getElementById("inputText").value;
        const sourceLang = document.getElementById("sourceLang").value;
        const targetLang = document.getElementById("targetLang").value;

        const response = await fetch(`/translate?source=${sourceLang}&target=${targetLang}&text=${encodeURIComponent(inputText)}`);
        const data = await response.json();

        if (response.ok) {
            document.getElementById("translatedText").innerText = data.TranslatedText;
        } else {
            document.getElementById("translatedText").innerText = `Translation Error: ${data.error}`;
        }
    }
async function speakText() {
    const translatedText = document.getElementById("translatedText").innerText;

    const response = await fetch(`/speak?text=${encodeURIComponent(translatedText)}`);
    const data = await response.json();

    console.log("Received audio data:", data.audio);  // Debug log to check the received audio data

    if (response.ok) {
        try {
            const audioContext = new AudioContext();
            const arrayBuffer = base64ToArrayBuffer(data.audio);
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            source.start();

        } catch (error) {
            console.error('Error playing audio:', error);
        }
    } else {
        alert(`Speech Error: ${data.error}`);
    }
}

function base64ToArrayBuffer(base64) {
    const binaryString = window.atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);

    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }

    return bytes.buffer;
}

</script>
    </body>
    </html>
    '''

@app.route('/translate')
def translate_text():
    source_language = request.args.get('source')
    target_language = request.args.get('target')
    text = request.args.get('text')

    try:
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        translated_text = response['TranslatedText']
        return jsonify({'TranslatedText': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/speak')
def speak_text():
    text = request.args.get('text')

    try:
        polly = boto3.client('polly', region_name='us-west-2')
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna'  # You can change the voice as per your preference
        )
        
        audio = response['AudioStream'].read()
        audio_base64 = audio.hex()

        return jsonify({'audio': audio_base64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)