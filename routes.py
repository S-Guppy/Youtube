from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html", title="channel")

@app.route('/all_channels')
def all_channels():
    conn=sqlite3.connect("channel.db")
    cur=conn.cursor()
    cur.execute("SELECT name, pfp FROM Channel")
    results=cur.fetchall()
    return render_template("all_channels.html",results=results)

@app.route('/channel/<int:id>')
def pizza(id):
    conn=sqlite3.connect("channel.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Channel WHERE id=?",(id,))
    channel=cur.fetchone()
    cur.execute("SELECT * FROM Member WHERE id IN(SELECT member_id FROM ChannelMember WHERE channel_id=(id=?))",(id,))
    channel=cur.fetchone()
    cur.execute("SELECT name, pfp FROM Genre WHERE id IN(SELECT genre_id FROM ChannelGenre WHERE channel_id=(id=?))",(id,))
    channel=cur.fetchall()
    cur.execute("SELECT handle, pfp FROM Social WHERE id IN(SELECT social_id FROM ChannelSocial WHERE channel_id=(id=?))",(id,))
    channel=cur.fetchall()
    return render_template('channel.html', channel=channel) #pizza_base=pizza_base, pizza_topping=pizza_topping)
    #return render_template('pizza.html', id=id)

if __name__ == "__main__":
    app.run(debug=True)

