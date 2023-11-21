from flask import render_template, redirect, url_for, request

from sostituzioni.logger import logger
from sostituzioni.model.auth import current_user, login_required, permesso, sso_login, logout_user, GOOGLE_SSO_REQ_URI
from sostituzioni.view.auth import auth


@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('online.index'))

    return render_template('login.html')


@auth.route('/googlesso')
def googlessoredirect():
    return redirect(GOOGLE_SSO_REQ_URI)


@auth.route('/loginredirect')
def loginredirect():

    sso_login(request)

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
