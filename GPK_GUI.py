#!/usr/bin/env python
# coding: utf-8
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
from  tkinter import filedialog
from tkinter import messagebox
import os
import Tetris

#Gpk Mods 
from gpk_cache import GPK_Cache
from GPK_PROFILE import *
from gpk_mtk_frame import gpk_mtk_frame
from gpk_todo_frame import gpk_to_do
from gpk_archive_frame import gpk_archive
from gpk_stat_frame import gpk_analysis
from gpk_weekView_frame import gpk_weekView

class gpk_Shell:
    def __init__(self):
        self.version = '0.02'
        self.shell_rt = tk.Tk()
        self.shell_rt.title("GPK_LOGIN")
        self.shell_rt.geometry('1100x850')
        self.cwd = os.getcwd()
        self.ACC = None
        self.PW = None
        self.Profile = None
        self.parent_address = "D:/GPK/gpk_saves/"
        try:
            os.makedirs(self.parent_address) 
        except FileExistsError:
            pass

                    
        #_________Finally_________#
        #Fetch Cache 
        try:
            with open(self.parent_address + "gpk_cache" , 'rb') as INfile:
                self.cache = pickle.load(INfile)                    
        except FileNotFoundError:
            self.cache = GPK_Cache(self.parent_address + "gpk_cache")
            self.cache.save() 
        #DRAW
        self._draw()
        #Insert Data
        if self.cache.Re_status():
            print("Remembered Acc")
            self.acc_entry.delete(0, 'end')
            self.acc_entry.insert('0',self.cache.get_AC())   
            self.pw_entry.delete(0, 'end')
            self.pw_entry.insert('0',self.cache.get_PW())  
            self.open_profile(self.cache.gpk_save_path)
        #Finally 
        self.shell_rt.mainloop()
    
    def authenticate(self)->bool:
        "Authenticates the user"
        if self.Profile is None:
            getattr(messagebox,'showwarning')("Access Denied","You must Load the saved file first.") 
            self.open_profile()
            return False
        else:
            return self.Profile.Verified(self.PW) 
        
        
    def gpk_login(self):
        self.ACC = self.acc_entry.get()
        try:
            self.PW = int(self.pw_entry.get())
        except:
            getattr(messagebox,'showwarning')("ERROR","PING must be Digits only!") 
        "If LogIn Successful,open the Main app and destroy the login."
        if self.authenticate():
            #If remember me is toggled 
            if self.remember.get():
                self.cache.set_info(self.ACC,self.PW)
                self.cache.set_save_path(self.file_path)
            else:
                self.cache.Re_Fal()
            self.cache.save()
            self.shell_rt.destroy()
            #________________#
            new_root = gpk_Main(self.Profile,self.file_path)
        else:
            getattr(messagebox,'showwarning')("Access Denied","WRONG PASSWORD")
        
        
    def close(self):
        self.shell_rt.destroy()
        
    #__________________REGISTRATION__________________#
    def new_account(self,name,password,tutorial = True):
        self.reg_window.destroy()
        getattr(messagebox,'showwarning')("Creating New Profile","This might take 10-20s to generate encryption keys...")
        self.Profile = PROFILE(name, int(password))
        #Finally, Create such a gpk file...
        try:
            file_name = "{}_user_file".format(name)
            entry = "C {} -n {}".format(self.parent_address,file_name)
            file_path = File_Exp(entry,RETURN= True) #Create a file at the destination 
            print("file_path:",file_path)
            if tutorial:
                self.Profile = self.tutorial(self.Profile)
            self.Profile.Save(str(file_path)) #Dump the information into the file
            
        except Exception as ex:
            print("Error,fail to create account:\n",ex)
            
        finally:
            self.open_profile() 
            
    def tutorial(self,Profile):
        ddl = str((datetime.datetime.now()+ datetime.timedelta(days = 1)).date())
        Profile.todos.add(task_name = 'Intepret Task ID ',task_ID = 'S_G1-1_K1',
                          task_time = 1,task_diff = 1,task_des = 'S_G1-1_K1 Means: Task is SPECIAL, under Goal 1-1, is the 1st Key Result',ddl = ddl)
        Profile.todos.add(task_name = 'Tutorial:Create a Task',task_ID = 'S_G3-0_K1',task_time = 1,task_diff = 1,
                          task_des = 'When you create a Task, a NULL task will be created, you can modify it and then add it \
by clicking the [Submit] button on the bottom left',ddl = ddl)
        Profile.todos.add(task_name = 'Tutorial:Delete a Task',task_ID = 'S_G3-0_K2',task_time = 1,task_diff = 1,
                          task_des ='Select a Task you wish to delete, and then click the delete button on the bottom left',ddl = ddl)
        Profile.todos.add(task_name = 'Tutorial:Complete a Task',task_ID ='S_G3-0_K3',task_time = 1,task_diff = 1,
                          task_des = 'If you are DONE with a task, be sure to UPDATE the time you took to complete, and click [Complete]\
the task will then be Archived into the Archive',ddl = ddl)
        return Profile  
        
    def gpk_reg(self):
        self.reg_window = tk.Toplevel()
        self.reg_window.title('Create New Account')
        #_____________________Draw_____________________________#
        name_label = tk.Label(master =self.reg_window,text = 'Name:')
        name_entry = tk.Entry(master = self.reg_window)
        pw_label = tk.Label(master =self.reg_window,text = 'PING(digit only):')
        pw_entry = tk.Entry(master = self.reg_window)
        submit_btn = tk.Button(master = self.reg_window, 
                             text = 'Submmit', command = lambda: self.new_account(name_entry.get(),pw_entry.get()) )
        #Packing...
        name_label.grid(padx = 5, pady = 5, row = 0, column = 0)
        name_entry.grid(padx = 5, pady = 5,row = 0, column = 1)
        pw_label.grid(padx = 5, pady = 5,row = 1, column = 0)
        pw_entry.grid(padx = 5, pady = 5,row = 1, column = 1)
        submit_btn.grid(padx = 5, pady = 5,row = 2, column = 1,columnspan = 2)
        
        
        
        
    """
    Creates a new GPK file when the 'New' menu item is clicked.
    """
    def new_profile(self):
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        profile_filename = filename.name
        self.file_path = profile_filename
        
            
        
    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """
    def open_profile(self,path = None):
        if path is None:
            filename = tk.filedialog.askopenfile(filetypes=[('Grand Peach King Profile', '*.gpk')],
                                                 initialdir = self.parent_address)
            self.file_path = filename.name
        else:
            self.file_path = path
        print(f"opening save at {self.file_path}")
        INfile = open( self.file_path ,"rb")
        self.Profile = pickle.load(INfile)
        INfile.close()
        #Update User Name
        user_name = str(self.file_path).split('.')[0].split("gpk_saves")[-1].split('user_file')[0].strip('/_\\')
        print(user_name)
        self.acc_entry.delete(0, 'end')
        self.acc_entry.insert('0',user_name)   
                                                                                                    
                                                                                                    
        
    def _draw(self):
        width = 180
        #ＵＰＰＥＲ　ＦＲＡＭＥ
        #____________Menus_______________
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.shell_rt)
        self.shell_rt['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        #___________WelcomePic___________
        self.frame_Upper = tk.Frame(master = self.shell_rt, bg = 'black')
        self.frame_Upper.configure(height = 500,width = width)
        self.frame_Upper.pack()
        self.okr_img = ImageTk.PhotoImage(Image.open(self.cwd + "/Pictures/OKR_Welcome.jpg"))
        self.top_pic = tk.Label(master = self.frame_Upper , image = self.okr_img, anchor = tk.S)
        self.top_pic.pack(fill = tk.BOTH ) 
        
        #ＬＯＷＥＲ　ＦＲＡＭＥ
        self.frame_Lower = tk.Frame(master = self.shell_rt) #, bg = 'orange')
        self.frame_Lower.configure(height = 200,width = width)
        self.frame_Lower.pack()
        
        #___________Acc_entry_______________
        self.acc_info_entry_frame = tk.Frame(master = self.frame_Lower)# ,bg = 'blue')
        self.acc_info_entry_frame.configure(height = 50, width = width)
        self.acc_info_entry_frame.pack(ipady = 0, ipadx = 50, expand = 1)
        
        self.acc_label = tk.Label(master = self.acc_info_entry_frame , text = 'Account:')
        self.acc_entry = tk.Entry(master = self.acc_info_entry_frame, width = 30)
        self.acc_entry.grid(padx = 20, pady = 10, row = 0, column = 1)
        self.acc_label.grid(padx = 20, pady = 10, row = 0, column = 0)
        ##____________pw_entry_________________
        self.pw_entry = tk.Entry(master = self.acc_info_entry_frame, width = 30 )
        self.pw_label = tk.Label(master = self.acc_info_entry_frame ,text = 'Pass Word:')
        self.pw_entry.grid(padx = 20,  pady = (5,10), row = 1, column = 1)
        self.pw_label.grid(padx = 15, pady = (5,10), row = 1, column = 0)
        
        
        #___________login_btn_________________
        self.login_btn_frame = tk.Frame(master = self.frame_Lower )#, bg = 'red' )
        self.login_btn_frame.configure(height = 50,width = 1000)
        self.login_btn_frame.pack( ipady = 0, ipadx = 50, expand = 1)
        
        self.img_login = ImageTk.PhotoImage(Image.open(self.cwd + "/Pictures/new_button_login.ico"))
        
        self.login_btn = tk.Button(master = self.login_btn_frame ,image = self.img_login , command = self.gpk_login)
        self.login_btn.grid(row = 1, column = 4)
        
        #___________Remember_Me_Check_Box___________
        self.remember = tk.IntVar()
        self.remember.set(int(self.cache.Re_status()))
        self.rmchbox = tk.Checkbutton(self.login_btn_frame,variable = self.remember,
                                      onvalue=1, offvalue=0)
        self.rmchbox.grid(row = 0, column = 3)
        self.rmchbox.configure( command = lambda: self.cache.Set_status(self.remember.get()) )
        self.rmchbox_label = tk.Label (self.login_btn_frame,text = "Remember Me").grid(row = 0, column = 4)
        
        #__________Register__________________
        self.reg_btn_frame = tk.Frame( self.frame_Lower)#, bg = 'green' )
        self.reg_btn_frame.configure(height = 50,width = 500)
        self.reg_btn_frame.pack(padx = 100,side = tk.LEFT, ipady = 10, ipadx = 50, expand = 0)
        self.register_btn = tk.Button(master = self.reg_btn_frame ,text = 'Register', command = self.gpk_reg)
        self.register_btn.pack(side = tk.LEFT)#grid( row = 0 , column = 0, columnspan = 1)
        self.version_label = tk.Label(master = self.reg_btn_frame ,
                                     text = f"""
                                            \t\t\t\t\t\t Version: {self.version}
                                            """ ).pack(pady = 10, padx = 100, side = tk.RIGHT)


class gpk_Main():
    def __init__(self,Profile,file_path):
        self.Profile = Profile
        self.file_path = file_path
        self.gpk_main_rt = tk.Tk()
        self.gpk_main_rt.option_add('*tearOff', False)
        self.gpk_main_rt.title("GPK_Main")
        base = 120
        width = base*16
        height = base*9
        self.geometry = {'width':width,'height':height}
        self.gpk_main_rt.geometry('{}x{}'.format(width,height))
        self.FRAMES = []
        
        #_________Finally_________#
        self._draw()
        self.gpk_main_rt.mainloop()
        
    def profile_save(self):
        self.Profile.Save(self.file_path)
        
    def Profile_call_back(self, Profile = None, Update = False, Return = False , call_frame_name = None):
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
            if call_frame_name is not None:
                self.call_frame(call_frame_name)
            
    

    def call_frame(self, frame_name):
        self.hide_all_frames(frame_name)
        getattr(self,frame_name).pack(fill = tk.BOTH,expand = 1)
    
    def hide_all_frames(self, exception):
        "Clears the Page for other Frames"
        for frame in self.FRAMES:
            if frame != exception:
                getattr(self,frame).pack_forget()
                
    def RETURN(self):
        self.gpk_main_rt.destroy()
        gpk_Shell()
    
    def _draw(self):
        #++++++++++++++++++++++++++ＭＥＮＵ++++++++++++++++++++++++++++++++++++++#
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.gpk_main_rt)
        self.gpk_main_rt['menu'] = menu_bar
        #_________________Menu->Today________________________
        menu_today = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_today, label='Today')
        menu_today.add_command(label='To_Do_List', command = lambda: self.call_frame('gpk_todo'))

        self.gpk_todo = gpk_to_do(self.gpk_main_rt,self.geometry,callback = self.Profile_call_back)
        self.FRAMES.append("gpk_todo")
        
        #_________________Menu->WEEK________________________
        menu_Week = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_Week, label='Week')
        menu_Week.add_command(label='Week Progress', command = lambda: self.call_frame('gpk_weekView'))
        
        self.gpk_weekView = gpk_weekView(self.gpk_main_rt,self.geometry,callback = self.Profile_call_back)
        self.FRAMES.append("gpk_weekView")
        
        # menu_Week.add_command(label='Week Planning', command = lambda: self.call_frame('gpk_weekPlanning'))
        # self.gpk_weekPlanning = gpk_weekPlanning(self.gpk_main_rt,self.geometry,callback = self.Profile_call_back)
        # self.FRAMES.append("gpk_weekPlanning")
        #_________________Menu->STORE________________________
        menu_Store = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_Store, label='Store')
        menu_Store.add_command(label='Store', command = lambda: self.call_frame('gpk_store'))
        
        self.gpk_store = gpk_store(self.gpk_main_rt)
        self.FRAMES.append("gpk_store")
        #_________________Menu->ANALYSIS________________________
        menu_Analysis = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_Analysis, label='Analysis')
        menu_Analysis.add_command(label='Statistics', command = lambda: self.call_frame('gpk_analysis'))
        menu_Analysis.add_command(label='Archive', command = lambda: self.call_frame('Archive'))
        
        self.Archive = gpk_archive(self.gpk_main_rt,self.Profile_call_back)
        self.FRAMES.append("Archive")
        self.gpk_analysis = gpk_analysis(self.gpk_main_rt,self.geometry,self.Profile_call_back)
        self.FRAMES.append("gpk_analysis")
        #_________________Menu->OKR________________________
        menu_OKR = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_OKR, label='OKR')
        menu_OKR.add_command(label='OKR Settings', command = lambda: self.call_frame('gpk_okr'))
        
        self.gpk_okr = gpk_okr(self.gpk_main_rt)
        self.FRAMES.append("gpk_okr")
        
        #_________________Menu->MeisterTask Add on________________
        MTK = tk.Menu(menu_bar) 
        menu_bar.add_cascade(menu=MTK, label='MTK Sync')
        MTK.add_command(label='Authentication Setting', command = lambda: self.call_frame('gpk_mtk_frame'))
    
        self.gpk_mtk_frame = gpk_mtk_frame(self.gpk_main_rt,call_back = self.Profile_call_back)
        self.FRAMES.append("gpk_mtk_frame")
        
        #_________________Menu->DashBoard________________________
        DashBoard = tk.Menu(menu_bar)#, postcommand = lambda: self.call_frame('gpk_dash_board'))
        menu_bar.add_cascade(menu=DashBoard, label='DashBoard')
        DashBoard.add_command(label='HOME', command = lambda: self.call_frame('gpk_dash_board'))
        
        #_________________Menu->Exit________________________
        Exit = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=Exit, label='Exit')
            
        Exit.add_command(label='Main Menu', command = self.RETURN)
        Exit.add_command(label='QUIT', command =  self.gpk_main_rt.destroy)
        
        #++++++++++++++++++++++++++DashBoard(HOME)++++++++++++++++++++++++++++++++++++++#
        self.gpk_dash_board = gpk_dash(self.gpk_main_rt,self.geometry,callback = self.Profile_call_back)
        self.gpk_dash_board.pack(fill = tk.BOTH,expand = 1)
        self.FRAMES.append("gpk_dash_board")
        
        test_btn = tk.Button(master =self.gpk_dash_board  ,text = 'WELCOME')
        test_btn.pack()

class gpk_okr(tk.Frame):
    def __init__(self,root):
        super().__init__(bg = 'black')
        self.root = root
        self._draw()
        
    def _draw(self):
        self.to_dos = tk.Button(master = self, text = 'WELCOME　to gpk_week')
        self.to_dos.pack()


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
        self.LeftFrame = tk.Frame(master = self, bg = 'red')
        self.LeftFrame.config(width = self.width/2, height = self.height)
        self.LeftFrame.pack(side = tk.LEFT)
        #___________RightFrame______________#
        self.to_dos = tk.Button(master = self, text = 'WELCOME　to gpk_okr')
        self.to_dos.pack()

# In[17]:


class gpk_store(tk.Frame):
    def __init__(self,root):
        super().__init__(bg = 'orange')
        self.root = root
        self._draw()

    def Tetris_start(self):
        self.Tetris = Tetris.Tetris(master = self)
        self.Tetris.start_game()
        
        
    def _draw(self):
        #Button
        self.Tetris_open = tk.Button(master = self, text = 'Tetris',command = self.Tetris_start)
        self.Tetris_open.pack()


if __name__ == "__main__":
    test = gpk_Shell()
