import os
import tempfile
from flask import Flask, request, jsonify
from utils import ocr_text

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    temp_dir = tempfile.mkdtemp()
    temp_filepath = os.path.join(temp_dir, file.filename)
    file.save(temp_filepath)

    try:
        result = ocr_text(temp_filepath)
        print('func1 result:', result)
    except Exception as e:
        return jsonify({'error': f'Error processing PDF: {str(e)}'})

    return jsonify({'message': 'File uploaded and processed successfully', 'result': result})


if __name__ == '__main__':
    app.run(debug=True)
