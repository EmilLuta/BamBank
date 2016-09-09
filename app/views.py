from flask import abort, flash, g, make_response, redirect, render_template, request, session, url_for
from flask.ext.login import login_required, login_user, logout_user
from sqlalchemy import or_, desc

from app import app, db, login_manager
from .password_services import PasswordService

from .forms import LoginForm, RegisterForm, TransactionForm
from .models import Transaction, User

# =========================================================================
# Flask-Login
# =========================================================================

@login_manager.user_loader
def load_user(id):
    user = User.query.filter_by(id=id).first()
    return user


@login_manager.unauthorized_handler
def unauthorized():
    flash('You need to log in first.', 'warning')
    session['next_url'] = request.url
    return redirect(url_for('login', next=request.url))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)

        flash('Logged in successfully.', 'info')

        next = request.args.get('next')

        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = PasswordService.encrypt_password(form.password.data)
        user = User(username=form.username.data, password=password_hash, balance=100)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('You have successfully registered!', 'info')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

# =========================================================================
# App pages
# =========================================================================

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@app.route('/transaction', methods=('GET', 'POST'))
@login_required
def transaction():
    current_user_id = session['user_id']
    form = TransactionForm(user_id=current_user_id)
    if form.validate_on_submit():
        current_user = User.query.get(current_user_id)
        transaction = Transaction(from_id=current_user_id, to_id=form.users.data, amount=form.amount.data)
        current_user.balance -= form.amount.data
        user = User.query.get(form.users.data)
        user.balance += form.amount.data
        db.session.add(transaction)
        db.session.add(current_user)
        db.session.add(user)
        db.session.commit()
        flash('Your balance is now {}'.format(current_user.balance), 'info')
        return render_template('index.html')

    return render_template('transaction.html', form=form)

@app.route('/transactions')
@login_required
def transactions():
    user_id = int(session['user_id'])
    transactions = Transaction.query.filter(or_(Transaction.from_id == user_id, Transaction.to_id == user_id)).order_by(desc(Transaction.created_at)).all()
    return render_template('transactions.html', transactions=transactions)

# =========================================================================
# Error pages
# =========================================================================

@app.errorhandler(404)
def error_404(error):
    return (render_template('404.html'), 404)


@app.errorhandler(500)
def error_500(error):
    return (render_template('500.html'), 500)
