from psychopy import visual, core, event

#setup stimulus
win = visual.Window([800,600],monitor="testMonitor", units="deg")
grating = visual.GratingStim(win=win, mask='circle', size=3, pos=[-4,0], sf=3)

fixation = visual.GratingStim(win, tex=None, mask='cross', sf=0, size=1,
    name='fixation', autoLog=False)

clock = core.Clock()

#draw the stimuli and update the window
while True: #this creates a never-ending loop
    grating.setPhase(0.05, '+')#advance phase by 0.05 of a cycle
    grating.draw()
    fixation.draw()
    win.flip()

    if len(event.getKeys())>0:
        break
    event.clearEvents()

#cleanup
win.close()
core.quit()

