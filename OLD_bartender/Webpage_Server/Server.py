from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import pickle
import os

user_flag=False
pass_flag=False
client_name=''
no_hour_flag=False
wrong_hour_flag=False

class my_server(BaseHTTPRequestHandler): #Main HTTP server handler to handle requests from the webpage

  def read_user_pass_list(self):
    client_names=[]
    client_password=[]


    if os.path.exists('Files/Client_Auth'):
      with open("Files/Client_Auth","rb") as fp:
        client_names,client_password=pickle.load(fp)
    return client_names,client_password
  
  
  def read_client_dict(self,client_name):
    if os.path.exists('Files/Client_Dict'):
      with open('Files/Client_Dict','rb') as fp:
        client_dict=pickle.load(fp)
      if client_name not in client_dict or len(client_dict[client_name])==0:
        return None
      else:
        return client_dict[client_name]
    else:
      return None

  def write_client_dict(self,client_name,list):
    if os.path.exists('Files/Client_Dict'):
      with open('Files/Client_Dict','rb') as fp:
        client_dict=pickle.load(fp)
      if client_name in client_dict:
        client_dict[client_name].append(list)
      else:
        client_dict[client_name]=[list]
      with open('Files/Client_Dict','wb') as fp:
        pickle.dump(client_dict,fp)

    else:
      client_dict={}
      client_dict[client_name]=[list]
      with open('Files/Client_Dict','wb') as fp:
        pickle.dump(client_dict,fp)
  
  def remove_client_dict(self,client_name,list):
    if os.path.exists('Files/Client_Dict'):
      with open('Files/Client_Dict','rb') as fp:
        client_dict=pickle.load(fp)
      client_list=client_dict[client_name]
      print(client_list)
      print(list)
      client_list.remove(list)
      client_dict[client_name]=client_list
      with open('Files/Client_Dict','wb') as fp:
        pickle.dump(client_dict,fp)


  def do_GET(self):
    global user_flag
    global pass_flag
    global client_name
    global no_hour_flag
    global wrong_hour_flag
    
    if self.path.endswith('/'):
      self.send_response(301)
      self.send_header('content-type','text/html')
      self.send_header('Location','/login')
      self.end_headers()

    if self.path.endswith('/login'):
      self.send_response(200)
      self.send_header('content-type','text/html')
      self.end_headers()

      output=''
      output+='<html><body>'
      output+='<h1><center>Login to the automated bartender</center></h1>'
      output+='<center><form method="POST" enctype="multipart/form-data" action="/login">'
      if(user_flag):
        output+='<br><label style="color:red;"> Wrong username or not registered</label>'
        user_flag=False
      elif(pass_flag):
        output+='<br><label style="color:red;"> Wrong Password</label>'
        pass_flag=False
      output+='<br><input name="Username" type="text" placeholder="Username">'
      output+='<br><input name="Password" type="password" placeholder="Password">'
      output+='<br><input type="submit" value="Log in" placeholder="Log in">'
      output+='</form></center>'
      output+='</body></html>'

      self.wfile.write(output.encode())

    if self.path.endswith('/mainpage'):
      if not client_name:
        self.send_response(301)
        self.send_header('content-type','text/html')
        self.send_header('Location','/login')
        self.end_headers()
      else:
        self.send_response(201)
        self.send_header('content-type','text/html')
        self.end_headers()

        output=''
        output+='<html><style>table, th, td {border: 1px solid black;}</style><body>'
        output+='<h1><center>Automated bartender</center></h1>'
        output+='<h2><center>Applied drink times</center></h2>'
        client_list=self.read_client_dict(client_name)
        if client_list != None:
          output+='<center><table style="width:100%"><tr><th>Drink name</th><th>Start Hour</th><th>End Hour</th></tr>'
          for lists in client_list:
            output+=f'<tr><td>{lists[0]}</td><td>{lists[1]}</td><td>{lists[2]}</td></tr>'
          output+='</table></center>'
        else:
          output+='<p><b> None </b></p>'
        output+='<h2><center>New drink times</center></h2>'
        if no_hour_flag:
          no_hour_flag=False
          output+='<center><br><label style="color:red;">Start hour or End Hour empty! </label></center>'
        if wrong_hour_flag:
          wrong_hour_flag=False
          output+='<center><br><label style="color:red;">Start Hour after End Hour! </label></center>'
        output+='<center><form method="POST" enctype="multipart/form-data" action="/mainpage">'
        output+='<label for="drink"> Select drink </label>'
        output+='<select id="drink" name="drink">'
        output+='<option value="Water">Water</option>'
        output+='<option value="Coffee">Coffee</option>'
        output+='<option value="Beer">Beer</option>'
        output+='<option value="Coca-Cola">Coca-Cola</option>'
        output+='<option value="Fanta">Fanta</option>'
        output+='<option value="Sprite">Sprite</option>'
        output+='</select>'
        output+='<input type="number" id="start-hour" name="Start Hour" placeholder="HH" maxlength="2" min="0" max="24">'
        output+='<input type="number" id="end-hour" name="End Hour" placeholder="HH" maxlength="2" min="0" max="24">'
        output+='<br><input type="submit" name="add_new" value="Add new setting">'
        output+='<input type="submit" name="log_out" value="Log out">'
        if client_list!=None:     
          output+='<br><select id="remove_drink" name="Remove Drink">'
          for lists in client_list:
            output+=f'<option value="{lists[0]} {lists[1]}-{lists[2]}">{lists[0]} {lists[1]}-{lists[2]}</option>'
          output+='<br><input type="submit" name="remove_selected" value="Remove Preference">'
        output+='</select>'
        output+='</form></center>'
        output+='</body></html>'

        self.wfile.write(output.encode())


  def do_POST(self):
    global user_flag
    global pass_flag
    #global client_names
    #global client_password
    global client_name
    global no_hour_flag
    global wrong_hour_flag
    
    if self.path.endswith('/login'):
      ctype,pdict=cgi.parse_header(self.headers.get('content-type'))
      pdict['boundary']=bytes(pdict["boundary"],"utf-8")
      content_len=int(self.headers.get('Content-length'))
      pdict['CONTENT_LENGTH']=content_len
      username=''
      password=''
      if ctype=='multipart/form-data':
        fields=cgi.parse_multipart(self.rfile,pdict)
        username=fields.get("Username")
        password=fields.get("Password")
      self.send_response(301)

      client_names,client_password=self.read_user_pass_list()
      
      if username[0] in client_names:
        if password[0]==client_password[client_names.index(username[0])]:
          client_name=username[0]
          self.send_header('Location','/mainpage')
        else:
          pass_flag=True
          self.send_header('Location','/login')
      else:
        user_flag=True
        self.send_header('Location','/login')

      self.end_headers()

    if self.path.endswith('/mainpage'):
      ctype,pdict=cgi.parse_header(self.headers.get('content-type'))
      pdict['boundary']=bytes(pdict["boundary"],"utf-8")
      content_len=int(self.headers.get('Content-length'))
      pdict['CONTENT_LENGTH']=content_len
      if ctype=='multipart/form-data':
        fields=cgi.parse_multipart(self.rfile,pdict)
        if "log_out" in fields:
          client_name=''
          self.send_response(301)
          self.send_header('content-type','text/html')
          self.send_header('Location','/login')
          self.end_headers()
        elif "add_new" in fields:
          if not (fields['Start Hour'][0] and fields['End Hour'][0]):
            no_hour_flag=True
            self.send_response(301)
            self.send_header('content-type','text/html')
            self.send_header('Location','/mainpage')
            self.end_headers()
          elif int(fields['Start Hour'][0])>int(fields['End Hour'][0]):
            wrong_hour_flag=True
            self.send_response(301)
            self.send_header('content-type','text/html')
            self.send_header('Location','/mainpage')
            self.end_headers()
          else:
            self.write_client_dict(client_name,[fields['drink'][0],int(fields['Start Hour'][0]),int(fields['End Hour'][0])])
            #client_dict[client_name].append([fields['drink'][0],int(fields['Start Hour'][0]),int(fields['End Hour'][0])])
            self.send_response(301)
            self.send_header('content-type','text/html')
            self.send_header('Location','/mainpage')
            self.end_headers()
        elif "remove_selected" in fields:
          to_be_removed=fields['Remove Drink'][0]
          to_be_removed_list=to_be_removed.split()
          temp_list=to_be_removed_list[1].split('-')
          del(to_be_removed_list[1])
          to_be_removed_list.extend(temp_list)
          to_be_removed_list[1]=int(to_be_removed_list[1])
          to_be_removed_list[2]=int(to_be_removed_list[2])
          self.remove_client_dict(client_name,to_be_removed_list)

          self.send_response(301)
          self.send_header('content-type','text/html')
          self.send_header('Location','/mainpage')
          self.end_headers()



if (__name__)=="__main__":
  if os.path.basename(os.getcwd())=='Project':
    os.chdir('Webpage_Server')
  server=HTTPServer(("localhost",8500),my_server)
  server.serve_forever()