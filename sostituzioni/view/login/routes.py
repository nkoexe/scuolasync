from flask import render_template, redirect, url_for, request
from . import login

import logging


@login.route('/login', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('login.html')

    usr = request.form['username']
    psw = request.form['password']

    logging.debug(f'Tentativo di login dell\'utente {usr}')

    if psw != 'ciao':
        logging.debug(f'Login di {usr} fallito.')

        return render_template('login.html')

    logging.debug(f'Login di {usr} effettuato con successo.')

    return redirect(url_for('online.index'))  # maybe distinguere qui un utente per la visualizzazione fisica?


@login.route('/logout')
def logout():
    return redirect(url_for('login.main'))
