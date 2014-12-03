###########################################################################
#
#   File Name      Date          Owner               Description
#   ----------   --------      ---------        -----------------
#   models.py    12/2/2014   Archana Bahuguna  Db table design/models 
#
#   Schema- models.db - tables: Users
#
###########################################################################

from flask.ext.sqlalchemy import SQLAlchemy
from views import app

import os

file_path = os.path.abspath(os.getcwd())+"/models.db"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+file_path
db = SQLAlchemy(app)
app.config['SQLALCHEMY_RECORD_QUERIES']=True

MAXUSRS = 1000
MAXPODCASTS = 10

class User(db.Model):
    """ Defines the columns and keys for User table """
    #Add sequence
    userid    = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(32))
    email     = db.Column(db.String(64))
    address   = db.Column(db.String(200))

    def __init__ (self, username, email, address):
        self.username = username
        self.email = email
        self.address = address

    podcasts = db.relationship("Podcast", backref = "user")

    def __repr__(self):
        return '%i        %s        %s         %s' % (self.userid, self.username, self.email, self.address)

class Podcast(db.Model):
    """ Defines the columns and keys for User table """
    #Add sequence
    podcastid  = db.Column(db.Integer, primary_key=True)
    userid   = db.Column(db.Integer, db.ForeignKey('user.userid'))
    podcastdata  = db.Column(db.String(1064))

    def __init__ (self, podcastdata, userid):
        self.podcastdata = podcastdata
        self.userid = userid

    def __repr__(self):
        return '%i        %i        %s ' % (self.podcastid, self.userid, self.podcastdata)

