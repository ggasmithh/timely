import PySimpleGUI as sg
import time
from csv import writer
from datetime import datetime
from os.path import exists

OUTPUT_PATH = "timely_data.csv"

def create_csv():
    with open(OUTPUT_PATH, "w", newline="") as f:
        csv_writer = writer(f)
        csv_writer.writerow(["Task", "Elapsed", "Start", "End"])

def format_time(elapsed_time):
    return "{:02d}:{:02d}".format((elapsed_time // 100) // 60, (elapsed_time // 100) % 60)

def append_to_csv(task_name, elapsed_time, start_datetime, end_datetime):
    if not exists(OUTPUT_PATH):
        create_csv()

    with open(OUTPUT_PATH, "a+", newline="") as f:
        csv_writer = writer(f)
        csv_writer.writerow([task_name, format_time(elapsed_time), start_datetime, end_datetime])

task_entry_column = [
    [
        sg.InputText(key="-TASK NAME-", size=(15, 1)),
        sg.Button("New Task")
    ]
]

task_viewer_column = [
        [sg.Text("Current Task:"), sg.Text(size=(15, 1), key="-CURRENT TASK-")],
        [sg.Button("Pause", key="-PAUSERUN-"), sg.Button("Stop")],
        [sg.Text("", size=(8, 2), key="-TIMER-")]
]

layout = [
    [
        sg.Column(task_entry_column),
        sg.VSeperator(),
        sg.Column(task_viewer_column),
    ]
]

window = sg.Window("timely", layout)
elapsed_time = 0
paused = True
task_start_time = 0
task_name = ""
start_datetime = ""

while True:
    if not paused:
        event, values = window.read(timeout=10)
        elapsed_time = int(round(time.time() * 100)) - task_start_time

    else: 
        event, values = window.read()

    if event == "-PAUSERUN-":
        event = window[event].GetText()
   
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "New Task":
        task_name = values["-TASK NAME-"]
        if task_name:
            paused = False
            window["-CURRENT TASK-"].update(task_name)
            task_start_time = int(round(time.time() * 100))
            elapsed_time = 0
            paused_time = task_start_time
            window["-TASK NAME-"].update("")
            start_datetime = datetime.now()
    
    elif event == "Pause":
        paused = True
        paused_time = int(round(time.time() * 100))
        window['-PAUSERUN-'].update(text="Run")

    elif event == "Run":
        paused = False
        task_start_time = task_start_time + int(round(time.time() * 100)) - paused_time
        window["-PAUSERUN-"].update(text="Pause")
    
    elif event == "Stop":

        append_to_csv(task_name, elapsed_time, start_datetime.strftime("%d/%m/%Y %H:%M:%S"), datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        elapsed_time = 0
        paused = True
        task_start_time = int(round(time.time() * 100))


    window['-TIMER-'].update(format_time(elapsed_time))
        
