# -*- coding:utf-8 -*-
import os
from flask import Flask, session, g, redirect, url_for, render_template, flash, Blueprint, current_app, abort
from flask_bootstrap import Bootstrap
from datetime import datetime
import ujson
from app.db import *
from . import main
from .forms import RawEntryForm, EditEntryForm
from app.parse import *
from app.pagination import *
from app.decorators import login_required
from app.details import get_details

@main.route('/',methods=['GET', 'POST'])
def browser_all_entries():
    '''Returns all entries (most recent entry at the top of the page).'''
    details = get_details()
    if not session.get('logged_in'):
        if details:
            register = False
        else:
            register = True
            details = {'chronofile_name': current_app.config['DEFAULT_NAME'],
                       'author_name': current_app.config['DEFAULT_AUTHOR']}
        return render_template('welcome.html', details=details, register=register)
    form = RawEntryForm()
    # Try to validate form and create a new entry
    if form.validate_on_submit():
        return parse_input(form.raw_entry.data, datetime.utcnow())
    # Otherwise, show the latest entries
    page = 1
    # Get entries for the given page
    entries_for_page = get_entries_for_page(page)
    # Check if there's another page, returns None if not
    next_page = check_next_page(page)
    return render_template('home.html', entries_for_page=entries_for_page, form=form, details=details, next_page=next_page)
