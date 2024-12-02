from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # Forward the message to the external backend
    try:
        backend_response = requests.post(
            'http://127.0.0.1:6000/chat',
            json={'message': user_input},
            timeout=20  # Timeout for the backend request
        )
        backend_response.raise_for_status()  # Raise error if response code is not 200
        backend_data = backend_response.json()  # Parse JSON response
        return jsonify({
            'response': backend_data.get('response'),
            'session_id': backend_data.get('session_id')  # Include session_id in the response
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to backend', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
