"""
@consegna_compito_bot
Autori: Chiara e Leonardo
"""
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

PUO SERVIRE 
update.message.reply_text(
        f"Ciao, {user.first_name}! Benvenuto nel bot.\n"
        "Scegli un'opzione:",
        reply_markup={
            "keyboard": [["Opzione 1"], ["Opzione 2"]],
            "one_time_keyboard": True,
            "resize_keyboard": True,
        },
    )
    
"""

from typing import final
from urllib.parse import urljoin
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes,Updater , CallbackQueryHandler, CallbackContext
import random
import requests
from bs4 import BeautifulSoup


print('Starting up bot...')

#TOKEN : final = "6669345460:AAFMtWB6HM_Gy-VJkPFaWf_8Lg0lvrcJur8"
#BOT_USERNAME : final = "@consegna_compito_unipg_bot"
TOKEN : final = "6370580588:AAGKKqCgMAtPduC4Nb63IzwPepFycdkvn8w"
BOT_USERNAME : final = "@consegna_compito_bot"
LINK : final = "https://www.dmi.unipg.it/dipartimento/rubrica?categoria=DOC&lettera=&pagina="
HEADERS : final = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Dizionario per tenere traccia degli utenti che hanno già premuto il pulsante
users_pressed_button = {}

#funzione per scaricare la pagina web
def get_html_content(LINK):
    response = requests.get(LINK, headers=HEADERS)
    # print(response.text)
    if response.status_code == 200:
        return response.text
    else:
        print("Errore nella request, codice:",response.status_code)
    

#funzione per analizzare la pagina
def extract_names_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    #iframe = soup.find("iframe")
    
    #iframe_url = urljoin(LINK, iframe["src"])
    #iframe_html = get_html_content(iframe_url)
    #iframe_soup = BeautifulSoup(iframe_html, "html.parser")

    table = soup.find("table", class_="table table-striped table-condensed") #trovo la tabella con la classe "table table-striped table-condensed"
    rows = table.find_all("tr")

    values = []
    for row in rows[0:6]:
        row_values = [value.get_text(strip=True) for value in row.find_all("td")]
        if any(row_values):
            values.append(row_values)

    values = [row for row in values if any(row[1:])]
    docenti_array = []

    for row in values:
        for value in row[1:]:
            docenti_array.append(value)

    table_string = "Elenco del personale\n\n"
    for row in values:
        #row_string = "\n".join([f"{header}: {value}" for header, value in zip(headers, row)])
        row_string = "\n".join([f"{value}" for value in zip(row)])
        table_string += f"{row_string}\n\n"

    return table_string

# funzioni utili
def get_user_id(update: Update):
    user_id = update.effective_user.id
    return user_id 

def remove_spaces(input_string):
    return "".join(input_string.split())

def random_with_50_percent_probability():
    return random.random() < 0.5

# commands
async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = get_user_id(update)
    users_pressed_button[user_id] = False  # Impostiamo l'utente come non ha ancora premuto il pulsante
    await update.message.reply_text(
        f"Ciao, {user.first_name}!\n"
        "Scegli un'opzione:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Studente", callback_data="opzione_1")],
            [InlineKeyboardButton("Professore", callback_data="opzione_2")],
        ]),
    )
    """
    start_msg = "Benvenuto a", BOT_USERNAME,".\n"\
	"- Se sei uno STUDENTE, questo bot ti permetterà di visualizzare l\'elenco dei docenti. \n"\
        "Ti permetterà inoltre di consegnare al proprio docente le foto della prova scritta. \n\n"\
        "- Se sei un DOCENTE, questo bot ti permetterà di visualizzare l\'elenco degli studenti che hanno consegnato. \n"\
        "Ti permetterà inoltre di visualizzare le foto caricate dagli studenti nel giorno corrente. \n\n"\
        "Per visualizzare i comandi disponibili utilizza /help\n\n"
    await update.message.reply_text(start_msg)
    """

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = "Ecco una lista dei *comandi* attualmente disponibili su questo bot:\n\n"\
        "- /help: Visualizza questo messaggio\n"\
        "- /lista_docenti: Visualizza l\'elenco dei docenti e i loro ID\n"\
        "- /consegna ID_docente: Permette il caricamento delle foto della prova scritta per la consegna al docente\n"\
        "- /consegne: Visualizza gli ID degli studenti che hanno effettuato consegne nel giorno corrente\n"\
        "- /leggi ID_studente: Visualizza le foto caricate dagli studenti nel giorno corrente\n"\
        "- /end: Interrompe il comando attualmente in esecuzione\n"
    await update.message.reply_text(help_msg)

async def lista_docenti_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #solo per studenti
    html_content = get_html_content(LINK)# Ottieni il contenuto HTML
    names = extract_names_html(html_content)# Analizza il contenuto con Beautiful Soup
    await update.message.reply_text(names)
    #bot.send_message(message.chat.id, table_string)

async def consegna_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #solo per studenti
    await update.message.reply_text('Non faccio nulla ancora')

async def consegne_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #solo per prof
    await update.message.reply_text('Non faccio nulla ancora')

async def leggi_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #solo per prof
    await update.message.reply_text('Non faccio nulla ancora')

async def end_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Non faccio nulla ancora')

#Funzioni

# Funzione di gestione del callback dei pulsanti inline
async def handle_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if not users_pressed_button.get(user_id, False):
        option_selected = query.data

        if option_selected == "opzione_1":
            await context.bot.send_message(chat_id=query.message.chat_id, text="Hai selezionato Studente. Scrivmi il tuo ID.")
        elif option_selected == "opzione_2":
            await context.bot.send_message(chat_id=query.message.chat_id, text="Hai selezionato Professore. Scrivmi il tuo ID.")
        else:
            await query.answer("Opzione non valida.")
        # Imposta l'utente come ha premuto il pulsante
        users_pressed_button[user_id] = True
    else:
        await query.answer("Hai già premuto il pulsante.")

#funzioni risposta ai messaggi
def handle_response_int(text: int,update: Update) -> str:
    #processed: str = text.lower()
    user_id = get_user_id(update)
    if users_pressed_button.get(user_id, False):
        if (len(text) == 6):
            result = random_with_50_percent_probability()

            if(result):
                return 'ID accettato'
            else:
                return 'risposta non accettata'
    else:
        return 'scegli studente o professore'
    
def handle_response(text: str,update: Update) -> str:
    processed: str = text.lower()

    return 'testo non accettato'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # informazioni del tipo di messaggio ricevuto
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # utile per debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    digit = remove_spaces(text)
    if digit.isdigit():
        response: str = handle_response_int(int(digit),update)
    else:
        response: str = handle_response(text,update)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    app.add_handler(CommandHandler('lista_docenti', lista_docenti_command))
    app.add_handler(CommandHandler('consegna', consegna_command))
    app.add_handler(CommandHandler('leggi', leggi_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT , handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=3)

print("terminato")
