import PySimpleGUI as sg
import time
from csv import writer
from datetime import datetime
from os.path import exists

OUTPUT_PATH = "timely_data.csv"
sg.ChangeLookAndFeel('LightGreen')

def create_csv():
    with open(OUTPUT_PATH, "w", newline="") as f:
        csv_writer = writer(f)
        csv_writer.writerow(["Task", "Elapsed", "Start", "End"])

def format_time(elapsed_time):
    return time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

def append_to_csv(task_name, elapsed_time, start_datetime, end_datetime):
    if not exists(OUTPUT_PATH):
        create_csv()

    with open(OUTPUT_PATH, "a+", newline="") as f:
        csv_writer = writer(f)
        csv_writer.writerow([task_name, format_time(elapsed_time), start_datetime, end_datetime])


task_entry_column = [
    [
        sg.InputText(key="-TASK NAME-", size=(32, 1), do_not_clear=False),
        sg.Button("New Task")
    ]
]

task_viewer_column = [
    [
        sg.Text("Current Task:"), sg.Text(size=(32, 1), key="-CURRENT TASK-"),
        sg.Text("", size=(8, 1), key="-TIMER-"),
        sg.Button("Pause", key="-PAUSE_RESUME-"), sg.Button("Stop")
    ]
]

layout = [
    [
        sg.Column(task_entry_column, visible=True),
        sg.Column(task_viewer_column, visible=False),
    ]
]


window = sg.Window("timely", layout)
elapsed_time = 0
paused = True
task_start_time = 0
task_name = ""
start_datetime = ""

task_entry_column_handle = layout[0][0]
task_viewer_column_handle = layout[0][1]

while True:
    if not paused:
        event, values = window.read(timeout=10)
        elapsed_time = time.time() - task_start_time

    else: 
        event, values = window.read()

    if event == "-PAUSE_RESUME-":
        event = window[event].GetText()
   
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "New Task":
        task_name = values["-TASK NAME-"]
        if task_name:
            paused = False

            window["-CURRENT TASK-"].update(task_name)

            task_start_time = time.time()
            elapsed_time = 0
            paused_time = task_start_time
            start_datetime = datetime.now()
            
            task_entry_column_handle.update(visible=False)
            task_viewer_column_handle.update(visible=True)
    
    elif event == "Pause":
        paused = True
        paused_time = time.time()
        window['-PAUSE_RESUME-'].update(text="Resume")

    elif event == "Resume":
        paused = False
        task_start_time = task_start_time + time.time() - paused_time
        window["-PAUSE_RESUME-"].update(text="Pause") # yikes this is probably bad
    
    elif event == "Stop":

        append_to_csv(task_name, elapsed_time, start_datetime.strftime("%d/%m/%Y %H:%M:%S"), datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        elapsed_time = 0
        paused = True
        
        task_entry_column_handle.update(visible=True)
        task_viewer_column_handle.update(visible=False)


    window['-TIMER-'].update(format_time(elapsed_time))
        
