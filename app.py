from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Hashtag %r>' % self.name


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    cover = db.Column(db.String(50), nullable=False, default='default.png')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('articles', lazy=True))
    hashtag = db.relationship('Hashtag', backref=db.backref('articles', lazy=True))

    def __repr__(self):
        return '<Article %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100))
    avatar = db.Column(db.String(50), nullable=False, default='default_user.png')

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/favorites')
def favorites():
    return render_template('favorites_posts.html')


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login_enter.html')


@app.route('/logout')
def logout():
    return 'Logout'


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return 'User page: ' + name + '-' + str(id)


@app.route('/post')
def post():
    return render_template('post.html')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
