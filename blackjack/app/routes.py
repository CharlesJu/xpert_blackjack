from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Card, Deck


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'Xpert @ SCU'},
            'body': 'Welcome to blackjack'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirects user to index if they've already been authenticated
        return redirect(url_for('index'))

    form = LoginForm()  # Create login form

    # Submit post request for login form
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # Checks if the login credentials are valid
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # login the user and check remember box
        login_user(user, remember=form.remember_me.data)
        # Get request for next page ("/index")
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user() # Logout endpoint
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Register as a new user
    """
    # If the user is already logged in, go to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    # Submit post request for form
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Add user to the database
        db.session.add(user)
        db.session.commit()
        
        flash('Congrats you are now a registered user, now please login')
        return redirect(url_for('login')) # Get request to redirect
   
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    """ User page
    """
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Welcome to blackjack'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/blackjack/<username>')
@login_required
def blackjack(username):
    """ Start blackjack game
    """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('blackjack.html', user=user)


@app.route('/gamestart/<username>')
@login_required
def gamestart(username):
    """ Start blackjack game
    """
    user = User.query.filter_by(username=username).first_or_404()

    # Create session dictionary to store decks and hands
    session['won'] = False
    session['lost'] = False
    session['myDeck'] = Deck()
    session['myhand'] = list()
    session['dealerhand'] = list()

    # Get 2 cards for player and 2 cards for dealer
    card1 = session['myDeck'].dealcard()
    card2 = session['myDeck'].dealcard()
    card3 = session['myDeck'].dealcard()
    card4 = session['myDeck'].dealcard()

    # Append cards to hand
    session['myhand'].append(card1)
    session['dealerhand'].append(card2)
    session['myhand'].append(card3)
    session['dealerhand'].append(card4)

    session['score'] = card1.get_value() + card3.get_value()
    session['dealerscore'] = card2.get_value() + card4.get_value()

    # Win condition
    if session['score'] == 21:
        session['won'] = True

    return render_template('gamestart.html', user=user, myhand=session["myhand"], dealerhand=session["dealerhand"],
                           deck=session["myDeck"], won=session["won"], lost=session["lost"])


@app.route('/hit/<username>')
@login_required
def hit(username):
    """ User hit endpoint
    """
    user = User.query.filter_by(username=username).first_or_404()

    # Deal and append card to hand
    nextCard = session["myDeck"].dealcard()
    session["myhand"].append(nextCard)

    # Recalculate score
    session['score'] = session['score'] + nextCard.get_value()

    # Win and lose conditions
    if session["score"] == 21:
        session["won"] = True
    elif session["score"] > 21:
        session["lost"] = True

    return render_template('hit.html', user=user, myhand=session["myhand"], dealerhand=session["dealerhand"],
                           deck=session["myDeck"], won=session["won"], lost=session["lost"])


@app.route('/stand/<username>')
@login_required
def stand(username):
    """ User stand endpoint
    """
    user = User.query.filter_by(username=username).first_or_404()

    # Deal cards to the dealer until the hand gets bigger than 17
    while session['dealerscore'] < 17:
        c = session['myDeck'].dealcard()
        session['dealerhand'].append(c)
        session['dealerscore'] = session['dealerscore'] + c.get_value()
    
    # Win and lose conditions
    if session['dealerscore'] > 21:
        session['won'] = True
    elif session['dealerscore'] > session['score']:
        session['lost'] = True

    return render_template('stand.html', user=user, myhand=session["myhand"], dealerhand=session["dealerhand"],
                           deck=session["myDeck"], won=session["won"], lost=session["lost"])
