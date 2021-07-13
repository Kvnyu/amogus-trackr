 # How to run frontend
 - Go into client
 - Run yarn 
 - Run yarn start
 # How to run backend
 - Go into server
 - Make virtual environment with `python3 -m venv venv`
 - Run `source venv/bin/activate`
 - Run `pip3 install -r requirements.txt`
 - Run `python3 main.py`


# Unsupported version error
If you get the following error:

The client is using an unsupported version of the Socket.IO or Engine.IO protocols
and fixed it by doing the following:

pip install --upgrade python-socketio==4.6.0

pip install --upgrade python-engineio==3.13.2

pip install --upgrade Flask-SocketIO==4.3.1