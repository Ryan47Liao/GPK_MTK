import tkinter as tk
import pickle
import GPK_PROFILE 
import pandas as pd
from PIL import ImageTk,Image
import os

class Profile_Test:
    def __init__(self,path = None, name = None):
        if path is not None:
            self.file_path = path
            INfile = open( self.file_path ,"rb")
            self.Profile = pickle.load(INfile)
            INfile.close()
        else:
            self.Profile = GPK_PROFILE.PROFILE(name,321890)
            self.file_path = f'D:/GPK/gpk_saves/{name}_TEST.gpk'
            self.Profile.Save(self.file_path)
        
    def profile_save(self):
        self.Profile.Save(self.file_path)
        
    def Profile_call_back(self,Profile = None, Update = False, Return = False):
            """
            Interact with subFrames and modify the Profile in the Main APP.
            Toggle Return to Get Profile 
            input Profile and Toggle update to update Profile
            """
            if Update:
                self.Profile = Profile #Update the Profile
                self.profile_save()
            elif Return:
                return self.Profile 
            else:
                pass
    
def df_to_Treeview(master, data:pd.core.frame.DataFrame, col_width = 120,col_minwidth = 25,col_anchor = tk.CENTER
              ,LABEL = False) :
    from tkinter import ttk
    if LABEL:
        label_text = "Parent"
        label_bool = tk.YES
        label_width = col_width
    else:
        label_text = ""
        label_bool = tk.NO
        label_width = 0
        
    my_tree = ttk.Treeview(master)
    #Define Our Columns
    my_tree ['columns'] = list(data.columns)
    #Format the columns & Create Headings (Bar at the very TOP):
    my_tree.column("#0",width = label_width, stretch = label_bool)
    my_tree.heading("#0", text = label_text)
    for col_name in list(data.columns):
        my_tree.column(col_name,anchor = col_anchor , width = col_width)
        my_tree.heading(col_name,text = col_name,anchor = col_anchor)
    #Add Data 
    iid = 0 #Item ID(UNIQUE)
    for row in range(data.shape[0]):
        data_i = list(data.loc[row,])
        my_tree.insert(parent = "", index = 'end', iid = iid, text = label_text, values = data_i)
        iid += 1

    return my_tree    

class gpk_mtk_frame(tk.Frame):
    def __init__(self,root,call_back=None):
        super().__init__(bg = 'purple')
        self.root = root
        
        if call_back is not None:
            self.call_back = call_back 
            self.Profile = self.call_back(Return = True)
        else:
            def PASS(*args,**kargs):
                return 
            self.call_back = PASS
        self._draw()
        
    def update_token(self):
        self.get_token()
        self.Key_entry.delete(0,tk.END)
        self.Key_entry.insert(0,str(self.token) )
        
    def get_token(self):
        self.Profile = self.call_back(Return = True)
        try:
            self.token = self.Profile.todos.get_token()
        except AttributeError as e:
            print("Token not found at the current profile")
            print(e)
    
    def set_token(self,token):
        self.Profile = self.call_back(Return = True)
        self.token = token 
        self.Profile.todos.set_token(token) 
        self.call_back(Profile = self.Profile,Update = True)
        
        
    def project_df(self):
        Profile = self.call_back(Return = True)
        TEST = Profile.todos 
        try:
            TEST.Get_info()
            return pd.DataFrame({'Project Name':list(TEST.PROJECTs.values()),
                          'Project ID':list(TEST.PROJECTs.keys())})
        except Exception as e:
            print(e)
            return pd.DataFrame({'Project Name':list( ),
                          'Project ID':list( )})
    
    def tree_update(self):
        try:
            self.treeview.destroy()
        except:
            pass 
        Profile = self.call_back(Return = True)
        self.treeview = df_to_Treeview(master=self, data = self.project_df())
        self.treeview.pack(pady = 20)
        self.treeview.bind("<<TreeviewSelect>>", self.node_select)
    
    def node_select(self,event = None):
        self.tree_index = int(self.treeview.selection()[0]) 
        self.update_project() # "Update the Current Project ID"
        
    def update_project(self):
        Profile = self.call_back(Return = True)
        ID = list(Profile.todos.PROJECTs.keys())[self.tree_index]
        print(f"ID {ID} selected.")
        Profile.todos.set_project_id(ID)
        self.call_back(Profile,Update = True)
        
    def _draw(self):
        #Token Set Up
        self.Key_label = tk.Label(master = self,text = 'Personal access tokens:')
        self.Key_entry = tk.Entry(master = self)
        self.submit_btn = tk.Button(master = self, text = 'Save', 
                               command = lambda: self.set_token(self.Key_entry.get()) )
        #Project SetUp
        self.tree_update()
        #Packing...
        self.Key_label.pack()
        self.Key_entry.pack()
        self.submit_btn.pack()
        #Refresh Btn 
        self.sync_ref_img = ImageTk.PhotoImage(Image.open(os.getcwd() + "/Pictures/sync_refresh.ico"))
        self.SYNC_btn = tk.Button(master =self, image  =  self.sync_ref_img , 
                                  command = self.tree_update)
        self.SYNC_btn.pack()
        try:
            self.update_token()
        except AttributeError:
            pass 
    
if __name__ == '__main__':
    root = tk.Tk()
    T = Profile_Test(name = 'Ryan')
    temp = gpk_mtk_frame(root,T.Profile_call_back)
    temp.pack()
    root.mainloop()