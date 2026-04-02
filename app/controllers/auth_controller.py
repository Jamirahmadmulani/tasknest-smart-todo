from flask import Blueprint, render_template, redirect, request, url_for, flash
from app.models.user import User
from app import db
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Basic Validation
        if not name or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for("auth.register"))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "warning")
            return redirect(url_for("auth.register"))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create new user
        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")



@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # Check password hash
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("task.dashboard"))
        else:
            flash("Invalid email or password!", "danger")

    return render_template("login.html")



@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
