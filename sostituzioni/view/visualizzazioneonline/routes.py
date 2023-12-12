from flask import render_template

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_required
from sostituzioni.view.visualizzazioneonline import online


@online.route('/')
@login_required
def index():
    return render_template('index.html', title=configurazione.get('systitle'), configurazione=configurazione)


@online.route('/testone')
def testone():
    from sostituzioni.model.model import Sostituzione
    data = {'pubblicato': True, 'data': '2023-12-09', 'ora_predefinita': '2', 'ora_inizio': '',
            'ora_fine': '', 'docente': 'Carlo Verdi', 'classe': '3 LC', 'aula': '204', 'note': 'wowowowowoow!!'}

    Sostituzione(id=None, aula=data.get('aula'), classe=data.get('classe'), docente=data.get('docente'), data=data.get('data'),
                 ora_inizio=data.get('ora_inizio'), ora_fine=data.get('ora_fine'), ora_predefinita=data.get('ora_predefinita'), note=data.get('note'), pubblicato=data.get('pubblicato')).inserisci()

    return 'ok'
