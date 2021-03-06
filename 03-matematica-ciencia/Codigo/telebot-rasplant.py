import time
import telebot
import threading
from time import sleep 
# from gpiozero import LightSensor, LED, Motor, DistanceSensor
from signal import pause
import datetime as dt

# Telegram bot configurations



notification_enable = True

# Rasberry PI configurations
# light = LED(17)
# motor = Motor(forward=4,backward=14)
# light_sensor = LightSensor(18)
# dist_sensor = DistanceSensor(23, 24, max_distance=1, threshold_distance=0.2)

#TODO:- Add "humedad" and temperature sensor
#           Turns the motor if its dry

###############################################################################
##########                 Bot Command Responder                     ##########
###############################################################################

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'Bienvenido al invernadero Capa de Ozono 7u7')

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    commandsList = '''
    /start    \t Inicia la comunicacion con el bot.
    /help     \t Desplega la lista de los comandos disponibles.
    /lights   \t Enciende las luces del invernadero.
    /nolights \t Apaga las luces del invernadero.
    /water    \t Enciende el motor para regar el invernadero.
    /nowater  \t Apaga el motor para regar el invernadero.
    /notifications     \t Encender notificationes.
    /notificationsoff  \t Apagar notificationes.
    '''
    bot.reply_to(message, commandsList)

@bot.message_handler(commands=['lights']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'Encendiendo luces')
    # light.on()

@bot.message_handler(commands=['nolights']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'Apagando luces')
    # light.off()

@bot.message_handler(commands=['water']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'Encendiendo motor de la bomba de agua')
    # motor.forward()

@bot.message_handler(commands=['nowater']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'Apagando motor de la bomba de agua')
    # motor.stop()

@bot.message_handler(commands=['notifications']) # help message handler
def send_welcome(message):
    global notification_enable
    notification_enable = True;
    bot.reply_to(message, 'Encendiendo notificaciones')

@bot.message_handler(commands=['notificationsoff']) # help message handler
def send_welcome(message):
    global notification_enable
    notification_enable = False;
    bot.reply_to(message, 'Apagando notificaciones')

# This is the main function to start responder bot
def bot_responder_init():
    while True:
        try:
            bot.polling(none_stop=True)
            # ConnectionError and ReadTimeout because of possible timout of the
            # requests library
            # maybe there are others, therefore Exception
        except Exception:
            time.sleep(15)

###############################################################################
##########                  Bot Command Informer                     ##########
###############################################################################

def action_on_dark():
    # light.on()
    if notification_enable :
        bot.send_message(user_chat_id,'ALERTA: Se hizo de noche y prendimos las luces')

def action_on_light():
    # light.off()
    if notification_enable :
        bot.send_message(user_chat_id,'ALERTA: Apagamos las luces')

def actions_on_proximity():
    # light.on()
    if notification_enable :
        bot.send_message(user_chat_id,'ALERTA: Es posible que alguien o algo se \
            acerco a tu invernadero, te recomendamos revisar.')

# def actions_when_out_of_range():
    # light.of()
    # Its posible to add more things however this is enough

def send_report_each_period(elapse):
    global notification_enable

    t = dt.datetime.now()
    while True:
        delta = dt.datetime.now()-t
        if delta.seconds >= elapse:
            if notification_enable :
                print("Han pasado {} seconds".format(elapse))
                bot.send_message(user_chat_id,'Han pasado {} segs'.format(elapse))
                # Update 't' variable to new time
                t = dt.datetime.now()


# def informer_main():
    # light_sensor.when_dark = action_on_dark
    # light_sensor.when_light = action_on_light
    # dist_sensor.when_in_range = actions_on_proximity
    # # dist_sensor.when_out_of_range = actions_when_out_of_range

    # pause()


###############################################################################
##########                          MAIN                             ##########
###############################################################################

# t1 = threading.Thread(target=informer_main)
t2 = threading.Thread(target=bot.polling)
t3 = threading.Thread(target=send_report_each_period,args=(20,))

# t1.start()
t2.start()
t3.start()

