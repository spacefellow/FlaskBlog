from flask import render_template, request, redirect, flash, url_for
from config import *
from models import Post, User
from forms import LoginForm, RegisterForm
from flask_login import login_required, logout_user, login_user, current_user

app = create_app()


@app.route('/', methods=("GET", "POST"))
def all_posts():
    posts = Post.query.all()
    print(posts)
    return render_template("posts.html", posts=posts)


@app.route('/user_posts', methods=("GET", "POST"))
@login_required
def user_posts():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('user_posts.html', user=user, title='User')


@app.route('/<int:post_id>', methods=("GET", "POST"))
def post_detail(post_id):
    post = Post.query.get(post_id)
    return render_template("post_detail.html", post=post)


@app.route('/user_posts/<int:post_id>', methods=("GET", "POST"))
@login_required
def user_post_detail(post_id):
    post = Post.query.get(post_id)
    return render_template("user_post_detail.html", post=post)


@app.route('/user_posts/<int:post_id>/delete', methods=("GET", "POST"))
@login_required
def delete_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('user_posts'))
    except Exception as ex:
        return flash(ex, 'Невозможно удалить запись')


@app.route('/user_posts/<int:post_id>/update', methods=("GET", "POST"))
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if request.method == "POST":
        try:
            post.title = request.form['title']
            post.intro = request.form['intro']
            post.text = request.form['text']
            db.session.commit()
            return redirect(url_for('user_posts'))
        except Exception as ex:
            flash(ex, 'Невозможно создать запись')
    else:
        return render_template("update_post.html", post=post)


@app.route('/create_post', methods=("GET", "POST"))
@login_required
def creat_post():
    if request.method == "POST":
        try:
            title = request.form['title']
            intro = request.form['intro']
            text = request.form['text']
            user_id = current_user.id
            posts = Post(title=title, intro=intro, text=text, user_id=user_id)
            db.session.add(posts)
            db.session.commit()
            return redirect(url_for('user_posts'))
        except Exception as ex:
            flash(ex, 'Невозможно создать запись')
    else:
        return render_template("create_post.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.pwd in form.pwd.data:
                login_user(user)
                return redirect(url_for('user_posts', username=user.username))
            else:
                flash("Invalid username or password!", "danger")
        except Exception as ex:
            flash(ex, "danger")
    return render_template("login.html",
                           form=form,
                           text="Login",
                           title="Login",
                           btn_action="Login")


@app.route("/register", methods=("GET", "POST"))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            email = form.email.data
            pwd = form.pwd.data
            newuser = User(username=username, email=email, pwd=pwd)
            db.session.add(newuser)
            db.session.commit()
            flash(f"Аккаун успешно зарегестрирован", "success")
            return redirect(url_for("login"))
        except Exception as ex:
            flash(ex, 'Пользователь не был зарегестрирован')
    return render_template("login.html",
                           form=form,
                           text="Create account",
                           title="Register",
                           btn_action="Register account")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('all_posts'))


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response
