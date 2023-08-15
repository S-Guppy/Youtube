from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Making the functions

def connect_database(statement, id, mode):
# there are like
    conn = sqlite3.connect("channel.db")
    cur = conn.cursor()
    if id != None:
        cur.execute(statement, id)
    else:
        cur.execute(statement)
    if mode == 1:
        results = cur.fetchall()
    else:
        results = cur.fetchone()
    return results


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


def detect_hehe(member_social, social_details):
    website_hehe = []
    for i in range(len(member_social)):
        try:
            website = member_social[i][0].split("/")[2]
        except Exception as e:
            print("Make sure there isn't a 'NULL' type value in 'SocialMember' so don't leave any part blank that table.", e)
            website = None
        for i in range(len(social_details)):
            try:
                if website == social_details[i][2]:
                    website_hehe.append([social_details[i][0], member_social[i][0], social_details[i][1]])
            except Exception as e:
                print(e)
    return website_hehe


# making routes #
@app.route('/')
def home():
    return render_template("home.html", title="channel")


@app.route('/all_channels')
def all_channels():
    channel_names = connect_database("SELECT id, name, pfp FROM Channel", None, 1)
    return render_template("all_channels.html", channel_names=channel_names)


@app.route('/all_members')
def all_members():
    member_names = connect_database("SELECT id, name, image FROM Member", None, 1)
    return render_template("all_members.html", member_names=member_names)


@app.route('/all_socials')
def all_socials():
    social_names = connect_database("SELECT * FROM Social", None, 1)
    return render_template("all_socials.html", social_names=social_names)


@app.route('/all_genres')
def all_genres():
    genre_names = connect_database("SELECT * FROM Genre", None, 1)
    return render_template("all_genres.html", genre_names=genre_names)


@app.route('/channel/<int:id>')
def channel(id):
    # Grabs all the information for MAIN channels only and stores it in a variable called channel
    channel = connect_database("SELECT * FROM Channel WHERE id=? and total_video IS NOT NULL", (id,), None)
    # This only grabs the info for other channels and stores it in a variable called channel_2
    other_channels = connect_database("SELECT name, subscriber, pfp FROM Channel WHERE id=? and total_video IS NULL", (id,), None)
    channel_member = connect_database("SELECT id, name FROM Member WHERE id IN (SELECT mid FROM ChannelMember WHERE cid=?)", (id,), 1)
    social_link = connect_database("SELECT link FROM ChannelSocial WHERE sid IS NOT NULL and cid=?", (id,), 1)
    social_name = connect_database("SELECT handle, pfp, website FROM Social WHERE id IN (SELECT sid FROM ChannelSocial WHERE cid=?)", (id,), 1)
    website_order = detect_website(social_link, social_name)
    channel_2 = connect_database("SELECT name, pfp FROM Channel WHERE id IN (SELECT primarychannel_id FROM Channel WHERE id=? and id IS NOT primarychannel_id)", (id,), None)
    return render_template('channel.html', website_order=website_order, channel=channel, other_channels=other_channels, channel_member=channel_member, channel_2=channel_2, social_link=social_link, social_name=social_name)


@app.route('/member/<int:id>')
def member(id):
    member = connect_database("SELECT * FROM Member where id=?", (id,), None)
    member_channel = connect_database("SELECT name, pfp FROM Channel WHERE id IN (SELECT cid FROM ChannelMember WHERE mid=?)", (id,), 1)
    member_social = connect_database("SELECT link FROM SocialMember WHERE sid IS NOT NULL and mid=?", (id,), 1)
    social_details = connect_database("SELECT handle, pfp, website FROM Social WHERE id IN (SELECT sid FROM SocialMember WHERE mid=?)", (id,), 1)
    website_hehe = detect_hehe(member_social, social_details)
    return render_template('member.html', website_hehe=website_hehe, member=member, member_channel=member_channel, member_social=member_social, social_details=social_details)


@app.route('/genre/<int:id>')
def genre(id):
    genre = connect_database("SELECT * FROM Genre where id=?", (id,), None)
    genre_channel = connect_database("SELECT name, pfp FROM Channel WHERE id IN (SELECT cid FROM ChannelGenre WHERE gid=?)", (id,), 1)
    return render_template('genre.html', genre=genre, genre_channel=genre_channel)


@app.route('/social/<int:id>')
def social(id):
    social = connect_database("SELECT * FROM Social where id=?",(id,), None)
    social_channel = connect_database("SELECT name, pfp FROM Channel WHERE id IN (SELECT cid FROM ChannelSocial WHERE sid=?)", (id,), 1)
    social_link = connect_database("SELECT link FROM ChannelSocial WHERE sid=?", (id,), None)
    return render_template('social.html', social=social, social_channel=social_channel, social_link=social_link)


if __name__ == "__main__":
    app.run(debug=True)
