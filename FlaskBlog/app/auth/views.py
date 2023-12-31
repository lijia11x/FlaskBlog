# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, render_template, flash, \
    Blueprint, current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import abort, redirect, url_for

import ujson
from app.db import *
from . import auth, pwd_context
from .forms import ChangeEmailForm, ChangePasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, \
    SetNewPasswordForm
from app.mail import send_email
from app.decorators import login_required
from app.details import get_details


@auth.route('/login', methods=['GET', 'POST'])
def login():
    details = get_details()
    if not get_record('auth', Query().email.exists()):
        flash('请先注册')
        return redirect(url_for('auth.register'))
    if session.get('logged_in'):
        return redirect(url_for('main.browse_all_entries'))
    form = LoginForm()
    if form.validate_on_submit():
        session['logged_in'] = True
        user_id = get_element_id('auth', Query().email == form.email.data)
        session['user_id'] = user_id
        if request.args.get('next'):
            return redirect(request.args.get('next'))
        else:
            return redirect(url_for('main.browse_all_entries'))
    return render_template('login.html', form=form, details=details)


@auth.route('/logout')
@login_required
def logout():
    session['logged_in'] = None
    flash('You have been logged out.')
    return redirect(url_for('main.browse_all_entries'))


@auth.route('/register',methods=['GET', 'POST'])
def register():
    ''' Register user and create pagination table with one page
        and no entries.'''
    details = get_details()
    if details:
        flash('A user is already registered. Log in.')
        return redirect(url_for('auth.login'))
    details = {'chronofile_name': current_app.config['DEFAULT_NAME'],
               'author_name': current_app.config['DEFAULT_AUTHOR']}
    register = True

    form = RegistrationForm()

    if form.validate_on_submit():
        password_hash = pwd_context.hash(form.password.data)
        creator_id = insert_record('auth', {'email': form.email.data, 'password_hash': password_hash})
        insert_record('admin', {'chronofile_name': current_app.config['DEFAULT_NAME'],
                                'author_name': current_app.config['DEFAULT_AUTHOR'], 'creator_id': creator_id})
        insert_record('pagination', {'page': 1, 'entries': None})
        flash('Registration successful. You can login now.')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form, details=details, register=register)


@auth.route('/reset_password', methods=['GET', 'POST'])
def request_reset():
    details = get_details()
    if not details:
        return abort(404)
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user_id = get_element_id('auth',Query().email==email)
        token = generate_confirmation_token(user_id)
        send_email(email,'Link to reset your password',
                   'email/reset_password', token=token)
        flash('Your password reset token has been sent.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form, details=details)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def confirm_password_request(token):
    details = get_details()
    if not details:
        return abort(404)

    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except:
        flash('The password reset link is invalid or has expired.')
        return redirect(url_for('auth.request_reset'))
    if not data.get('confirm'):
        flash('The password reset link is invalid or has expired.')
        return redirect(url_for('auth.request_reset'))

    user_id = data.get('confirm')
    form = SetNewPasswordForm()
    if form.validate_on_submit():
        new_password_hash = pwd_context.hash(form.new_password.data)
        get_table('auth').update({'password_hash': new_password_hash}, eids=[user_id])
        flash('密码已更新成功，您可以继续登录')
        return redirect(url_for('auth.login'))
    return render_template('set_new_password.html', form=form, token=token, details=details)

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    details = get_details()
    form = ChangeEmailForm()
    if form.validate_on_submit():
        new_email = form.new_email.data
        user_id = session.get('user_id')
        get_table('auth').update({'email': new_email}, eids=user_id)
        flash('您的邮箱已更改成功')
        return redirect(url_for('admin.view_admin'))
    return render_template('change_email.html', form=form, details=details)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    details = get_details()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        new_password_hash = pwd_context.hash(form.new_password.data)
        get_table('auth').update({'password_hash': new_password_hash}, eids=[session.get('user_id')])
        flash('Your password has been updated.')
        return redirect(url_for('admin.view_admin'))
    return render_template('change_password.html', form=form, details=details)

def generate_confirmation_token(user_id, expiration=3600):
    serial = Serializer(current_app.config['SECRET_KEY'], expiration)
    return serial.dumps({'confirm': user_id})
