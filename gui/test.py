import tkinter as tk
from tkinter import filedialog

# Initialize variables to track the current step
current_step = 0
highlighted_cells = []
global_m = 0
global_n = 0
text_items = {}  # Dictionary to store text items

def browse_file():
    file_path = filedialog.askopenfilename()
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)
    load_map(file_path)

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
    selected_level = level_var.get()
    if selected_level == "1":
        algo_frame.grid(row=1, column=3, padx=10, pady=10, sticky='w')
    else:
        algo_frame.grid_remove()

def highlight_next_step():
    global current_step
    global highlighted_cells

    if current_step < len(expanded) + len(path):
        if current_step % 2 == 0 and current_step // 2 < len(expanded):
            cell = expanded[current_step // 2]
            highlight_cell(cell, 'yellow')
            highlighted_cells.append((cell, 'yellow', text_items[cell][2]))
        elif current_step % 2 == 1 and current_step // 2 < len(path):
            cell = path[current_step // 2]
            highlight_cell(cell, 'green')
            highlighted_cells.append((cell, 'green', 'yellow'))
        current_step += 1

def highlight_previous_step():
    global current_step
    global highlighted_cells

    if current_step > 0:
        current_step -= 1
        cell, _, previous_color = highlighted_cells.pop()
        restore_original_color(cell, previous_color)

def highlight_cell(cell, color):
    global global_m, global_n, text_items
    i, j = cell
    rect, text_id, _ = text_items[(i, j)]
    canvas.itemconfig(rect, fill=color)
    
def restore_original_color(cell, original_color):
    global text_items
    i, j = cell
    rect, text_id, _ = text_items[(i, j)]
    canvas.itemconfig(rect, fill=original_color)

# Sample data for path and expanded
path = [(1,2), (1,3), (1,4), (1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (7,6), (7,7), (7,8)]
expanded = [(1,2), (1,3), (1,4), (1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (7,6), (7,7), (7,8)]

# Initialize the main window
root = tk.Tk()
root.title("Delivery Path Finder")

# Configure the grid layout
root.columnconfigure(1, weight=1)
root.rowconfigure(3, weight=1)

# Input File Section
input_file_frame = tk.Frame(root)
input_file_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

input_file_label = tk.Label(input_file_frame, text="Input File")
input_file_label.pack(side="left")

input_file_entry = tk.Entry(input_file_frame, width=50)
input_file_entry.pack(side="left", padx=(5, 10), fill='x', expand=True)

browse_button = tk.Button(input_file_frame, text="Browse", command=browse_file)
browse_button.pack(side="left")

# Level Section
level_label = tk.Label(root, text="Level:")
level_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

level_var = tk.StringVar(root)
level_var.set("1")  # default value
level_options = ["1", "2", "3", "4"]
level_menu = tk.OptionMenu(root, level_var, *level_options)
level_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')
level_var.trace("w", on_level_change)

# Algorithm Selection Frame
algo_frame = tk.Frame(root)
algo_label = tk.Label(algo_frame, text="Thuật toán tìm kiếm:")
algo_label.pack(side="left")

algo_var = tk.StringVar(algo_frame)
algo_var.set("BFS")  # default value
algo_options = ["BFS", "DFS", "UCS", "GBFS", "A*"]
algo_menu = tk.OptionMenu(algo_frame, algo_var, *algo_options)
algo_menu.pack(side="left", padx=10, pady=10)
algo_frame.grid(row=1, column=3, padx=10, pady=10, sticky='w')

# Canvas for Displaying Map
canvas_frame = tk.Frame(root)
canvas_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

canvas = tk.Canvas(canvas_frame, width=600, height=400, bg='light gray')
canvas.pack(expand=True, fill='both')

# Time and Fuel Section
time_fuel_frame = tk.Frame(root)
time_fuel_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w')

time_label = tk.Label(time_fuel_frame, text="Time:")
time_label.pack(side="left")

time_entry = tk.Entry(time_fuel_frame, width=10)
time_entry.pack(side="left", padx=(0, 10))

fuel_label = tk.Label(time_fuel_frame, text="Fuel:")
fuel_label.pack(side="left")

fuel_entry = tk.Entry(time_fuel_frame, width=10)
fuel_entry.pack(side="left", padx=(0, 10))

# Previous and Next Step Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=5, column=3, padx=10, pady=10, sticky='e')

previous_step_button = tk.Button(button_frame, text="Previous Step", command=highlight_previous_step)
previous_step_button.pack(side="left", padx=(0, 10))

next_step_button = tk.Button(button_frame, text="Next Step", command=highlight_next_step)
next_step_button.pack(side="left")

# Run the application
root.mainloop()
