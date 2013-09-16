nebulousChat
============
nebulousChat is a work-in-progress chat client with nested messages. 
It is written in Python 2.7 and has a wxPython GUI.


Usage
-----
`python server.py n` launches a server on port `n`.

`python gui.py` launches the client GUI, which is the preferred mode 
of use. This requires [wxPython](http://www.wxpython.org/), which 
you may be able to install using `apt-get install python-wxgtk2.8`.

Alternatively, `python client.py your.domain.or.ip port` launches a 
client on the command line, which will connect to 
`your.domain.or.ip:port`.


Todo
----
- [x] stuff
- [ ] other stuff
