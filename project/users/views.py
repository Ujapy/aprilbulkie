from flask import render_template, Blueprint, flash, url_for, request, redirect, abort
from project.users.forms import (RegistrationForm, LoginForm,
                                 EmailForm, PasswordForm)
from sqlalchemy.exc import IntegrityError
from project import db, app, bcrypt, mail
from project.models import User
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from threading import Thread
from datetime import datetime
from project.decorators import check_confirmed




users_blueprint = Blueprint('users', __name__)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()


def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    confirm_url = url_for(
        'users.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html_body = render_template(
        'email_confirmation.html',
        confirm_url=confirm_url)
    
    html = 'To Confirm your email address click on the link above'
    sender = 'ujahdotpy@gmail.com'

    send_email('Confirm Your Email Address', sender, [user_email], html, html_body )

def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
 
    password_reset_url = url_for(
        'users.reset_with_token',
        token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)
 
    html_body = render_template(
        'email_password_reset.html',
        password_reset_url=password_reset_url)
    
    html = 'To reset your password click on the link above'
    sender = 'ujahdotpy@gmail.com'
 
    send_email('Password Reset Requested', sender, [user_email], html, html_body)

################
#### routes ####
################
@app.route("/")
@users_blueprint.route('/index')
@login_required
def index():

    return render_template('index.html')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                new_user = User(form.username.data, form.firstname.data, form.surname.data,
                form.sex.data, form.email.data, form.address.data, form.phone.data, 
                form.phone2.data, hash_password )
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                send_confirmation_email(new_user.email)
                flash('Thanks for registering!  Please check your email to confirm your email address.', 'success')               
                return redirect(url_for('users.unconfirmed'))
            except IntegrityError:
                db.session.rollback()
                flash('ERROR! Email ({}), Username({}) already exists.'.format(form.email.data, form.username.data), 'error')
    return render_template('register.html', title='Register', form = form)

@users_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))
 
    user = User.query.filter_by(email=email).first()
 
    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'info')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Thank you for confirming your email address!', 'success')
 
    return redirect(url_for('users.login'))

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                user.last_logged_in = user.current_logged_in
                user.current_logged_in = datetime.now()
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thanks for logging in, {}'.format(current_user.username),'success')
                next_page = request.args.get('next')
                return redirect(next_page)if next_page else redirect(url_for('users.index'))
            else:
                flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('users.login'))

@users_blueprint.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return render_template('password_reset_email.html', form=form)

        if user.email_confirmed:
            send_password_reset_email(user.email)
            flash('Please check your email for a password reset link.', 'success')
        else:
            flash('Your email address must be confirmed before attempting a password reset.', 'error')
        return redirect(url_for('users.login'))

    return render_template('password_reset_email.html', form=form)


@users_blueprint.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))
 
    form = PasswordForm()
 
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return redirect(url_for('users.login'))

        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user.password = hash_password
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))
 
    return render_template('reset_password_with_token.html', form=form, token=token)

@users_blueprint.route('/user_profile')
@login_required
@check_confirmed
def user_profile():
    return render_template('user_profile.html')

@users_blueprint.route('/email_change', methods=["GET", "POST"])
@login_required
def user_email_change():
    form = EmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user_check = User.query.filter_by(email=form.email.data).first()
                if user_check is None:
                    user = current_user
                    user.email = form.email.data
                    user.email_confirmed = False
                    user.email_confirmed_on = None
                    user.email_confirmation_sent_on = datetime.now()
                    db.session.add(user)
                    db.session.commit()
                    send_confirmation_email(user.email)
                    flash('Email changed!  Please confirm your new email address (link sent to new email).', 'success')
                    return redirect(url_for('users.user_profile'))
                else:
                    flash('Sorry, that email already exists!', 'error')
            except IntegrityError:
                flash('Error! That email already exists!', 'error')
    return render_template('email_change.html', form=form)


@users_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.email_confirmed:
        return redirect('users.index')
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')

@users_blueprint.route('/resend_confirmation')
@login_required
def resend_email_confirmation():
    try:
        send_confirmation_email(current_user.email)
        flash('Email confirmation has been sent to your mail.  Please check your email!', 'success')
    except IntegrityError:
        flash('Error!  Unable to send email to confirm your email address.', 'error')
 
    return redirect(url_for('users.index'))

@users_blueprint.route('/admin_view_users')
@login_required
def admin_view_users():
    if current_user.role != 'admin':
        abort(403)
    else:
        users = User.query.order_by(User.id).all()
        return render_template('admin_view_users.html', users=users)
    return redirect(url_for('stocks.watch_list'))
"""def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                   sender='ujahdotpy@gmail.com',
                   recipients=[user.email])
    msg.body = f'''To reset your password visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
if you did not make this request then simply ignore and no changes will be made.
'''
    mail.send(msg)
@users_blueprint.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    form = RequestResetForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)

@users_blueprint.route('/reset_request/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm(request.form)
    if form.validate_on_submit():

        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #user.authenticated = True
        user.password = hash_password
        db.session.commit()
        flash('Your password has been updated! You are now able to Login', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password', form=form)"""
