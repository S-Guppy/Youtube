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
    cur.execute("SELECT * FROM Channel WHERE id=?",(id,))
    channel=cur.fetchone()
    cur.execute("SELECT name FROM Member WHERE id IN (SELECT mid FROM ChannelMember WHERE cid=?)", (id,))
    channel_member=cur.fetchall()
    cur.execute("SELECT handle, pfp FROM Social WHERE id IN (SELECT sid FROM ChannelSocial WHERE cid=?)",(id,))
    channel_social=cur.fetchall()
    cur.execute("SELECT link FROM ChannelSocial WHERE sid = 1 and cid=?" ,(id,))
    channel_insta=cur.fetchone()
    cur.execute("SELECT link FROM ChannelSocial WHERE sid = 2 and cid=?",(id,))
    channel_twitter=cur.fetchone()
    cur.execute("SELECT link FROM ChannelSocial WHERE sid = 3 and cid=?",(id,))
    channel_tiktok=cur.fetchone()
    cur.execute("SELECT link FROM ChannelSocial WHERE sid = 4 and cid=?",(id,))
    channel_facebook=cur.fetchone()
    cur.execute("SELECT link FROM ChannelSocial WHERE sid is null and cid=?",(id,))
    channel_nope=cur.fetchone()
    cur.execute("SELECT name, pfp FROM Channel WHERE id IN (SELECT primarychannel_id FROM Channel WHERE id=?)", (id,))
    channel_2=cur.fetchone()
    return render_template('channel.html', channel=channel, channel_member=channel_member, channel_social=channel_social, channel_2=channel_2, channel_insta=channel_insta, channel_twitter=channel_twitter, channel_tiktok=channel_tiktok, channel_facebook=channel_facebook, channel_nope=channel_nope)



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

if __name__ == "__main__":
    app.run(debug=True)

