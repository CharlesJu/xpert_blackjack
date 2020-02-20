from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_session import Session 
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Card, Deck


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats you are now a registered user, now please login')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register',form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts= [
        {'author': user, 'body': 'Test1'},
        {'author': user, 'body': 'Test2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/blackjack/<username>')
@login_required
def blackjack(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('blackjack.html', user=user)

@app.route('/gamestart/<username>')
@login_required
def gamestart(username):
    user = User.query.filter_by(username=username).first_or_404()
    session["won"] = False
    session["lost"] = False
    session["myDeck"] = Deck()
    session["myhand"] = list()
    session["dealerhand"] = list()
    
    card1 = myDeck.dealcard()
    card2 = myDeck.dealcard()
    card3 = myDeck.dealcard()
    card4 = myDeck.dealcard()

    if card1.get_value() + card3.get_value() == 21:
        won = True

    myhand.append(card1)
    dealerhand.append(card2)
    myhand.append(card3)
    dealerhand.append(card4)

    return render_template('gamestart.html', user = user, myhand = myhand, dealerhand = dealerhand, deck=myDeck, won = won, lost = lost)

@app.route('/hit/<username>')
@login_required
def hit(username):
    user = User.query.filter_by(username=username).first_or_404()
    myhand = request.args.get('myhand', type=list)
    dealerhand = request.args.get('dealerhand', type=list)
    myDeck = request.args.get('mydeck', Deck())
    won = request.args.get('won', type=bool)
    lost = request.args.get('lost', type=bool)

    nextCard = myDeck.dealcard()
    nextCard.get_value()
    myhand.append(nextCard)

    score = 0
    for card in myhand:
        score = score + 0


    return render_template('hit.html', user = user, myhand = myhand, dealerhand = dealerhand, deck=myDeck, won = won, lost = lost)


@app.route('/stand/<username>')
@login_required
def stand(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('stand.html', user = user, myhand = myhand, dealerhand = dealerhand, deck=myDeck, won = won, lost = lost)









