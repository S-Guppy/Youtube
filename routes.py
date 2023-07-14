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
    cur.execute("SELECT id, name, pfp FROM Channel")
    results=cur.fetchall()
    return render_template("all_channels.html",results=results)

@app.route('/all_members')
def all_members():
    conn=sqlite3.connect("channel.db")
    cur=conn.cursor()
    cur.execute("SELECT id, name, image FROM Member")
    results=cur.fetchall()
    return render_template("all_members.html",results=results)

@app.route('/all_socials')
def all_socials():
    conn=sqlite3.connect("channel.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Social")
    results=cur.fetchall()
    return render_template("all_socials.html",results=results)

@app.route('/all_genres')
def all_genres():
    conn=sqlite3.connect("channel.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Genre")
    results=cur.fetchall()
    return render_template("all_genres.html",results=results)

@app.route('/channel/<int:id>')
def channel(id):
    conn=sqlite3.connect("channel.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Channel WHERE id=? and total_video IS NOT NULL",(id,))
    channel=cur.fetchone()
    cur.execute("SELECT name, subscriber, pfp FROM Channel WHERE id=? and total_video IS NULL", (id,))
    second_channel=cur.fetchone()
    cur.execute("SELECT name FROM Member WHERE id IN (SELECT mid FROM ChannelMember WHERE cid=?)", (id,))
    channel_member=cur.fetchall()
    cur.execute("SELECT link FROM ChannelSocial WHERE sid IS NOT NULL and cid=?" ,(id,))
    channel_insta=cur.fetchall()
    cur.execute("SELECT handle FROM Social WHERE id IN (SELECT sid FROM ChannelSocial WHERE cid=?)", (id,))
    social_name=cur.fetchall()
    cur.execute("SELECT name, pfp FROM Channel WHERE id IN (SELECT primarychannel_id FROM Channel WHERE id=?)", (id,))
    channel_2=cur.fetchone()
    return render_template('channel.html', channel=channel, second_channel=second_channel, channel_member=channel_member, channel_2=channel_2, channel_insta=channel_insta, social_name=social_name)

@app.route('/member/<int:id>')
def member(id):
    conn=sqlite3.connect("channel.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Member where id=?",(id,))
    member=cur.fetchone()
    cur.execute("SELECT name, pfp FROM Channel WHERE id IN (SELECT cid FROM ChannelMember WHERE mid=?)",(id,))
    member_channel=cur.fetchall()
    return render_template('member.html', member=member, member_channel=member_channel)

@app.route('/genre/<int:id>')
def genre(id):
    conn=sqlite3.connect("channel.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Genre where id=?",(id,))
    genre=cur.fetchone()
    cur.execute("SELECT name, pfp FROM Channel WHERE id IN (SELECT cid FROM ChannelGenre WHERE gid=?)",(id,))
    genre_channel=cur.fetchall()
    return render_template('genre.html', genre=genre, genre_channel=genre_channel)

@app.route('/social/<int:id>')
def social(id):
    conn=sqlite3.connect("channel.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Social where id=?",(id,))
    social=cur.fetchone()
    cur.execute("SELECT name, pfp FROM Channel WHERE id IN (SELECT cid FROM ChannelSocial WHERE sid=?)",(id,))
    social_channel=cur.fetchall()
    cur.execute("SELECT link FROM ChannelSocial WHERE sid=?", (id,))
    social_link=cur.fetchone()
    return render_template('social.html', social=social, social_channel=social_channel, social_link=social_link)

if __name__ == "__main__":
    app.run(debug=True)

