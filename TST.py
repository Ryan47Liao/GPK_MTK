#Packages
import pickle
import GPK_PROFILE
import datetime
from gpk_utilities import *
import random 
import numpy as np
from gpk_Score import *
from tkinter import messagebox
import matplotlib.pyplot as plt

from GPK_Notion import GPK_Notion
import tkinter as tk
#Fetch Profile 
#Profile 
User_name = 'LEO'
with open(f"D:\GPK\gpk_saves\\{User_name}_user_file.gpk",'rb') as INfile:
    Profile = pickle.load(INfile)
    
# OUTfile = open('D:\GPK\gpk_saves\zuyeyang_user_file.gpk' ,"wb")
# pickle.dump(Profile,OUTfile)
# OUTfile.close()



if __name__ == '__main__':
    from gpk_utilities import Notion_sync
    Notion_sync(share_link = 'https://www.notion.so/fcd7611030e44d718e1dc635045e444a?v=75003026d2b248298c05f086b22aba76',
                Profile = Profile,
                TODO = Profile.todos,
                Misc = False)