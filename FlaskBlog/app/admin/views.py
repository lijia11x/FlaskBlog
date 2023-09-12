# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, render_template, flash, \
                  Blueprint
import ujson
from app.db import *
from . import admin
from .form import RenameChronofileForm, RenameAuthorForm
from app.decorators import login_required
from app.details import get_details

@admin.route('/')
@login_required
def view_admin():
    '''Display name of site, author, etc. as well as links to edit
        those details and change email, password, etc.'''

    details = get_details()
    return render_template('admin.html', details=details)


@admin.route('/rename_blogfile',methods=['GET','POST'])
@login_required
def rename_blog():
    details = get_details()
    form = RenameChronofileForm()
    if form.validate_on_submit():
        update_record('admin', {'chronofile_name':form.new_name.data},Query().creator_id==session.get('user_id'))
        flash('Blog name updated')
        return redirect(url_for('admin.view_admin'))
    return render_template('rename_chronofile.html', form=form, details=details)  # GET请求返回页面


@admin.route('/rename_author', methods=['GET','POST'])
@login_required
def rename_author():
    details = get_details()
    form = RenameAuthorForm()
    if form.validate_on_submit():
        update_record('admin',{'author_name': form.new_name.data}, Query().creator_id==session.get('user_id'))
        flash('Author name updated')
        return redirect(url_for('admin.view_admin'))
    return render_template('rename_author.html', form=form, details=details)



