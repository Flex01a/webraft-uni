from flask import Flask, render_template, request
from chatbot_webraft import chatbot
model = "webraft-uni" 

#create model
chatbot.create_model(model)
ip_ban_list = []
#load CSV dataset , Mention input column (question) and label column (answer)
chatbot.dataset("try.csv","context","response",model) 
app = Flask(__name__)
app.static_folder = 'static'
@app.route("/")
def home():
  ip = request.environ.get('REMOTE_ADDR')
  if ip in ip_ban_list:
     abort(403)
   
  return render_template("index.html")
@app.route("/get")
def get_bot_response():
    f = open("log.txt", "a")
    
    

    userText = request.args.get('msg')
    if "python code" in userText:
      
      x = "Here is the code: \n <br> ```<pre><code class='language-python'> <font color='#ddd'>"+chatbot.model_load("pywriter",userText,model)+"</font></code></pre>```"
      f.write("Ip: "+request.remote_addr+" Message: ' "+userText+" ' Bot: ' "+x+" '\n")
      return x
    elif "php code" in userText:
      return chatbot.model_load("phpwriter",userText,model)
    elif "js code" in userText:
      return chatbot.model_load("jswriter",userText,model)
    else:
      a = chatbot.model_load("spimx",userText,model)
      f.write("Ip: "+request.remote_addr+" Message: ' "+userText+" ' Bot: "+a+"' \n")
      return a
    f.close()
if __name__ == "__main__":
    app.run(host = "0.0.0.0",
  port = 8080)
