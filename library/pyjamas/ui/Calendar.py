# Date Time Example
# Copyright (C) 2009 Yit Choong (http://code.google.com/u/yitchoong/)
# Copyright (C) 2009 Luke Kenneth Casson Leighton <lkcl@lkcl.net>
# Copyright (C) 2012 Łukasz Mach <maho@pagema.net>

from pyjamas.ui.SimplePanel import SimplePanel
from pyjamas import Factory
from pyjamas.ui.VerticalPanel import  VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.PopupPanel import  PopupPanel
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Composite import Composite
from pyjamas.ui.Label import Label
from pyjamas.ui.Button import Button
from pyjamas.ui.Hyperlink import Hyperlink
from pyjamas.ui.HyperlinkImage import HyperlinkImage
from pyjamas.ui.HTML import HTML
from pyjamas.ui.FocusPanel import FocusPanel
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.Image import Image
from pyjamas.ui import HasAlignment
from pyjamas import DOM

import time
from datetime import datetime

BLANKCELL = "99"

class Calendar(FocusPanel):
    monthsOfYear = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    daysOfWeek = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
    daysOfWeek3 = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    today = 'Today'
    tomorrow = 'Tomorrow'
    yesterday = 'Yesterday'
    cancel = 'Cancel'

    def __init__(self, **kwargs):
        self.backyear = kwargs.pop('BackyearSymbol', '<<')
        self.backmonth = kwargs.pop('BackmonthSymbol', '<')
        self.fwdyear = kwargs.pop('FwdyearSymbol', '>>')
        self.fwdmonth = kwargs.pop('FwdmonthSymbol', '>')
        self.addbuttons = kwargs.pop('AddButtons', True)
        self.mindate = kwargs.pop('MinDate', None) # (yr, mnth, day)
        self.maxdate = kwargs.pop('MaxDate', None) # (yr, mnth, day)
        self.weekdaylength = kwargs.pop('WeekdayLength', 1) 
        if kwargs.pop('ArrowButtons', False):
            self.bkls = Button
        else:
            self.bkls = Hyperlink

        FocusPanel.__init__(self, **kwargs)

        self.setDate()

        self.todayYear = self.currentYear
        self.todayMonth = self.currentMonth
        self.todayDay = self.currentDay
        self.selectedDateListeners = []
        self.defaultGrid = None # used later

    def setDate(self, _date=None, m=None, d=None):
        """ _date - object of datetime.date class """
        if m is None and d is None:
            if _date is None:
                y, m, d = time.strftime("%Y-%m-%d").split("-")
            else:
                m = _date.month
                y = _date.year
                d = _date.day
        else:
            y = _date

        self.currentYear = int(y)
        self.currentMonth = int(m)
        self.currentDay = int(d)

    def getMonthsOfYear(self):
        return self.monthsOfYear

    def getDaysOfWeek(self):
        if self.weekdaylength == 1:
            return self.daysOfWeek
        return self.daysOfWeek3

    def addSelectedDateListener(self, listener):
        self.selectedDateListeners.append(listener)

    def removeSelectedDateListener(self, listener):
        self.selectedDateListeners.remove(listener)

    def isLeapYear(self, year):
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return True
        else:
            return False

    def _indaterange(self, year, mnth, day=None):

        if self.mindate is not None:
            if year < self.mindate[0]:
                return False
            if year == self.mindate[0]:
                if mnth < self.mindate[1]:
                    return False
                if day is not None:
                    if mnth == self.mindate[1] and day < self.mindate[2]:
                        return False

        if self.maxdate is not None:
            if year > self.maxdate[0]:
                return False
            if year == self.maxdate[0]:
                if mnth > self.maxdate[1]:
                    return False
                if day is not None:
                    if mnth == self.maxdate[1] and day > self.maxdate[2]:
                        return False

        return True

    def getDaysInMonth(self, mth, year):
        days = 0
        if mth in [1, 3, 5, 7, 8, 10, 12]:
            days=31
        elif mth in [4, 6, 9, 11]:
            days = 30
        elif (mth==2 and self.isLeapYear(year)):
            days = 29
        else:
            days = 28
        return days

    def setPosition(self, left, top):
        element = self.getElement()
        DOM.setStyleAttribute(element, "left", "%dpx" % left)
        DOM.setStyleAttribute(element, "top", "%dpx" % top)

    def show(self, left, top):
        if left < 0:
            left = 0
        if top < 0:
            top = 0
        self.setPosition(left, top)
        self.drawCurrent()
        self.setVisible(True)

    def drawCurrent(self):
        yr, mth, day = self.currentYear, self.currentMonth, self.currentDay
        self.draw(int(mth), int(yr))

    def draw(self, month , year):
        tod = time.localtime()
        mm = tod.tm_mon
        yy = tod.tm_year
        # has today changed and thus changed month? cater to rare case
        # where widget in created on last day of month and
        # page left till next day
        hasChangeMonth = False
        if yy != self.todayYear or mm != self.todayMonth:
            hasChangeMonth = True
            self.todayYear = yy
            self.todayMonth = mm

        # check to see if we have drawn the full widget before
        if self.defaultGrid is None:
            self.drawFull(month, year)
        else:
            # ok means we are re-drawing, but first check if it is the same
            # as the defaultGrid, if yes, just use it
            if not hasChangeMonth and month == self.todayMonth and \
                   year == self.todayYear:
                self.middlePanel.setWidget(self.defaultGrid)
                self.currentMonth = self.todayMonth
                self.currentYear = self.todayYear
            else:
                # we have to redraw the grid -- bah
                g = self.drawGrid(month, year)

                if hasChangeMonth:
                    # reset the default grid as we have changed months
                    self.defaultGrid = grid

            #
            # what about the title panel?
            #
            txt = "<b>"
            txt += self.getMonthsOfYear()[month-1] + "&nbsp;" + str(year)
            txt += "</b>"
            self.titlePanel.setWidget(HTML(txt))
            self.setVisible(True)

    def drawFull(self, month, year):
        # should be called only once when we draw the calendar for
        # the first time
        self.vp = VerticalPanel()
        self.vp.setSpacing(0)
        self.vp.setPadding(0)
        self.vp.addStyleName("calendarbox calendar-module calendar")
        self.setWidget(self.vp)
        self.setVisible(False)
        #
        mth = int(month)
        yr = int(year)

        tp = HorizontalPanel(Width="100%")
        tp.addStyleName("calendar-top-panel")
        tp.setSpacing(0)
        tp.setPadding(0)

        self.h1 = None
        self.h2 = None
        self.h4 = None
        self.h5 = None
        if self.backyear:
            self.h1 = self.bkls(self.backyear, StyleName="calendar-arrows")
            self.h1.addClickListener(getattr(self, 'onPreviousYear'))
            tp.add(self.h1)
            tp.setCellHorizontalAlignment(self.h1, "left")
        if self.backmonth:
            self.h2 = self.bkls(self.backmonth, StyleName="calendar-arrows")
            self.h2.addClickListener(getattr(self, 'onPreviousMonth'))
            tp.add(self.h2)
            tp.setCellHorizontalAlignment(self.h2, "left")

        # titlePanel can be changed, whenever we draw, so keep the reference
        txt = "<b>"
        txt += self.getMonthsOfYear()[mth-1] + " " + str(yr)
        txt += "</b>"
        self.titlePanel = SimplePanel()
        self.titlePanel.setWidget(HTML(txt))
        self.titlePanel.setStyleName("calendar-center")

        tp.add(self.titlePanel)
        tp.setCellHorizontalAlignment(self.titlePanel, "center")
        tp.setCellWidth(self.titlePanel, "100%")

        if self.fwdmonth:
            self.h4 = self.bkls(self.fwdmonth, StyleName="calendar-arrows")
            self.h4.addClickListener(getattr(self, 'onNextMonth'))
            tp.add(self.h4)
            tp.setCellHorizontalAlignment(self.h4, "right")
            tp.setCellWidth(self.h4, "100%")
            self.h4.setWidth("100%")
        if self.fwdyear:
            self.h5 = self.bkls(self.fwdyear, StyleName="calendar-arrows")
            self.h5.addClickListener(getattr(self, 'onNextYear'))
            tp.add(self.h5)
            tp.setCellHorizontalAlignment(self.h5, "right")

        tvp = VerticalPanel(Width="100%")
        tvp.setSpacing(2)
        tvp.add(tp)

        self.vp.add(tvp)

        # done with top panel

        self.middlePanel = SimplePanel()
        grid = self.drawGrid(mth, yr)
        self.middlePanel.setWidget(grid)
        self.vp.add(self.middlePanel)
        self.defaultGrid = grid

        if self.addbuttons:
            #
            # some links & handlers
            #
            bh1 = Hyperlink(self.yesterday)
            bh1.addClickListener(getattr(self, 'onYesterday'))
            bh2 = Hyperlink(self.today)
            bh2.addClickListener(getattr(self, 'onToday'))
            bh3 = Hyperlink(self.tomorrow)
            bh3.addClickListener(getattr(self, 'onTomorrow'))
            bh4 = Hyperlink(self.cancel)
            bh4.addClickListener(getattr(self, 'onCancel'))

            #
            # add code to test another way of doing the layout
            #
            b = HorizontalPanel()
            b.add(bh1)
            b.add(bh2)
            b.add(bh3)
            b.addStyleName("calendar-shortcuts")
            self.vp.add(b)
            b2 = SimplePanel()
            b2.add(bh4)
            b2.addStyleName("calendar-cancel")
            self.vp.add(b2)

        self.checkLinks(mth, yr)
        self.setVisible(True)

    def checkLinks(self, month, year):

        if self.backyear:
            ok = self._indaterange(year-1, month)
            self.h1.setEnabled(ok)
        if self.backmonth:
            py, pm = self._previousMonth(year, month)
            ok = self._indaterange(py, pm)
            print "prevmonth", month, year, py, pm, ok
            self.h2.setEnabled(ok)
        if self.fwdmonth:
            ny, nm = self._nextMonth(year, month)
            ok = self._indaterange(ny, nm)
            print "nextmonth", month, year, ny, nm, ok
            self.h4.setEnabled(ok)
        if self.fwdyear:
            ok = self._indaterange(year+1, month)
            self.h5.setEnabled(ok)

    def drawGrid(self, month, year):
        # draw the grid in the middle of the calendar

        self.checkLinks(month, year)

        daysInMonth = self.getDaysInMonth(month, year)
        # first day of the month & year
        secs = time.mktime((year, month, 1, 0, 0, 0, 0, 0, -1))
        struct = time.localtime(secs)
        # 0 - sunday for our needs instead 0 = monday in tm_wday
        startPos = (struct.tm_wday + 1) % 7
        slots = startPos + daysInMonth - 1
        rows = int(slots/7) + 1
        grid = Grid(rows+1, 7, # extra row for the days in the week
                    StyleName="calendar-grid") 
        grid.setWidth("100%")
        grid.addTableListener(self)
        self.middlePanel.setWidget(grid)
        cf = grid.getCellFormatter()
        #
        # put some content into the grid cells
        #
        for i in range(7):
            grid.setText(0, i, self.getDaysOfWeek()[i])
            cf.addStyleName(0, i, "calendar-header")
        #
        # draw cells which are empty first
        #
        day = 0
        pos = 0
        while pos < startPos:
            grid.setHTML(1, pos , BLANKCELL)
            cf.setStyleName(1, pos, "calendar-blank-cell")
            pos += 1
        # now for days of the month
        row = 1
        day = 1
        col = startPos
        while day <= daysInMonth:
            if pos % 7 == 0 and day != 1:
                row += 1
            col = pos % 7
            if not self._indaterange(self.currentYear, self.currentMonth, day):
                grid.setHTML(row, col, BLANKCELL)
                cf.setStyleName(row, col, "calendar-blank-cell")
                day += 1
                pos += 1
                continue
            grid.setHTML(row, col, str(day))
            if self.currentYear == self.todayYear and \
               self.currentMonth == self.todayMonth and day == self.todayDay:
                cf.setStyleName(row, col, "calendar-cell-today")
            else:
                cf.setStyleName(row, col, "calendar-day-cell")
            day += 1
            pos += 1
        #
        # now blank lines on the last row
        #
        col += 1
        while col < 7:
            grid.setHTML(row, col, BLANKCELL)
            cf.setStyleName(row, col, "calendar-blank-cell")
            col += 1

        return grid

    def onCellClicked(self, grid, row, col):
        if row == 0:
            return
        text = grid.getText(row, col).strip()
        if text == BLANKCELL:
            return
        try:
            selectedDay = int(text)
        except ValueError, e:
            return
        # fire event to all listeners
        for listener in self.selectedDateListeners:
            if hasattr(listener, "onDateSelected"):
                listener = listener.onDateSelected
            listener(self.currentYear, self.currentMonth, selectedDay)
        self.setVisible(False)

    def onPreviousYear(self, event):
        self.drawPreviousYear()

    def onPreviousMonth(self, event):
        self.drawPreviousMonth()

    def onNextMonth(self, event):
        self.drawNextMonth()

    def onNextYear(self, event):
        self.drawNextYear()

    def onDate(self, event, yy, mm, dd):
        for listener in self.selectedDateListeners:
            if hasattr(listener, "onDateSelected"):
                listener.onDateSelected(yy, mm, dd)
            else:
                listener(yy, mm, dd)
        self.setVisible(False)

    def onYesterday(self, event):
        yesterday = time.localtime(time.time() - 3600 * 24)
        mm = yesterday.tm_mon
        dd = yesterday.tm_mday
        yy = yesterday.tm_year
        self.onDate(event, yy, mm, dd)

    def onToday(self, event):
        tod = time.localtime()
        mm = tod.tm_mon
        dd = tod.tm_mday
        yy = tod.tm_year
        self.onDate(event, yy, mm, dd)

    def onTomorrow(self, event):
        tom = time.localtime(time.time() + 3600 * 24)
        mm = tom.tm_mon
        dd = tom.tm_mday
        yy = tom.tm_year
        self.onDate(event, yy, mm, dd)

    def onCancel(self, event):
        self.setVisible(False)

    def drawDate(self, month, year):
        self.currentMonth = month
        self.currentYear = year
        self.draw(self.currentMonth, self.currentYear)

    def _previousMonth(self, y=None, m=None):
        if y is None:
            y = self.currentYear
        if m is None:
            m = self.currentMonth
        if int(self.currentMonth) == 1:
            return (int(self.currentYear) - 1, 12)
        return int(self.currentYear), int(self.currentMonth) - 1

    def drawPreviousMonth(self):
        self.currentYear, self.currentMonth = self._previousMonth()
        self.draw(self.currentMonth, self.currentYear)
        self.checkLinks(self.currentMonth, self.currentYear)

    def _nextMonth(self, y=None, m=None):
        if y is None:
            y = self.currentYear
        if m is None:
            m = self.currentMonth
        if int(self.currentMonth) == 12:
            return (int(self.currentYear) + 1, 1)
        return int(self.currentYear), int(self.currentMonth) +1

    def drawNextMonth(self):
        self.currentYear, self.currentMonth = self._nextMonth()
        self.draw(self.currentMonth, self.currentYear)
        self.checkLinks(self.currentMonth, self.currentYear)

    def drawPreviousYear(self):
        self.currentYear = int(self.currentYear) - 1
        self.draw(self.currentMonth, self.currentYear)

    def drawNextYear(self):
        self.currentYear = int(self.currentYear) + 1
        self.draw(self.currentMonth, self.currentYear)

Factory.registerClass('pyjamas.ui.Calendar', 'Calendar', Calendar)


class DateField(Composite):

    icon_img = "icon_calendar.gif"
    icon_style = "calendar-img"
    today_text = "Today"
    today_style = "calendar-today-link"

    def __init__(self, format='%d-%m-%Y'):
        self.format = format
        self.tbox = TextBox()
        self.tbox.setVisibleLength(10)
        # assume valid sep is - / . or nothing
        if format.find('-') >= 0:
            self.sep = '-'
        elif format.find('/') >= 0:
            self.sep = '/'
        elif format.find('.') >= 0:
            self.sep = '.'
        else:
            self.sep = ''
        # self.sep = format[2] # is this too presumptious?
        self.calendar = Calendar()
        self.img = Image(self.icon_img)
        self.img.addStyleName(self.icon_style)
        self.calendarLink = HyperlinkImage(self.img)
        self.todayLink = Hyperlink(self.today_text)
        self.todayLink.addStyleName(self.today_style)
        #
        # lay it out
        #
        hp = HorizontalPanel()
        hp.setSpacing(2)
        vp = VerticalPanel()
        hp.add(self.tbox)
        vp.add(self.calendarLink)
        vp.add(self.todayLink)
        #vp.add(self.calendar)
        hp.add(vp)

        Composite.__init__(self)
        self.initWidget(hp)
        #
        # done with layout, so now set up some listeners
        #
        self.tbox.addFocusListener(self) # hook to onLostFocus
        self.calendar.addSelectedDateListener(getattr(self, "onDateSelected"))
        self.todayLink.addClickListener(getattr(self, "onTodayClicked"))
        self.calendarLink.addClickListener(getattr(self, "onShowCalendar"))

    def getTextBox(self):
        return self.tbox

    def getCalendar(self):
        return self.calendar

    def setID(self, id):
        self.tbox.setID(id)

    def onDateSelected(self, yyyy, mm, dd):
        secs = time.mktime((int(yyyy), int(mm), int(dd), 0, 0, 0, 0, 0, -1))
        d = time.strftime(self.format, time.localtime(secs))
        self.tbox.setText(d)

    def onLostFocus(self, sender):
        #
        text = self.tbox.getText().strip()
        # if blank - leave it alone
        if text and len(text) == 8:
            # ok what format do we have? assume ddmmyyyy --> dd-mm-yyyy
            txt = text[0:2] + self.sep + text[2:4] + self.sep + text[4:8]
            self.tbox.setText(txt)

    def onFocus(self, sender):
        pass

    def onTodayClicked(self, event):
        today = time.strftime(self.format)
        self.tbox.setText(today)

    def onShowCalendar(self, sender):
        txt = self.tbox.getText().strip()
        try:
            if txt:
                _d = datetime.strptime(txt,self.format).date()
                self.calendar.setDate(_d)
        except ValueError: pass

        p = CalendarPopup(self.calendar)
        x = self.tbox.getAbsoluteLeft() + 10
        y = self.tbox.getAbsoluteTop() + 10
        p.setPopupPosition(x, y)
        p.show()

Factory.registerClass('pyjamas.ui.Calendar', 'DateField', DateField)


class CalendarPopup(PopupPanel):
    def __init__(self, c):
        PopupPanel.__init__(self, True)
        p = SimplePanel()
        p.add(c)
        c.show(10, 10)
        p.setWidth("100%")
        self.setWidget(p)

Factory.registerClass('pyjamas.ui.Calendar', 'CalendarPopup', CalendarPopup)

