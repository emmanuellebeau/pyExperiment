#from psychopy import visual, core, event, gui #import some libraries from PsychoP
import os

from tkinter import *
fields = [('Subject ID', 'Entry'), ('Age', 'Entry'), ('Run', 'List'), ('Session', 'List')]

def fetch(entries):
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        print('%s: "%s"' % (field, text))
    root.destroy()

def makeform(root, fields):
    entries = []
    for field, type in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w')
        if type=='Entry':
            if field == 'Subject ID':
                ent = Entry(row)
                ent.insert(END, 'sub-')
            else:
                ent = Entry(row)
            entries.append((field, ent))
        else:
            var = IntVar()
            var.set(1)
            ent = OptionMenu(row, var, *list(range(10)))
            entries.append((field, var))

        row.pack(side=TOP, fill=X, padx=2, pady=2)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)


    return entries
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


root = Tk()
root.attributes("-topmost", True)
root.title('Test')
ents = makeform(root, fields)
root.bind('<Return>', (lambda event, e=ents: fetch(e)))
b1 = Button(root, text='OK',
      command=(lambda e=ents: fetch(e)))
b1.pack(side=LEFT, padx=5, pady=5)
b2 = Button(root, text='Quit', command=root.destroy)
b2.pack(side=LEFT, padx=5, pady=5)
center(root)
root.mainloop()



# win = visual.Window([800,600],monitor="testMonitor", units="deg")
# rad = visual.RadialStim(win, mask='gauss', pos=(-4, 0), size=6, radialCycles=5, angularCycles=5, ori=45)
# myGabor = visual.GratingStim(win,  mask='gauss', pos=(4, 0), size=6, ori=45, sf=5)  # gives a 'Gabor'
# rect = visual.Rect(win, width=10, height=0.5, pos=(0, 4), fillColor="white")
#
# w = 3.5
# x_pos = -5 + w*0.5
# rect2 = visual.Rect(win, width=w, height=0.5, pos=(x_pos, -4), fillColor="white")
# rect.draw()
# rect2.draw()
# rad.draw()
# myGabor.draw()
# win.flip()
# core.wait(6)

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
