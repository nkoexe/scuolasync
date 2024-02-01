# File di configurazione del sistema

! obsoleto, da rifare completamente
File json per le impostazioni di configurazione.

### Struttura del file

Il file di configurazione è composto in due parti, sezioni e opzioni.

```jsonc
{
  "sezioni": {
    ...
  },
  "opzioni": {
    ...
  }
}
```

## Sezioni
Le sezioni sono definite nella prima metà nel file, sono meramente una lista di titoli che indicano nella visualizzazione come vengono suddivise le opzioni.
Sono identificate da un id univoco che ha soltanto uso interno, non verrà mostrato all'utente.
Ogni opzione ha un attributo `sezione` che fa riferimento all'identificativo della sezione alla quale appartiene.
Ogni sezione ha attributi di titolo e descrizione, che verranno mostrati nell'interfaccia di impostazioni per dirigere l'utente.

```jsonc
"sezioni": {
  // identificativo della sezione
  "sistema": {
      // Titolo della sezione
      "titolo": "Sistema", 
      // Breve descrizione
      "descrizione": "Impostazioni base"
  },
  ...
}
```

---

## Opzioni


La singola opzione può avere diversi tipi di campi, tutti con questa struttura base:

```jsonc
    "type": "text",
    "default": "Example text",
    "value": "Example text"
```

### Lista di tutti i campi previsti

### 1. Testo

- **Descrizione**: Opzione che accetta input di testo.

#### Attributi di Testo:

- **Lunghezza Massima** (max_length):
  - **Descrizione**: Specifica la lunghezza massima consentita per l'input di testo.
  - **Tipo**: Numero intero.
  - **Esempio**: `{"max_length": 30}`

### 2. Selezione

- **Descrizione**: Opzione che permette la selezione di un valore da un insieme di opzioni predefinite.

#### Attributi di Selezione:

- **Scelte** (choices):
  - **Descrizione**: Lista delle opzioni tra cui l'utente può selezionare.
  - **Tipo**: Lista di stringhe.
  - **Esempio**: `{"choices": ["In Produzione", "In Manutenzione", "In Sviluppo"]}`

### 3. Numero

- **Descrizione**: Opzione che accetta input numerici.

#### Attributi di Numero:

- **Intervallo** (range):
  - **Descrizione**: Specifica l'intervallo di valori consentito per l'input numerico.
  - **Tipo**: Lista contenente due valori (minimo e massimo).
  - **Esempio**: `{"range": [-10, 399]}`

### 4. Numero con Unità di Misura

- **Descrizione**: Opzione che accetta input numerici con unità di misura.

#### Attributi di Numero con Unità di Misura:

- **Scelte Unità** (unit_choices):
  - **Descrizione**: Lista delle unità di misura disponibili.
  - **Tipo**: Lista di stringhe.
  - **Esempio**: `{"unit_choices": ["px", "em", "rem", "cm"]}`
  
### 5. Booleano

- **Descrizione**: Opzione che rappresenta uno stato di vero o falso.

#### Attributi Booleani:

- Nessun attributo specifico oltre al valore booleano stesso.

### 6. Percorso

- **Descrizione**: Opzione che rappresenta un percorso di file o directory nel sistema.

#### Attributi di Percorso:

- **Radice** (root):
  - **Descrizione**: Specifica la radice del percorso (ad esempio, "/" per radice del filesystem).
  - **Tipo**: Stringa.
  - **Esempio**: `{"root": "/"}`


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
