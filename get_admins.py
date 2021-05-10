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
     command +="\" \"https://byui.instructure.com/api/v1/accounts/" 
     command += str(webpage_ID)
     command += "/admins?per_page=100&page="
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
