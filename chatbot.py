# pip install python-telegram-bot  v13
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler, CallbackContext, JobQueue
from secret import bot_token
from telegram import KeyboardButton, ReplyKeyboardMarkup, Location
from datetime import datetime
import time

data = {}


def welcome(update, context):
    # messaggio di benvenuto
    msg = f'''Ciao {update.effective_user.first_name}, benvenuto in <b>DT-Chatbot</b>. Ecco l'elenco dei comandi:
    <b>- new_user [username] </b> (ad esempio: new_user philippe) per memorizzare un nuovo username.
    <b>- share_loc [username]</b> (ad esempio share_loc philippe) per trasmettere la posizione al chatbot.
    <b>- get_data [username]</b> (ad esempio get_data philippe) per vedere le posizioni visitate dall'utente.'''
    update.message.reply_text(msg, parse_mode='HTML')


def process_chat(update, context):
    print(context)
    msg = update.message.text.lower()
    # nuovo username
    if msg.startswith('new_user'):
        cmd, username = msg.split(' ')
        if username in data:
            update.message.reply_text("Già presente", parse_mode='HTML')
        else:
            data[username] = []
            context.user_data['username'] = username
            update.message.reply_text(f"Benvenuto {username}", parse_mode='HTML')
    # condivisione della posizione
    elif msg.startswith('share_loc'):
        cmd, username = msg.split(' ')
        if username in data:
            # keyboard = [[KeyboardButton("Condividi posizione", request_location=True)]]
            # reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            # update.message.reply_text(f"Ok {username}, comincia a condividere la posizione", reply_markup=reply_markup)
            update.message.reply_text(f"Ok {username}, comincia a condividere la posizione", parse_mode='HTML')
        else:
            update.message.reply_text(f"Mi dispiace {username}, ma il tuo username non è ancora registrato.",
                                      parse_mode='HTML')
    # visione delle posizioni visitate
    elif msg.startswith('get_data'):
        cmd, username = msg.split(' ')
        if username in data:
            locations = data[username]
            if locations:
                location_text = "\n".join([f"Lat: {loc.latitude}, Lon: {loc.longitude}" for loc in locations])
                update.message.reply_text(f"Posizioni visitate da {username}:\n{location_text}")
            else:
                update.message.reply_text(f"Nessuna posizione registrata per {username}.")
        else:
            update.message.reply_text(f"Mi dispiace {username}, ma il tuo username non è ancora registrato.",
                                      parse_mode='HTML')
    else:
        welcome(update, context)


def process_location(update, context):
    print(context)
    location = update.message.location
    username = context.user_data.get('username', 'Utente Sconosciuto')
    # se il messaggio in ingresso è una 'posizione'
    if location:
        if username in data:
            data[username].append(location)
        else:
            data[username] = [location]
        lat = location.latitude
        lon = location.longitude
        i = 0
        while i < 10:
            update.message.reply_text(
                f"Posizione {i+1} condivisa da {username} - Latitudine: {lat}, Longitudine: {lon}, Data: {datetime.now()}")
            time.sleep(5)
            i += 1
        # print sul terminale
        print(f"Posizione {i+1} condivisa da {username} - Latitudine: {lat}, Longitudine: {lon}, Data: {datetime.now()}")


def main():
    print('bot started')
    upd = Updater(bot_token, use_context=True)
    disp = upd.dispatcher

    disp.add_handler(CommandHandler("start", callback=welcome))
    disp.add_handler(MessageHandler(Filters.regex('^.*$'), callback=process_chat))
    disp.add_handler(MessageHandler(Filters.location, callback=process_location))

    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    main()
