from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
hi

# Making the fucntions
def detect_website(social_link, social_name):
    # The function creates a new list which will store and link (for example) www.instagram.com/norrisnuts to Instagram as well as holding the website's profile picture of your choice.
    website_order = []
    for i in range(len(social_link)):
        try:
            # This will find the 'www.(something).com' part of the link 
            website = social_link[i][0].split("/")[2]
        except Exception as e:
            print("Make sure there isn't a 'NULL' type value in 'ChannelSocial' so don't leave any part blank in that table.", e)
            website = None
        for i in range(len(social_name)):
            try:
                if website == social_name[i][2]:
                    website_order.append([social_name[i][0], social_link[i][0], social_name[i][1]])
            except Exception as e:
                print(e)
    return website_order

# making routes #
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
# Grabs all the information for MAIN channels only and stores it in a variable called channel
    cur.execute("SELECT * FROM Channel WHERE id=? and total_video IS NOT NULL",(id,))
    channel=cur.fetchone()
# This only grabs the info for other channels and stores it in a variable called channel_2
    cur.execute("SELECT name, subscriber, pfp FROM Channel WHERE id=? and total_video IS NULL", (id,))
    second_channel=cur.fetchone()
    cur.execute("SELECT id, name FROM Member WHERE id IN (SELECT mid FROM ChannelMember WHERE cid=?)", (id,))
    channel_member=cur.fetchall()
    cur.execute("SELECT link FROM ChannelSocial WHERE sid IS NOT NULL and cid=?" ,(id,))
    social_link=cur.fetchall()
    cur.execute("SELECT handle, pfp, website FROM Social WHERE id IN (SELECT sid FROM ChannelSocial WHERE cid=?)", (id,))
    social_name=cur.fetchall()
    website_order = detect_website(social_link, social_name)
    cur.execute("SELECT name, pfp FROM Channel WHERE id IN (SELECT primarychannel_id FROM Channel WHERE id=? and id IS NOT primarychannel_id)", (id,))
    channel_2=cur.fetchone()
    return render_template('channel.html', website_order=website_order, channel=channel, second_channel=second_channel, channel_member=channel_member, channel_2=channel_2, social_link=social_link, social_name=social_name)

@app.route('/member/<int:id>')
def member(id):
    conn=sqlite3.connect("channel.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Member where id=?",(id,))
    member=cur.fetchone()
    cur.execute("SELECT name, pfp FROM Channel WHERE id IN (SELECT cid FROM ChannelMember WHERE mid=?)",(id,))
    member_channel=cur.fetchall()
    cur.execute("SELECT link FROM SocialMember WHERE sid IS NOT NULL and mid=?" ,(id,))
    social_link=cur.fetchall()
    cur.execute("SELECT handle FROM Social WHERE id IN (SELECT sid FROM SocialMember WHERE mid=?)", (id,))
    member_social=cur.fetchall()
    cur.execute("SELECT link FROM SocialMember WHERE sid IS NOT NULL and mid=?" ,(id,))
    channel_fb=cur.fetchall()
    cur.execute("SELECT handle FROM Social WHERE id IN (SELECT sid FROM SocialMember WHERE mid=?)", (id,))
    member_s=cur.fetchall()
    cur.execute("SELECT link FROM SocialMember WHERE sid IS NOT NULL and mid=? UNION SELECT handle FROM Social WHERE id IN (SELECT sid from ChannelSocial WHERE cid=?)",(id, id,))
    working=cur.fetchall()
    return render_template('member.html', member=member, member_channel=member_channel, member_social=member_social, social_link=social_link, channel_fb=channel_fb, member_s=member_s)

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


