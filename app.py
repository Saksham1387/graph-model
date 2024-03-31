# from flask import Flask, request, send_file
# import matplotlib
# matplotlib.use('Agg')  # Use a non-interactive backend for matplotlib
# import librosa
# import librosa.display
# import matplotlib.pyplot as plt
# from flask_cors import CORS
# import tempfile

# app = Flask(__name__)
# CORS(app)

# # Enable Cross-Origin Resource Sharing with specific settings if needed
# CORS(app, supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'])
# CORS(app, supports_credentials=True, allow_headers=['Form-data', 'Authorization'], methods=['GET', 'POST', 'OPTIONS'])

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     # Check if the request contains a file
#     if 'file' not in request.files:
#         return "No file part", 400

#     file = request.files['file']
#     if file.filename == '':
#         return "No selected file", 400

#     if file and file.filename.endswith('.wav'):
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_file:
#             file.save(audio_file.name)
#             y, sr = librosa.load(audio_file.name, sr=None)

#             # Generate the waveform plot
#             plt.figure(figsize=(12, 4))
#             librosa.display.waveshow(y, sr=sr)
#             plt.title('Waveform')
#             plt.xlabel('Time (seconds)')
#             plt.ylabel('Amplitude')

#             # Save the plot to a temporary image file
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as img_file:
#                 plt.savefig(img_file.name)
#                 plt.close()  # Close the plot to free up memory

#                 # Serve the image file as the response
#                 return send_file(img_file.name, as_attachment=True, download_name='waveform.png')

#     return "Invalid file type. Please upload a .wav file.", 400

# if __name__ == '__main__':
#     app.run(debug=True, port=5007)

from flask import Flask, request, send_file
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for matplotlib
import librosa
import matplotlib.pyplot as plt
from flask_cors import CORS
import tempfile
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.wav'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_file:
            file.save(audio_file.name)
            y, sr = librosa.load(audio_file.name, sr=None)

            # Generate the waveform plot using matplotlib directly
            plt.figure(figsize=(12, 4))
            times = np.arange(len(y)) / sr
            plt.plot(times, y)
            plt.title('Waveform')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Amplitude')

            # Save the plot to a temporary image file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as img_file:
                plt.savefig(img_file.name)
                plt.close()  # Ensure the plot is closed after saving

                # Serve the image file as the response
                return send_file(img_file.name, as_attachment=True, download_name='waveform.png')

    return "Invalid file type. Please upload a .wav file.", 400

if __name__ == '__main__':
    app.run(debug=True, port=5007)
