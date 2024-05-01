from flask import Flask, request, jsonify, send_file # type: ignore
import io
from prediction_code import return_all_images, do_basic_analysis
from PIL import Image # type: ignore
import base64
import json
from flask_cors import CORS # type: ignore

app = Flask(__name__)
cors = CORS(app)


@app.route('/analyse', methods=['POST'])
def upload_file():
    if "image" not in request.files:
        return json.dumps({"error": 400, "message": "image file not present"})
    # For simplicity, let's just return the filename and content type
    image_binary = request.files['image'].read() # Reading image from request
    output = do_basic_analysis(image_binary)
    print(f"Output {output}")
    return json.dumps(output)

@app.route('/complete_analysis', methods=['POST'])
def complete_analysis():
    if "image" not in request.files:
        return json.dumps({"error": 400, "message": "image file not present"})
    # For simplicity, let's just return the filename and content type
    image_binary = request.files['image'].read() # Reading image from request
    output = return_all_images(image_binary)
    print(f"Output {output}")
    return json.dumps(output)

@app.route('/images', methods = ['POST'])
def images():
    body = request.get_json()

    if 'file' not in body:
        return jsonify({'error': 'No file part'})

    file = body['file']
    print(file)

    if file == '':
        return jsonify({'error': 'No selected file'})
    return send_file(
                     file,
                     download_name=file.split("/")[-1],
                     mimetype='image/png'
               )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000,debug=True)
