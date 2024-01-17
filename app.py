from flask import Flask, render_template, jsonify, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_python_code', methods=['POST'])
def run_python_code():
    try:
        button_number = request.json.get('buttonNumber')
        
        # Modify this part based on the action you want for each button
        if button_number == 1:
            result = subprocess.check_output(['python', 'hello_world.py'], text=True)
        elif button_number == 2:
            result = subprocess.check_output(['python', 'decryption.py'], text=True)
        else:
            return jsonify({'error': 'Invalid button number'})

        return jsonify({'result': result.strip()})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Error: {e.output.decode("utf-8").strip()}'})

if __name__ == '__main__':
    app.run(debug=True)



