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
from pyjamas import Factory
from pyjamas import DOM

from pyjamas.ui.ComplexPanel import ComplexPanel

class AbsolutePanel(ComplexPanel):

    elem_props = [
           ("left", "Widget Left Position", "WidgetLeftPos", None, None),
           ("top", "Widget Top Position", "WidgetTopPos", None, None),
            ]

    def _getElementProps(self):
        return ComplexPanel._getElementProps() + self.elem_props
    
    def __init__(self, **ka):
        element = ka.pop('Element', None) or DOM.createDiv()
        self.setElement(element)
        DOM.setStyleAttribute(element, "position", "relative")
        DOM.setStyleAttribute(element, "overflow", "hidden")
        ComplexPanel.__init__(self, **ka)

    def add(self, widget, left=None, top=None):
        ComplexPanel.add(self, widget, self.getElement())

        if left is not None or top is not None:
            self.setWidgetPosition(widget, left, top)

    def getWidgetPosition(self, widget):
        self.checkWidgetParent(widget)

        h = widget.getElement()
        return DOM.getStyleAttribute(h, "left"), DOM.getStyleAttribute(h, "top")

    def setWidgetLeftPos(self, widget, left):
        self.setWidgetPosition(widget, left=left)

    def setWidgetTopPos(self, widget, top):
        self.setWidgetPosition(widget, top=top)

    def getWidgetLeftPos(self, widget):
        self.checkWidgetParent(widget)
        return DOM.getStyleAttribute(widget.getElement(), "top")

    def getWidgetTopPos(self, widget):
        self.checkWidgetParent(widget)
        return DOM.getStyleAttribute(widget.getElement(), "left")

    def setWidgetPosition(self, widget, left=None, top=None):
        self.checkWidgetParent(widget)

        h = widget.getElement()
        if (left == -1) and (top == -1):
            DOM.setStyleAttribute(h, "left", "")
            DOM.setStyleAttribute(h, "top", "")
            DOM.setStyleAttribute(h, "position", "static")
        else:
            DOM.setStyleAttribute(h, "position", "absolute")
            if left is not None:
                if not isinstance(left, basestring):
                    left = "%dpx" % left
                DOM.setStyleAttribute(h, "left", left)
            if top is not None:
                if not isinstance(top, basestring):
                    top = "%dpx" % top
                DOM.setStyleAttribute(h, "top", top)

    def getWidgetLeft(self, widget):
        self.checkWidgetParent(widget)
        return DOM.getIntAttribute(widget.getElement(), "offsetLeft")

    def getWidgetTop(self, widget):
        self.checkWidgetParent(widget)
        return DOM.getIntAttribute(widget.getElement(), "offsetTop")

    def checkWidgetParent(self, widget):
        if widget.getParent() != self:
            raise Exception("Widget must be a child of this panel.")

Factory.registerClass('pyjamas.ui.AbsolutePanel', 'AbsolutePanel', AbsolutePanel)

