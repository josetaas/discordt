import discordt

dtcontroller = discordt.DTController()

# instantaneous message display
# set to false if bot will be sending messages
dtcontroller.local_message_display = True

# if you need access to discord.py's Discord.Client
client = dtcontroller.dtclient.discordClient

# only on_message and
# on_ready have implementations in dtclient
@dtcontroller.dtclient.event
def on_message(message):
    pass

@dtcontroller.dtclient.event
def on_ready():
    # printing message on output box
    dtcontroller.print_output('Hello world!')

# if you need the rest of the events:
# but do not use on on_message and on_ready
# as they will just get overwritten
@dtcontroller.dtclient.discordClient.event
def on_disconnect():
    pass

# dtcontroller.run() -- just starts interface, must use /login
# dtcontroller.run(email, password) -- logs in directly (bot use)
dtcontroller.run()
