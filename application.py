import os

from datetime import datetime
from flask import Flask, render_template, url_for, session, request, redirect, flash
from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__)
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = "my secret key"
socketio = SocketIO(app)


@app.route("/")
def index():
  return render_template('index.html')

@app.route("/chat", methods=["GET", "POST"])
def chat():
  if request.method=='POST':

    if not request.form['name'] or not request.form['room']:
      flash('name and room required')
      return redirect('/')

    session['name'] = request.form['name']
    session['room'] = request.form['room']
    return render_template('chat.html', name=session['name'], room=session['room'], login=True)

  else:
    return render_template('index.html', message="you have to login and choose a room")

@socketio.on("message")
def handlemessage(msg):
  print('message : ' + msg )
  send(msg, broadcast=True)

@socketio.on("submit message")
def message(data):
  time = datetime.now().strftime("%A %d %b at %H:%M")
  message = data["message"]
  room = data['room']
  emit("announce message", {"message": message, 'time': time}, room=room, broadcast=True)

@socketio.on('join')
def on_join(data):
  time = datetime.now().strftime("%A %d %b at %H:%M")
  name = data['username']
  room = data['room']
  join_room(room)
  emit("confirm user connected", {"user": name, 'time': time}, room=room, broadcast=True)

@socketio.on('leave')
def on_leave(data):
  time = datetime.now().strftime("%A %d %b at %H:%M")
  name = data['username']
  room = data['room']
  leave_room(room)
  emit("confirm user disconnected", {"user": name, 'time': time}, room=room, broadcast=True)

if __name__ == '__main__':
  app.run()