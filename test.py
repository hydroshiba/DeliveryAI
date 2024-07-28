import tkinter as tk
from tkinter import filedialog, messagebox
from core import Reader
from core import Agent
from level.basic import BFS
from level.basic import DFS
from level.basic import UCS
from level.basic import GBFS
from level.basic import AStar
from level.constrained import TimeSearch
from level.constrained import FuelSearch

graph = None
agents = None
agent = None
expanded = []
path = []
file_path = None
previous_time = []
previous_fuel = []
previous_cost = []

# Initialize variables to track the current step
current_step = 0
highlighted_cells = []
global_m = 0
global_n = 0
text_items = {}  # Dictionary to store text items

# Initialize variables for automatic stepping
running = False
step_delay = 100  # Delay in milliseconds

def reset_state():
    global current_step, highlighted_cells, text_items, path, expanded, running, previous_time, previous_fuel, previous_cost
    
    current_step = 0
    highlighted_cells = []
    text_items.clear()
    path = []
    expanded = []
    canvas.delete("all")
    running = False
    previous_time = []
    previous_fuel = []
    previous_cost = []


def on_algo_change(*args):
    global graph, agents, agent, expanded, path, file_path

    reset_state()
    load_map(file_path)

    selected_algo = algo_var.get()
    time_var.set(0)
    fuel_var.set(0)
    time_limit_var.set(0)
    fuel_limit_var.set(0)
    path_cost_var.set(0)
    
    if selected_algo == "BFS":
        search = BFS()
    elif selected_algo == "DFS":
        search = DFS()
    elif selected_algo == "UCS":
        search = UCS()
    elif selected_algo == "GBFS":
        search = GBFS()
    elif selected_algo == "A*":
        search = AStar()

    search.run(graph, agent)
    path = search.path
    expanded = search.expanded

def browse_file():
    global graph, agents, agent, path, expanded, file_path
    
    file_path = filedialog.askopenfilename()
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)
    reset_state()  # Reset state before loading the new map
    load_map(file_path)

    graph, agents = Reader.read(file_path)
    level = level_var.get()
    agent = agents[0]

    if level == '1': 
        on_algo_change()
    elif level == '2':
        search = TimeSearch()
        search.run(graph, agent)
        path = search.path
        expanded = search.expanded
        time_var.set(agent.time)
        fuel_var.set(0)
        time_limit_var.set(agent.time)
        fuel_limit_var.set(0)
        path_cost_var.set(0)
    elif level == '3':
        search = FuelSearch()
        search.run(graph, agent)
        path = search.path
        expanded = search.expanded
        time_var.set(agent.time)
        fuel_var.set(agent.fuel)
        time_limit_var.set(agent.time)
        fuel_limit_var.set(agent.fuel)
        path_cost_var.set(0)

def load_map(file_path):
    global global_m, global_n
    global text_items
    text_items.clear()

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Read information from the first line
    n, m, t, f = map(int, lines[0].split())
    global_m, global_n = m, n  # Store the dimensions globally

    # Read the following lines into the map
    map_data = [line.split() for line in lines[1:]]

    selected_level = level_var.get()

    # Process map_data based on the current level
    if selected_level == "1":
        map_data = [[cell if cell in ['0', '-1', 'S', 'G'] else '0' for cell in row] for row in map_data]
    elif selected_level == "2":
        map_data = [[cell if cell.isdigit() or cell in ['S', 'G', '-1'] else '0' for cell in row] for row in map_data]
    elif selected_level == "3":
        map_data = [[cell if cell not in ['S1', 'S2', 'G1', 'G2'] else '0' for cell in row] for row in map_data]
    elif selected_level == "4":
        pass  # No need to change anything

    # Draw the map on the canvas
    canvas.delete("all")
    canvas.update_idletasks()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    cell_size = min(canvas_width // m, canvas_height // n)

    x_offset = (canvas_width - m * cell_size) // 2
    y_offset = (canvas_height - n * cell_size) // 2

    for i in range(n):
        for j in range(m):
            x1, y1 = x_offset + j * cell_size, y_offset + i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            
            if map_data[i][j] == '-1':
                color = 'dark gray'
            elif map_data[i][j][0] == 'S':
                color = 'sea green'
            elif map_data[i][j][0] == 'G':
                color = 'firebrick'
            elif map_data[i][j][0] == 'F':
                color = 'salmon'
            elif map_data[i][j].isdigit() and int(map_data[i][j]) > 0:
                color = 'medium purple'
            else:
                color = 'white'
                
            rect = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', tags='cell')
            
            if map_data[i][j] not in ['0', '-1']:
                text_id = canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=map_data[i][j], fill='white', font=('TkDefaultFont', cell_size // 2))
                text_items[(i, j)] = (rect, text_id, color)
            else:
                text_items[(i, j)] = (rect, None, color)
    
    canvas.config(scrollregion=canvas.bbox("all"))

def on_level_change(*args):
    global graph, agents, agent, file_path
    global path, expanded

    reset_state()
    load_map(file_path)

    selected_level = level_var.get()
    if selected_level == "1":
        algo_frame.grid(row=1, column=3, padx=10, pady=10, sticky='w')
    else:
        algo_frame.grid_remove()

    agent = agents[0]
    if selected_level == '1': 
        on_algo_change()
    elif selected_level == '2': 
        search = TimeSearch()
        search.run(graph, agent)
        path = search.path
        expanded = search.expanded
        time_var.set(0)
        fuel_var.set(0)
        time_limit_var.set(agent.time)
        fuel_limit_var.set(0)
        path_cost_var.set(0)
    elif selected_level == '3':
        search = FuelSearch()
        search.run(graph, agent)
        path = search.path
        expanded = search.expanded
        time_var.set(0)
        fuel_var.set(agent.fuel)
        time_limit_var.set(agent.time)
        fuel_limit_var.set(agent.fuel)
        path_cost_var.set(0)

def highlight_next_step():
    global current_step, highlighted_cells, time_var, fuel_var, path_cost_var, running, previous_time, previous_fuel, previous_cost

    selected_level = level_var.get()

    cells = expanded + path
    total_steps = len(cells)
    expanded_steps = len(expanded)

    if len(path) == 0:
        messagebox.showinfo("Notification", "Path not found")
        running = False
        return

    if current_step == total_steps:
        running = False
        return
    
    cell = cells[current_step]

    if current_step < expanded_steps:
        if len(highlighted_cells) > 0:
            highlight_cell(highlighted_cells[-1][0], 'royal blue')
            highlighted_cells[-1] = (highlighted_cells[-1][0], 'royal blue', highlighted_cells[-1][2])

        highlight_cell(cell, 'navy blue')
        previous_color = 'royal blue' if (cell, 'royal blue', text_items[cell][2]) in highlighted_cells else text_items[cell][2]
        highlighted_cells.append((cell, 'navy blue', previous_color))
    else:
        if current_step == expanded_steps:
            highlight_cell(cells[expanded_steps - 1], 'royal blue')
            highlighted_cells[-1] = (highlighted_cells[-1][0], 'royal blue', highlighted_cells[-1][2])

        color = 'sea green' if cell == path[0] else 'firebrick' if cell == path[-1] else 'navy blue'
        previous_color = 'royal blue' if (cell, 'royal blue', text_items[cell][2]) in highlighted_cells else text_items[cell][2]
        
        highlight_cell(cell, color)
        highlighted_cells.append((cell, color, previous_color))

        if current_step > expanded_steps:
            previous_cost.append(path_cost_var.get())  # Save current path cost
            previous_time.append(time_var.get())  # Save current time
            previous_fuel.append(fuel_var.get())  # Save current fuel (if fuel_var is defined)

            new_cost = path_cost_var.get() + 1
            new_time = time_var.get() + (1 if int(selected_level) > 1 else 0)
            new_fuel = fuel_var.get() - (1 if int(selected_level) > 2 else 0)

            if text_items[cell][1] is not None:
                cell_value = canvas.itemcget(text_items[cell][1], 'text')
                if int(selected_level) > 1 and cell_value.isdigit():
                    new_time += int(cell_value)
                if int(selected_level) > 2 and cell_value.startswith('F'):
                    new_fuel = int(fuel_limit_entry.get()) # Reset fuel to fuel limit
                    new_time += int(cell_value[1:])

            path_cost_var.set(new_cost)
            time_var.set(new_time)
            fuel_var.set(new_fuel)

            previous_cost[-1] = new_cost  # Save the updated cost after increasing
            previous_time[-1] = new_time  # Save the updated time after increasing
            previous_fuel[-1] = new_fuel  # Save the updated fuel after increasing

        # if selected_level != "1" and current_step >= expanded_steps and current_step > expanded_steps:
        #     previous_time.append(time_var.get())  # Save current time
        #     previous_fuel.append(fuel_var.get())  # Save current fuel (if fuel_var is defined)
        #     previous_cost.append(path_cost_var.get())  # Save current path cost
        #     new_time = time_var.get() + 1
        #     new_fuel = fuel_var.get() - 1
        #     new_cost = path_cost_var.get() + 1
        #     if text_items[cell][1] is not None:
        #         cell_value = canvas.itemcget(text_items[cell][1], 'text')
        #         if cell_value.isdigit():
        #             new_time += int(cell_value)
        #         if cell_value.startswith('F'):
        #             new_fuel = int(fuel_limit_entry.get())  # Reset fuel to fuel limit
        #             new_time += 1

        #     time_var.set(new_time)
        #     fuel_var.set(new_fuel)
        #     path_cost_var.set(new_cost)
        #     previous_time[-1] = new_time  # Save the updated time after reducing
        #     previous_fuel[-1] = new_fuel
        #     previous_cost[-1] = new_cost

    current_step += 1
    time_entry.update_idletasks()
    fuel_entry.update_idletasks()
    path_cost_entry.update_idletasks()


def highlight_previous_step():
    global current_step, highlighted_cells, running, previous_time, previous_fuel, previous_cost

    if len(path) == 0:
        messagebox.showinfo("Notification", "Path not found")
        running = False
        return

    if current_step > 0:
        current_step -= 1
        cell, current_color, previous_color = highlighted_cells.pop()
        highlight_cell(cell, previous_color)

        if current_step < len(expanded):
            if len(highlighted_cells) > 0:
                highlight_cell(highlighted_cells[-1][0], 'navy blue')
        else:
            if current_step == len(expanded):
                highlight_cell(expanded[-1], 'navy blue')
                highlight_cell(path[0], 'sea green')
            elif current_step > len(expanded):
                highlight_cell(path[0], 'sea green')
                highlight_cell(path[-1], 'firebrick')

        # Restore time, fuel, and cost variables
        if previous_time:
            restored_time = previous_time.pop()
            if text_items[cell][1] is not None:
                cell_value = canvas.itemcget(text_items[cell][1], 'text')
                if cell_value.isdigit():
                    restored_time -= int(cell_value)  # Restore cell value
                if cell_value.startswith('F'):
                    restored_time -= 1
            time_var.set(restored_time - 1)  # Restore 1
        
        restored_cost = 0
        if previous_cost:
            restored_cost = previous_cost.pop()
            path_cost_var.set(restored_cost - 1) 

        if previous_fuel:
            restored_fuel = previous_fuel.pop()
            if text_items[cell][1] is not None:
                cell_value = canvas.itemcget(text_items[cell][1], 'text')
                if cell_value.startswith('F'):
                    restored_fuel -= restored_cost
            fuel_var.set(restored_fuel + 1)

    time_entry.update_idletasks()
    fuel_entry.update_idletasks()
    path_cost_entry.update_idletasks()


def highlight_cell(cell, color):
    global text_items
    i, j = cell
    rect, text_id, _ = text_items[(i, j)]
    canvas.itemconfig(rect, fill = color)

def run_steps():
    global running
    if running:
        highlight_next_step()
        root.after(step_delay, run_steps)

def start_running():
    global running, current_step
    if running: return

    if current_step == len(expanded) + len(path):
        on_level_change()

    running = True
    run_steps()

def stop_running():
    global running
    running = False

# Initialize the main window
root = tk.Tk()
root.title("Delivery Path Finder")
# Set the main window background color
root.configure(bg='')

# Configure the grid layout
root.columnconfigure(1, weight=1)
root.rowconfigure(3, weight=1)

# Input File Section
input_file_frame = tk.Frame(root)
input_file_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

input_file_label = tk.Label(input_file_frame, text="Input File")
input_file_label.pack(side="left")

input_file_entry = tk.Entry(input_file_frame, width=80)
input_file_entry.pack(side="left", padx=10)

browse_button = tk.Button(input_file_frame, text="Browse", command=browse_file)
browse_button.pack(side="left")

# Level Section
level_frame = tk.Frame(root)
level_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

level_label = tk.Label(level_frame, text="Level:")
level_label.pack(side="left")

level_var = tk.StringVar(value="1")
level_dropdown = tk.OptionMenu(level_frame, level_var, "1", "2", "3", "4")
level_dropdown.pack(side="left")
level_var.trace_add("write", on_level_change)

# Algorithm Selection Section
algo_frame = tk.Frame(root)
algo_frame.grid(row=1, column=3, padx=10, pady=10, sticky='w')

algo_label = tk.Label(algo_frame, text="Searching algorithm:")
algo_label.pack(side="left")

algo_var = tk.StringVar(value="A*")
algo_dropdown = tk.OptionMenu(algo_frame, algo_var, "A*", "BFS", "DFS", "UCS", "GBFS")
algo_dropdown.pack(side="left")
algo_var.trace_add("write", on_algo_change)

# Canvas for visualization
canvas = tk.Canvas(root, bg='light gray', width=600, height=400)
canvas.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

# Time, Fuel, and Path Cost Information
info_frame = tk.Frame(root)
info_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

path_cost_label = tk.Label(info_frame, text="Path Cost:")
path_cost_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

path_cost_var = tk.IntVar(value=0)
path_cost_entry = tk.Entry(info_frame, textvariable=path_cost_var, width=10)
path_cost_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

# Time Constraint
time_label = tk.Label(info_frame, text="Time:")
time_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

time_var = tk.IntVar(value=0)
time_entry = tk.Entry(info_frame, textvariable=time_var, width=10)
time_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

time_limit_label = tk.Label(info_frame, text="Time Limit:")
time_limit_label.grid(row=1, column=2, padx=10, pady=5, sticky='w')

time_limit_var = tk.IntVar(value=0)
time_limit_entry = tk.Entry(info_frame, textvariable=time_limit_var, width=10)
time_limit_entry.grid(row=1, column=3, padx=10, pady=5, sticky='w')

# Fuel Constraint
fuel_label = tk.Label(info_frame, text="Fuel:")
fuel_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

fuel_var = tk.IntVar(value=0)
fuel_entry = tk.Entry(info_frame, textvariable=fuel_var, width=10)
fuel_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

fuel_limit_label = tk.Label(info_frame, text="Fuel Capacity:")
fuel_limit_label.grid(row=2, column=2, padx=10, pady=5, sticky='w')

fuel_limit_var = tk.IntVar(value=0)
fuel_limit_entry = tk.Entry(info_frame, textvariable=fuel_limit_var, width=10)
fuel_limit_entry.grid(row=2, column=3, padx=10, pady=5, sticky='w')

# Control Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=4, column=3, padx=10, pady=10, sticky='e')

run_button = tk.Button(button_frame, text="Run", command=start_running)
run_button.grid(row=0, column=0, padx=5, pady=5)

pause_button = tk.Button(button_frame, text="Pause", command=stop_running)
pause_button.grid(row=0, column=1, padx=5, pady=5)

# Previous and Next Step Buttons
previous_step_button = tk.Button(button_frame, text="Previous Step", command=highlight_previous_step)
previous_step_button.grid(row=1, column=0, padx=5, pady=5)

next_step_button = tk.Button(button_frame, text="Next Step", command=highlight_next_step)
next_step_button.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()
