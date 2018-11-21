document.addEventListener('DOMContentLoaded', () => {
  var socket = io.connect('http://127.0.0.1:5000')
  console.log('hey there')

  socket.on('connect', () => {
    socket.send('user is connected')
    document.querySelector('#message').onsubmit = () => {
      let message = document.querySelector('#input_message').value
      socket.emit('submit message', {'message': message})
      document.querySelector('#input_message').value = ""
      return false
    }

  })
  socket.on('announce message', data => {
    const li = document.createElement('li')
    li.innerHTML = `message: ${data.message}`
    document.querySelector('#chat').append(li)
  })
})
