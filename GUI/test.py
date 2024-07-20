import tkinter as tk
from tkinter import filedialog

def browse_file():
    file_path = filedialog.askopenfilename()
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)
    load_map(file_path)

def load_map(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Đọc thông tin từ dòng đầu tiên
    n, m, t, f = map(int, lines[0].split())

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
                color = 'yellow'
            elif map_data[i][j] in ['S1', 'S2']:
                color = 'light green'
            elif map_data[i][j] == '0':
                color = 'white'
            elif map_data[i][j].isdigit():
                color = 'light blue'
            else:
                color = 'white'
                
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
            
            if map_data[i][j] not in ['0', '-1']:
                canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=map_data[i][j])
    
    canvas.config(scrollregion=canvas.bbox("all"))

# Initialize the main window
root = tk.Tk()
root.title("Delivery Path Finder")

# Configure the grid layout
root.columnconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

# Input File Section
input_file_frame = tk.Frame(root)
input_file_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

input_file_label = tk.Label(input_file_frame, text="Input File")
input_file_label.pack(side="left")

input_file_entry = tk.Entry(input_file_frame, width=50)
input_file_entry.pack(side="left", padx=(5, 10), fill='x', expand=True)

browse_button = tk.Button(input_file_frame, text="Browse", command=browse_file)
browse_button.pack(side="left")

# Level Section
level_label = tk.Label(root, text="Level:")
level_label.grid(row=1, column=0, padx=10, pady=10)

level_var = tk.StringVar(root)
level_var.set("1")  # default value
level_options = ["1", "2", "3", "4"]
level_menu = tk.OptionMenu(root, level_var, *level_options)
level_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')

# Canvas for Displaying Map
canvas_frame = tk.Frame(root)
canvas_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

canvas = tk.Canvas(canvas_frame, width=600, height=400, bg='light gray')
canvas.pack(expand=True, fill='both')

# Time and Fuel Section
time_fuel_frame = tk.Frame(root)
time_fuel_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w')

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
button_frame.grid(row=4, column=2, padx=10, pady=10, sticky='e')

previous_step_button = tk.Button(button_frame, text="Previous Step")
previous_step_button.pack(side="left", padx=(0, 10))

next_step_button = tk.Button(button_frame, text="Next Step")
next_step_button.pack(side="left")

# Run the application
root.mainloop()
