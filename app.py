import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():

    conn = sqlite3.connect('database.db')
    print("database has opened")

    conn.execute("CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, address TEXT, password TEXT, repeat_password TEXT)")
    print("Users table was created")

    conn.execute("INSERT INTO users(name, email, address, password, repeat_password) VALUES('aashiq', 'adams.aashiq@gmail.com', 'here', '123', '123')")

    conn.execute("CREATE TABLE IF NOT EXISTS products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT)")
    print("Products was created")

    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    print(cur.fetchall())


init_sqlite_db()


@app.route('/add-data/', methods=['POST'])
def add_new_record():
    if request.method == 'POST':
        msg = None

        post_data = request.get_json()
        name = post_data['name']
        email = post_data['email']
        address = post_data['address']
        password = post_data['password']
        repeat_password = post_data['repeat_password']
        print(name,email,address)
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                con.row_factory = dict_factory
                cur.execute("INSERT INTO users(name, email, address, password, repeat_password) VALUES(?, ?, ?, ?, ?)", (name, email, address, password, repeat_password))
                con.commit()
                msg = name + " successfully added to the table."
        except Exception as e:
            con.rollback()
            msg = "Error occured in insert operation " + str(e)
        finally:
            con.close()
            return jsonify( msg = msg )


@app.route('/show-records/', methods=['GET'])
def list_users():
    try:
        con = sqlite3.connect('database.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        con.commit()
        rows = cur.fetchall()

    except Exception as e:
        print("Something happened when getting data from db:"+str(e))
    return jsonify(rows)


@app.route('/products/', methods=['GET'])
def insert_products():
    with sqlite3.connect('database.db') as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('iPhone 6', 'Rated: 9.4/10', 'Keep your contacts and important documents close at hand with this Apple iPhone 6, which connects with iCloud to share documents and information with your computer. The slim design of this phone doesn't skimp on features while being heavy on styleKeep your contacts and important documents close at hand with this Apple iPhone 6, which connects with iCloud to share documents and information with your computer. The slim design of this phone doesn't skimp on features while being heavy on style','Available:  R120', 'https://i.postimg.cc/T2B22f2X/product-5.jpg')")
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('iPhone 6s', 'Rated: 9/10', 'With just a single press, 3D Touch lets you do more than ever before. Live Photos bring your memories to life in a powerfully vivid way. And that's just the beginning. Take a deeper look at iPhone 6s, and you'll find innovation on every level.', 'Available:  R200', 'https://i.postimg.cc/qv8PTdqQ/h4-slide.png')")
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('LG', 'Rated: 7.5/10', 'The screen has a resolution of 720 x 1520 Pixels and 271 ppi pixel density.', 'Available: R220', 'https://i.postimg.cc/bYZNjshT/product-3.jpg')")
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('Sony Xperia', 'Rated: 7/10', 'If you spend some time with the Xperia Z5 you'll realise it's a great phone; with an ace camera, vibrant display and plenty of power tucked underneath its frosted glass back.','Available:  R170', 'https://i.postimg.cc/prw6w0tg/product-4.jpg)")
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('Mac Book', 'Rated: 9.8/10', 'Apple MacBook Pro is a macOS laptop with a 13.30-inch display that has a resolution of 2560x1600 pixels.','Available:  R185', 'https://i.postimg.cc/fRfMvdcw/product-thumb-3.jpg')")
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('iPhone 6', 'Rated: 9.4/10', 'Keep your contacts and important documents close at hand with this Apple iPhone 6, which connects with iCloud to share documents and information with your computer. The slim design of this phone doesn't skimp on features while being heavy on styleKeep your contacts and important documents close at hand with this Apple iPhone 6, which connects with iCloud to share documents and information with your computer. The slim design of this phone doesn't skimp on features while being heavy on style','Available:  R90', 'https://i.postimg.cc/T2B22f2X/product-5.jpg')")
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('iPod', 'Rated: 7/10', 'The new iPod touch has the A10 Fusion chip, up to 256GB of storage, and Group FaceTime. All in our most portable iOS device.','Available:  R275', 'https://i.postimg.cc/RF0yK6Rb/h4-slide3.png')")
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('Nokia Lumia', 'Rated: 7/10', 'Nokia Lumia 520 is powered by a 1GHz dual-core processor. It comes with 512MB of RAM.','Available:  R120', 'https://i.postimg.cc/g0mfcB6p/product-2.jpg')")
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('Nokia Microsoft', 'Rated: 7.5/10', '1KG Cranberries Dried.\n','Available:  R180', 'https://i.postimg.cc/pX8Wp4y5/h4-slide7.png')")
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('Samsung Note', 'Rated: 10/10', '1KG Sunflower Seeds.\n','Available:  R140', 'https://i.postimg.cc/SKZqBp13/product-6.jpg')")
        cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('Samsung s6', 'Rated: 8.5/10', '1KG Hazelnuts.\n','Available:  R280', 'https://i.postimg.cc/0N5PXNn7/product-thumb-2.jpg')")
        con.commit()

        return {'msg': 'Data added to the database.'}


@app.route('/show-products/', methods= ['GET'])
def show_products():
    data = []
    try:
        con = sqlite3.connect('database.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('SELECT * FROM products')
        con.commit()
        data = cur.fetchall()

    except Exception as e:
        print("There was an error fetching products from the database")
    finally:
        con.close()
        return jsonify(data)


if __name__=='__main__':
    app.run(debug=True)
