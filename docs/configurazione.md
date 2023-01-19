# File di configurazione del sistema

File json per le impostazioni di configurazione.

## Struttura del file

Il file di configurazione è una lista di sezioni:

```jsonc
    "sistema": {  // identificativo della sezione che verrà utilizzato per la navigazione
        "title": "Sistema",  // Titolo della sezione
        "descr": "",  // Descrizione
        "options": {  // Lista di impostazioni che fanno parte della sezione
        }
    }
```

Che a loro volta contengono una lista di opzioni:

```jsonc
    "settingid": {  // identificativo per uso interno dell'opzione, deve essere univoco
        "title": "Setting title",  // Testo che verrà mostrato come titolo dell'opzione
        "descr": "Descriptive text of the setting.",  // Descrizione della funzione dell'opzione
        "config": {  // Campo dell'opzione
        }
      }
```

La singola opzione può avere diversi tipi di campi, tutti con questa struttura base:

```jsonc
    "type": "text",
    "default": "Example text",
    "value": "Example text"
```

### Lista di tutti i campi previsti

I campi possibili sono: text, num, unitnum, bool, color, select.

Ogni campo è identificato dal suo attributo "type", che può solo avere uno dei sopracitati nominativi.

- Testo semplice

```jsonc
  "config": {
    "type": "text",
    "max-lenght": 50, // Per non impostare una lunghezza massima, scrivere 'null' (senza virgolette)
    "default": "Example text",
    "value": "Example text"
  }
```

- Numero

```jsonc
  "config": {
    "type": "num",
    "interval": [0, 100], // Impostare [null, null] per non imporre limiti
    "default": 45,
    "value": 57
  }
```

- Numero con unità di misura

```jsonc
  "config": {
    "type": "unitnum",
    "interval": [0, 100], // Impostare [null, null] per non imporre limiti
    "default": 45,
    "value": 57,
    "units": ["px", "pt", "em"],
    "defaultunit": "pt",
    "unit": "px",
  }
```

- Booleano vero/falso

```jsonc
  "config": {
    "type": "bool",
    "default": false,
    "value": true
  }
```

- Color

```jsonc
  "config": {
    "type": "color",
    "default": "#000000",
    "value": "#ffffff"
  }
```

- Selezione dropdown

```jsonc
  "config": {
    "type": "select",
    "choices": ["In Produzione", "In Manutenzione", "In Sviluppo"],
    "default": 0,
    "value": 2
  }
```
