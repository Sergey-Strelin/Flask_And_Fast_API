"""
Чтобы не забыть - получение секретного ключа:
import secrets
secrets.token_hex()
"""

from flask import Flask, render_template, request, make_response

app = Flask(__name__)
app.secret_key = '6389965c46e1a38d44115dd0ff9419c2d7dcccd9f3f0ef406537ae3d9a3e18f0'


@app.route('/')
def index():
    context = {'title': 'main'}
    return render_template('index.html', **context)


@app.route('/cookie_form/', methods=['GET', 'POST'])
def set_cookie():
    if request.method == 'POST':
        context = {'title': 'main', 'name': request.form.get('login')}
        name = request.form.get('login')
        response = make_response(render_template('index.html', **context))
        response.set_cookie('Login', name)
        return response
    context = {'title': 'cookies'}
    return render_template('cookie_form.html', **context)


@app.route('/delcookie/')
def delcookie():
    context = {'title': 'cookies'}
    response = make_response(render_template('cookie_form.html', **context))
    response.set_cookie(*request.cookies, expires=0)
    return response


if __name__ == '__main__':
    app.run()
