import tkinter as tk 
from gpk_utilities import * 


class gpk_dash(tk.Frame):
    def __init__(self,root,geometry,callback  = None):
        super().__init__(bg = 'green')
        self.root = root
        self.callback = callback
        self.height = geometry['height']
        self.width = geometry['width']
        self._draw()
        
    def _draw(self):
        #___________LeftFrame______________#
        self.LeftFrame = tk.Frame(master = self, bg = 'orange')
        self.LeftFrame.config(width = self.width/2, height = self.height)
        self.LeftFrame.pack(side = tk.LEFT, anchor = 'w')
        #___________RightFrame______________#
        self.RightFrame = tk.Frame(master = self, bg = 'green')
        self.RightFrame.config(width = self.width/2, height = self.height)
        self.RightFrame.pack(side = tk.LEFT, anchor = 'e')