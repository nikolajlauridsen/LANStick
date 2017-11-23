# LANStick
Move files between two computers over LAN with a one time password.

## Operation
LANStick is fairly simple, a raspberry pi is set up as a rendevouz server,
which passes on metadata about the file(s) to be transmitted.

The sending client sends it's host & port to the rendevouz sever, as well as
metadata and a one-time hashed passphrase as an id, the client then outputs
the passphrase to the console.

On the receiving client the passphrase from the sending client is typed in.
The password is then hashed and send to the server, requesting connection information.
If the hashed passphrase matches a connection info ID the info is returned to the recieving client.

Once the receiving client gets hold of the connection information it opens a
socket connection to the sending host and the file is transmitted.

If you choose a folder as a target it will automatically be zipped to a randomly
named zip file, which will be send, and then extracted and deleted on the receiving side

## Inspiration
This project is heavily inspired by [https://github.com/warner/magic-wormhole](Magic Wormhole).

However this solution is not nearly as good, or safe as *Magic Wormhole*, the goal
with LANStick is to create a simple way to move files over a LAN network which is deemed "safe"
which is also why security isn't the top priority.


:warning: This is an incomplete project
