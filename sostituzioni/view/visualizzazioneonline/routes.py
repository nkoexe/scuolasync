from flask import render_template, request

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_required, role_required, current_user
from sostituzioni.view.visualizzazioneonline import online


code = 'my85nyh5724025g740389ny91cf6ntynm5ynm89346y86y30h6yn0g6ny832yn7fkuy84532gdsfhiofg78432n5fayht4nh78523th789treaju89f32gb5ayhn89rewbn679532yj8953ayn79532yj89weuj088'


@online.route('/infopoint/frontend')
def test():
    if request.args.get('code') == code:
        return 'infopoint!!!! wowow!!!'

    return 'no'


@online.route('/')
@login_required
def index():
    return render_template('index.html', title=configurazione.get('systitle'), configurazione=configurazione, utente=current_user)


@online.route('/testone')
def testone():
    from sostituzioni.model.model import Sostituzione
    data = {'pubblicato': True, 'data': '2023-12-25', 'ora_predefinita': '2', 'ora_inizio': '',
            'ora_fine': '', 'docente': 'Alessandro Stucchi', 'classe': '1 LC', 'aula': '101', 'note': ''}

    Sostituzione(id=None, aula=data.get('aula'), classe=data.get('classe'), docente=data.get('docente'), data=data.get('data'),
                 ora_inizio=data.get('ora_inizio'), ora_fine=data.get('ora_fine'), ora_predefinita=data.get('ora_predefinita'), note=data.get('note'), pubblicato=data.get('pubblicato')).inserisci()

    return 'ok'
