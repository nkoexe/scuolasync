from flask import render_template, redirect, url_for, request

from sostituzioni.logger import logger
from sostituzioni.view.auth import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    usr = request.form['username']
    psw = request.form['password']

    logger.debug(f'Tentativo di login dell\'utente {usr}')

    if psw != 'ciao':
        logger.debug(f'Login di {usr} fallito.')

        return render_template('login.html')

    logger.debug(f'Login di {usr} effettuato con successo.')

    return redirect(url_for('online.index'))  # maybe distinguere qui un utente per la visualizzazione fisica?


@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))
