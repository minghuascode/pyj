# Copyright 2006 James Tauber and contributors
# Copyright (C) 2009 Luke Kenneth Casson Leighton <lkcl@lkcl.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pyjamas import DOM
from pyjamas import Factory

from pyjamas.ui.Widget import Widget
from pyjamas.ui.Focus import FocusMixin
from pyjamas.ui.ClickListener import ClickHandler
from pyjamas.ui.KeyboardListener import KeyboardHandler
from pyjamas.ui.FocusListener import FocusHandler
from pyjamas.ui.MouseListener import MouseHandler

class FocusWidget(Widget, FocusHandler, KeyboardHandler,
                          MouseHandler, ClickHandler,
                          FocusMixin):

    _props = [("readonly", "Read only", "Readonly", False),
            ] + Widget._props

    def __init__(self, element, **kwargs):
        self.setElement(element)
        Widget.__init__(self, **kwargs)
        FocusHandler.__init__(self)
        KeyboardHandler.__init__(self)
        ClickHandler.__init__(self)
        MouseHandler.__init__(self)

    def getProps(self):
        return self._props

# TODO: sort out Element **kwargs, see Factory.createWidgetOnElement
#Factory.registerClass('pyjamas.ui.FocusWidget', 'FocusWidget', FocusWidget)

