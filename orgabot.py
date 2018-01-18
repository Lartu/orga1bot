# -*- coding: utf-8 -*-
# -*- coding:utf-8 -*-
# Ensamblador de Orga I por Martín del Río (2017)

import telegram
from telegram import *
from telegram.ext import *

import ensambladorORGA1

TOKEN = '' #<- Poner token propio acá

#Creamos nuestra instancia "mi_bot" a partir de ese TOKEN
mi_bot = telegram.Bot(token=TOKEN)  
mi_bot_updater = Updater(mi_bot.token)  
dispatcher = mi_bot_updater.dispatcher


#Definiciones de comandos ---------------------------------------------------
def enviarTexto(bot, update, texto):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	bot.sendMessage(chat_id=update.message.chat_id, text=texto,parse_mode=telegram.ParseMode.HTML);

def enviarAudio(bot, update, audioFile):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_AUDIO)
	audio = open(audioFile, 'rb')
	bot.sendVoice(chat_id=update.message.chat_id, voice=audio)

def start(bot=mi_bot, update=mi_bot_updater):  
	enviarTexto(bot, update, "Encendido.")

def ensamblarCodigoHex(bot, update):
	mensaje = update.message.text.strip()
	mensaje = mensaje[mensaje.find(' ')+1:]
	codigo = mensaje.split("\n")
	enviarTexto(bot, update, "Ensamblado hexadecimal:\n"+ensambladorORGA1.ensamblar(codigo, True))

def ensamblarCodigoBin(bot, update):
	mensaje = update.message.text.strip()
	mensaje = mensaje[mensaje.find(' ')+1:]
	codigo = mensaje.split("\n")
	enviarTexto(bot, update, "Ensamblado binario:\n"+ensambladorORGA1.ensamblar(codigo, False))

def ejecutarCodigo(bot, update):
	enviarTexto(bot, update, "¡Función aún en desarrollo!")

#Comandos -------------------------------------------------------------------
start_handler = CommandHandler('start', start) 
dispatcher.add_handler(start_handler)

hexHand = CommandHandler('hex', ensamblarCodigoHex)
dispatcher.add_handler(hexHand)

binHand = CommandHandler('bin', ensamblarCodigoBin)
dispatcher.add_handler(binHand)

ejHand = CommandHandler('ejecutar', ejecutarCodigo)
dispatcher.add_handler(ejHand)

#echo_handler = MessageHandler(Filters.text, echo)
#dispatcher.add_handler(echo_handler)
#-------------------------------------------------------------------------

mi_bot_updater.start_polling()

while True: #Ejecutamos nuestro programa por siempre  
	pass
