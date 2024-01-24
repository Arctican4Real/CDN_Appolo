# Import tkinter for GUI creation and ttk for themed widgets
import tkinter as tk
from tkinter import ttk
import json
#import tracksearchdownload.py
bgBlack = "#171D1C"
fgWhite = "#EFE9F4"
accentBlue = "#3695F5"
#search_image1 = Image.open("<path/image_name>")
# Create the main window object
ws = tk.Tk()
  # Set the geometry of the main window (width x height)
ws.geometry("690x690")
ws.configure(bg='#3695F5')
artist=" "
# Create a StringVar to hold the text input value
text = tk.StringVar()

# Create a frame to hold other widgets
Frm = tk.Frame(ws)

# Configure the column weights of the main window to manage space distribution
ws.columnconfigure(0, weight=1)
ws.columnconfigure(1, weight=1)
ws.columnconfigure(2, weight=1)
# Create a label for the search input
search_label = tk.Label(text="Artist Name:  ", bg=bgBlack,fg=fgWhite,)
# Place the search label in the grid layout
search_label.grid(column=0, row=2, padx=5, pady=5)

# Create an entry widget for text input, linked to the text StringVar
modify = tk.Entry(ws, textvariable=text,bg=bgBlack, fg=fgWhite)
# Place the entry widget in the grid layout and set focus
modify.grid(column=1, row=2, padx=5, pady=5)
modify.focus()

# Create a label to display output
output_label = tk.Label(text=" ")
# Place the output label in the grid layout
output_label.grid(column=0, row=3)

# Define the function to be called when the search button is pressed
def find():
                output_label.config(text=" ")
                output_label.config(text=text.get())
                search_label = tk.Label(text="Artist Name:  ")
                # Remove any previous 'found' tag from the output label
    
# Create a button that will call the find function when pressed
buttn = tk.Button(ws, text='Search', bd='5', command=find)
# Place the button in the grid layout
buttn.grid(column=2, row=2, padx=5, pady=5)
columns = ('Song_Name', 'Artist')
tree = ttk.Treeview(ws, columns=columns, show='headings')
tree.heading('Song_Name', text='Song Name')
tree.heading('Artist', text='Artist')
contacts=[]
#for key in json.loads["data"]:
#                contacts.append((f'{key}', f'{artist}'))
def OnDoubleClick(event):
        item = tree.selection()[0]
        chosenTrack =item
tree.bind("<Double-1>", OnDoubleClick)
tree.grid(column=2, row=3, padx=5, pady=5)

# Start the main loop of the application
ws.mainloop()