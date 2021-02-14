# sqlite3 to be used as the database engine
import sqlite3
# hashids as the library to generate a short unique ID from integers
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for


# opens a connection to the database.db
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
# configure a secret key to ensure the hashes are unpredictable
app.config['SECRET_KEY'] = 'techchallenge'

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])


@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('Please enter the URL!')
            return redirect(url_for('index'))

        # store the submitted url in the urls table
        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)',
                                (url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        # to generate unique hash
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        # render the index.html template by passing the short_url variable to it
        return render_template('index.html', short_url=short_url)

    # index.html is the form for users to enter a url to shorten
    return render_template('index.html')


@app.route('/<id>')
def url_redirect(id):
    conn = get_db_connection()

    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]
        url_data = conn.execute('SELECT original_url, clicks FROM urls'
                                ' WHERE id = (?)', (original_id,)
                                ).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']

        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',
                     (clicks+1, original_id))

        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))
