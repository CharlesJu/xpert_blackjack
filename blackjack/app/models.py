from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login
from flask_login import UserMixin
from sqlalchemy.sql import func
import random


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    reservations = db.relationship('Reservation', backref='reserver', lazy= 'dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Card:
    suits = ['Spades', 'Hearts','Diamonds','Clubs']
    ranks = [str(n) for n in range(2,11)]+['J','Q','K','A']

    def __init__(self, suit,cardvalue):
        if suit.title() not in self.suits:
            raise ValueError("'{}' is not a valid suit. Valid suits are -- {} -- passed in as a string".format(suit, self.suits))
        if cardvalue.upper() not in self.ranks:
            raise ValueError("'{}' is not a valid card value. Valid suits are -- {} -- passed in as a string".format(cardvalue, self.rank))
        self.rank = cardvalue.upper()
        self.suit = suit.title()     

        if self.rank == 'A':
            self.value = 11
        elif self.rank == 'J' or self.rank == 'Q' or self.rank == 'K':
            self.value = 10
        else:
            self.value = int(self.rank)

    def get_rank(self):
        return self.rank

    def get_value(self):
        return self.value

    def set_value(self, x):
        self.value = x

    def __repr__(self):
        return 'Card {} of {}'.format(self.rank, self.suit)


class Deck:
    def __init__(self):
        self.loadnewdeck()
        self.shuffledeck()

    def loadnewdeck(self):
        self.deck = list()
        for rank in Card.ranks:
            for suit in Card.suits:
                self.deck.append(Card(suit, rank))

    def shuffledeck(self):
        random.shuffle(self.deck)

    def cardsleftindeck(self):
        return len(self.deck)

    def dealcard(self):
        return self.deck.pop()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=func.now())
    end_time = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_comments = db.Column(db.String(140))
    reservations = db.relationship('Reservation', backref='reserved_device', lazy='dynamic')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

