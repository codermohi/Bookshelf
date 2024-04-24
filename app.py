from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Bookshelf_3@bookshelfdb.cvwiqy4owpk4.ap-south-1.rds.amazonaws.com/bookshelfdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Bookshelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float)

    def __init__(self,title,author,price):
        self.title = title
        self.author = author
        self.price = price



@app.route('/')
def index():
    books = Bookshelf.query.all()
    return render_template('index.html', books=books)

@app.route('/add/', methods =['POST'])
def insert_book():
    if request.method == "POST":
        book = Bookshelf(
            title = request.form.get('title'),
            author = request.form.get('author'),
            price = request.form.get('price')
        )
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully")
        return redirect(url_for('index'))


@app.route('/update/', methods = ['POST'])
def update():
    if request.method == "POST":
        my_data = Bookshelf.query.get(request.form.get('id'))

        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.price = request.form['price']

        db.session.commit()
        flash("Book is updated")
        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Bookshelf.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book is deleted")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)

