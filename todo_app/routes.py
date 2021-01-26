from todo_app import app, db
from todo_app.models import Users, Tasks
from flask import request, render_template, redirect, url_for
from flask.globals import session


@app.route("/")
@app.route("/home")
def home():
    try:
        username = session["user"]
    except:
        return redirect(url_for("login"))

    user = Users.query.filter_by(username=username).first()
    tasks = Tasks.query.filter_by(user_id=user.id).all()

    return render_template("home.html", tasks=tasks)
    


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        session["user"]

        return redirect(url_for("home"))
    except:
        pass
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = Users.query.filter_by(email=email).first()

        if not user:
            return render_template("login.html", error="Email não existe")

        can_login = user.verify_password(password)

        if not can_login or email == "" or password == "" or not user:
            return render_template("login.html", error="Email ou senha incorretos")
        
        session["user"] = user.username

        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        session["user"]

        return redirect(url_for("home"))
    except:
        pass
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if username == "" or email == "" or password == "":
            return render_template("register.html", error="Preencha todos os campos")

        user = Users(username, email, password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/task/create", methods=["GET", "POST"])
def create_task():
    try:
        session["user"]
    except:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        
        user = Users.query.filter_by(username=session["user"]).first()
        task = Tasks(title, description, user.id)

        db.session.add(task)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("createTask.html")



@app.route("/task/<id>", methods=["GET", "POST"])
def view_task(id):
    try:
        session["user"]
    except:
        return redirect(url_for("login"))

    task = Tasks.query.filter_by(id=id).first()

    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form["description"]

        db.session.commit()

    return render_template("viewTask.html", task=task)


@app.route("/task/delete/<id>")
def delete_task(id):
    try:
        session["user"]
    except:
        return redirect(url_for("login"))
    
    task = Tasks.query.filter_by(id=id).first()

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("home"))
