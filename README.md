# Discordt

Discordt is a command-line interface for [discordapp](https://discordapp.com) using the [discord.py](https://github.com/Rapptz/discord.py) wrapper and curses.  
Since Discord has yet to release an official API, anything could break at any point.

## Installation

Simply clone the repository, then run `pip install -e .` in the repository's directory.  

## Usage

Running `discordt` will bring up the command-line client.  
However, if you want to import discordt in your own code:

```python
import discordt

dtcontroller = discordt.DTController()

@dtcontroller.dtclient.event
def on_message(message):
    pass

@dtcontroller.dtclient.event
def on_ready():
    dtcontroller.print_output('Hello world!')

dtcontroller.run('example@example.com', '123456')
```

See examples for more detailed usage.
