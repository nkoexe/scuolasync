import logging
from flask import render_template, redirect, url_for, request

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import current_user, login_required, permesso, sso_login, logout_user, GOOGLE_SSO_REQ_URI
from sostituzioni.view.auth import auth


logger = logging.getLogger(__name__)


@auth.route('/fottiti')
def fottiti():
    return "vai a fotterti"


@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('online.index'))

    # 3 lines of development speedup, remove in production pls ty
    from sostituzioni.model.auth import authenticate_user
    authenticate_user('niccolo.ragazzi@gandhimerano.com')
    return redirect(url_for('online.index'))

    return render_template('login.html', title=configurazione.get('systitle'))


@auth.route('/googlesso')
def googlessoredirect():
    return redirect(GOOGLE_SSO_REQ_URI)


@auth.route('/loginredirect')
def loginredirect():
    """Richiesta di autorizzazione dopo l'autenticazione con Google"""

    authenticated = sso_login(request)

    if authenticated:
        return redirect(url_for('online.index'))
    else:
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
