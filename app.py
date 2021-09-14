from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/blog_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    intro = db.Column(db.String(300))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Articles %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def posts():
    articles = Articles.query.all()
    return render_template("posts.html", articles=articles)


@app.route('/<int:id>', methods=['POST', 'GET'])
def post_detail(id):
    article = Articles.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def creat_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        articles = Articles(title=title, intro=intro, text=text)
        db.session.add(articles)
        db.session.commit()

        try:
            db.session.add(articles)
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR"

    else:
        return render_template("create-article.html")


if __name__ == '__main__':
    app.run()
