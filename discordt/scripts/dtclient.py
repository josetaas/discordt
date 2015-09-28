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

import discord
import threading

def _null_event(*args, **kwargs):
    pass

##
# Handles communication with
# discord.py wrapper
##
class DTClient(object):

    def __init__(self, on_message, on_ready):
        self.on_message = on_message
        self.on_ready = on_ready

        self.channel = None
        self.connected = False
        self.textchannels = []
        self.textlogs = {}
        self.user = None

        self.events = {
            'on_ready': _null_event,
            'on_disconnect': _null_event,
            'on_error': _null_event,
            'on_response': _null_event,
            'on_message': _null_event,
            'on_message_delete': _null_event,
            'on_message_edit': _null_event,
            'on_status': _null_event,
            'on_channel_delete': _null_event,
            'on_channel_create': _null_event,
            'on_channel_update': _null_event,
            'on_member_join': _null_event,
            'on_member_remove': _null_event,
            'on_member_update': _null_event,
            'on_server_create': _null_event,
            'on_server_delete': _null_event,
        }

    def run(self, email, password):
        """Starts Discord client thread."""
        self.thread = threading.Thread(target=self._run,args=(email, password))
        self.thread.daemon = True
        self.thread.start()

    def get_channels(self):
        """Returns an array of Discord.Channel."""
        self.textchannels = []
        for server in self._discordClient.servers:
            for channel in server.channels:
                #if not channel.server.name+channel.name in self.textchannels:
                if channel.type == 'text':
                    self.textchannels.append(channel)
        return self.textchannels

    def get_channel(self, i):
        channel = self.discordClient.get_channel(i)
        return channel

    # index passed is 1-based
    def switch_channel(self, index):
        if len(self.textchannels) >= index:
            self.channel = self.textchannels[index-1]
        else:
            raise Exception
        #if name in self.textchannels:
        #    self.channel = self._discordClient.get_channel(self.textchannels[name])
        #else:
        #    raise Exception

    def send_message(self, message):
        #channel = self._discordClient.get_channel(self.channel)
        t = threading.Thread(target=self._discordClient.send_message,args=(self.channel, message))
        t.daemon = True
        t.start()

    def get_users(self):
        if self.channel is not None:
            return self.channel.server.members
        else:
            raise Exception

    def event(self, function):
        if function.__name__ not in self.events:
            return

        self.events[function.__name__] = function
        return function

    def _run(self, email, password):
        self._discordClient = discord.Client()
        self._discordClient.login(email, password)

        @self._discordClient.event
        def on_message(message):
            if message.channel.id not in self.textlogs:
                self.textlogs[message.channel.id] = []
            self.textlogs[message.channel.id].append(message)
            self.on_message(message)
            self._invoke_event('on_message', message)

        @self._discordClient.event
        def on_ready():
            self.user = self._discordClient.user
            self.on_ready()
            self._invoke_event('on_ready')

        self._discordClient.run()

    def _invoke_event(self, event_name, *args, **kwargs):
        try:
            self.events[event_name](*args, **kwargs)
        except:
            pass
