import tkinter as tk 
from Plan_load import progress
from time import sleep

class tkProgress(tk.Tk):
    def __init__(self, title, description, todo_stack : list= None
                , auto_update = False, Control = False,
                 step = 0.01 , rps = 10, 
                 base = 40, blank = "  ", 
                 font = ('times new roman',14),
                 cnf = {} ):
        try:
            self._Stack = (f for f in todo_stack)
            self.total_f = len(todo_stack)
        except:
            self._Stack = None
        self.step = step 
        self.font = font
        self.description = description
        self.rps = rps 
        super().__init__( **cnf )
        self.geometry(f'{16*base}x{9*base}')
        self.title( title ) 
        #DRAW
        self._draw(Control)
        #Pre-Set
        self.Reset()
        #Finally;
        if todo_stack is not None:
            self.after(1000, self._update)
        
    def Reset(self):
        self.count = 0
        self.PG.set(progress(0))
        
    def _update(self,step = None, auto_update = False):
        if self._Stack is not None:
            try:
                next_f = next(self._Stack)
                step = 1/self.total_f
                next_f()
                self.count += step
                #print(self.count)
                self.PG.set( progress(self.count) )
                #print(self.PG.get())
                self.after( 1, lambda: self._update(step) )
            except StopIteration:
                # sleep(1)
                # self.destroy() 
                pass
        else:
            if step is None:
                step = self.step
            if self.count < 1: 
                self.count += step
                #print(self.count)
                self.PG.set( progress(self.count) )
                #print(self.PG.get())
            else:
                auto_update = False
            if auto_update and self._RUN.get():
                self.after(int(1000/self.rps), lambda:self._update(step,auto_update))
            
    def _draw(self,Control):
        self._RUN = tk.IntVar()
        self._RUN.set(1)
        #Add description:
        description = tk.Label(self,text = self.description, font = self.font)
        description.pack(padx = 10, pady = 10)
        #Progress Bar 
        self.PG = tk.StringVar()
        self.PG_widget = tk.Label(self,textvariable = self.PG)
        self.PG_widget.pack()
        if Control:
            #Start Update
            self.autoUpdate_btn = tk.Button(self,text = 'Start Auto',
                                        command = lambda: self._update(auto_update=True))
            self.autoUpdate_btn.pack(padx = 10, pady = 10)
            #Allow Refresh:
            self.Run_ckbx = tk.Checkbutton(self,text = 'Auto Update', variable = self._RUN)
            self.Run_ckbx.pack()
            #Update Manually:
            self.Update_btn = tk.Button(self,text = 'Update',
                                        command = self._update)
            self.Update_btn.pack(padx = 10, pady = 10)
            #Reset Btn 
            self.Reset_btn = tk.Button(self,text = 'Reset',
                            command = self.Reset)
            self.Reset_btn.pack(padx = 10, pady = 10)
            #Destroy Btn
            Destory = tk.Button(self,text = 'Destroy', command = self.destroy)
            Destory.pack()
            
if __name__ == '__main__':
    class remember:
        def __init__(self,f,*args,**kargs):
            self._f = f 
            self.args = args
            self.kargs = kargs 
        
        def __call__(self):
            return self._f(*self.args,**self.kargs)
    
    import copy
    def sleeper(todo):
        print('Sleep')
        sleep(1)
        print(todo)
    
    todo_stack = []
    for i in range(10):
        todo_stack.append( remember(sleeper, f'the {copy.deepcopy(i)}th sleeper'))
    test = tkProgress('Progress Bar','Here is the Progress:',Control = True , todo_stack = todo_stack)
    test.mainloop()