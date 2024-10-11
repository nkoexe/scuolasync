# 🎯 **Testare l'Installazione**

Per verificare che tutto funzioni correttamente:

1. Apri un browser e accedi all'indirizzo del server, come `http://scuolasync.fuss.bz.it`.
2. Se tutto è stato configurato correttamente, dovresti vedere l'interfaccia di **ScuolaSync**.
3. Se ci sono problemi, controlla i log di Gunicorn e Nginx:

```bash
journalctl -u scuolasync.service
cat /var/log/nginx/error.log
```

---

# 🛠️ **Risoluzione dei Problemi Comuni**

## 1. **Errore "Permission denied"**
   - Verifica che l'utente abbia i permessi corretti sulle directory. Correggi i permessi con:

   ```bash
   sudo chown -R <USER>:<GROUP> /home/scuolasync
   ```

## 2. **Problemi con la Porta 5123**
   - Se la porta **5123** è già in uso, puoi modificarla nel file `scuolasync.service` e nella configurazione di Nginx. Assicurati che nessun altro servizio stia utilizzando la porta con il comando:

   ```bash
   sudo lsof -i :5123
   ```

Con questa guida, hai tutto il necessario per installare e configurare **ScuolaSync**. Se riscontri ulteriori problemi, puoi consultare la documentazione ufficiale o contattare il supporto tecnico.