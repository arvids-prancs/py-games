from flask import Flask, render_template, json, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os.path
import datetime
from Config import Config

# from livereload import Server
app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = Config.SECRET_KEY

# db
db = SQLAlchemy(app)

many_to_many_movie_studios = db.Table('movie_studios',
                                      db.Column('mov_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                                      db.Column('studio_id', db.Integer, db.ForeignKey('studios.id'), primary_key=True)
                                      )

many_to_many_movie_categories = db.Table('movie_categories',
                                         db.Column('mov_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                                         db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
                                         )


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title_lat = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    studios = db.relationship('Studios', secondary=many_to_many_movie_studios, lazy='subquery', backref=db.backref('studios', lazy=True))
    categories = db.relationship('Categories', secondary=many_to_many_movie_categories, lazy='subquery', backref=db.backref('categories', lazy=True))


class Studios(db.Model):
    __tablename__ = 'studios'
    id = db.Column(db.Integer, primary_key=True)
    title_lat = db.Column(db.String(100), nullable=False)


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    lat_singular = db.Column(db.String(30), nullable=False)


routes = {
    "home": {
        'id': 0,
        'route': '/',
        'page_title': "Manas spēles",
        'nav_title': '',
        'template': 'home.html'
    },
    "blackjack": {
        'id': 1,
        'route': '/blackjack',
        'page_title': "Blekdžeks - Manas spēles",
        'nav_title': 'Blekdžeks',
        'template': 'blackjack.html',
        'ico': 'js/blackjack/img/favicon.png'
    },
    "countries": {
        'id': 2,
        'route': '/countries',
        'page_title': "Valstis - Manas spēles",
        'nav_title': 'Valstis',
        'template': 'countries.html',
        'ico': 'js/valstis/img/globe-earth.png'
    },
    "chat": {
        'id': 3,
        'route': '/chat',
        'page_title': "Čats - Manas spēles",
        'nav_title': 'Čats',
        'template': 'chat.html',
        'ico': 'js/chat/img/chat.png'
    },
    "movies": {
        'id': 4,
        'route': '/movies',
        'page_title': "Filmas - Manas spēles",
        'nav_title': 'Filmas',
        'template': 'movies.html',
        'ico': 'img/movie.png'
    }
}


@app.route(routes['home']['route'])
def home():
    return index(routes['home'])


@app.route(routes['blackjack']['route'])
def blackjack():
    return index(routes['blackjack'])


@app.route(routes['countries']['route'])
def countries():
    return index(routes['countries'])


# chat
@app.route(routes['chat']['route'])
def chat():
    return index(routes['chat'])


@app.route('/chats/lasi')
def ielasit_chatu():
    with open("static/js/chat/chats.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data["messages"])


@app.route('/chats/suuti', methods=["POST"])
def suuti_zinju():
    with open('static/js/chat/chats.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    message = request.json
    message['timestamp'] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    data["messages"].append(message)
    data.update(data)
    with open('static/js/chat/chats.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return ielasit_chatu()


@app.route(routes['movies']['route'])
def movies():
    # return render_template('movies.html', movies=Movies.query.all())
    return index(routes['movies'], {'movies': Movies.query.order_by(Movies.year.desc()).all()})


@app.errorhandler(404)
def page_404(e):
    return render_template('404.html'), 404


def index(page, data=None):
    if data is None:
        data = {}
    return render_template('index.html',
                           csstime=os.path.getmtime("static/css/main.css"),
                           nav=[routes['blackjack'], routes['countries'], routes['chat'], routes['movies']],
                           page=page,
                           data=data
                           )


if __name__ == '__main__':
    # server = Server(app.wsgi_app)
    # server.serve()
    app.run()
