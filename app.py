from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return 'Hello world'


@app.route('/about')
def about():
    return 'About as'


@app.route('/info')
def info():
    return 'Read me'


@app.route('/catalog')
def catalog():
    return 'Сhoose a product'


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return 'User page' + name + '-' + id


if __name__ == '__main__':
    app.run(debug=True)
