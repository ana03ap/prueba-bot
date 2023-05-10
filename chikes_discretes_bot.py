
'''
BOT DE TELEGRAM

Integrantes: Ana Ardila, Emily Roldán, Esteban Perez. 

---Para estrellas y constelaciones---

• Mostrar un grafico de todas las estrellas.

• Mostrar un grafico con todas las estrellas y, adicionalmente, una constelacion en particular, escogida por el usuario.

• Mostrar todas las estrellas y todas las constelaciones

el error UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail. es común en Matplotlib cuando se intenta crear una figura o gráfico en un hilo que no sea el principal, como un hilo de fondo o un proceso separado. Esta advertencia indica que puede haber problemas con el bucle de eventos de la GUI al usar Matplotlib en un hilo que no sea el principal, lo que puede causar problemas como gráficos no responsivos o congelados.

---Relaciones de recurrencia ---

• Recibir como parametros los casos bases, coeficientes y el g(n),
     devolver la relacion de recurrencia resuelta

'''

import telebot
import threading
from metodos import *
from RRNHCCC import *
from telebot.types import ReplyKeyboardMarkup # para hacer el 
from telebot.types import ForceReply # para citar un mensaje

TOKEN  = '5927693160:AAHJnpw6gYO-ORnLMKfXfeKQgo7uMmZW7x4'
bot = telebot.TeleBot(TOKEN)# instanciar el bot

datos_rrnhccc= {} #inicializar un diccionario global  para guardar los datos ingresados por el usuario a la hora de preguntar grado, coeficientes, casos bases y g(n)

@bot.message_handler(commands=["start"])
def start(message):
    #da la bienvenida al usuario del bot
    bot.reply_to(message, "Hola! Bienvenidx al BOT de lxs chikes discretes!\n\nEn este BOT vas a poder observar un gráfico de todas las estrellas también de ciertas constelaciones!! \nAparte de esto, vas a poder resolver relaciones de recurrencia no lineal con coeficientes constantes!! \nSi quieres ver estrellas escribe el comando /estrellas para más información al respecto. Por otro lado, si quieres resolver relaciones de recurrencia escribe el comando /rrnhccc !! \n\nPara informacion general escribe el comando /help ")


@bot.message_handler(commands=["help"])
def help(message):
    #da la bienvenida al usuario del bot

    #para el formato del texto sería <b>constelaciones<b/> + "\n"
    bot.reply_to(message,"1. Para estrellas y constelaciones escribir comando /estrellas. \n2. Para relaciones de recurrencia escribir /rrnhccc  ", parse_mode="html")

@bot.message_handler(commands=["estrellas"])
def estrellas(message):
    #da la bienvenida al usuario del bot

    #para el formato del texto sería <b>constelaciones<b/> + "\n"
    bot.reply_to(message,"Bienvenido!!!\n ¿quieres observar estrellas o solo constelaciones?!!!\n Para observar solo  estrellas digita el comando /dibujar_estrellas  \nPara observar estrellas y una constelacion digita el comando /constelacion \nPara ver estrellas y todas  las constelaciones digita el comando /constelaciones  ", parse_mode="html")

@bot.message_handler(commands=["dibujar_estrellas"])
def dibujoEstrellas(message):
    plt.clf()
    dibujarEstrellas("constelaciones\stars.txt")
    foto = open("estrellas.png", "rb")
    bot.send_photo(message.chat.id,foto,"Aqui puedes observar TODAS las estrellas ✨🌠")

@bot.message_handler(commands=["constelacion"])
def constelacion(message):
    plt.clf()
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulse una opcion", resize_keyboard=True)
    markup.add("Boyero","Casiopea","Cazo","Cygnet", "Geminis", "Hydra", "OsaMayor", "OsaMenor")
    msg =  bot.send_message(message.chat.id,"Las constelaciones disponible son las siguientes:\n1. Boyero\n2. Casiopea\n3. Cazo\n4. Cygnet\n5. Geminis\n6. Hydra\n7.OsaMayor\n8. OsaMenor \nPor favor ingresa solo el numero", reply_markup=markup)
    # hacer un if para cada caso
    

    bot.register_next_step_handler(msg,constelacion_ingresada)# main es la respuesta que va a lidiar con esa respuesta. 
    
def constelacion_ingresada(message):
    if message.text!="Boyero" and message.text!="Casiopea" and message.text!="Cazo" and message.text!="Cygnet" and message.text!="Geminis" and message.text!="Hydra" and message.text!="OsaMayor" and message.text!="OsaMenor":
         msg = bot.send_message(message.chat.id,"error! ")
         bot.register_next_step_handler(msg,constelacion_ingresada)
    else:# aquí si entro algun dato
        archivo = ""
        archivo = "constelaciones/"+message.text+".txt"
        plt.clf()
        constelacion = message.text
        main(archivo)
        foto2 = open("estrellas_constelacion.png", "rb")
        bot.send_photo(message.chat.id,foto2,"Aqui puedes observar TODAS las estrellas y la constelación que escogiste!")

@bot.message_handler(commands=["constelaciones"])
def constelaciones(message):
    main()
    foto = open("estrellas.png", "rb")
    bot.send_photo(message.chat.id,foto,"Aqui puedes observar TODAS las estrellas y TODAS las constelaciones")




#------------------RELACION DE RECURRENCIA----------------
@bot.message_handler(commands=["rrnhccc"])
def rrnhccc(message):
    bot.reply_to(message,"Holaa, vamos a hacer relaciones de recurrencia. Para realizarla vas a tener que indicarnos los siguientes datos: \n1. El grado de la relacion de recurrencia. \n2. Los coeficientes de la relación de recurrencia. \n3. Los caso base \n4. Ingresar si la funcione es o no homogenea \n5.Por ultimo ingresar el g(n) en la forma Pt(n)R**n. \n\n Ejemplo\nSi tengo la funcion de recurrencia \n  ->>  f(n) = 2f(n-2)+f(n-1), k=2, f(0)=f(1)   , n>1\n El grado sería 2, los coeficientes sería 1,1,2 los casos casos bases serían 1,1 y es homogenea", parse_mode="html")
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "¿Cuál es el grado de la relación de recurrencia? ", reply_markup=markup)
    bot.register_next_step_handler(msg,preguntar_coeficientes)


def preguntar_coeficientes(message):
    if not (message.text.isdigit() and int(message.text) >= 0):
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Error!. Debes indicar un npumero. Recuerda quitar los espacios y escribirlo en formato numérico \n¿Cuál es el grado de la recurrencia")
        bot.register_next_step_handler(msg,preguntar_coeficientes)
    elif "." in message.text:# para verificar que no entren decimales 
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Error!. Debes indicar un numero ENTERO. \n¿Cuál es el grado de la recurrencia")
        bot.register_next_step_handler(msg,preguntar_coeficientes)
    else: # aqui ya se sabe que el dato ingresado es un numero, es positivo y es un entero 
        datos_rrnhccc[message.chat.id] = {}# crear un diccionario vacio pero para cada persona que ingrese. 
        datos_rrnhccc[message.chat.id] ["grado"] = int(message.text) # agregando  el grado al diccionario 

        # --Ahora aquí se va a preguntar los coeficientes. 
        '''
        se va a realizar un for pa eso.
        hacer las validadciones aqui dentro enseguida con algun while
        '''
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Escribe los coeficientes de la relacion de recurrencia separados por comas y sin colocar espacios, tal como se muestra en el ejemplo", reply_markup=markup)
        bot.register_next_step_handler(msg,casos_base)
        
'''
1. esa vuelta no debe tener grado +1 
2. no debe tener espacio
3. no debe ser una vaina como 3/4. sino un int o un float. pasarlo a float pa estar seguros
4. los casos bases son numero de grados
'''
def casos_base(message):# aquí se comprueban los coeficientes y se preguntas los casos base
    coeficientes = []
    grado = datos_rrnhccc[message.chat.id]["grado"]
    comprobando = message.text 
    comprabando_lista =  comprobando.strip().split(',')
    for i in comprabando_lista:
        print(i)
        #markup = ForceReply()
       # msg = bot.send_message(message.chat.id, f"Agregre el coeficiente de f(n {-i} ) -> ", reply_markup=markup)
        #bot.register_next_step_handler(msg,casos_base)

        # verificar que sean numeros
        
        if(es_numero_real(i.replace(" ",""))):
            print(i)
            coeficientes.append(int(i.replace(" ","")))
        else:# no es un numero que metoda todo el string otra vez
            markup = ForceReply()
            msg = bot.send_message(message.chat.id, "Error!. Vuelve a indicar los coeficientes como se te especificó anteriormente")
            bot.register_next_step_handler(msg,casos_base)
            break

        # cuando termine del ciclo
    if len(coeficientes) >grado+1:
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Error!. Vuelve a indicar los coeficientes como se te especificó anteriormente")
        bot.register_next_step_handler(msg,casos_base)
    else:
        print(coeficientes)
        datos_rrnhccc[message.chat.id] ["coeficientes"] = coeficientes
        print("ok!")
        # aqui pedir los casos base
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Escribe los casos base de la relacion de recurrencia separados por comas y sin colocar espacios, tal como se muestra en el ejemplo", reply_markup=markup)
        bot.register_next_step_handler(msg,opcion)

def opcion(message):# recibe caso base y pregunta por si es homogeneo o no
    casos_base = []
    grado = datos_rrnhccc[message.chat.id]["grado"]
    comprobando = message.text 
    comprabando_lista =  comprobando.strip().split(',')
    for i in comprabando_lista:
        print(i)
        if(es_numero_real(i.replace(" ",""))):
            print(i)
            casos_base.append(int(i.replace(" ","")))
        else:# no es un numero que metoda todo el string otra vez
            markup = ForceReply()
            msg = bot.send_message(message.chat.id, "Error!. Vuelve a indicar los casos base como se te especificó anteriormente")
            bot.register_next_step_handler(msg,casos_base)
            break

        # cuando termine del ciclo
    if len(casos_base) >grado:
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Error!. Vuelve a indicar los casos base  como se te especificó anteriormente")
        bot.register_next_step_handler(msg,casos_base)
    else:
        print(casos_base)
        datos_rrnhccc[message.chat.id] ["casos_base"] = casos_base
        print("ok!")
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulse una opción", resize_keyboard=True)
        markup.add("1", "0")
        msg =  bot.send_message(message.chat.id,"Es homogenea? 1. Si 0.No", reply_markup=markup)
    # hacer un if para cada caso
    

    bot.register_next_step_handler(msg,gn)# main es la respuesta que va a lidiar con esa respuesta. 
        # aqui pedir opcion

def gn(message):
    if message.text!="1" and message.text!="0":
         msg = bot.send_message(message.chat.id,"error! ")
         bot.register_next_step_handler(msg,gn)
    else:
        datos_rrnhccc[message.chat.id] ["opcion"] = int(message.text)
        if(opcion==int(0)):
            #aqui es NO homogenea
            datos_rrnhccc[message.chat.id] ["pt"] = "0"
            datos_rrnhccc[message.chat.id] ["R"] = int(message.text)
        else:
            markup = ForceReply()
            msg = bot.send_message(message.chat.id, "Escriba el g(n) de la forma Pt(n)R**n, \nIngrese Pt(n): ", reply_markup=markup)
            bot.register_next_step_handler(msg,pt)
            # ingresar pt y r
            #aquí es homogenea

def pt(message): 
    datos_rrnhccc[message.chat.id] ["pt"] = message.text
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "Escriba el g(n) de la forma Pt(n)R**n, \nIngrese R: ", reply_markup=markup)
    bot.register_next_step_handler(msg,R)
    # no se verifica nada pq el pt varia 

    pass
def R(message):#ULTIMA FUNCION SI NO ES HOMOGENEA. 
    if(es_numero_real(message.text)):
        datos_rrnhccc[message.chat.id] ["R"] = float(message.text)
        grado = datos_rrnhccc[message.chat.id] ["grado"] 
        coeficientes = datos_rrnhccc[message.chat.id] ["coeficientes"]
        casos_base = datos_rrnhccc[message.chat.id] ["casos_base"] 
        opcion = datos_rrnhccc[message.chat.id] ["opcion"]
        pt = datos_rrnhccc[message.chat.id] ["pt"] 
        R = datos_rrnhccc[message.chat.id] ["R"] 
        respuesta = mainRRNHCCC(grado,coeficientes,casos_base,opcion,pt,R)
        msg = bot.send_message(message.chat.id, respuesta)
    else:
        msg = bot.send_message(message.chat.id,"error! ")
        bot.register_next_step_handler(msg,R)


    # aqui verificar opcion 

# text es cualquier texto, imagen u otra cosa que pueda enviar el mensaje 
@bot.message_handler(content_types=["text"])
def mensajes_recibidos(message):
    # esto envia un mensaje pero sin citarlo 
    print(message.text.capitalize()) # if message.text es true  o sea tenga contenido 
    if message.text and message.text.startswith("/"):# entra aquí si es un comando
        bot.send_message(message.chat.id,"comando no disponible, recuerda escribir correctamente los comandos!! ")
    else: 
        bot.send_chat_action(message.chat.id,"typing")
        bot.send_message(message.chat.id, "escoge alguna opcion de los comandos para comenzar!!")
      


    
def recibir_mensajes():
    bot.infinity_polling()

if __name__ == "__main__":

    print("iniciando el bot")

    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Iniciar el bot"),
        telebot.types.BotCommand("/estrellas", "Obtener información acerca de los comandos a usar para dibujar estrellas y constelaciones"),
        telebot.types.BotCommand("/help", "Obtener informacion general"),
        telebot.types.BotCommand("/dibujar_estrellas", "ver todas las estrellas "),
        telebot.types.BotCommand("/constelacion", "ver todas las estrellas y una constelacion"),
        telebot.types.BotCommand("/constelaciones", "Observar todas las estrellas y todas las constelaciones"),
        telebot.types.BotCommand("/rrnhccc", "Realiza relaciones de recurrencia"),

    ])

    hilo_bot = threading.Thread(name = "hilo_bot", target = recibir_mensajes)
    hilo_bot.start()
    print("fin")


