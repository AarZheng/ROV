from flask import Flask, Response, render_template_string, request
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import cv2
import atexit

# === GPIO Setup ===
LED_PIN = 18  # Use any GPIO pin you prefer
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.HIGH)  # Light starts ON

# Ensure GPIO is cleaned up on exit
atexit.register(GPIO.cleanup)

# === Camera Setup ===
app = Flask(__name__)
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

# === Stream Generator ===
def generate_frames():
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# === Routes ===

@app.route('/')
def index():
    return render_template_string('''
        <html>
        <head><title>RPi Camera Stream</title></head>
        <body>
            <h1>RPi Camera Stream with Light Control</h1>
            <img src="/video_feed" width="640" height="480"/><br><br>
            <form method="POST" action="/toggle">
                <button type="submit">{{ 'Turn Light OFF' if light_on else 'Turn Light ON' }}</button>
            </form>
        </body>
        </html>
    ''', light_on=GPIO.input(LED_PIN))

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle', methods=['POST'])
def toggle_light():
    current_state = GPIO.input(LED_PIN)
    GPIO.output(LED_PIN, not current_state)
    return index()

# === Run App ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

