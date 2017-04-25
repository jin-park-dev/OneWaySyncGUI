from tkinter import *
import threading
from tkinter import filedialog
from functools import partial
from tkinter import ttk
import time

import utils


"""
contains GUI related info
"""


# original_folder = r'X:\1 Music Vid\1 Dances\1 Lessons\1 Lessons Share'
# copy_folder = r'D:\OneDrive\Pictures\4 Sharing with Others\Dances'

def run_sync():
    progbar.start(interval=2)
    path_source = entry_source.get()
    path_destination = entry_destination.get()

    def callback():
        test_obj = utils.MyCopier(path_source, path_destination)
        test_obj.run()
    t_sync = threading.Thread(target=callback)
    t_sync.start()


    def progress_checker():
        time.sleep(0.2)
        run_cond = True
        progbar.stop()
        progbar.start(interval=50)
        while run_cond:
            if not t_sync.is_alive():
                run_cond = False
                progbar.stop()
            time.sleep(0.5)

    #what I want to do is while thread above is alive keep progress bar running.

    t_checker = threading.Thread(target=progress_checker)
    t_checker.start()


def choose_paths(entry):
    entry_previous = entry.get()
    entry_previous_len = len(entry.get())

    entry.delete(0, last=entry_previous_len)
    entry.insert(0, filedialog.askdirectory())

    entry_new_len = len(entry.get())
    if entry_new_len == 0:
        entry.insert(0, entry_previous)

root = Tk()

root.iconbitmap(default="Connection Sync-50.ico")
root.wm_title("Dance Sync (1-way)")
#root.resizable(width=False, height=False)
root.wm_resizable(width=False, height=False)



Label(root, text="Source").grid(row=0, column=0)
Label(root, text="Destination").grid(row=1, column=0)

entry_source = Entry(root, width=100)
entry_source.grid(row=0, column=1)
entry_source.insert(0, r'X:\1 Music Vid\1 Dances\1 Lessons\1 Lessons Share')
entry_partial = partial(choose_paths, entry_source)
Button(root, text="...", command=entry_partial).grid(row=0, column=3)


entry_destination = Entry(root, width=100)
entry_destination.grid(row=1, column=1)
entry_destination.insert(0, r'D:\OneDrive\Pictures\4 Sharing with Others\Dances')
destination_partial = partial(choose_paths, entry_destination)
Button(root, text="...", command=destination_partial).grid(row=1, column=3)

progbar = ttk.Progressbar(root, mode='indeterminate', length = 600)
progbar.grid(row=2, columnspan=3)


#Enables, or disables showing of log_box.
log_box = Text(root)
is_there_log = False
def enable_log():
    if not is_there_log:
        global is_there_log
        is_there_log = True
        log_box.grid(row=5, columnspan=3)
    elif is_there_log:
        global is_there_log
        is_there_log = False
        log_box.grid_remove()

label_enable_copy = Label(root, text='Enable Copy')
label_enable_copy.grid(row=3, column=1)
var_enable_copy = IntVar()
checkBtn_enable_copy = Checkbutton(root, variable=var_enable_copy)
checkBtn_enable_copy.grid(row=4, column=1)


Button(root, text="Sync", command=run_sync).grid(row=4, column=0)
Button(root, text="Log", command=enable_log).grid(row=4, column=2)
Button(root, text="Quit", command=root.quit).grid(row=4, column=3)
# Button(root, text="Dev_Test", command=clear_entry).grid(row=2, column=3)
