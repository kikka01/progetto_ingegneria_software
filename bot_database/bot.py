from typing import final
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, CallbackContext
import random
import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from datetime import datetime

print('Starting up bot...')

TOKEN : final = *****
BOT_USERNAME : final = "@consegna_compito_unipg_bot"
LINK : final = "https://www.dmi.unipg.it/dipartimento/rubrica?categoria=DOC&lettera=&pagina="
HEADERS : final = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Dizionario per tenere traccia degli utenti che hanno già premuto il pulsante
users_pressed_button = {}
users_autentication = {} #dizionario che ci dice se l'utente si è autenticato correttamente
users_class = {} #dizionario user_id e "studente"/"professore"
users_name = {} #salva il nome dell'user, quindi o la matricola o il cognome e nome del prof 
prof_names = []
users_foto = {} # salva quando l'user è uno studente il professore scelto 

#funzione per scaricare la pagina web
def get_html_content(LINK):
    response = requests.get(LINK, headers=HEADERS)
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

#funzione per verificare l'autenticazione degli studenti nel database
def autenticazione_studenti(matricola_fornita, password_fornita):
    cursor.execute("select * from studenti_e_password where ID_studente = ?", (matricola_fornita,))
    row = cursor.fetchone()
    if row is not None and password_fornita == row[1]:
        result = True
    else:
        result = False
    return result

#funzione per verificare l'autenticazione dei prof nel database
def autenticazione_prof(nome_prof_fornito, password_fornita):
    cursor.execute("select * from docenti_e_password where ID_docente = ?", (nome_prof_fornito,))
    row = cursor.fetchone()
    if row is not None and password_fornita == str(row[1]):
        result = True
    else:
        result = False
    return result

#estrae foto dal database e le restituisce a lista
def get_photos_from_database(matricola, nome_prof):
    photos = [] #lista composta da due elementi 
    cursor.execute("select * from compiti_consegnati where ID_studente == ? and ID_docente == ?",(matricola,nome_prof))
    for row in cursor.fetchall(): #fetchall = tutte le righe estratte
        #output_string = "({}) Lo studente {} ha consegnato al docente {}, in data {}".format(row[0], row[1], row[2], row[3]) 
        photos.append([row[0],row[3]]) #il primo è un immagine e il secondo è la data e ora 
    return photos

#inserisce foto nel database e gli altri dati
def save_photo_in_database(prof_name, numpydata, matricola):
    current_date = datetime.now()
    formatted_date_time = current_date.strftime("%Y-%m-%d %H:%M:%S") #es. "2023-07-29 15:30:45"
    item = [numpydata, matricola, prof_name, formatted_date_time]  #array con i dati che voglio inserire

    cursor.execute('insert into compiti_consegnati values (?,?,?,?);', item) #code_foto, ID_studente, ID_docente, data_e_ora
    connection.commit()  #conferma i dati e li scrive nel database

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
    users_class[user_id] = "False"
    users_pressed_button[user_id] = False  # Impostiamo l'utente come non ha ancora premuto il pulsante
    users_autentication[user_id] = False
    users_name[user_id] = "None"
    users_foto[user_id] = "False"
    await update.message.reply_text(
        f"Ciao, {user.first_name}!\n"
        "Chi sei ?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Studente", callback_data="Studente")],
            [InlineKeyboardButton("Professore", callback_data="Professore")],
        ]),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = "Ecco una lista dei comandi attualmente disponibili su questo bot:\n\n"\
        "- /help: Visualizza questo messaggio\n"\
        "- /lista_docenti: Visualizza l\'elenco dei docenti e ti permette di scegliere a chi inviare le foto del compito, se sei uno studente\n"\
        "- /consegna: Permette il caricamento delle foto della prova scritta per la consegna al docente selezionato in precedenza\n"\
        "- /lista_consegne: Visualizza gli ID degli studenti che hanno effettuato consegne nel giorno corrente\n"\
        "- /leggi matricola-studente: Visualizza le foto caricate dagli studenti nel giorno corrente\n"\
        "- /delete : Permette al docente di eliminare dal database le consegne fatte a lui\n "
    await update.message.reply_text(help_msg)

#solo per studenti
async def lista_docenti_command(update: Update, context: CallbackContext): #context: ContextTypes.DEFAULT_TYPE
    user_id = get_user_id(update)
    
    if users_class:
        class_of_user = users_class[user_id]
    else :
        users_class[user_id] = "False"
        class_of_user = "False"
        await update.message.reply_text("Non hai il permeso di eseguire questo comando")

    if class_of_user == "Studente" and users_autentication.get(user_id, True): # cioè è uno studente e si è autenticato
        html_content = get_html_content(LINK)# Ottieni il contenuto HTML
        names = extract_names_html(html_content)# Analizza il contenuto con Beautiful Soup

        keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in names]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Seleziona un professore:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Non hai il permeso di eseguire questo comando")

async def consegna_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #solo per studenti
    user_id = get_user_id(update)
    if users_class:
        class_of_user = users_class[user_id]
    else :
        await update.message.reply_text('Autenticati prima')
    if class_of_user == "Studente":
        nome_prof = users_foto[user_id]
        if nome_prof != "False":
            users_foto[user_id] = nome_prof + " True"
        await update.message.reply_text('Invia le foto e scrivi \"fine\" per salvarle nel database.')
    else:
        await update.message.reply_text('Non puoi eseguire questo comando se sei un Professore')

async def lista_consegne_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #solo per prof
    user_id = get_user_id(update)
    if users_class:
        class_of_user = users_class[user_id]
    else :
        await update.message.reply_text('Autenticati prima')
    if class_of_user == "Professore":
        nome_prof = users_name[user_id]
        cursor.execute("select * from compiti_consegnati where ID_docente == ?",(nome_prof,))
        rows = cursor.fetchall()
        if(rows):
            for row in rows:
                output_string = " Lo studente {} ha consegnato al docente {}, in data {}".format( row[1], row[2], row[3])
                await update.message.reply_text(output_string)
            await update.message.reply_text("Scrivi /leggi seguito dal numero della matricola per vedere le immagini dello studente relativo.")
        else:
            await update.message.reply_text("Non hai nessun compito da scaricare. Premi /start per ritornare alla pagina iniziale.")
    else:
        await update.message.reply_text('Non puoi eseguire questo comando se sei uno Studente')
    
async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #solo per prof
    user_id = get_user_id(update)
    if users_class:
        class_of_user = users_class[user_id]
    else :
        await update.message.reply_text('Autenticati prima')
    if class_of_user == "Professore":
        nome_prof = users_name[user_id]
        cursor.execute("delete from compiti_consegnati where ID_docente ==  ?;", (nome_prof,))
        connection.commit()
        await update.message.reply_text('Foto eliminate con successo.')
    else:
        await update.message.reply_text('Non puoi eseguire questo comando se sei uno Studente')
    

async def leggi_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #solo per prof
    user_id = get_user_id(update)
    if users_class:
        class_of_user = users_class[user_id]
    else :
        await update.message.reply_text('Autenticati prima')
    if class_of_user == "Professore":
        args = context.args
        if args:
            matricola_st = args[0]
            nome_prof = users_name[user_id]
            foto_date_database = []
            foto_date_database = get_photos_from_database(matricola_st,nome_prof)
            if foto_date_database:
                await update.message.reply_text("Hai selezionato "+ matricola_st)
                for foto,data in foto_date_database:
                        await update.message.reply_text("Consegnato in data = "+ data)
                        await update.message.reply_photo(photo=foto)            
            await update.message.reply_text("Scegli tra: \n/start per ritornare alla pagina iniziale. \n/delete per eliminare tutte le consegne che hai ricevuto. \n/leggi seguito dal numero della matricola dello studente del quale si vogliono scaricare le foto.")
        else:
            await update.message.reply_text("Inserisci il numero della matricola corrispondente allo studente del quale si vogliono scaricare le immagini, dopo il comando")
        
    else:
        await update.message.reply_text('Non puoi eseguire questo comando se sei uno Studente')


#Funzioni

# Funzione di gestione del callback dei pulsanti inline
async def handle_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = get_user_id(update)
    option_selected = query.data
    if option_selected == "Studente" or option_selected == "Professore":
        if not users_pressed_button.get(user_id, False):
            users_class[user_id] = option_selected

            if option_selected == "Studente":
                await context.bot.send_message(chat_id=query.message.chat_id, text="Hai selezionato Studente. Scrivi la tua matricola e la password.")
            elif option_selected == "Professore":
                await context.bot.send_message(chat_id=query.message.chat_id, text="Hai selezionato Professore. Scrivi il tuo cognome, nome e password.")
            else:
                await query.answer("Opzione non valida.")
            users_pressed_button[user_id] = True
        else:
            await query.answer("Hai già premuto il pulsante. Per modificare la scelta riavvia il bot con /start")
    elif [[option_selected == name] for name in prof_names]:
        users_foto[user_id] = str(option_selected)
        await context.bot.send_message(chat_id=query.message.chat_id, text="Hai selezionato "+option_selected+". Esegui il comando /consegna per inviare le foto.")

def handle_response(text: str,update: Update) -> str:
    user_id = get_user_id(update)
    processed: str = text.lower()
    if users_class:
        class_of_user =users_class[user_id]
    else :
        users_class[user_id] = "False"
        class_of_user = "False"
        return "Scegli studente o professore"
    strings = text.split()
    if class_of_user == "Studente" and not users_autentication.get(user_id, True):
        if len(strings) == 2:
            result = autenticazione_studenti(strings[0], strings[1])
            if result:
                users_name[user_id] = strings[0]
                users_autentication[user_id] = True
                return "Autenticazione eseguita correttamente, per vedere la lista dei professori usa /lista_docenti"
            else:
                users_autentication[user_id] = False
                return "Autenticazione rifiutata"
        else:
            return 'testo non accettato'
    if class_of_user == "Professore" and not users_autentication.get(user_id, True):
        if len(strings) > 2:
            password = strings[len(strings)-1]
            nome = ' '.join( x for x in strings if x not in password)
            result = autenticazione_prof(nome, password)
            if result:
                users_name[user_id] = nome
                users_autentication[user_id] = True
                return "Autenticazione eseguita correttamente, usa il comando /lista_consegne per vedere la lista degli studenti che hanno consegnato"
            else:
                users_autentication[user_id] = False
                return "Autenticazione rifiutata"
        else:
            return 'testo non accettato'
    if class_of_user == "Studente" and users_autentication.get(user_id, True):
        if processed == "fine":
            users_foto[user_id] = "False"
            return "foto salvate premi /start per ritornare all'inizio oppure seleziona un professore a cui inviare le foto" #termina bot
    elif class_of_user == "Professore" and users_autentication.get(user_id, True):
        return "input non accettato"
    return 'sei già autenticato'

async def handle_image(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    
    
    if users_class:
        class_of_user =users_class[user_id]
    else :
        users_class[user_id] = "False"
        class_of_user = "False"
        await update.message.reply_text("Non hai il permeso di eseguire questo comando")
    
    nome_bool = users_foto[user_id]
    strings = nome_bool.split()
    bool_str = strings[len(strings)-1]
    if class_of_user == "Studente" and users_autentication.get(user_id, True) and bool_str == "True": # cioè è uno studente e si è autenticato e ha inserito il comando
        prof_name = ' '.join( x for x in strings if x not in bool_str)
        matricola = users_name[user_id]
        img = update.message.photo[-1].file_id #await
        save_photo_in_database(prof_name, img ,matricola) 

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # informazioni del tipo di messaggio ricevuto
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # utile per debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if type(text)==str:
        response: str = handle_response(text,update)
    else:
        handle_image(update, CallbackContext)
        response: str = "img"

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
    script_directory = os.path.dirname(os.path.abspath(__file__)) #prende il path assoluto della cartella corrente
    database_path = os.path.join(script_directory, 'database.db') #ci aggiungo il nome del database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()  # Ottieni il cursore per eseguire le query

    # Creazione della tabella "studenti_e_password" nel database con due campi: ID_studente, password_studente
    tab1 = "create table if not exists studenti_e_password (" \
           "ID_studente integer primary key not null," \
           "password_studente char(3) not null);"
    connection.execute(tab1)  # creazione della tabella vuota

    # Inserimento di dati (righe) nella tabella studenti_e_password
    item1 = [331332, 'abc']  #array con i dati che voglio inserire
    cursor.execute('insert or ignore into studenti_e_password values (?,?);', item1) #ID_studente, password_studente
    connection.commit()  #conferma i dati e li scrive nel database

    item2 = [330350, 'def']
    cursor.execute('insert or ignore into studenti_e_password values (?,?);', item2)
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
        cursor.execute('insert or ignore into docenti_e_password values (?,?);', item) #ID_docente = nome e cognome, password_docente
        connection.commit() #conferma i dati e li scrive nel database
    
    # Creazione della tabella "compiti_consegnati" nel database con quattro campi: code_foto, ID_studente, ID_docente, data_ora
    tab3 = "create table if not exists compiti_consegnati (" \
           "code_foto text primary key not null," \
           "ID_studente integer not null," \
           "ID_docente varchar(30) not null," \
           "data_e_ora varchar(20) not null);"
    connection.execute(tab3)  # creazione della tabella vuota

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    app.add_handler(CommandHandler('lista_docenti', lista_docenti_command))
    app.add_handler(CommandHandler('consegna', consegna_command))
    app.add_handler(CommandHandler('lista_consegne', lista_consegne_command))
    app.add_handler(CommandHandler('leggi', leggi_command))
    app.add_handler(CommandHandler('delete', delete_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT , handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')

    # Run the bot
    app.run_polling(poll_interval=3)


# Chiusura di connessione e cursore del database
cursor.close()
connection.close()

print("terminato")
