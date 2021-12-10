import telebot
import datetime
import json
from string import punctuation
import random
import pickle
from tensorflow.keras.models import load_model

api = ''
bot = telebot.TeleBot(api)

with open("intents.json") as data_file:
    data = json.load(data_file)
model = load_model('bot_model.tf')
le_filename = open("label_encoder.pickle", "rb")
le = pickle.load(le_filename)
le_filename.close()

def log(message,perintah):
    tanggal = datetime.datetime.now()
    tanggal = tanggal.strftime('%d-%B-%Y')
    nama_awal = message.chat.first_name
    nama_akhir =  message.chat.last_name
    id_user = message.chat.id
    text_log = '{}, {}, {} {}, {} \n'.format(tanggal,id_user, nama_awal, nama_akhir, perintah)
    print(text_log)
    log_bot = open('log_bot.txt','a')
    log_bot.write(text_log)
    log_bot.close()

def preprocess_string(string):
    string = string.lower()
    exclude = set(punctuation)
    string = ''.join(ch for ch in string if ch not in exclude)
    return string

@bot.message_handler(commands=['start'])
def action_start(message):
    log(message,'start')
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    bot.reply_to(message,'Halo {} {}, Halo Selamat datang di Resto Bot ID, silahkan gunakan perintah /help untuk mengetahui cara kerja bot ini'
    .format(first_name,last_name))

@bot.message_handler(commands=['help'])
def action_help(message):
    log(message,'help')
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    bot.reply_to(message,'''
Hi {} {}, Cara menggunakan chatbot ini mudah kok, tinggal ketik aja, misalnya:
    - Selamat pagi
    - Permisi
    - Mau liat menu dong
    - Disini sedia apa aja?
    - Makanannya enak
    - Terima kasih
Silahkan berkreasi sesuka kamu :)    
    '''.format(first_name, last_name))

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    inp = preprocess_string(message.text)
    prob = model.predict([inp])
    results = le.classes_[prob.argmax()]
    if prob.max() < 0.1:
        bot.reply_to(message, "Maaf kak, aku ga ngerti")
    else:
        for tg in data['intents']:
            if tg['tag'] == results:
                responses = tg['responses']
        bot.reply_to(message, random.choice(responses))

print('Bot start running....')
bot.polling()