from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/eryuk/OneDrive/Desktop/To-Do-App/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)

@app.route("/add",methods =["POST"])
def addTodo():
    mytitle = request.form.get("title")
    mytime_str = request.form.get("time")
    mytime = datetime.strptime(mytime_str, '%Y-%m-%dT%H:%M')
    mytodotype = request.form.get("todotype")
    newTodo = Todo(title= mytitle,complete = False, time=mytime,todotype = mytodotype)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))
    
@app.route("/delete/<string:id>")
def deletetodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def complete(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo.todotype == "Only Once":
        todo.complete = True
        now = datetime.now()
        todo.time = datetime.strftime(now,'%x %X') 
        db.session.commit()
        return redirect(url_for("index"))
    elif todo.todotype == "Daily":
        
        now = datetime.now()
        todo.time = datetime.strftime(now,'%x %X')
        todo.complete = True
        newtime = now + timedelta(days=1)
        newtime = datetime.strftime(newtime,'%x %X')
        newtodo = Todo(title = todo.title,complete=False ,time = newtime,todotype = todo.todotype)
        
        
        db.session.add(newtodo)
        db.session.commit()
        return redirect(url_for("index"))
    
    elif todo.todotype == "Weekly":
        
        now = datetime.now()
        todo.time = datetime.strftime(now,'%x %X')
        todo.complete = True
        newtime = now + timedelta(weeks=1)
        newtime = datetime.strftime(newtime,'%x %X')
        newtodo = Todo(title = todo.title,complete=False ,time = newtime,todotype = todo.todotype)
        
        
        db.session.add(newtodo)
        db.session.commit()
        return redirect(url_for("index"))
    




class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)
    time = db.Column(db.String(80))
    todotype = db.Column(db.String(80))
    

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)