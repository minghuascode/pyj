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

# setWidget recoded to call _mapWidget - makes support for mshtml simpler
# added by Phil Charlesworth 2010-09-16
#
# removeWidget recoded to call _unmapWidget - makes support for mshtml simpler
# added by Phil Charlesworth 2010-09-16
#

from pyjamas import DOM
from pyjamas import Factory

from pyjamas.ui.Panel import Panel
from pyjamas.ui import Event
from pyjamas.ui.CellFormatter import CellFormatter
from pyjamas.ui.RowFormatter import RowFormatter

widgethash = {}

def _getargs(parent, args):
    row, col = parent.getIndex(args[0])
    return row, col, args[1]

class HTMLTable(Panel):

    _props = [ ("border", "Border width", "BorderWidth", int),
              ("spacing", "Spacing", "CellSpacing", None),
              ("padding", "Padding", "CellPadding", None)
             ]

    elem_props = [
           ("visible", "Cell Visible", "CellVisible", None, True),
           ("wordwrap", "Cell Word wrap", "CellWordWrap", None, True),
           ("stylename", "Cell Style", "CellStyleName", None, ""),
           ("height", "Cell Height", "CellHeight", str, None),
           ("width", "Cell Width", "CellWidth", str, None),
           ("halign", "Cell Horizontal Alignment",
                      "CellHorizontalAlignment", None, "left"),
           ("valign", "Cell Vertical Alignment",
                      "CellVerticalAlignment", None, "top"),
                 ]

    def _getElementProps(self):
        return Panel._getElementProps() + self.elem_props

    def __init__(self, **kwargs):
        if not kwargs.has_key('CellFormatter'):
            kwargs['CellFormatter'] = CellFormatter(self)
        if not kwargs.has_key('RowFormatter'):
            kwargs['RowFormatter'] = RowFormatter(self)

        self.tableListeners = []
        self.dbltableListeners = []
        self.widgetMap = {}

        if kwargs.has_key('Element'):
            self.tableElem = kwargs.pop('Element')
            fc = DOM.getFirstChild(self.tableElem)
            if fc:
                self.bodyElem = fc
            else:
                self.bodyElem = DOM.createTBody()
                DOM.appendChild(self.tableElem, self.bodyElem)
        else:
            self.tableElem = DOM.createTable()
            self.bodyElem = DOM.createTBody()
            DOM.appendChild(self.tableElem, self.bodyElem)
        self.setElement(self.tableElem)

        self.sinkEvents(Event.ONCLICK | Event.ONDBLCLICK)

        Panel.__init__(self, **kwargs)

    @classmethod
    def _getProps(self):
        return Panel._getProps() + self._props

    def addDblTableListener(self, listener):
        self.dbltableListeners.append(listener)

    def addTableListener(self, listener):
        self.tableListeners.append(listener)

    def clear(self):
        for row in range(self.getRowCount()):
            for col in range(self.getCellCount(row)):
                child = self.getWidget(row, col)
                if child is not None:
                    self.removeWidget(child)
                else:
                    self.clearCell(row, col)
        # assert len(self.widgetMap) == 0

    def clearCell(self, row, column):
        td = self.cellFormatter.getElement(row, column)
        return self.internalClearCell(td)

    def getCellCount(self, row):
        return 0

    def getCellFormatter(self):
        return self.cellFormatter

    def getCellPadding(self):
        return DOM.getIntAttribute(self.tableElem, "cellPadding")

    def getCellSpacing(self):
        return DOM.getIntAttribute(self.tableElem, "cellSpacing")

    def getHTML(self, row, column):
        element = self.cellFormatter.getElement(row, column)
        return DOM.getInnerHTML(element)

    def getRowCount(self):
        return 0

    def getRowFormatter(self):
        return self.rowFormatter

    def getText(self, row, column):
        self.checkCellBounds(row, column)
        element = self.cellFormatter.getElement(row, column)
        return DOM.getInnerText(element)

    # also callable as getWidget(widgetElement)
    def getWidget(self, row, column=None):
        if column is None:
            key = self.computeKeyForElement(row)
        else:
            self.checkCellBounds(row, column)
            key = self.computeKey(row, column)

        if key is None:
            return None
        return self.widgetMap[key]

    # next three functions are part of the standard Builder API for panels
    def getIndex(self, widget):
        """ given a widget, return its index.
        """
        for row in xrange(self.getDOMRowCount()):
            for col in xrange(self.getDOMCellCount(row)):
                if self.getWidget(row, col) is widget:
                    return (row, col)
        return None

    def getIndexedChild(self, index):
        return self.getWidget(index[0], index[1])

    def addIndexedItem(self, index, item):
        row, col = index
        while row >= self.getDOMRowCount():
            self.insertRow(self.getDOMRowCount())
        while col >= self.getDOMCellCount(row):
            self.insertCells(row, self.getDOMCellCount(row), 1)
        self.setWidget(row, col, item)
        
    def add(self, item, row, col):
        self.addIndexedItem((row, col), item)

    def isCellPresent(self, row, column):
        # GWT uses "and", possibly a bug
        if row >= self.getRowCount() or row < 0:
            return False

        if column < 0 or column >= self.getCellCount(row):
            return False

        return True

    def __iter__(self):
        """ only gets widgets: does not obtain HTML or Text cells!
        """
        return self.widgetMap.itervalues()

    def _onBrowserEvent(self, event, event_type):

        td = self.getEventTargetCell(event)
        if td is None:
            return
        tr = DOM.getParent(td)
        body = DOM.getParent(tr)
        row = DOM.getChildIndex(body, tr)
        column = DOM.getChildIndex(tr, td)

        if event_type == 'dblclick':
            lists = self.dbltableListeners
        else:
            lists = self.tableListeners

        for listener in lists:
            if event_type == 'click' and \
               hasattr(listener, 'onCellClicked'):
                listener.onCellClicked(self, row, column)
            elif event_type == 'dblclick' and \
               hasattr(listener, 'onCellDoubleClicked'):
                listener.onCellDoubleClicked(self, row, column)
            else:
                listener(self)

    def onBrowserEvent(self, event):
        event_type = DOM.eventGetType(event)
        if event_type != "dblclick" and event_type != "click":
            return 

        self._onBrowserEvent(event, event_type)

    def remove(self, widget):
        if widget.getParent() != self:
            return False

        self.removeWidget(widget)
        return True

    def removeDblClickTableListener(self, listener):
        self.dbltableListeners.remove(listener)

    def removeTableListener(self, listener):
        self.tableListeners.remove(listener)

    def setBorderWidth(self, width):
        if width is None:
            DOM.removeAttribute(self.tableElem, "border")
        else:
            DOM.setAttribute(self.tableElem, "border", str(width))

    def setCellPadding(self, padding):
        DOM.setAttribute(self.tableElem, "cellPadding", str(padding))

    def setCellSpacing(self, spacing):
        DOM.setAttribute(self.tableElem, "cellSpacing", str(spacing))

    def setHTML(self, row, column, html):
        self.prepareCell(row, column)
        td = self.cleanCell(row, column)
        if html is not None:
            DOM.setInnerHTML(td, html)

    def setText(self, row, column, text):
        self.prepareCell(row, column)
        td = self.cleanCell(row, column)
        if text is not None:
            DOM.setInnerText(td, text)

    def setWidget(self, row, column, widget):
        self.prepareCell(row, column)
        if widget is None:
            return

        widget.removeFromParent()
        td = self.cleanCell(row, column)
        self._mapWidget(widget)
        self.adopt(widget, td)

    def _mapWidget(self, widget):
        widget_hash = widget
        element = widget.getElement()
        widgethash[element] = widget_hash
        self.widgetMap[widget_hash] = widget

    def cleanCell(self, row, column):
        td = self.cellFormatter.getRawElement(row, column)
        self.internalClearCell(td)
        return td

    def computeKey(self, row, column):
        element = self.cellFormatter.getRawElement(row, column)
        child = DOM.getFirstChild(element)
        if child is None:
            return None

        return self.computeKeyForElement(child)

    def computeKeyForElement(self, widgetElement):
        return widgethash.get(widgetElement)

    def removeWidget(self, widget):
        self.disown(widget)
        self._unmapWidget(widget)
        return True

    def _unmapWidget(self, widget):
        element = widget.getElement()
        del self.widgetMap[self.computeKeyForElement(element)]
        del widgethash[element]
    
    def checkCellBounds(self, row, column):
        self.checkRowBounds(row)
        #if column<0: raise IndexError, "Column " + column + " must be non-negative: " + column

        cellSize = self.getCellCount(row)
        #if cellSize<column: raise IndexError, "Column " + column + " does not exist, col at row " + row + " size is " + self.getCellCount(row) + "cell(s)"

    def checkRowBounds(self, row):
        rowSize = self.getRowCount()
        #if row >= rowSize or row < 0: raise IndexError, "Row " + row + " does not exist, row size is " + self.getRowCount()

    def createCell(self):
        return DOM.createTD()

    def getBodyElement(self):
        return self.bodyElem

    # also callable as getDOMCellCount(row)
    def getDOMCellCount(self, element, row=None):
        if row is None:
            return self.getDOMCellCountImpl(self.bodyElem, element)
        return self.getDOMCellCountImpl(element, row)

    def getDOMCellCountImpl(self, element, row):
        return element.rows.item(row).cells.length

    # also callable as getDOMRowCount(element)
    def getDOMRowCount(self, element=None):
        if element is None:
            element = self.bodyElem
        return self.getDOMRowCountImpl(element)

    def getDOMRowCountImpl(self, element):
        return element.rows.length

    def getEventTargetCell(self, event):
        td = DOM.eventGetTarget(event)
        while td is not None:
            tagName = DOM.getAttribute(td, "tagName")
            if tagName is not None and tagName.lower() == "td":
                tr = DOM.getParent(td)
                body = DOM.getParent(tr)
                if DOM.compare(body, self.bodyElem):
                    return td
            if DOM.compare(td, self.bodyElem):
                return None
            td = DOM.getParent(td)

        return None

    def insertCell(self, row, column):
        tr = self.rowFormatter.getRow(self.bodyElem, row)
        td = self.createCell()
        DOM.insertChild(tr, td, column)

    def insertCells(self, row, column, count):
        tr = self.rowFormatter.getRow(self.bodyElem, row)
        for i in range(column, column + count):
            td = self.createCell()
            DOM.insertChild(tr, td, i)

    def insertRow(self, beforeRow):
        if beforeRow != self.getRowCount():
            self.checkRowBounds(beforeRow)

        tr = DOM.createTR()
        DOM.insertChild(self.bodyElem, tr, beforeRow)
        return beforeRow

    def internalClearCell(self, td):
        maybeChild = DOM.getFirstChild(td)
        widget = None
        if maybeChild is not None:
            widget = self.getWidget(maybeChild)

        if widget is not None:
            self.removeWidget(widget)
            return True

        DOM.setInnerHTML(td, "")
        return False

    def prepareCell(self, row, column):
        pass

    def prepareRow(self, row):
        pass

    def removeCell(self, row, column):
        self.checkCellBounds(row, column)
        td = self.cleanCell(row, column)
        tr = self.rowFormatter.getRow(self.bodyElem, row)
        DOM.removeChild(tr, td)

    def removeRow(self, row):
        for column in range(self.getCellCount(row)):
            self.cleanCell(row, column)
        DOM.removeChild(self.bodyElem, self.rowFormatter.getRow(self.bodyElem, row))

    def setCellFormatter(self, cellFormatter):
        self.cellFormatter = cellFormatter

    def setRowFormatter(self, rowFormatter):
        self.rowFormatter = rowFormatter

    def getCellVisible(self, context):
        row, col = self.getIndex(context)
        print "getCellVisible", self, context, row, col
        self.getCellFormatter().getVisible(row, col)

    def getCellWidth(self, context):
        row, col = self.getIndex(context)
        self.getCellFormatter().getWidth(row, col)

    def getCellHeight(self, context):
        row, col = self.getIndex(context)
        self.getCellFormatter().getHeight(row, col)

    def getCellWordWrap(self, context):
        row, col = self.getIndex(context)
        self.getCellFormatter().getWordWrap(row, col)

    def getCellStyleName(self, context):
        row, col = self.getIndex(context)
        self.getCellFormatter().getStyleName(row, col)

    def getCellVerticalAlignment(self, context):
        row, col = self.getIndex(context)
        self.getCellFormatter().getVerticalAlignment(row, col)

    def getCellHorizontalAlignment(self, context):
        row, col = self.getIndex(context)
        print "getHorizontalAlignment", self, context, row, col
        self.getCellFormatter().getHorizontalAlignment(row, col)

    def setCellVisible(self, context, val):
        row, col = self.getIndex(context)
        print "setCellVisible", self, context, row, col, val
        self.getCellFormatter().setVisible(row, col, val)

    def setCellWidth(self, context, val):
        row, col = self.getIndex(context)
        self.getCellFormatter().setWidth(row, col, val)

    def setCellHeight(self, context, val):
        row, col = self.getIndex(context)
        self.getCellFormatter().setHeight(row, col, val)

    def setCellWordWrap(self, context, val):
        row, col = self.getIndex(context)
        self.getCellFormatter().setWordWrap(row, col, val)

    def setCellStyleName(self, context, val):
        row, col = self.getIndex(context)
        self.getCellFormatter().setStyleName(row, col, val)

    def setCellVerticalAlignment(self, context, val):
        row, col = self.getIndex(context)
        self.getCellFormatter().setVerticalAlignment(row, col, val)

    def setCellHorizontalAlignment(self, context, val):
        row, col = self.getIndex(context)
        print "setHorizontalAlignment", self, context, row, col, val
        self.getCellFormatter().setHorizontalAlignment(row, col, val)


Factory.registerClass('pyjamas.ui.HTMLTable', 'HTMLTable', HTMLTable)

