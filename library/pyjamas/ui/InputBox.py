#!/usr/bin/python
# vim: set fileencoding=utf8

# Crossword Puzzle Loader Demo
# Copyright (C) 2011 Camille Dalmeras
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pyjd

from pyjamas.ui.HTML import HTML
from pyjamas.ui.Grid import Grid
from pyjamas.ui.FocusPanel import FocusPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui import KeyboardListener
from pyjamas.Timer import Timer
from pyjamas import DOM
from pyjamas import Factory

import re

class InputBox(FocusPanel):

    _props = [ ("maxLength", "Max Length", "MaxLength", int),
               ("text", "Text", "Text", None),
               ("matchPattern", "Match Pattern", "matchPattern", None),
             ]

    @classmethod
    def _getProps(self):
        return FocusPanel._getProps() + self._props

    def __init__(self, **kwargs):
        """ setMatchPattern - defaults to '' to match everything
            match pattern examples: '^[0-9]*$' is for digits only
                                    '^[0-9,A-Z]*$' is for digits and uppercase
            setMaxLength
            setText
        """

        kwargs['MatchPattern'] = kwargs.pop('MatchPattern', '')
        gs = kwargs.pop('StyleName', 'inputbox')
        self.tp = Grid(StyleName=gs)
        self.cf = self.tp.getCellFormatter()
        FocusPanel.__init__(self, Widget=self.tp, **kwargs)

        self.addTableListener(self)
        self.addKeyboardListener(self)
        self.addFocusListener(self)

        self.word_selected_pos = None
        self.ctimer = Timer(notify=self.cursorFlash)
        self.focusset = False
        self.cstate = False
        self._keypressListeners = []
  
    def addKeypressListener(self, listener):
        self._keypressListeners.append(listener)

    def removeKeypressListener(self, listener):
        self._keypressListeners.remove(listener)

    def getMatchPattern(self):
        return self.mp

    def setMatchPattern(self, mp):
        self.mp = mp
        self.rexp = re.compile(self.mp)

    def addDblTableListener(self, listener):
        self.tp.addDblTableListener(listener)

    def addTableListener(self, listener):
        self.tp.addTableListener(listener)

    def _highlight_cursor(self, row, col, highlight):
        """ highlights (or dehighlights) the currently selected cell
        """
        self.cf.setStyleName(row, col, "inputbox-square-word-cursor", highlight)

    def resize(self, width, height):
        self.tp.resize(width, height)

    def set_grid_value(self, v, y, x):

        v = v or '&nbsp;'
        self.tp.setWidget(y, x, HTML(v, StyleName="inputbox-square"))
        self.cf.setAlignment(y, x,  HasAlignment.ALIGN_CENTER,
                                    HasAlignment.ALIGN_MIDDLE)

    def onKeyDown(self, sender, keycode, modifiers):

        evt = DOM.eventGetCurrentEvent()
        DOM.eventPreventDefault(evt)

        if self.word_selected_pos is None:
            return

        val = chr(keycode)

        # check up/down/left/right cursor keys
        # the basic rule is: if in same plane, go that way, else "flip"
        # and then, obviously on the next press, the cursor will move
        # when the key is pressed in that same plane
        if keycode == KeyboardListener.KEY_DELETE:
            self.shift_letters_back()
            return
        elif keycode == KeyboardListener.KEY_BACKSPACE:
            if not self.nasty_hack():
                if self.move_cursor(-1):
                    self.shift_letters_back()
            return
        elif keycode == KeyboardListener.KEY_LEFT:
            self.move_cursor(-1)
            return
        elif keycode == KeyboardListener.KEY_RIGHT:
            self.move_cursor(1)
            return

        print "onKeyDown", keycode, val, self.rexp.match(val)

        if self.rexp.match(val):
            self.press_letter(val)

    def press_letter(self, val):

        print "press letter", val
        # check the key is a letter, and there's a grid position highlighted
        if self.word_selected_pos is None:
            return

        row = 0
        col = self.word_selected_pos

        # remove error highlighting, update value, move cursor (if possible)
        self.cf.removeStyleName(row, col, "inputbox-square-word-error")
        self.set_grid_value(val, row, col)
        self.move_cursor(1)

        for listener in self._keypressListeners:
            listener.onKeyPressed(val)

    def nasty_hack(self):
        """ breaking of backspace/delete rules for the final character
        """

        row = 0
        col = self.word_selected_pos

        txt = self.get_char(col)
        if txt is None or txt == "&nbsp;":
            return False

        self.set_grid_value("&nbsp;", row, col)
        return True

    def shift_letters_back(self):
        """ this function is used by del and backspace, to move the letters
            backwards from after the cursor.  the only difference between
            backspace and delete is that backspace moves the cursor and
            _then_ does letter-moving.
        """

        row = 0
        col = self.word_selected_pos
        x2 = self.tp.getColumnCount()-1
        
        while (x2 != col):
            txt = self.get_char(col+1)
            self.set_grid_value(txt, row, col)
            col += 1
        self.set_grid_value("&nbsp;", row, col)
            
    def move_cursor(self, dirn):

        x2 = self.tp.getColumnCount()

        row = 0
        col = self.word_selected_pos

        if dirn == 1 and x2 == col+1:
            return False

        if dirn == -1 and 0 == col+1:
            return False

        if dirn == 1 and x2 != col:
            c = self.get_char(col)
            if c is None or c == '&nbsp;':
                return False

        self.highlight_cursor(False)

        col += dirn
        if col < x2 and col >= 0:
            self.word_selected_pos = col

        self.highlight_cursor(True)

        return True

    def onKeyUp(self, sender, keycode, modifiers):
        evt = DOM.eventGetCurrentEvent()
        DOM.eventCancelBubble(evt, True)
        DOM.eventPreventDefault(evt)

    def onKeyPress(self, sender, keycode, modifiers):
        evt = DOM.eventGetCurrentEvent()
        DOM.eventPreventDefault(evt)

    def highlight_cursor(self, highlight):
        """ highlights (or dehighlights) the currently selected cell
        """
        if self.word_selected_pos is None:
            return
        row = 0
        col = self.word_selected_pos
        self._highlight_cursor(row, col, highlight)

    def select_char(self, col):

        # de-highlight cursor
        self.highlight_cursor(False)

        if self.get_char(0) is None or self.get_char(0) == '&nbsp;':
            col = 0

        while (self.get_char(col-1) is None or \
              self.get_char(col-1) == '&nbsp;') and col > 1:
            col -= 1

        self.word_selected_pos = col
        self.highlight_cursor(True)

    def getMaxLength(self):
        return self.tp.getColumnCount()

    def setMaxLength(self, x):
        l = self.tp.getColumnCount()
        self.tp.resize(1, x)
        self.clear(l)

    def clear(self, fromrange=0):
        for i in range(fromrange, self.tp.getColumnCount()):
            self.set_grid_value("&nbsp;", 0, i)

    def onCellClicked(self, listener, row, col, direction=None):
        self.select_char(col)

    def cursorFlash(self, timr):
        if not self.focusset:
            return
        self.highlight_cursor(self.cstate)
        self.cstate = not self.cstate

    def onFocus(self, sender):
        self.focusset = True
        self.ctimer.scheduleRepeating(800)

    def onLostFocus(self, sender):
        self.focusset = False
        self.ctimer.cancel()
        self.highlight_cursor(False)

    def get_char(self, x):
        w = self.tp.getWidget(0, x)
        return w and w.getHTML()

    def getText(self):
        txt = ''
        for i in range(self.tp.getColumnCount()):
            c = self.get_char(i)
            if c is None or c == '&nbsp;':
                break
            txt += c
        return txt

    def setText(self, txt):
        self.clear()
        if len(txt) > self.getMaxLength(): # hm... cheat...
            self.setMaxLength(len(txt))
        for (i, c) in enumerate(txt):
            self.set_grid_value(c, 0, i)
        self.select_char(min(self.getMaxLength()-1, len(txt)))

Factory.registerClass('pyjamas.ui.InputBox', 'InputBox', InputBox)


