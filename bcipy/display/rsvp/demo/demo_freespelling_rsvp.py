from psychopy import visual, core

from bcipy.display.rsvp.rsvp_disp_modes import FreeSpellingDisplay
from bcipy.helpers.triggers import _write_triggers_from_sequence_free_spell
from bcipy.acquisition.marker_writer import NullMarkerWriter

# Initialize Stimulus Parameters
# Task Bar
color_task = 'White'
font_task = 'Times'
height_task = 0.1
text_task = ' '

# Text Bar
color_text = 'white'
font_text = 'Times'

pos_text = (0, -.75)
text_text = 'Demo For Free Spelling Task'
txt_height = 0.1

# Stimuli
font_sti = 'Times'
pos_sti = (0, 0)
sti_height = 0.6

# Initialize Stimulus
is_txt_sti = True

if is_txt_sti:
    ele_sti = [
        ['+', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', '<', '-', 'L'],
        ['+', 'F', 'G', 'E', '-', 'S', 'Q', 'W', 'E', '<', 'A', 'Z'],
        ['+', 'F', 'G', 'E', '-', 'S', 'Q', 'W', 'E', '<', 'A', 'Z'],
        ['+', 'F', 'G', 'E', '-', 'S', 'Q', 'W', 'E', '<', 'A', 'Z']]
    color_sti = [['red', 'white', 'white', 'white', 'white', 'white',
                  'white', 'white', 'white', 'white', 'white', 'white']] * 4
else:
    ele_sti = [['static/images/RSVP_images/A.jpg',
                'static/images/RSVP_images/Red_Cross.png',
                'static/images/RSVP_images/C.jpg',
                'static/images/RSVP_images/D.jpg',
                'static/images/RSVP_images/E.jpg',
                'static/images/RSVP_images/P.jpg'],
               ['static/images/RSVP_images/T.jpg',
                'static/images/RSVP_images/Red_Cross.png',
                'static/images/RSVP_images/B.jpg',
                'static/images/RSVP_images/C.jpg',
                'static/images/RSVP_images/D.jpg',
                'static/images/RSVP_images/E.jpg']]

time_flash = .25
time_target = 2
time_cross = .6

timing_sti = [[time_cross] + [time_flash] * (len(ele_sti[0]) - 1)] * 4

task_text = ['', 'L', 'LO', 'LOL']
task_color = [['white'], ['white'], ['white'], ['white']]

# Initialize decision
ele_list_dec = [None, ['[L]'], ['[O]'], ['[L]']]
ele_list_dec_time = [[0], [2], [2], [2]]

# Initialize Window
win = visual.Window(size=[500, 500], screen=0, allowGUI=False,
                    allowStencil=False, monitor='testMonitor', color='black',
                    colorSpace='rgb', blendMode='avg',
                    waitBlanking=True,
                    winType='pyglet',)
win.recordFrameIntervals = True
frameRate = win.getActualFrameRate()

print(frameRate)

# Initialize Clock
clock = core.StaticPeriod(screenHz=frameRate)
experiment_clock = core.MonotonicClock(start_time=None)


rsvp = FreeSpellingDisplay(
    window=win, clock=clock,
    experiment_clock=experiment_clock,
    marker_writer=NullMarkerWriter(),
    text_info=text_text,
    color_info=color_text, pos_info=pos_text,
    height_info=txt_height,
    font_info=font_text,
    color_task=['white'],
    font_task=font_task, text_task=' ',
    height_task=height_task,
    font_sti=font_sti, pos_sti=pos_sti,
    sti_height=sti_height,
    stim_sequence=['a'] * 10, color_list_sti=['white'] * 10,
    time_list_sti=[3] * 10,
    is_txt_sti=is_txt_sti)

counter = 0
decision_made = 0

# uncomment trigger_file lines for demo with triggers!
# trigger_file = open('free_spell_trigger_trigger_file.txt', 'w')
for idx_o in range(len(task_text)):

    if decision_made == 1:
        decision_made = 0

    rsvp.draw_static()
    win.flip()
    rsvp.sti.height = sti_height

    # Schedule a sequence
    rsvp.stim_sequence = ele_sti[counter]
    if is_txt_sti:
        rsvp.color_list_sti = color_sti[counter]

    rsvp.time_list_sti = timing_sti[counter]

    core.wait(.4)

    sequence_timing = rsvp.do_sequence()

#     # if wanting to test triggers from display
    # _write_triggers_from_sequence_free_spell(sequence_timing, trigger_file)

    core.wait(.5)
    counter += 1

    if ele_list_dec[idx_o] is not None:
        # Get stimuli parameters
        rsvp.stim_sequence = ele_list_dec[idx_o]
        rsvp.color_list_sti = ['green']
        rsvp.time_list_sti = ele_list_dec_time[idx_o]
        rsvp.do_sequence()
        decision_made = 1
        rsvp.update_task_state(text=task_text[idx_o],
                               color_list=task_color[idx_o])

    core.wait(.5)

win.close()
# trigger_file.close()

# Print intervals
# intervalsMS = np.array(win.frameIntervals) * 1000
# print(intervalsMS)
