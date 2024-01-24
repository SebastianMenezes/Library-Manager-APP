from flask import Flask, render_template, request, redirect, url_for, flash
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) 
template_dir = os.path.join(template_dir, 'src', 'templates')
app = Flask(__name__, template_folder = template_dir)

#Application Routes
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM books")
    myresult = cursor.fetchall()
    #Convert data into dictionary
    insertObject= []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data = insertObject)

#Route for adding books
@app.route('/books', methods=['POST'])
def addBook():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    genre = request.form['genre']

    if title and author and year and genre:
        cursor = db.database.cursor()
        sql = "INSERT INTO books (title, author, year, genre) VALUES (%s, %s, %s, %s)"
        data = (title, author, year, genre)
        cursor.execute(sql, data)
        db.database.commit()
    else:
       return render_template('error.html') 

    return redirect(url_for('home'))

#Route for deleting books
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM books WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

#Route for editing book info
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    genre = request.form['genre']

    if title and author and year and genre:
        cursor = db.database.cursor()
        sql = "UPDATE books SET title = %s, author = %s, year = %s, genre = %s WHERE id = %s"
        data = (title, author, year, genre, id)
        cursor.execute(sql, data)
        db.database.commit()
    else:
       return render_template('error.html') 

    return redirect(url_for('home'))

# Route for searching books by ID
@app.route('/search', methods=['GET'])
def search():
    book_id = request.args.get('id')
    cursor = db.database.cursor()
    sql = "SELECT * FROM books WHERE id=%s"
    data = (book_id,)
    cursor.execute(sql, data)
    result = cursor.fetchone()

    if result:
        # Convert the result into a dictionary
        columnNames = [column[0] for column in cursor.description]
        searchObject = dict(zip(columnNames, result))
    else:
        searchObject = None

    cursor.close()
    return render_template('search.html', result=searchObject)

if __name__ == '__main__':
    app.run(debug = True, port=4000)

    