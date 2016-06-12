import os.path
import Tkinter as tk
import ImageTk
import Image
import tier_optimizer 
import threading

SPRITES_PATH = "./sprites/"

def initPopulationCallback():
	def callback():
		g = Genetic()
	
	t = threading.Thread(target=callback)
	t.start()


class StatusBar(tk.Frame):   
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.variable=tk.StringVar()        
        self.label=tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                           textvariable=self.variable, justify='right',
                           font=('arial',8,'normal'))
        self.variable.set('')
        self.label.pack(fill=tk.X)        
        self.pack(side='bottom', fill='x')

root = tk.Tk()
img = ImageTk.PhotoImage(Image.open(SPRITES_PATH + "ferrothorn" + ".png"))

d=StatusBar(root)

d.variable.set("")

init_button = tk.Button(root, bg='#99DDDE', relief='flat', text ="Initialize Population", command = initPopulationCallback)

init_button.pack(side='bottom')


root.geometry('600x300')
root.mainloop()




