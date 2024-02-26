from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, disconnect
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

active_users = set()  # Set to store active users

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('A user has connected.')
    for user in active_users:
        send(f'SERVER~{user[1]} has connected.', broadcast=True)

@socketio.on('join')
def handle_join(data):
    username = data['username']
    active_users.add((request.sid, username))  # Convertimos el diccionario a una tupla de (sid, username)
    send(f'SERVER~{username} has connected.', broadcast=True)

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    username, message = msg.split('~', 1)
    time = datetime.now().strftime('%H:%M:%S')
    send(f'{time} - {username}: {message}', broadcast=True)

# Handle disconnect event
@socketio.on('disconnect')
def handle_disconnect():
    disconnected_user = [user for user in active_users if user[0] == request.sid]
    if disconnected_user:
        username = disconnected_user[0][1]
        active_users.remove(disconnected_user[0])
        send(f'SERVER~{username} has disconnected.', broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='192.168.0.28')
