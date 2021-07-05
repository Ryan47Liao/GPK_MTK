from gpk_utilities import *
import tkinter as tk
from tkinter import ttk

class gpk_weekView(tk.Frame):
    def __init__(self,root,geometry,callback  = None):
        super().__init__(bg = 'pink')
        self.root = root
        self.callback = callback
        self.height = geometry['height']
        self.width = geometry['width']
        self._draw()
        
    def _draw(self):
        #___________LeftFrame______________#
        self.LeftFrame = tk.Frame(master = self, bg = 'blue')
        self.LeftFrame.config(width = self.width/2, height = self.height)
        self.LeftFrame.pack(side = tk.LEFT)
        #___________RightFrame______________#
        self.RightFrame = tk.Frame(master = self, bg = 'green')
        self.RightFrame.config(width = self.width/2, height = self.height)
        self.RightFrame.pack(side = tk.LEFT)
        
class gpk_weekPlanning(tk.Frame):
    def __init__(self,root,geometry,callback  = None):
        super().__init__(bg = 'pink')
        self.callback = callback
        self.height = geometry['height']
        self.width = geometry['width']
        self.root = root
        self._draw()
        
    def _draw(self):
        #___________LeftFrame______________#
        self.LeftFrame = tk.Frame(master = self, bg = 'orange')
        self.LeftFrame.config(width = self.width/2, height = self.height)
        self.LeftFrame.pack(side = tk.LEFT)
        #___________RightFrame______________#
        self.RightFrame = tk.Frame(master = self, bg = 'pink')
        self.RightFrame.config(width = self.width/2, height = self.height)
        self.RightFrame.pack(side = tk.LEFT)