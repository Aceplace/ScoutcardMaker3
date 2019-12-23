import tkinter as tk

root = tk.Tk()
root.geometry('500x300')
root.title("Scout Card Maker")

main_frame = tk.Frame(root, bg="gray70", relief=tk.SUNKEN, padx=5, pady=7)
main_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()

