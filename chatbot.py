# pip install python-telegram-bot  v13
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler, \
    CallbackContext
from secret import bot_token
# from telegram import KeyboardButton, ReplyKeyboardMarkup, Location
from datetime import datetime
from requests import get, post

data = {}
base_url = 'https://europe-west1-degori-test2.cloudfunctions.net/save_data'


def welcome(update, context):
    # messaggio di benvenuto
    msg = f'''Ciao {update.effective_user.first_name}, benvenuto in <b>DT-Chatbot</b>. Ecco l'elenco dei comandi:
    <b>- new_user [username] </b> (ad esempio: new_user philippe) per memorizzare un nuovo username.
    <b>- get_data [username]</b> (ad esempio get_data philippe) per vedere le posizioni visitate dall'utente.'''
    update.message.reply_text(msg, parse_mode='HTML')


def process_chat(update, context):
    # print(context)
    msg = update.message.text.lower()

    # comando 1: nuovo username e condivisione della posizione
    if msg.startswith('new_user'):
        cmd, username = msg.split(' ')
        if username in data:
            update.message.reply_text("Mi dispiace, questo username è già presente")
        else:
            data[username] = []
            context.user_data['username'] = username
            # keyboard = [[KeyboardButton("Condividi posizione", request_location=True)]]
            # reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            # update.message.reply_text(f"Ok {username}, comincia a condividere la posizione", reply_markup=reply_markup)
            update.message.reply_text(f"Benvenuto {username}! Comincia a condividere la posizione in tempo reale")

    # comando 2: visione delle posizioni visitate
    elif msg.startswith('get_data'):
        cmd, username = msg.split(' ')
        if username in data:
            locations = data[username]
            if locations:
                location_text = "\n".join([
                                              f"- Lat: {loc[0].latitude}, Lon: {loc[0].longitude}, Data: {loc[1].strftime('%Y-%m-%d %H:%M:%S')}"
                                              for loc in locations])
                update.message.reply_text(f"Posizioni visitate da {username}:\n{location_text}")
            else:
                update.message.reply_text(f"Nessuna posizione registrata per {username}.")
        else:
            update.message.reply_text(f"Mi dispiace {username}, ma il tuo username non è ancora registrato.")
    else:
        welcome(update, context)


def get_location(update, context):
    # print(context)
    message = None
    username = context.user_data.get('username', 'Utente Sconosciuto')
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    if username in data:
        data[username].append((message.location, datetime.now()))
    else:
        data[username] = [(message.location, datetime.now())]
    lat = message.location.latitude
    lon = message.location.longitude
    position = f'POINT({lon} {lat})'
    # print(position)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # r = post(f'{base_url}', json={'username': username, 'lat': lat, 'lon': lon, 'date': timestamp})
    r = post(f'{base_url}', json={'username': username, 'position': position, 'date': timestamp})
    # print sul terminale
    # print(f"Posizione condivisa da {username} - Lat: {lat}, Lon: {lon}, Data: {timestamp}")
    print(r.text)
    # update.message.reply_text(f"{username} - Latitudine: {lat}, Longitudine: {lon}, Data: {datetime.now()}")


def main():
    print('bot started')
    upd = Updater(bot_token, use_context=True)
    disp = upd.dispatcher

    disp.add_handler(CommandHandler("start", callback=welcome))
    disp.add_handler(MessageHandler(Filters.regex('^.*$'), callback=process_chat))
    disp.add_handler(MessageHandler(Filters.location, callback=get_location))

    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    main()
