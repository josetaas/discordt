"""
The MIT License (MIT)

Original work Copyright (c) 2015 Rapptz
Modified work Copyright 2015 Jose Francisco Taas

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import discordt

import discord
import time
from datetime import datetime
from dateutil import tz

##
# Handles communication between
# DTClient and DTInterface
##
class DTController(object):

    def __init__(self):
        self.dtclient = discordt.DTClient(self.on_message, self.on_ready)
        self.dtinterface = discordt.DTInterface(self.on_return_key)

        # instantaneous message display
        # set to false if bot will be sending messages
        self.local_message_display = True

        self._unread_channels = {}

    def run(self, email='', password=''):
        if email != '' and password != '':
            self._login_command(['', email, password])

        while True:
            self.dtinterface.update()
            time.sleep(0.01)

    def on_message(self, message):
        """Discord.Client on_message event"""
        if self.dtclient.channel is None or message.channel.id != self.dtclient.channel.id:
            self.on_unread_message(message)
            return

        if message.author.id != self.dtclient.user.id or not self.local_message_display:
            self.print_message(message)

    def on_ready(self):
        """Discord.Client on_ready event"""
        self.dtclient.connected = True
        self.dtinterface.clear()
        self.dtinterface.print_output('Connected! Type /help for a list of commands.')
        self.process_message('/channels')

    def on_return_key(self, message):
        """DTInterface on_return_key event. Triggers when enter/return key is pressed."""
        self.process_message(message)

    def on_unread_message(self, message):
        self._unread_channels[message.channel.id] = True
        self.dtinterface.print_info(
                'You have unread messages. Type /channels to list channels.', 3)

    def process_message(self, message):
        if message[0] == '/':
            self._process_command(message)
        else:
            if self.dtclient.channel is None:
                return

            # TODO TODO TODO TODO TODO use Discord.Message instead
            # really really really really really really sorry
            # dummy class for instantaneous message display

            if self.local_message_display:
                class Message_Dummy(object): pass

                tmp = Message_Dummy()
                tmp.channel = Message_Dummy()
                tmp.channel.server = Message_Dummy()
                tmp.author = Message_Dummy()
                tmp.timestamp = Message_Dummy()

                tmp.timestamp = datetime.utcnow()
                tmp.channel.server.name = self.dtclient.channel.server.name
                tmp.channel.name = self.dtclient.channel.name
                tmp.author.name = self.dtclient.user.name
                tmp.content = message
                self.print_message(tmp)

            self.dtclient.send_message(message)

    def print_message(self, message):
        """Displays message from Discord.Message object on the output box."""
        #msg = datetime.now().strftime('%H:%M:%S')
        #msg = message.timestamp.strftime('%H:%M:%S')
        msg = self._convert_tz(message.timestamp).strftime('%H:%M:%S')
        self.dtinterface.print_output(msg, False)
        self.dtinterface.print_output('  [', False)
        msg = message.channel.server.name
        self.dtinterface.print_output(msg, False, 2)
        self.dtinterface.print_output('] <', False)
        msg = message.channel.name
        self.dtinterface.print_output(msg, False, 4)
        self.dtinterface.print_output('>  ', False)
        msg = message.author.name
        self.dtinterface.print_output(msg, False, self._color_hash(msg))
        msg = ' : ' + message.content
        self.dtinterface.print_output(msg)

    def print_output(self, string, colorpair=1):
        """Displays a string on the output box"""
        self.dtinterface.print_output(string, colorpair=1)

    def _color_hash(self, key):
        i = 0
        for c in key:
            i += ord(c)
        i = (i%7)+2
        return i

    def _convert_tz(self, dt):
        dt = dt.replace(tzinfo=tz.tzutc())
        local = dt.astimezone(tz.tzlocal())
        return local

    def _process_command(self, command):
        args = command.split( )
        if '/help' in command:
            self._help_command()
        elif '/exit' in command:
            self.dtinterface.close()
            sys.exit()
        elif '/login' in command:
            self._login_command(args)
        elif '/clear' in command:
            self.dtinterface.clear()
        ## commands that require login
        elif self.dtclient.connected == False:
            self.dtinterface.print_output('Login required!')
            self.dtinterface.print_output('/login email password')
        elif '/channels' in command:
            self._channels_command()
        elif '/connect' in command:
            self._connect_command(args)
        elif '/who' in command:
            self._who_command()
        else:
            self.dtinterface.print_output('Unknown command!')

    def _help_command(self):
        self.dtinterface.print_output('\n\t /login email password', colorpair = 7)
        self.dtinterface.print_output('\t   login command')
        self.dtinterface.print_output('\t /channels', colorpair = 7)
        self.dtinterface.print_output('\t   lists channels')
        self.dtinterface.print_output('\t /connect channel_index', colorpair = 7)
        self.dtinterface.print_output('\t   connects to specified channel_index as displayed in /channels')
        self.dtinterface.print_output('\t /who', colorpair = 7)
        self.dtinterface.print_output('\t   lists online users in current channel')
        self.dtinterface.print_output('\t /clear', colorpair = 7)
        self.dtinterface.print_output('\t   clears output box')
        self.dtinterface.print_output('\t /exit', colorpair = 7)
        self.dtinterface.print_output('\t   closes discord terminal client')
        self.dtinterface.print_output('')

    def _login_command(self, args):
        if len(args) < 3:
            self.dtinterface.print_output('Incorrect syntax!')
            self.dtinterface.print_output('/login email password')
            return

        if self.dtclient.connected:
            self.dtinterface.print_output('You are already logged in.')
            return

        self.dtinterface.print_output('Connecting to Discord...')
        self.dtclient.run(args[1], args[2])

    def _channels_command(self):
        self.dtinterface.clear()
        channels = self.dtclient.get_channels()

        x = 1
        server = ''
        for channel in channels:
            if channel.server.name != server:
                server = channel.server.name
                self.dtinterface.print_output('\n    ' + server + '\n', True, colorpair=self._color_hash(server))

            # change color if channel has unread messages
            colorpair = 3
            if channel.id not in self._unread_channels or not self._unread_channels[channel.id]:
                colorpair = 4

            self.dtinterface.print_output('        '+ str(x).rjust(3) + ') ', False)
            self.dtinterface.print_output(channel.name, True, colorpair)
            x = x + 1
        self.dtinterface.print_output('')

    def _connect_command(self, args):
        if len(args) < 2:
            self.dtinterface.print_output('Incorrect syntax!')
            self.dtinterface.print_output('/connect index')
            return

        try:
            self.dtclient.switch_channel(int(args[1]))
            channel = self.dtclient.textchannels[int(args[1])-1]
        except:
            self.dtinterface.print_output('Failed to connect to ' + args[1] + '.')
            return

        self.dtinterface.print_output('Switched to ', False)
        self.dtinterface.print_output(channel.name, False, 4)
        self.dtinterface.print_output('.')

        # clear output then display stored channel messages
        self.dtinterface.clear()
        if channel.id in self.dtclient.textlogs:
            for msg in self.dtclient.textlogs[channel.id]:
                self.print_message(msg)

        self.dtinterface.set_input_status(channel.server.name, channel.name)

        if channel.id in self._unread_channels:
            self._unread_channels[channel.id] = False

        try:
            values = self._unread_channels.itervalues()
        except AttributeError:
            values = self._unread_channels.values()

        if True not in values:
            self.dtinterface.print_info('You have no unread messages.')


    def _who_command(self):
        try:
            users = self.dtclient.get_users()
        except:
            self.dtinterface.print_output('Not connected to a channel.')
        self.dtinterface.print_output('')
        x = 0
        for user in users:
            if user.status != 'offline':
                if user.status == 'online':
                    self.dtinterface.print_output(user.name.ljust(16), False, 7)
                elif user.status == 'idle':
                    self.dtinterface.print_output(user.name.ljust(16), False, 5)
                self.dtinterface.print_output('\t', False)
                x = x + 1
                if x%4 == 0:
                    self.dtinterface.print_output('')
        self.dtinterface.print_output('\n')
