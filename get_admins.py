import os
import subprocess
from canvas_token import token 

directory = "input"
try:
    os.stat(directory)
except:
    os.mkdir(directory)

def get_command(webpage_ID, page_num, list):
     command = "curl -H \"Authorization: Bearer "
     command += token
     command +="\" \"" 
     command += str(webpage_ID)
     command += ""
     command += str(page_num)
     command += "\" > "
     command += directory
     command += "/list"
     command += str(list)
     command += ".json" 
     return command

def page_count(command):
    #takes just the URL from the command
    URL = command.split()[5][1:-2]
    
os.system(get_command(1,1,1))
page_count(get_command(1,1,1))
