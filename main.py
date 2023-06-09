# record of journeys
import datetime, os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates', static_folder='static')
tickets = 0

def addToFile(timestamp):
  with open("flexipass1.txt","a") as file:
    file.write(timestamp+"\n")

def getHistory():
  global tickets
  tickets = 10
  HTMLoutput = "<ol>"
  with open("flexipass1.txt","r") as file:
    line = file.readline().strip()
    while line != "":
      HTMLoutput += "<li><a href=\"javascript:alert('"+ line + "');\"><img class='used'/></a></li>"
      line = file.readline().strip()
      tickets = tickets - 1
  for index in range(0,tickets):
    HTMLoutput += "<li><img class='unused'/></li>"
  HTMLoutput += "</ol>"
  print(HTMLoutput)
  return HTMLoutput

@app.route('/new_flexipass', methods=['POST'])
def new_flexipass():
  print("Make a new flexipass")
  newname = str(datetime.datetime.utcnow()) + "_flexipass.txt"
  os.rename('flexipass1.txt',newname)
  open("flexipass1.txt","w")
  return redirect(url_for('index'))

@app.route('/handle_data', methods=['POST'])
def handle_data():
    global tickets
    thisTimestamp = request.form['timestamp']
    print(thisTimestamp)
    addToFile(thisTimestamp)
    return redirect(url_for('index'))
# return a response

@app.route('/')
def index():
    global tickets
    HTMLhistory = getHistory()
    if tickets <= 0:
      use = "hidden"
      new = "visible"
    else:
      use = "visible"
      new = "hidden"
    return render_template('index.html', utc_dt=datetime.datetime.utcnow(),history=HTMLhistory,tickets_left=tickets, form_use=use, form_new=new)


app.run(host='0.0.0.0', port=81)
