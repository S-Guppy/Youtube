from flask import Flask, render_template, abort
import sqlite3

app = Flask(__name__)

# Making the functions


def connect_database(statement, id, mode):
    # there are 3 variables in this function
    # the function runs a query and stores the result as a statement
    conn = sqlite3.connect("channel.db")
    cur = conn.cursor()
    if id is not None:
        cur.execute(statement, id)
        # for pages where the id changes(chosen by the user)
    # the 2nd variable is what is inputed into the query when the function runs
    else:
        cur.execute(statement)
    if mode == 1:
        # if the 3rd variable is a 1 - this means many results are returned and
        # fetchall needs to be run
        results = cur.fetchall()
    else:
        results = cur.fetchone()
    return results


def detect_website(social_link, social_name):
    # The function creates a new list which will store and link
    # (for example) www.instagram.com/norrisnuts to Instagram as well as
    # holding the website's profile picture.
    website_order = []
    for i in range(len(social_link)):
        try:
            # This will find the 'www.(something).com' part of the link
            website = social_link[i][0].split("/")[2]
        except Exception as e:
            print("Make sure there isn't a 'NULL' type value in \
            'ChannelSocial' so don't leave any part blank in that table.", e)
            website = None
        for i in range(len(social_name)):
            try:
                if website == social_name[i][2]:
                    website_order.append([social_name[i][0],
                                          social_link[i][0],
                                          social_name[i][1]])
            except Exception as e:
                print(e)
    return website_order


def detect_social(member_sociallink, social_details):
    social_order = []
    for i in range(len(member_sociallink)):
        try:
            website = member_sociallink[i][0].split("/")[2]
        except Exception as e:
            print("Make sure there isn't a 'NULL' type value in 'SocialMember'\
                  so don't leave any part blank that table.", e)
            website = None
        for i in range(len(social_details)):
            try:
                if website == social_details[i][2]:
                    social_order.append([social_details[i][0],
                                         member_sociallink[i][0],
                                         social_details[i][1]])
            except Exception as e:
                print(e)
    return social_order


# making routes
@app.route('/')
def home():
    return render_template("home.html", title="channel")


@app.route('/all_channels')
def all_channels():
    channel_names = connect_database("SELECT id,\
                                     name, pfp FROM Channel", None, 1)
    return render_template("all_channels.html", channel_names=channel_names)


@app.route('/all_members')
def all_members():
    member_names = connect_database("SELECT id, name,\
                                    image FROM Member", None, 1)
    return render_template("all_members.html", member_names=member_names)


@app.route('/all_socials')
def all_socials():
    social_names = connect_database("SELECT * FROM Social", None, 1)
    return render_template("all_socials.html", social_names=social_names)


@app.route('/all_genres')
def all_genres():
    genre_names = connect_database("SELECT * FROM Genre", None, 1)
    return render_template("all_genres.html", genre_names=genre_names)


@app.errorhandler(404)
# Learnt how to make 404 error page
# https://www.youtube.com/watch?v=9l3wwMHFrks&t=10s&ab_channel=Cairocoders
def invalid_route(e):
    return render_template("404.html"), 404


@app.route('/channel/<int:id>')
def channel(id):
    # Grabs all the info for all channels
    channel = connect_database("SELECT * FROM Channel WHERE id=?", (id,), None)
    if channel is None:
        abort(404)
    # https://stackoverflow.com/questions/25599923/abort-404-not-working-in-flask-after-request
    # the link above helped me to write the if statement below
    # if channel is None:
    #    return render_template("404.html")
    # This only grabs the info for other channels
    merch_link = connect_database("SELECT merch FROM Channel where id=? and \
            merch is NOT NULL", (id,), None)
    channel_member = connect_database("SELECT id, name, image FROM Member \
            WHERE id IN (SELECT mid FROM ChannelMember WHERE cid=?)", (id,), 1)
    channel_genre = connect_database("SELECT * FROM Genre WHERE id IN \
            (SELECT gid FROM ChannelGenre WHERE cid=?)", (id,), 1)
    social_link = connect_database("SELECT link FROM ChannelSocial WHERE sid \
            IS NOT NULL and cid=?", (id,), 1)
    social_name = connect_database("SELECT handle, pfp, website FROM Social \
            WHERE id IN (SELECT sid FROM ChannelSocial WHERE cid=?)", (id,), 1)
    # "website_order" takes the variables and runs them through the
    # "detect_website" function which was made above - this is so that the
    # links are displayed using the particular social media site name
    website_order = detect_website(social_link, social_name)
    # Grabs the name and pfp of the main channel that is associated with
    # other channels - this is not displayed on the main channels page
    channel_2 = connect_database("SELECT id, name, pfp FROM Channel WHERE id\
            IN (SELECT primarychannel_id FROM Channel \
            WHERE id=? and id IS NOT primarychannel_id)", (id,), None)
    return render_template('channel.html', channel=channel,
                           website_order=website_order,
                           channel_member=channel_member,
                           channel_2=channel_2,
                           channel_genre=channel_genre,
                           social_link=social_link,
                           social_name=social_name,
                           merch_link=merch_link)


@app.route('/member/<int:id>')
def member(id):
    # Grabs all the information for ALL members
    member = connect_database("SELECT * FROM Member where id=?", (id,), None)
    if member is None:
        abort(404)
    # This query calls for the channels the one member is active on
    member_channel = connect_database("SELECT id, name, pfp FROM Channel WHERE\
            id IN (SELECT cid FROM ChannelMember WHERE mid=?)", (id,), 1)
    member_sociallink = connect_database("SELECT link FROM SocialMember WHERE \
            sid IS NOT NULL and mid=?", (id,), 1)
    social_details = connect_database("SELECT handle, pfp, website FROM Social\
            WHERE id IN (SELECT sid FROM SocialMember WHERE mid=?)", (id,), 1)
    social_order = detect_social(member_sociallink, social_details)
    return render_template('member.html', social_order=social_order,
                           member=member,
                           member_channel=member_channel,
                           member_sociallink=member_sociallink,
                           social_details=social_details)


@app.route('/genre/<int:id>')
def genre(id):
    # Grabs all the information for ALL genres
    genre = connect_database("SELECT * FROM Genre where id=?", (id,), None)
    if genre is None:
        abort(404)
    genre_channel = connect_database("SELECT id, name, pfp FROM Channel WHERE \
                id IN (SELECT cid FROM ChannelGenre WHERE gid=?)", (id,), 1)
    return render_template('genre.html', genre=genre,
                           genre_channel=genre_channel)


@app.route('/social/<int:id>')
def social(id):
    # Grabs all the information for ALL genres
    social = connect_database("SELECT * FROM Social \
            where id=?", (id,), None)
    if social is None:
        abort(404)
    social_channel = connect_database("SELECT name, pfp FROM Channel WHERE id \
            IN (SELECT cid FROM ChannelSocial WHERE sid=?)", (id,), 1)
    social_link = connect_database("SELECT link FROM ChannelSocial \
            WHERE sid=?", (id,), None)
    social_member = connect_database("SELECT name, image FROM Member WHERE id\
            IN (SELECT mid FROM SocialMember WHERE sid =?)", (id,), 1)
    social_memberlink = connect_database("SELECT link FROM SocialMember\
            WHERE sid=?", (id,), None)
    return render_template('social.html', social=social,
                           social_channel=social_channel,
                           social_link=social_link,
                           social_member=social_member,
                           social_memberlink=social_memberlink)


if __name__ == "__main__":
    app.run(debug=True)
