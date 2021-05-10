import os
from canvas_token import token 

directory = "input"
try:
    os.stat(directory)
except:
    os.mkdir(directory)

def getURL(webpage_ID, page_num, list):
     URL = "curl -H \"Authorization: Bearer "
     URL += token
     URL +="\" \"https://byui.instructure.com/api/v1/accounts/" 
     URL += str(webpage_ID)
     URL += "/admins?per_page=100&page="
     URL += str(page_num)
     URL += "\" > "
     URL += directory
     URL += "/list"
     URL += str(list)
     URL += ".json" 
     return URL

os.system(getURL(1,1,1))
