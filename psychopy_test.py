from psychopy import visual, core, event, gui #import some libraries from PsychoP
import os




win = visual.Window([800,600],monitor="testMonitor", units="deg")
rad = visual.RadialStim(win, mask='gauss', pos=(-4, 0), size=6, radialCycles=5, angularCycles=5, ori=45)
myGabor = visual.GratingStim(win,  mask='gauss', pos=(4, 0), size=6, ori=45, sf=5)  # gives a 'Gabor'
rect = visual.Rect(win, width=10, height=0.5, pos=(0, 4), fillColor="white")

w = 3.5
x_pos = -5 + w*0.5
rect2 = visual.Rect(win, width=w, height=0.5, pos=(x_pos, -4), fillColor="white")
rect.draw()
rect2.draw()
rad.draw()
myGabor.draw()
win.flip()
core.wait(6)

class Parent():
    def __init__(self, a):
        self.a = a
        self.f = f
    def print_a(self):
        print(self.a)

class Child(Parent):
    def __init__(self, **args):
        super(Child, self).__init__(**args)
        self.c = 111

b = Child(a='dfd')


#create a window
# def getinfo():
#     myDlg = gui.Dlg(title="This experiment")
#     myDlg.addText('Subject info')
#     myDlg.addField('Subject ID:', 'sub-')
#     ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
#
#     if myDlg.OK:  # or if ok_data is not None
#         return ok_data
#     else:
#         sys.exit('User cancelled!')
#
# subject_info = getinfo()
#
# win = visual.Window([800,600],monitor="testMonitor", units="deg")
# win.flip()
#
# core.wait(3)
