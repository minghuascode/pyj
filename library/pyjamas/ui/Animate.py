from pyjamas import DOM
from pyjamas import Window
from pyjamas.Timer import Timer

class Movement(object):

    def __init__(self, vel_x=0, vel_y=0, accel_x=0.0, accel_y=0.0,
                       end_action=None):
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.accel_x = accel_x
        self.accel_y = accel_y
        self.end_action = end_action

    def move(self, widget):
        left = widget.getParent().getWidgetLeft(widget)
        top = widget.getParent().getWidgetTop(widget)
        print left, top
        left = left or 0
        top = top or 0
        left += self.vel_x
        top += self.vel_y
        self.vel_x += self.accel_x
        self.vel_y += self.accel_y
        widget.getParent().setWidgetPosition(widget, left, top)
        return (left, top)

    def move_off_screen(self, widget):
        (left, top) = self.move(widget)
        width = widget.getOffsetWidth()
        height = widget.getOffsetHeight()
        if (left + width) <= 0:
            return self.end(widget)
        if (top + height) <= 0:
            return self.end(widget)
        width = Window.getClientWidth()
        height = Window.getClientHeight()
        if left >= width:
            return self.end(widget)
        if top >= height:
            return self.end(widget)
        return True
 
    def end(self, widget):
        if self.end_action:
            self.end_action()


class Animate(object):

    def __init__(self, widget, action, fps=50):
        self.widget = widget
        self.action = action
        self.fps = fps

        self.timer = Timer(0, self)
        self.timer.scheduleRepeating(int(1000.0/fps))

    def onTimer(self, sender):
        params = self.action(self.widget)
        if not params:
            self.timer.cancel()
            return
