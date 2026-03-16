from flask import Flask, render_template, request, jsonify
import subprocess, os, signal, csv, sys
from datetime import date
from models.encode_faces import encode_faces

app = Flask(__name__)
recognizer_process = None

@app.route('/')
def index():
    encode_faces()  # Auto-run when page loads
    attendance = []
    filename = f'attendance/{date.today()}.csv'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            attendance = list(reader)
    return render_template('dashboard.html', attendance=attendance)

@app.route('/start', methods=['POST'])
def start_recognizer():
    global recognizer_process
    if not recognizer_process or recognizer_process.poll() is not None:
        script_path = os.path.abspath("recognizer.py")
        python_exe = sys.executable
        recognizer_process = subprocess.Popen(
            [python_exe, script_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return jsonify({'status': 'started'})
    return jsonify({'status': 'already running'})

@app.route('/stop', methods=['POST'])
def stop_recognizer():
    global recognizer_process
    if recognizer_process and recognizer_process.poll() is None:
        recognizer_process.terminate()
        recognizer_process = None
        return jsonify({'status': 'stopped'})
    return jsonify({'status': 'not running'})

@app.route('/get_attendance')
def get_attendance():
    attendance = []
    filename = f'attendance/{date.today()}.csv'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            attendance = [{'name': row[0], 'time': row[1]} for row in reader]
    return jsonify(attendance)

if __name__ == '__main__':
    app.run(debug=True)
