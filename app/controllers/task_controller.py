from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.task import Task
from app import db
from datetime import datetime

task = Blueprint("task", __name__)

@task.route("/")
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", tasks=tasks)

@task.route("/add", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        deadline = datetime.strptime(request.form["deadline"], "%Y-%m-%d")
        priority = request.form["priority"]

        new_task = Task(
            title=title,
            description=description,
            deadline=deadline,
            priority=priority,
            user_id=current_user.id
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("task.dashboard"))

    return render_template("add_task.html")

@task.route("/update/<int:id>")
@login_required
def update_task(id):
    task = Task.query.get_or_404(id)
    task.status = "Done" if task.status == "Pending" else "Pending"
    db.session.commit()
    return redirect(url_for("task.dashboard"))

@task.route("/delete/<int:id>")
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("task.dashboard"))
