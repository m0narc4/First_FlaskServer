from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy  # для работы с БД
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # подключение к нужной бд и задание ей имени
db = SQLAlchemy(app)


class Article(db.Model):  # создание класса (таблица в бд)
    id = db.Column(db.Integer, primary_key=True)  # создание полей в таблице
    intro = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Article %r>' % self.id  # для извлечения

# для создания базы данных на сервере надо прописать в терминале следующие команды
# from <имя файла> import <переменная приложения, в данном случае app>, <название переменной бд>
# app.app_context().push()
# db.create_all()

# После запуска этих команд в директории проекта появляется папка instance с файлом бд внутри


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/posts")
def posts():
    # Создание объекта, через который будем получать все записи в базе данных
    # order_by - сортировка по какому-нибудь полю
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)  # articles можно назвать по-другому


@app.route("/posts/<int:ind>")
def post_additional(ind):
    article = Article.query.get(ind)
    return render_template("posts_additional.html", article=article)


@app.route("/posts/<int:ind>/delete")
def post_delete(ind):
    article = Article.query.get_or_404(ind) # та же функция get, но возвращающая ошибку 404 в случае, если в бд нет записи с такой id

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "При удалении статьи произошла ошибка"


@app.route("/posts/<int:ind>/update", methods=['POST', 'GET'])
def post_update(ind):
    article = Article.query.get(ind)
    if request.method == 'POST':
        article.title = request.form['title']  # обращаемся к форме и элементу с name="title"
        article.intro = request.form['intro']  # обращаемся к форме и элементу с name="title"
        article.text = request.form['text']  # обращаемся к форме и элементу с name="title"

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("update.html", article=article)


@app.route("/create-article", methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']  # обращаемся к форме и элементу с name="title"
        intro = request.form['intro']  # обращаемся к форме и элементу с name="title"
        text = request.form['text']  # обращаемся к форме и элементу с name="title"

        article = Article(title=title, intro=intro, text=text)  # создаём объект на основе класса
        try:  # сохраняем объект (по сути запись в таблице) в бд
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)