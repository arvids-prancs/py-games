from flask import Flask, render_template
import os.path

# from livereload import Server

app = Flask(__name__)

app.debug = True

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


@app.errorhandler(404)
def page_404(e):
    return render_template('404.html'), 404


def index(page):
    return render_template('index.html',
                           csstime=os.path.getmtime("static/css/main.css"),
                           nav=[routes['blackjack'], routes['countries']],
                           page=page
                           )


if __name__ == '__main__':
    # server = Server(app.wsgi_app)
    # server.serve()
    app.run()
