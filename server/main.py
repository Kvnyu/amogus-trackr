from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from random import randint
from time import sleep
from threading import Thread, Event


#  Flask Server Initialization
app = Flask(__name__)

# Flask app confi
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

# Adding CORS to flask App
CORS(app, resources={r"/*": {"origins": "*"}})

# Connection Socket -- Flask // and adding cors origins
socketio = SocketIO(app, cors_allowed_origins='*')

thread = Thread()
thread_stop_event = Event()

def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        number = randint(0,5)
        print(number)
        socketio.emit('newNumber', {'number': number})
        socketio.sleep(2)

# Connections Event
@socketio.on('connect')
def connection():
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('update')
def handleUpdate(update):
    emit('')




if __name__ == '__main__':
    socketio.run(app)