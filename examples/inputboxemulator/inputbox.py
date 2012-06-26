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

from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.InputBox import InputBox


if __name__ == '__main__':
    pyjd.setup("./public/inputbox.html")
    app = InputBox(MatchPattern="^[0-9,A-Z,:]*$")
    app.setMaxLength(20)
    RootPanel("keypad").add(app)

    pyjd.run()

