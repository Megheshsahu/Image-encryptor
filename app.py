
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        key = request.form.get('key')
        file = request.files.get('file')
        if not file or not key:
            flash('Please provide both an image file and a key.')
            return redirect(url_for('index'))
        filename = secure_filename(file.filename)
        # Backend check for PNG file type
        if not filename.lower().endswith('.png') or file.mimetype != 'image/png':
            flash('Only PNG files are allowed.')
            return redirect(url_for('index'))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        output_bytes = None
        try:
            with open(file_path, 'rb') as f:
                data = bytearray(f.read())
            key_bytes = key.encode('utf-8')
            processed = bytes(
                b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)
            )
            output_bytes = BytesIO(processed)
            output_bytes.seek(0)
        except Exception as e:
            flash(f'Error: {e}')
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for('index'))
        if os.path.exists(file_path):
            os.remove(file_path)
        out_name = f"{'encrypted' if action == 'encrypt' else 'decrypted'}_{filename}"
        return send_file(output_bytes, as_attachment=True, download_name=out_name)
    return render_template('index.html')




# Allow running with 'python app.py' for simple deployment
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)



