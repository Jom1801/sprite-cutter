from flask import Flask, request, render_template, send_file
from PIL import Image
import os
import io
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cut', methods=['POST'])
def cut_sprite():
    image = request.files['image']
    rows = int(request.form['rows'])
    cols = int(request.form['cols'])

    img = Image.open(image)
    img_w, img_h = img.size
    frame_w = img_w // cols
    frame_h = img_h // rows

    output_zip = io.BytesIO()
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for r in range(rows):
            for c in range(cols):
                box = (c*frame_w, r*frame_h, (c+1)*frame_w, (r+1)*frame_h)
                frame = img.crop(box)

                img_bytes = io.BytesIO()
                frame.save(img_bytes, format='PNG')
                img_bytes.seek(0)

                zipf.writestr(f"sprite_{r}_{c}.png", img_bytes.read())

    output_zip.seek(0)
    return send_file(output_zip, download_name="sprites.zip", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
