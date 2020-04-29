from flask import Flask, render_template, json, jsonify, request
import os.path
import datetime

# from livereload import Server

app = Flask(__name__)

app.debug = True
app.config['JSON_AS_ASCII'] = False

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


# @app.route('/health')
# def health_check():
#     return "OK"


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


@app.errorhandler(404)
def page_404(e):
    return render_template('404.html'), 404


def index(page):
    return render_template('index.html',
                           csstime=os.path.getmtime("static/css/main.css"),
                           nav=[routes['blackjack'], routes['countries'], routes['chat']],
                           page=page
                           )


if __name__ == '__main__':
    # server = Server(app.wsgi_app)
    # server.serve()
    app.run()
