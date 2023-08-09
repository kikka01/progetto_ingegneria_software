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
import re
import sqlite3


print('Starting up bot...')

TOKEN : final = "6669345460:AAFMtWB6HM_Gy-VJkPFaWf_8Lg0lvrcJur8"
BOT_USERNAME : final = "@consegna_compito_unipg_bot"
#TOKEN : final = "6370580588:AAGKKqCgMAtPduC4Nb63IzwPepFycdkvn8w"
#BOT_USERNAME : final = "@consegna_compito_bot"
LINK : final = "https://www.dmi.unipg.it/dipartimento/rubrica?categoria=DOC&lettera=&pagina="
HEADERS : final = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Dizionario per tenere traccia degli utenti che hanno già premuto il pulsante
users_pressed_button = {}
users_autentication = {} #dizionario che ci dice se l'utente si è autenticato correttamente
users_class = [] #ogni elemento della lista è una tupla composta da [user_id, "studente"/"professore"]
prof_names = []

def get_class_of_user(id):
    for id_u,clas in users_class:
        if id == id_u:
            return clas
    return "errore"

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
    table = soup.find("table", class_="table table-striped table-condensed") #trovo la tabella con la classe "table table-striped table-condensed"
    rows = table.find_all("tr")
    names = []
    for row in rows[0:]:
        row_values = [value.get_text(strip=True) for value in row.find_all("td")] #lista che contiene i testi dei tag <td> (colonne) presenti nella riga corrente della tabella
        if any(row_values):
            names.append(row_values[0])
            prof_names.append(row_values[0])

    return names


################################################################################

"""# PROVA DATABASE

# Connessione al database
connection = sqlite3.connect('database.db')
cursor = connection.cursor()  # Ottieni il cursore per eseguire le query


# Creazione della tabella "studenti_e_password" nel database con due campi: ID_studente, password_studente
tab1 = "create table studenti_e_password (" 
       "ID_studente primary key int not null," \
       "password_studente char(3) not null);"
connection.execute(tab1)  # creazione della tabella vuota

# Inserimento di dati (righe) nella tabella studenti_e_password
item1 = [331332, 'abc']  #array con i dati che voglio inserire
cursor.execute('insert into studenti_e_password values (?,?);', item1) #ID_studente, password_studente
connection.commit()  #conferma i dati e li scrive nel database

item2 = [330350, 'def']
cursor.execute('insert into studenti_e_password values (?,?);', item2)
connection.commit()  #conferma i dati e li scrive nel database


# Creazione della tabella "docenti_e_password" nel database con due campi: ID_docente, password_docente
tab2 = "create table docenti_e_password (" 
       "ID_docente primary key varchar(30) not null," \
       "password_docente int not null);"
connection.execute(tab2)  # creazione della tabella vuota

# Inserimento di dati (righe) nella tabella docenti_e_password
item = []
for i in range(0,len(names)-1):
    item = [names[i],i]
    cursor.execute('insert into docenti_e_password values (?,?);', item) #ID_docente, password_docente
    connection.commit() #conferma i dati e li scrive nel database


# Creazione della tabella "compiti_consegnati" nel database con quattro campi: code_foto, ID_studente, ID_docente, data_ora
tab3 = "create table compiti_consegnati (" 
       "code_foto int primary key not null," \
       "ID_studente int not null," \
       "ID_docente varchar(30) not null," \
       "data_e_ora varchar(20) not null);"
connection.execute(tab3)  # creazione della tabella vuota

# Inserimento di dati (righe) nella tabella compiti_consegnati
current_date = datetime.now()
formatted_date_time = current_date.strftime("%Y-%m-%d %H:%M:%S") #es. "2023-07-29 15:30:45"

item = []  #array con i dati che voglio inserire
# Riempo item con i nuovi dati da aggiungere
#item[0] = ?? #code_foto (con numpy)
#item[1] = ?? #ID_studente
#item[2] = ?? #ID_docente
item[3] = formatted_date_time #data_e_ora
cursor.execute('insert into compiti_consegnati values (?,?,?,?);', item) #code_foto, ID_studente, ID_docente, data_e_ora
connection.commit()  #conferma i dati e li scrive nel database


# Lettura (query) della tabella compiti_consegnati
cursor.execute("select * from compiti_consegnati") #DA INSERIRE FILTRI
# esempi filtri:
# cursor.execute("select * from compiti_consegnati where ID_studente == 331332")
for row in cursor.fetchall(): #fetchall = tutte le righe estratte
    print("({}) studente {} consegna a docente {}, in data {}".format(row[0], row[1], row[2], row[3]))
    #formattazione: segnaposto={}
    #row = struttura (array) con i dati che vengono estratti da ogni riga


# Chiusura di connessione e cursore del database
cursor.close()
connection.close()
"""

#################################################################################

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
    users_autentication[user_id] = False
    await update.message.reply_text(
        f"Ciao, {user.first_name}!\n"
        "Chi sei ?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Studente", callback_data="Studente")],
            [InlineKeyboardButton("Professore", callback_data="Professore")],
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
        "- /leggi ID_studente: Visualizza le foto caricate dagli studenti nel giorno corrente\n"
    await update.message.reply_text(help_msg)

#solo per studenti
async def lista_docenti_command(update: Update, context: CallbackContext): #context: ContextTypes.DEFAULT_TYPE
    user_id = get_user_id(update)
    
    if users_class:
        class_of_user = get_class_of_user(user_id)
    else :
        class_of_user = "non valido"
        await update.message.reply_text("Non hai il permeso di eseguire questo comando")

    if class_of_user == "Studente" and users_autentication.get(user_id, True): # cioè è uno studente e si è autenticato
        html_content = get_html_content(LINK)# Ottieni il contenuto HTML
        names = extract_names_html(html_content)# Analizza il contenuto con Beautiful Soup

        keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in names]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Seleziona un professore:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Non hai il permeso di eseguire questo comando")

async def lista_consegne_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #solo per prof
    user_id = get_user_id(update)
    if users_class:
        class_of_user = get_class_of_user(user_id)
    else :
        await update.message.reply_text('Autenticati prima')
    if class_of_user == "Professore":
        await update.message.reply_text('Scivi matricola studente.')
    elif class_of_user == "Studente":
        await update.message.reply_text('Invia le foto e scrivi \"fine\" per salvarle nel database.')
    
    cursor.execute("select * from compiti_consegnati")
    for row in cursor.fetchall():
        output_string = "({}) Lo studente {} ha consegnato al docente {}, in data {}".format(row[0], row[1], row[2], row[3])
        update.message.reply(output_string)

async def leggi_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #solo per prof
    '''
    #await update.message.reply_text('Scrivi ID dello studente di cui vuoi vedere le foto')
    #la riga prima è da mettere quando chiamerò la funzione (devo capire bene come)
    studente_richiesto = update.message.text
    cursor.execute("select * from compiti_consegnati where ID_studente == studente_richiesto")
    for row in cursor.fetchall(): #fetchall = tutte le righe estratte
        output_string = "({}) Lo studente {} ha consegnato al docente {}, in data {}".format(row[0], row[1], row[2], row[3])
        update.message.reply(output_string)
    '''
    await update.message.reply_text('Non faccio nulla ancora')


#Funzioni

# Funzione di gestione del callback dei pulsanti inline
async def handle_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = get_user_id(update)#query.from_user.id
    option_selected = query.data
    if option_selected == "Studente" or option_selected == "Professore":
        if not users_pressed_button.get(user_id, False):
            users_class.append([user_id,option_selected ])

            if option_selected == "Studente":
                await context.bot.send_message(chat_id=query.message.chat_id, text="Hai selezionato Studente. Scrivi la tua matricola.")
            elif option_selected == "Professore":
                await context.bot.send_message(chat_id=query.message.chat_id, text="Hai selezionato Professore. Scrivi la tua matricola.")
            else:
                await query.answer("Opzione non valida.")
            # Imposta l'utente come ha premuto il pulsante
            users_pressed_button[user_id] = True
        else:
            await query.answer("Hai già premuto il pulsante.")
    elif [[option_selected == name] for name in prof_names]:
        await context.bot.send_message(chat_id=query.message.chat_id, text="Hai selezionato "+option_selected+". Esegui il comando /consegna per inviare le foto.")

#funzioni risposta ai messaggi
def handle_response_int(text: int,update: Update) -> str:
    #processed: str = text.lower()
    user_id = get_user_id(update)
    number = text
    text = str(text)
    if users_pressed_button.get(user_id, False):
        if (len(text) == 6):
            result = random_with_50_percent_probability()

            if(result):
                users_autentication[user_id] = True
                return 'ID accettato'
            else:
                users_autentication[user_id] = False
                return 'risposta non accettata'
    else:
        users_autentication[user_id] = False
        return 'scegli studente o professore'
    
def handle_response(text: str,update: Update) -> str:
    user_id = get_user_id(update)
    processed: str = text.lower()
    if users_class:
        class_of_user = get_class_of_user(user_id)
    else :
        return "Autenticati prima"

    if class_of_user == "Studente" and users_autentication.get(user_id, True):
        if processed == "termina":
            return "foto salvate" #termina bot
    elif class_of_user == "Professore" and users_autentication.get(user_id, True):
        return "fai gestione altri comandi"
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

    # Connessione al database
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()  # Ottieni il cursore per eseguire le query

    # Creazione della tabella "studenti_e_password" nel database con due campi: ID_studente, password_studente
    tab1 = "create table if not exists studenti_e_password (" \
           "ID_studente integer primary key not null," \
           "password_studente char(3) not null);"
    connection.execute(tab1)  # creazione della tabella vuota

    # Inserimento di dati (righe) nella tabella studenti_e_password
    item1 = [331332, 'abc']  #array con i dati che voglio inserire
    cursor.execute('insert into studenti_e_password values (?,?);', item1) #ID_studente, password_studente
    connection.commit()  #conferma i dati e li scrive nel database

    item2 = [330350, 'def']
    cursor.execute('insert into studenti_e_password values (?,?);', item2)
    connection.commit()  #conferma i dati e li scrive nel database

    # Creazione della tabella "docenti_e_password" nel database con due campi: ID_docente, password_docente
    tab2 = "create table if not exists docenti_e_password (" \
           "ID_docente varchar(30) primary key not null," \
           "password_docente integer not null);"
    connection.execute(tab2)  # creazione della tabella vuota

    # Inserimento di dati (righe) nella tabella docenti_e_password
    html_content = get_html_content(LINK) # Ottieni il contenuto HTML
    names = extract_names_html(html_content) # Analizza il contenuto con Beautiful Soup
    item = []
    for i in range(0,len(names)-1):
        item = [names[i],i]
        cursor.execute('insert into docenti_e_password values (?,?);', item) #ID_docente, password_docente
        connection.commit() #conferma i dati e li scrive nel database
    
    # Creazione della tabella "compiti_consegnati" nel database con quattro campi: code_foto, ID_studente, ID_docente, data_ora
    tab3 = "create table if not exists compiti_consegnati (" \
           "code_foto integer primary key not null," \
           "ID_studente integer not null," \
           "ID_docente varchar(30) not null," \
           "data_e_ora varchar(20) not null);"
    connection.execute(tab3)  # creazione della tabella vuota


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


# Chiusura di connessione e cursore del database
cursor.close()
connection.close()

print("terminato")
