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

import curses
import sys

##
# Handles TUI using curses
##
class DTInterface(object):

    def __init__(self, on_return_key):
        self.on_return_key = on_return_key
        self._init_curses()
        self.print('DISCORD TERMINAL CLIENT', colorpair = 4)
        self.print('Type /help to list available commands.')
        self.print_info('Welcome to Discord!')

    def update(self):
        try:
            self._getkey()
        except:
            self.close()
            sys.exit()

    def close(self):
        """Restores terminal to default behaviour."""
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.nl()
        curses.endwin()

    def clear(self):
        """Clears output box"""
        self._output_box.erase()
        self._refresh()

    def print(self, message, newline = True, colorpair=1):
        """Displays a message in the output box."""
        if newline:
            message = message + '\n'
        self._output_box.attron(curses.color_pair(colorpair))
        self._output_box.addstr(message)
        self._refresh()

    def print_info(self, message, colorpair=1):
        """Displays a message in the info box."""
        self._info_box.erase()
        self._refresh()

        self._info_box.attron(curses.color_pair(colorpair))
        self._info_box.addstr(message)
        self._refresh()

    def set_input_status(self, server, channel):
        """Sets the information displayed in the input box"""
        self.input_status = '[' + server + '] '
        self.input_status += '<' + channel + '> '
        self._update_input_status()

    def _init_curses(self):

        # initialize curses
        self.stdscr = curses.initscr()
        
        # set custom color pairs
        # TODO check COLORS for number of
        # supported pairs
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1,-1,-1)
        curses.init_pair(2,curses.COLOR_BLUE,-1)
        curses.init_pair(3,curses.COLOR_RED,-1)
        curses.init_pair(4,curses.COLOR_CYAN,-1)
        curses.init_pair(5,curses.COLOR_YELLOW,-1)
        curses.init_pair(6,curses.COLOR_MAGENTA,-1)
        curses.init_pair(7,curses.COLOR_GREEN,-1)
        curses.init_pair(8,curses.COLOR_BLUE,-1)
        curses.init_pair(9,curses.COLOR_BLUE,-1)

        # change terminal behaviour
        curses.noecho()
        curses.cbreak()
        curses.nonl()
        self.stdscr.keypad(True)

        # create windows
        self._output_box = curses.newwin(curses.LINES-3,curses.COLS,0,0)
        self._output_box.scrollok(True)
        self._output_box.idlok(1)
        self._info_box = curses.newwin(1,curses.COLS,curses.LINES-2,0)
        self._input_box = curses.newwin(1,curses.COLS,curses.LINES-1,0)
        self._input_buffer = ''
        self.set_input_status('none', 'none')


    def _getkey(self):
        c = self._input_box.getch()
        if c == curses.KEY_BACKSPACE or c == 127:
            yx = self._input_box.getyx()
            if len(self.input_status) != yx[1]:
               self._input_box.delch(yx[0], yx[1]-1)
               self._input_buffer = self._input_buffer[:-1]
        elif c == curses.KEY_ENTER or c == 13:
            if len(self._input_buffer) != 0:
                self._update_input_status() # delete line without removing channel
                self.on_return_key(self._input_buffer)
                self._input_buffer = ''
        else:
            self._input_buffer += chr(c)
            self._input_box.addstr(chr(c))
        self._refresh()


    def _refresh(self):
        self._output_box.refresh()
        self._info_box.refresh()
        self._input_box.refresh()

    def _update_input_status(self):
        self._input_box.deleteln()
        self._input_box.addstr(self._input_box.getyx()[0], 0, self.input_status)
        self._refresh()

