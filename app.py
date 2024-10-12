from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="elvo",
    password="Elvo=1234",
    database="inventory_db"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    return render_template('index.html', inventory=inventory)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form['item-name']
    category = request.form['category']
    quantity = request.form['quantity']
    price = request.form['price']
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO inventory (item_name, category, quantity, price) VALUES (%s, %s, %s, %s)", (item_name, category, quantity, price))
    db.commit()
    
    return redirect(url_for('index'))

@app.route('/update_item/<int:id>', methods=['POST'])
def update_item(id):
    item_name = request.form['item-name']
    category = request.form['category']
    quantity = request.form['quantity']
    price = request.form['price']
    
    cursor = db.cursor()
    cursor.execute("UPDATE inventory SET item_name=%s, category=%s, quantity=%s, price=%s WHERE id=%s", (item_name, category, quantity, price, id))
    db.commit()
    
    return redirect(url_for('index'))

@app.route('/delete_item/<int:id>', methods=['POST'])
def delete_item(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM inventory WHERE id=%s", (id,))
    db.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

