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
import pyjd
if pyjd.is_desktop:
    from __pyjamas__ import doc
from pyjamas import Factory

from pyjamas import DOM

from pyjamas.ui.HTMLTable import HTMLTable
from pyjamas.ui.RowFormatter import RowFormatter
from pyjamas.ui.FlexCellFormatter import FlexCellFormatter 

class FlexTable(HTMLTable):
    def __init__(self, **kwargs):
        if not kwargs.has_key('CellFormatter'):
            kwargs['CellFormatter'] = FlexCellFormatter(self)
        HTMLTable.__init__(self, **kwargs)

    elem_props = HTMLTable.elem_props + [
           ("rowspan", "Cell Row Span", "CellRowSpan", int, None),
           ("colspan", "Cell Column Span", "CellColSpan", int, None),
                 ]

    def _getElementProps(self):
        return self.elem_props

    def addCell(self, row):
        self.insertCell(row, self.getCellCount(row))

    def getCellCount(self, row):
        self.checkRowBounds(row)
        return self.getDOMCellCount(self.getBodyElement(), row)

    def getFlexCellFormatter(self):
        return self.getCellFormatter()

    def getRowCount(self):
        return self.getDOMRowCount()

    def removeCells(self, row, column, num):
        for i in range(num):
            self.removeCell(row, column)

    def prepareCell(self, row, column):
        self.prepareRow(row)
        #if column < 0: throw new IndexOutOfBoundsException("Cannot create a column with a negative index: " + column);

        cellCount = self.getCellCount(row)
        required = column + 1 - cellCount
        if required > 0:
            self.addCells(self.getBodyElement(), row, required)

    def prepareRow(self, row):
        #if row < 0: throw new IndexOutOfBoundsException("Cannot create a row with a negative index: " + row);

        rowCount = self.getRowCount()
        for i in range(rowCount, row + 1):
            self.insertRow(i)

    def addCells(self, table, row, num):
        rowElem = table.rows.item(row)
        for i in range(num):
            cell = doc().createElement("td")
            rowElem.appendChild(cell)

    def getCellColSpan(self, context):
        row, col = self.getIndex(context)
        self.getCellFormatter().getColSpan(row, col)

    def setCellColSpan(self, context, val):
        row, col = self.getIndex(context)
        self.getCellFormatter().setColSpan(row, col, val)

    def getCellRowSpan(self, context):
        row, col = self.getIndex(context)
        self.getCellFormatter().getRowSpan(row, col)

    def setCellRowSpan(self, context, val):
        row, col = self.getIndex(context)
        self.getCellFormatter().setRowSpan(row, col, val)


Factory.registerClass('pyjamas.ui.FlexTable', 'FlexTable', FlexTable)

