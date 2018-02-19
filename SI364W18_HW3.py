## SI 364 - Winter 2018
## HW 3

####################
## Import statements
####################

# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, ValidationError
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell # New

# Basic Flask application setup
basedir = os.path.abspath(os.path.dirname(__file__)) # In case we need to reference the base directory of the application
# To set up application and defaults for running
############################
# Application configurations
############################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwertyhaha'
## TODO 364: Create a database in postgresql in the code line below, and fill in your app's database URI. It should be of the format: postgresql://localhost/YOUR_DATABASE_NAME

## Your final Postgres database should be your uniqname, plus HW3, e.g. "jczettaHW3" or "maupandeHW3"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:guest@localhost:5432/wjchatHW3" #sets correct path
## Provided:
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##################
### App setup ####
##################
db = SQLAlchemy(app) # For database use

#########################
#########################
######### Everything above this line is important/useful setup,
## not problem-solving.##
#########################
#########################

#########################
##### Set up Models #####
#########################

## TODO 364: Set up the following Model classes, as described, with the respective fields (data types).

## The following relationships should exist between them:
# Tweet:User - Many:One

# - Tweet
## -- id (Integer, Primary Key)
## -- text (String, up to 280 chars)
## -- user_id (Integer, ID of user posted -- ForeignKey)

class Tweet(db.Model):
    __tablename__ = 'tweets'
    tweetID = db.Column(db.Integer, primary_key = True)
    tweetText = db.Column(db.String(280))
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))

  

## Should have a __repr__ method that returns strings of a format like:
#### {Tweet text...} (ID: {tweet id})
    def __repr__(self):
        return ('<{Tweet %r}>' %self.tweetText) + ('<ID: %r>' %self.tweetID)

# - User
## -- id (Integer, Primary Key)
## -- username (String, up to 64 chars, Unique=True)
## -- display_name (String, up to 124 chars)
## ---- Line to indicate relationship between Tweet and User tables (the 1 user: many tweets relationship)

class User(db.Model):
    __tablename__ = 'users'
    userID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    displayName = db.Column(db.String(124))
    tweets = db.relationship('Tweet',backref='User')


## Should have a __repr__ method that returns strings of a format like:
#### {username} | ID: {id}
    def __repr__(self):
        return ('<{Username: %r}>' %self.username) + ('<ID: %r>' %self.userID)

########################
##### Set up Forms #####
########################

# TODO 364: Fill in the rest of the below Form class so that someone running this web app will be able to fill in information about tweets they wish existed to save in the database:

## -- text: tweet text (Required, should not be more than 280 characters)
## -- username: the twitter username who should post it (Required, should not be more than 64 characters)
## -- display_name: the display name of the twitter user with that username (Required, + set up custom validation for this -- see below)


def display_validate(form, field):
    if len(field.data.split()) < 2:
        raise ValidationError('Display name must be at least 2 words long.')

def username_validate(form, field):
    if field.data[0] == '@':
        raise ValidationError('Username cannot start with @.')

class TweetForm(FlaskForm):

    

    text = StringField("Enter the tweet here:", validators = [Required(), Length(max=280, message = 'Length cannot be over 280 characters.')])
    username = StringField("Enter the username here:", validators = [Required(), Length(max=64, message = "Length cannot be over 64 characters."), username_validate])
    display_name = StringField("Enter the display name of the twitter user:", validators = [Required(), display_validate])
    submit = SubmitField('submit me')

    

# HINT: Check out index.html where the form will be rendered to decide what field names to use in the form class definition

# TODO 364: Set up custom validation for this form such that:
# - the twitter username may NOT start with an "@" symbol (the template will put that in where it should appear)
# - the display name MUST be at least 2 words (this is a useful technique to practice, even though this is not true of everyone's actual full name!)
   


# TODO 364: Make sure to check out the sample application linked in the readme to check if yours is like it!


###################################
##### Routes & view functions #####
###################################

## Error handling routes - PROVIDED
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#############
## Main route
#############

## TODO 364: Fill in the index route as described.

# A template index.html has been created and provided to render what this route needs to show -- YOU just need to fill in this view function so it will work.
# Some code already exists at the end of this view function -- but there's a bunch to be filled in.
## HINT: Check out the index.html template to make sure you're sending it the data it needs.
## We have provided comment scaffolding. Translate those comments into code properly and you'll be all set!

# NOTE: The index route should:
# - Show the Tweet form.
# - If you enter a tweet with identical text and username to an existing tweet, it should redirect you to the list of all the tweets and a message that you've already saved a tweet like that.
# - If the Tweet form is entered and validates properly, the data from the form should be saved properly to the database, and the user should see the form again with a message flashed: "Tweet successfully saved!"
# Try it out in the sample app to check against yours!



@app.route('/', methods=['GET', 'POST'])
def index():

        # Initialize the form

    form = TweetForm()

    # tweet_number = 0  revisit

        # If the form was posted to this route,
    ## Get the data from the form

    num_tweets = len(Tweet.query.all())
    if form.validate_on_submit():
        text = form.text.data #get tweet text
        username = form.username.data #get username
        display_name = form.display_name.data #get display name

####revisit
        # Get the number of Tweets
        # q = db.query('select * from tweets')
        # q.getresult()

        # tweet_number = len(q)


        ## Find out if there's already a user with the entered username
        user = User.query.filter_by(username = username).first()
        ## If there is, save it in a variable: user
        ## Or if there is not, then create one and add it to the database
        if not user:
            user = User(username = username, displayName = display_name)  #creates user database object
            db.session.add(user)
            db.session.commit()

        ## If there already exists a tweet in the database with this text and this user id (the id of that user variable above...) ## Then flash a message about the tweet already existing
         

        t = Tweet.query.filter_by(tweetText = text, userID = user.userID).first()
        if t:
            flash('This tweet already exists, redirecting.')
            return redirect('/all_tweets')

        ## And redirect to the list of all tweets
        else:
        ## Assuming we got past that redirect,
        ## Create a new tweet object with the text and user id
            
            tweet = Tweet(tweetText = text, userID = user.userID)
        ## And add it to the database

            db.session.add(tweet)
            db.session.commit()

            flash('The tweet was successfully added')
            return redirect(url_for('index'))
        ## Flash a message about a tweet being successfully added
        ## Redirect to the index page

    # PROVIDED: If the form did NOT validate / was not submitted
    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
    return render_template('index.html', form = form, num_tweets = num_tweets) # TODO 364: Add more arguments to the render_template invocation to send data to index.html

@app.route('/all_tweets')
def see_all_tweets():

    tweets = Tweet.query.all()

    all_tweets = []

    for tweet in tweets:
        user = User.query.filter_by(userID = tweet.userID).first()
        all_tweets.append((tweet.tweetText, user.username))

    return render_template('all_tweets.html', all_tweets = all_tweets) # Replace with code
    # TODO 364: Fill in this view function so that it can successfully render the template all_tweets.html, which is provided.


    # HINT: Careful about what type the templating in all_tweets.html is expecting! It's a list of... not lists, but...
    # HINT #2: You'll have to make a query for the tweet and, based on that, another query for the username that goes with it...


@app.route('/all_users')
def see_all_users():
    pass # Replace with code
    # TODO 364: Fill in this view function so it can successfully render the template all_users.html, which is provided.
    users = User.query.all()


    return render_template('all_users.html', users = users)

# TODO 364
# Create another route (no scaffolding provided) at /longest_tweet with a view function get_longest_tweet (see details below for what it should do)
# TODO 364
# Create a template to accompany it called longest_tweet.html that extends from base.html.


@app.route('/longest_tweet')
def longest_tweets():
    tweets = Tweet.query.all()

    list_tweets = []

    longest_tweet = ['', '']

    for tweet in tweets:
        list_tweets.append([tweet.tweetText, tweet.tweetText.replace(' ', ''), tweet])


    for each in list_tweets:

        if len(each[1]) > len(longest_tweet[0]):
            longest_tweet[0] = each[0]
            user = User.query.filter_by(userID = each[2].userID).first()
            longest_tweet[1] = user.username


        if len(each[1]) == len(longest_tweet):

            if min(each[1].lower(), longest_tweet.lower()) == each[1].lower():
                longest_tweet[0] = each[0]
                user = User.query.filter_by(userID = each[2].userID).first()
                longest_tweet[1] = user.username

        


    return render_template('longest_tweet.html', tweet = longest_tweet)





# NOTE:
# This view function should compute and render a template (as shown in the sample application) that shows the text of the tweet currently saved in the database which has the most NON-WHITESPACE characters in it, and the username AND display name of the user that it belongs to.
# NOTE: This is different (or could be different) from the tweet with the most characters including whitespace!
# Any ties should be broken alphabetically (alphabetically by text of the tweet). HINT: Check out the chapter in the Python reference textbook on stable sorting.
# Check out /longest_tweet in the sample application for an example.

# HINT 2: The chapters in the Python reference textbook on:
## - Dictionary accumulation, the max value pattern
## - Sorting
# may be useful for this problem!


if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual
