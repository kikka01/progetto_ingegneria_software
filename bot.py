"""
@consegna_compito_bot
Autori: Chiara e Leonardo
"""

import logging
import telegram
# import telegram.ext
# import telebot
# import sqlite3
# import settings
import bs4  # permette di estrarre facilmente dei dati dalle pagine HTML che compongono i siti web
from bs4 import BeautifulSoup
import requests  # per accedere ai siti web tramite richieste HTTP
#bs4 va installata usando il comando: pip install bs4
#requests va installata usando il comando: pip install requests
import webbrowser  # per aprire automaticamente i siti web sul browser


token = "6370580588:AAGKKqCgMAtPduC4Nb63IzwPepFycdkvn8w"
bot = telebot.TeleBot(token)

# roba che non so se effettivamente è utile
updater = Updater(token)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("end", end))
updater.start_polling()
updater.idle()


# Gestore del comando /start
# Studenti e docenti possono utilizzare il comando /start per avviare il bot.
def start(update, context):      #update rappresenta un update in arrivo, context serve a portare informazioni aggiuntive all'update
    chat_id = update.effective_chat.id   #id della chat da cui stiamo ricevendo il comando
    update.message.reply_text("start")   #utility per rispondere velocemente al messaggio ricevuto
    print("start called from chat with id = {}".format(chat_id))


def start(update, context):
    start_msg = "*Benvenuto a* @consegna_compito_bot.\n"\
	"- Se sei uno STUDENTE, questo bot ti permetterà di visualizzare l\'elenco dei docenti. \n"\
        "Ti permetterà inoltre di consegnare al proprio docente le foto della prova scritta. \n\n"\
        "- Se sei un DOCENTE, questo bot ti permetterà di visualizzare l\'elenco degli studenti che hanno consegnato. \n"\
        "Ti permetterà inoltre di visualizzare le foto caricate dagli studenti nel giorno corrente. \n\n"\
        "Per visualizzare i comandi disponibili utilizza /help\n\n"
    update.message.reply_markdown(start_msg, reply_markup=ReplyKeyboardRemove())
    pp.flush()


def help(update, context):
    help_msg = "Ecco una lista dei *comandi* attualmente disponibili su questo bot:\n\n"\
        "- /help: Visualizza questo messaggio\n"\
        "- /lista_docenti: Visualizza l\'elenco dei docenti e i loro ID\n"\
        "- /consegna ID_docente: Permette il caricamento delle foto della prova scritta per la consegna al docente\n"\
        "- /consegne: Visualizza gli ID degli studenti che hanno effettuato consegne nel giorno corrente\n"\
        "- /leggi ID_studente: Visualizza le foto caricate dagli studenti nel giorno corrente\n"\
        "- /end: Interrompe il comando attualmente in esecuzione\n"
    update.message.reply_markdown(help_msg)

# Gestore del comando /lista_docenti
# Gli studenti possono utilizzare il comando /lista_docenti per ottenere
# l'elenco dei docenti e i loro ID.
# Per il comando /lista_docenti, recupera le informazioni sui docenti dalla
# tabella "docenti" e invia un messaggio contenente l'elenco degli studenti
# e dei loro ID.
LINK = "https://www.dmi.unipg.it/dipartimento/rubrica?categoria=DOC&lettera=&pagina="


# Gestore del comando /consegna
# Gli studenti possono utilizzare il comando /consegna ID_docente per caricare
# la foto della prova scritta per la consegna al docente.
# Per il comando /consegna, salva le informazioni sulla consegna nella tabella
# "consegne", inclusa la foto caricata dallo studente.


# Gestore del comando /consegne
# I docenti possono utilizzare il comando /consegne per visualizzare gli ID
# degli studenti che hanno effettuato consegne nel giorno corrente.
# Per il comando /consegne, recupera gli ID degli studenti che hanno effettuato
# consegne nel giorno corrente dalla tabella "consegne" e invia un messaggio
# contenente l'elenco degli ID degli studenti.


# Gestore del comando /leggi
# I docenti possono utilizzare il comando /leggi ID_studente per visualizzare
# o scaricare le foto caricate dagli studenti nel giorno corrente.
# Per il comando /leggi, recupera le foto caricate dagli studenti nel giorno
# corrente dalla tabella "consegne" utilizzando l'ID dello studente specificato
# e invia o rendi scaricabile la foto al docente.


# Gestore del comando /end
# Studenti e docenti possono utilizzare il comando /end per terminare il bot.
def end(update, context):
    chat_id = update.effective_chat.id
    update.message.reply_text("end")
    print("end called from chat with id = {}".format(chat_id))
