from flask import render_template, redirect, url_for, request

from sostituzioni.logger import logger
from sostituzioni.model.auth import current_user, login_required, permesso, login_user, logout_user
from sostituzioni.view.auth import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('online.index'))
        return render_template('login.html')

    if request.method == 'POST':
        # maybe distinguere qui un utente per la visualizzazione fisica?
        usr = request.form['username']
        psw = request.form['password']

        if psw == 'ciao':
            # login_user()
            return redirect(url_for('online.index'))

        return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.login'))
