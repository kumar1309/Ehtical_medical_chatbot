from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from groq import Groq
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # Required for session management
socketio = SocketIO(app)

# Initialize Groq client
client = Groq(api_key="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")

# Store active doctor connections and patient requests
active_doctors = {}
patient_requests = {}
active_chats = {}

def groq_chatbot_response(conversation_history):
    """Get a diagnostic response from the Groq LLaMA model with conversation history."""
    system_prompt = """You are a medical diagnostic AI assistant. Your role is to:
1. Ask relevant questions about symptoms
2. Provide potential diagnoses based on symptoms
3. Suggest appropriate management steps and precautions
4. Recommend when to seek professional medical help
5. Provide general health advice
6. Remember and reference previous symptoms and information shared by the user

Important: Always include a medical disclaimer and encourage users to seek professional medical help for serious conditions.
Maintain context from previous messages to provide more accurate and contextual responses."""

    # Format conversation history into messages
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
        temperature=0.7,
        max_tokens=1000
    )
    return chat_completion.choices[0].message.content

@app.route('/')
def index():
    # Clear any existing conversation when starting fresh
    session['conversation'] = []
    return render_template('login.html')

@app.route('/chatbot')
def chatbot():
    # Initialize conversation history if not exists
    if 'conversation' not in session:
        session['conversation'] = []
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check for doctor login
    if username == 'doctor@gmail.com' and password == '123':
        session['doctor_logged_in'] = True
        session['doctor_id'] = 'doctor_' + str(hash(username))  # Generate unique doctor ID
        return redirect(url_for('doctor_dashboard'))
    
    # Check for patient login
    users = {
        "mohan@gmail.com": "123"  # Example username and password
    }

    if username in users and users[username] == password:
        # Initialize conversation history for new session
        session['conversation'] = []
        return redirect(url_for('chatbot'))
    else:
        return render_template('login.html', error='Incorrect username or password.')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()

    # Initialize conversation if not exists
    if 'conversation' not in session:
        session['conversation'] = []

    # Handle initial greeting
    if not user_message:
        initial_greeting = """Welcome to the Medical Diagnostic Assistant! 

I'm here to help you understand your symptoms and provide basic medical advice. To get started, please:
1. Describe your symptoms in detail
2. Mention when they started
3. Include any relevant medical history

Important: This is an AI assistant and not a replacement for professional medical care. For emergencies or serious conditions, please seek immediate medical attention.

How can I help you today?"""
        
        # Store the greeting in conversation history
        session['conversation'] = [
            {"role": "assistant", "content": initial_greeting}
        ]
        return jsonify({"response": initial_greeting})

    # Add user message to conversation history
    session['conversation'].append({"role": "user", "content": user_message})

    # Get response with conversation history
    response = groq_chatbot_response(session['conversation'])

    # Add assistant response to conversation history
    session['conversation'].append({"role": "assistant", "content": response})

    # Limit conversation history to last 10 messages to prevent context overflow
    if len(session['conversation']) > 10:
        session['conversation'] = session['conversation'][-10:]

    # Make sure to save the session after modifying it
    session.modified = True

    return jsonify({
        "response": response
    })

@app.route('/reset', methods=['POST'])
def reset_conversation():
    session['conversation'] = []
    return jsonify({"status": "success"})

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if not session.get('doctor_logged_in'):
        return redirect(url_for('index'))
    return render_template('doctor_dashboard.html')

@app.route('/request_doctor', methods=['POST'])
def request_doctor():
    data = request.json
    patient_id = data.get('patient_id')
    patient_requests[patient_id] = {
        'status': 'pending',
        'patient_id': patient_id,
        'timestamp': datetime.now().isoformat()
    }
    # Emit to all connected doctors
    socketio.emit('new_request', {
        'patient_id': patient_id,
        'timestamp': patient_requests[patient_id]['timestamp']
    }, namespace='/doctor')
    return jsonify({'status': 'success'})

@socketio.on('connect', namespace='/doctor')
def handle_doctor_connect():
    if session.get('doctor_logged_in'):
        join_room('doctors')
        active_doctors[session['doctor_id']] = request.sid
        # Send any pending requests to the newly connected doctor
        for patient_id, request_data in patient_requests.items():
            if request_data['status'] == 'pending':
                emit('new_request', {
                    'patient_id': patient_id,
                    'timestamp': request_data['timestamp']
                }, room=request.sid)

@socketio.on('connect', namespace='/patient')
def handle_patient_connect():
    print('Patient connected')
    # Store patient's socket ID
    patient_id = request.sid
    join_room(patient_id)

@socketio.on('message', namespace='/patient')
def handle_patient_message(data):
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')
    patient_id = request.sid
    
    if receiver == 'doctor':
        # Find the doctor's socket ID
        doctor_id = active_chats.get(patient_id)
        if doctor_id and doctor_id in active_doctors:
            # Send to doctor only
            emit('new_message', {
                'sender': 'patient',
                'message': message
            }, room=active_doctors[doctor_id], namespace='/doctor')

@socketio.on('message', namespace='/doctor')
def handle_doctor_message(data):
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')
    doctor_id = session.get('doctor_id')
    
    if receiver in active_chats:
        # Find the patient's socket ID
        patient_id = receiver
        # Send to patient only
        emit('new_message', {
            'sender': 'doctor',
            'message': message
        }, room=patient_id, namespace='/patient')

@socketio.on('accept_request', namespace='/doctor')
def handle_accept_request(data):
    patient_id = data.get('patient_id')
    doctor_id = session.get('doctor_id')
    
    if patient_id in patient_requests:
        patient_requests[patient_id]['status'] = 'accepted'
        patient_requests[patient_id]['doctor_id'] = doctor_id
        active_chats[patient_id] = doctor_id
        
        # Send acceptance to patient
        emit('request_accepted', {
            'doctor_id': doctor_id,
            'patient_id': patient_id
        }, room=patient_id, namespace='/patient')
        
        # Notify doctor
        emit('chat_started', {
            'patient_id': patient_id,
            'doctor_id': doctor_id
        }, room=active_doctors[doctor_id], namespace='/doctor')

if __name__ == '__main__':
    socketio.run(app, debug=True)
