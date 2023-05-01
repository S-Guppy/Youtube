from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", title="BOB")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/all_pizzas')
def alls_pizzas():
    conn=sqlite3.connect("pizzanew.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Pizza")
    results=cur.fetchall()
    return render_template("all_pizzas.html",results=results)

@app.route('/pizza/<int:id>')
def pizza(id):
    conn=sqlite3.connect("pizzanew.db")
    cur=conn.cursor()
    cur.execute("SELECT *FROM Pizza WHERE id=?",(id,))
    pizza=cur.fetchone()
    cur.execute("SELECT name FROM Base WHERE id=?",(pizza[4],))
    pizza_base=cur.fetchone()
    cur.execute("SELECT name FROM Topping WHERE id IN(SELECT tid FROM PizzaTopping WHERE pid=(id=?))",(id,))
    pizza_topping=cur.fetchall()
    return render_template('pizza.html', pizza=pizza, pizza_base=pizza_base, pizza_topping=pizza_topping)
    #return render_template('pizza.html', id=id)

if __name__ == "__main__":
    app.run(debug=True)