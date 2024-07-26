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

graph = None
agents = None
agent = None
expanded = []
path = []
file_path = None

# Initialize variables to track the current step
current_step = 0
highlighted_cells = []
global_m = 0
global_n = 0
text_items = {}  # Dictionary to store text items

# Initialize variables for automatic stepping
running = False
step_delay = 200  # Delay in milliseconds

def reset_state():
    global current_step
    global highlighted_cells
    global text_items
    global path
    global expanded
    global running
    
    current_step = 0
    highlighted_cells = []
    text_items.clear()
    path = []
    expanded = []
    canvas.delete("all")
    running = False

def on_algo_change(*args):
    global graph, agents, agent
    global expanded, path, file_path

    reset_state()
    load_map(file_path)

    selected_algo = algo_var.get()
    
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
    global graph, agents, agent
    global path, expanded
    global file_path
    
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

def load_map(file_path):
    global global_m, global_n
    global text_items
    text_items.clear()

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Đọc thông tin từ dòng đầu tiên
    n, m, t, f = map(int, lines[0].split())
    global_m, global_n = m, n  # Store the dimensions globally

    # Đọc các dòng tiếp theo vào bản đồ
    map_data = [line.split() for line in lines[1:]]

    selected_level = level_var.get()

    # Xử lý map_data theo level hiện tại
    if selected_level == "1":
        map_data = [[cell if cell in ['0', '-1', 'S', 'G'] else '0' for cell in row] for row in map_data]
    elif selected_level == "2":
        map_data = [[cell if cell.isdigit() or cell in ['S', 'G', '-1'] else '0' for cell in row] for row in map_data]
    elif selected_level == "3":
        map_data = [[cell if cell not in ['S1', 'S2', 'G1', 'G2'] else '0' for cell in row] for row in map_data]
    elif selected_level == "4":
        pass  # Không cần thay đổi gì

    # Vẽ bản đồ lên canvas
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
                color = 'black'
            elif map_data[i][j] == 'S':
                color = 'green'
            elif map_data[i][j] in ['G', 'G1', 'G2']:
                color = 'red'
            elif map_data[i][j] in ['F', 'F1']:
                color = 'orange'
            elif map_data[i][j] in ['S1', 'S2']:
                color = 'light green'
            elif map_data[i][j] == '0':
                color = 'white'
            elif map_data[i][j].isdigit():
                color = 'light blue'
            else:
                color = 'white'
                
            rect = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray', tags='cell')
            
            if map_data[i][j] not in ['0', '-1']:
                text_id = canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=map_data[i][j])
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

def highlight_next_step():
    global current_step
    global highlighted_cells

    total_steps = len(expanded) + len(path)
    expanded_steps = len(expanded)

    if len(path) == 0:
        messagebox.showinfo("Thông báo", "Không có đường đi")
        return

    if current_step < total_steps:
        if current_step < expanded_steps:
            cell = expanded[current_step]
            highlight_cell(cell, 'yellow')
            highlighted_cells.append((cell, 'yellow', text_items[cell][2]))
        else:
            path_step = current_step - expanded_steps
            if path_step < len(path):
                cell = path[path_step]
                previous_color = 'yellow' if (cell, 'yellow', text_items[cell][2]) in highlighted_cells else text_items[cell][2]
                highlight_cell(cell, 'green')
                highlighted_cells.append((cell, 'green', previous_color))
        current_step += 1

def highlight_previous_step():
    global current_step
    global highlighted_cells

    if len(path) == 0:
        messagebox.showinfo("Thông báo", "Không có đường đi")
        return

    if current_step > 0:
        current_step -= 1
        cell, current_color, previous_color = highlighted_cells.pop()
        highlight_cell(cell, previous_color)

def highlight_cell(cell, color):
    global text_items
    i, j = cell
    rect, text_id, _ = text_items[(i, j)]
    canvas.itemconfig(rect, fill=color)

def run_steps():
    global running
    if running:
        highlight_next_step()
        root.after(step_delay, run_steps)

def start_running():
    global running
    running = True
    run_steps()

def stop_running():
    global running
    running = False

# Initialize the main window
root = tk.Tk()
root.title("Delivery Path Finder")

# Set theme light colors
bg_color = "#ffffff"  # white background
fg_color = "#000000"  # black foreground
highlight_color = "#e0e0e0"  # light gray highlight

# Set the main window background color
root.configure(bg=bg_color)

# Configure the grid layout
root.columnconfigure(1, weight=1)
root.rowconfigure(3, weight=1)

# Input File Section
input_file_frame = tk.Frame(root, bg=bg_color)
input_file_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

input_file_label = tk.Label(input_file_frame, text="Input File", bg=bg_color, fg=fg_color)
input_file_label.pack(side="left")

input_file_entry = tk.Entry(input_file_frame, width=50, bg=highlight_color, fg=fg_color)
input_file_entry.pack(side="left", padx=(5, 10), fill='x', expand=True)

browse_button = tk.Button(input_file_frame, text="Browse", command=browse_file, bg=highlight_color, fg=fg_color)
browse_button.pack(side="left")

# Level Selection
level_label = tk.Label(root, text="Level:", bg=bg_color, fg=fg_color)
level_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

level_var = tk.StringVar(root)
level_var.set("1")  # default value
level_options = ["1", "2", "3", "4"]
level_menu = tk.OptionMenu(root, level_var, *level_options)
level_menu.config(bg=highlight_color, fg=fg_color)
level_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')
level_var.trace_add("write", on_level_change)

# Algorithm Selection Frame
algo_frame = tk.Frame(root, bg=bg_color)
algo_label = tk.Label(algo_frame, text="Thuật toán tìm kiếm:", bg=bg_color, fg=fg_color)
algo_label.pack(side="left")

algo_var = tk.StringVar(algo_frame)
algo_var.set("BFS")  # default value
algo_options = ["BFS", "DFS", "UCS", "GBFS", "A*"]
algo_menu = tk.OptionMenu(algo_frame, algo_var, *algo_options)
algo_menu.config(bg=highlight_color, fg=fg_color)
algo_menu.pack(side="left", padx=10, pady=10)
algo_frame.grid(row=1, column=3, padx=10, pady=10, sticky='w')
algo_var.trace_add("write", on_algo_change)

# Canvas for Displaying Map
canvas_frame = tk.Frame(root, bg=bg_color)
canvas_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

canvas = tk.Canvas(canvas_frame, width=600, height=400, bg='light gray')
canvas.pack(expand=True, fill='both')

# Time and Fuel Section
time_fuel_frame = tk.Frame(root, bg=bg_color)
time_fuel_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w')

time_label = tk.Label(time_fuel_frame, text="Time:", bg=bg_color, fg=fg_color)
time_label.pack(side="left")

time_entry = tk.Entry(time_fuel_frame, width=10, bg=highlight_color, fg=fg_color)
time_entry.pack(side="left", padx=(0, 10))

fuel_label = tk.Label(time_fuel_frame, text="Fuel:", bg=bg_color, fg=fg_color)
fuel_label.pack(side="left")

fuel_entry = tk.Entry(time_fuel_frame, width=10, bg=highlight_color, fg=fg_color)
fuel_entry.pack(side="left", padx=(0, 10))

# Button Frame
button_frame = tk.Frame(root, bg=bg_color)
button_frame.grid(row=5, column=3, padx=10, pady=10, sticky='e')

# Run and Pause Buttons
run_button = tk.Button(button_frame, text="Run", command=start_running, bg=highlight_color, fg=fg_color)
run_button.grid(row=0, column=0, padx=5, pady=5)

pause_button = tk.Button(button_frame, text="Pause", command=stop_running, bg=highlight_color, fg=fg_color)
pause_button.grid(row=0, column=1, padx=5, pady=5)

# Previous and Next Step Buttons
previous_step_button = tk.Button(button_frame, text="Previous Step", command=highlight_previous_step, bg=highlight_color, fg=fg_color)
previous_step_button.grid(row=1, column=0, padx=5, pady=5)

next_step_button = tk.Button(button_frame, text="Next Step", command=highlight_next_step, bg=highlight_color, fg=fg_color)
next_step_button.grid(row=1, column=1, padx=5, pady=5)

# Run the application
root.mainloop()
