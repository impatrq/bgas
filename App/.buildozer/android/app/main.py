from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from datetime import datetime, timedelta
from kivy.clock import Clock
import csv
from functools import partial
import textwrap
import requests

#importo los datos de la app e imagenes de los widgets
datos = f"./datos.csv"
logo = f"./images/logo.png"
cuadrao = "./images/cuadrao.png"
emergenV = "./images/bloque_emergente_verde.png"
emergenA = "./images/bloque_emergente_amarillo.png"
emergenR = "./images/bloque_emergente_rojo.png"
emergenL = "./images/bloque_emergente_verde_largo.png"
interrogacion = "./images/signo_interrogacion.png"
interrogacion_o = "./images/signo_interrogacion_oscuro.png"
tacho = "./images/tacho.png"
lapizF = "./images/lapiz.png"
tacho_o = "./images/tacho_oscuro"
lapizF_o = "./images/lapiz_oscuro.png"
newbox = "./images/new.png"
newbox_o = "./images/new_oscuro.png"
lizo = "./images/fondo_lizo.png"
lizo_o = "./images/fondo_lizo_oscuro.png"
#declaro una lista que contenera el tamano de X e Y de la pantalla
Wsize = []
#variable que define si una ventana esta abierta o no
cant = 0
#variable que define si la app cumplio sus funciones de apertura o no
inicio = 0

#tamano X e Y de la pantalla (para android)
ancho =  Window.width
alto = Window.height
Wsize.append(ancho)
Wsize.append(alto)

#tamano prefijado para pantallas de computadoras (para pruebas)
#Wsize = (360, 720)
Window.size = Wsize

#inicia la construccion de la app
class Bgas(MDApp):
    #lista que contendra las propiedades de los widgets
    widgets = ListProperty([])
    def build(self):
        global inicio, Wsize
        #la dispocision va a ser "libre"
        layout = FloatLayout()
        LabelBase.register(name='letra', fn_regular='./static/PublicSans-Regular.ttf')

        with layout.canvas.before:  #fondo de la app
            Color(rgb=get_color_from_hex('#00686C'))
            Rectangle(pos_hint=(0, 0), size=(Wsize[0], Wsize[1]))
        
        user = TextInput(multiline=False, size_hint=(0, 0), pos_hint={'center_x':2, 'center_y':2})
        widgetlogo_fondo = Image(source = logo, pos_hint = {'center_x':0.5, 'center_y':0.4}, size_hint = (1.2, 1.2), opacity = 0.15)
        with layout.canvas.before:
            layout.add_widget(widgetlogo_fondo)
        
        #empiezo a declarar las caracteristicas de los widgets
        newbox_button = Button(
            size_hint=(0.4, 0.21),
            pos_hint={'center_x':0.2, 'center_y':0.82},
            background_normal = newbox,
            background_down = newbox_o
        )
        interrB = Button(
            size_hint=(0.4, 0.21),
            pos_hint={'center_x':0.8, 'center_y':0.82},
            background_normal = interrogacion,
            background_down = interrogacion_o
            )
        inicio1 = Label(
            text = 'Añadir\nGenerador',
            pos_hint = {'center_x':0.2, 'center_y':0.95},
            font_name = 'letra',
            font_size = Wsize[1]/35,
            halign = 'center'
            )
        inicio2 = Label(
            text = 'Ayuda',
            pos_hint = {'center_x':0.8, 'center_y':0.95},
            font_name = 'letra',
            font_size = Wsize[1]/30,
            halign = 'center'
            )
        watfondo = Image(source = emergenL,
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            size_hint = (0.9, 0.9)
            )
        watext = textwrap.fill(f'''
Felicitaciones por la compra de su unidad B-Gas!

Esta aplicacion permite monitorear los tiempos de utilidad y vencimientos de los generadores que pueda tener. Ademas, con nuestro dispositivo remoto conectado puede ver en tiempo real los parametros de sus generadores.

Ademas de los botones "Añadir generador" y "Ayuda", tocar en el nombre de un generador abre una ventana con informacion sobre el mismo, el lapiz al lado de un generador permite cambiarle el nombre, y el tacho de basura es para borrarlo.

En caso de un error que no permita abrir la aplicacion, o la corrupcion de los datos de la app en general, borre los datos de la app o reinstalela a su estado por defecto
''', width = 40, replace_whitespace=False)
        wat = Label(
            text = watext,
            font_name = "letra",
            pos_hint = {'center_x': 0.5, 'center_y':0.6},
            font_size = Wsize[1]/45
        )
        newbox_button.bind(on_press=self.add_box)

        watfondo = Image(source = emergenL, pos_hint = {'center_x': 0.5, 'center_y': 0.5}, size_hint = (1, 1))

        with layout.canvas.before:
            Color(rgba=get_color_from_hex('#000000'))
            caja = Rectangle(
                pos=(Wsize[0]/40, Wsize[1]/40),
                size=((Wsize[0]/40)*38, Wsize[1]/1.45)
            )
        #agrego al display los widgets fundamentales para el funcionamiento de la app
        layout.add_widget(user)
        layout.add_widget(newbox_button)
        layout.add_widget(interrB)
        layout.add_widget(inicio1)
        layout.add_widget(inicio2)
        
        #protocolo para primer ciclo de la app
        if inicio == 0:
            #pido el tiempo actual
            tiempo_actual = datetime.now()
            #extraigo de data los parametros de generadores anteriores
            with open (datos, mode='r') as file:
                read = csv.reader(file)
                data = list(read)
                #declaro widgets exclusivos de los generadores
                backwat = Button(
                    text='Volver',
                    size_hint=(0.2, 0.067),
                    pos_hint={'center_x': 0.25, 'y':0.1},
                    font_size = Wsize[1]/40,
                    background_normal = lizo,
                    background_down = lizo_o,
                    font_name = "letra"
                )
                tutorialf = partial(self.tutorial, arg1 = watfondo, arg2 = wat, arg3 = backwat)
                backwatf = partial(self.watbye, arg1 = watfondo, arg2 = wat, arg3 = backwat)
                interrB.bind(on_press = tutorialf)
                backwat.bind(on_press = backwatf)
                
                #leo linea por linea los datos
                for line in data:
                    name = line[1]
                    start = line[2]
                    tiempo_faltante = Label(
                        text='Cargando...',
                        size_hint=(None, None),
                        pos_hint={'x': 0.4, 'y': 45},
                        font_size = Wsize[1]/40,
                        font_name = "letra"
                    )
                    spawn = Button(
                        text=f'{name}',
                        size_hint=(0.93, 0.069),
                        pos_hint={'center_x': 0.5, 'y': 0.63-(data.index(line)*0.0833)},
                        font_size = Wsize[1]/40,
                        background_normal = lizo,
                        background_down = lizo_o,
                        font_name = "letra"
                    )
                    salir = Button(
                        text='Volver',
                        size_hint=(0.2, 0.067),
                        pos_hint={'center_x': 0.2, 'y':0.1},
                        font_size = Wsize[1]/40,
                        background_normal = lizo,
                        background_down = lizo_o,
                        font_name = "letra"
                    )
                    borrar = Button(
                        size_hint=(0.21, 0.1),
                        pos_hint={'center_x': 0.85, 'y': 0.66-(len(self.widgets)*0.0833)},
                        background_normal = tacho,
                        background_down = tacho_o
                    )
                    lapiz = Button(
                        size_hint=(0.21, 0.1),
                        pos_hint={'center_x': 0.15, 'y': 0.66-(len(self.widgets)*0.0833)},
                        background_normal = lapizF,
                        background_down = lapizF_o
                    )
                    seguro = Label(
                        text = f"""
Estás seguro que quieres borrar
{line[1]}?
                        """,
                        font_size = Wsize[1]/40,
                        font_name = "letra"
                    )
                    si = Button(
                        text = "Borrar",
                        background_normal = lizo,
                        background_down = lizo_o,
                        size_hint=(0.22, 0.07),
                        pos_hint={'center_x': 0.25, 'center_y': 0.15},
                        font_size = Wsize[1]/40,
                        font_name = "letra"
                    )
                    no = Button(
                        text = "No",
                        background_normal = lizo,
                        background_down = lizo_o,
                        size_hint=(0.22, 0.07),
                        pos_hint={'center_x': 0.75, 'center_y': 0.15},
                        font_size = Wsize[1]/40,
                        font_name = "letra"
                    )
                    seguridad = [seguro, si, no]
                    spawnf = partial(self.info, arg1=line[0])
                    salirf = partial(self.salida, arg1=line[0])
                    borrarf = partial(self.remove_box, arg1=line[0])
                    editarf = partial(self.editar, arg1=line[0])
                    confirmf = partial(self.confirm_remove, arg1=line[0])
                    notf = partial(self.not_remove, arg1=line[0])
                    spawn.bind(on_press = spawnf)
                    salir.bind(on_press = salirf)
                    borrar.bind(on_press = borrarf)
                    lapiz.bind(on_press = editarf)
                    si.bind(on_press = confirmf)
                    no.bind(on_press = notf)
                    emergentev = Image(
                        source = emergenV,
                        pos_hint = {'center_x':0.5, 'center_y':0.4},
                        size_hint = (0.95, 0.95)
                        )
                    emergentea = Image(
                        source = emergenA,
                        pos_hint = {'center_x':0.5, 'center_y':0.4},
                        size_hint = (0.95, 0.95)
                        )
                    emergenter = Image(
                        source = emergenR,
                        pos_hint = {'center_x':0.5, 'center_y':0.4},
                        size_hint = (0.95, 0.95)
                        )
                    time = datetime.strptime(line[0], '%Y/%m/%d %H:%M:%S')
                    emergente = [emergentev, emergentea, emergenter]
                    parameters = [0, 0, 0] #pressure, temperature, gas%
                    
                    #intento sacar de nuestra base de datos en la red local los datos de cada generador posible
                    try:
                        info = requests.get('http://apiweb-ivancenyko.vercel.app/bgas').json()
                        nameL = name.lower()
                        if nameL in info:
                            pressure = info[nameL][0]
                            temperature = info[nameL][1]
                            gas = info[nameL][2]
                            cosas = [pressure, temperature, gas]
                            for i in range(len(parameters)):
                                parameters[i-1] = cosas[i-1]
                    except:
                        pass
                    
                    #genero una lista que funciona como conjunto de los parametros de c/generador
                    ingreso = [time, tiempo_faltante, spawn, salir, borrar, emergente, lapiz, name, seguridad, start, parameters]
                    self.widgets.append(ingreso)

                    #agrego los objetos del generador en el display
                    layout.add_widget(spawn)
                    layout.add_widget(borrar)
                    layout.add_widget(lapiz)
                    Clock.schedule_interval(lambda dt: self.update_labels(), 0.001)
                    
            inicio +=1

        return layout
    
    #en caso que se quiera agregar un generador
    def add_box(self, instance):
        global cant, inicio
        tiempo_actual = datetime.now()

        #si hay otra ventana abierta, o si se alcanzo el limite de generadores, no pasa nada (a solucionar)
        with open (datos, mode='r') as file:
            read = csv.reader(file)
            data = list(read)
            largo = len(data)
        if len(self.widgets) > 7:
            pass
        elif cant == 0:

            #vuelvo a declarar muchos widgets porque varian sus parametros segun el origen
            tiempo_faltante = Label(
                text='Cargando...',
                size_hint=(None, None),
                pos_hint={'center_x': 0.5, 'center_y': 0.45},
                font_size = Wsize[1]/40,
                font_name = "letra"
                )
            spawn = Button(
                text=f'',
                size_hint=(0.93, 0.069),
                pos_hint={'center_x': 0.5, 'center_y': 0.66-(len(self.widgets)*0.0833)},
                font_size = Wsize[1]/40,
                background_normal = lizo,
                background_down = lizo_o,
                font_name = "letra"
                )
            salir = Button(
                text='Volver',
                size_hint=(0.2, 0.067),
                pos_hint={'center_x': 0.2, 'y':0.1},
                font_size = Wsize[1]/40,
                background_normal = lizo,
                background_down = lizo_o,
                font_name = "letra"
                )
            borrar = Button(
                size_hint=(0.21, 0.1),
                pos_hint={'center_x': 0.85, 'center_y': 0.66-(len(self.widgets)*0.0833)},
                background_normal = tacho,
                background_down = tacho_o
            )
            lapiz = Button(
                size_hint=(0.21, 0.1),
                pos_hint={'center_x': 0.15, 'center_y': 0.66-(len(self.widgets)*0.0833)},
                background_normal = lapizF,
                background_down = lapizF_o
            )
            seguro = Label(
                font_name = "letra",
                font_size = Wsize[1]/40
            )
            si = Button(
                text = "Borrar",
                background_normal = lizo,
                background_down = lizo_o,
                size_hint=(0.22, 0.07),
                pos_hint={'center_x': 0.25, 'center_y': 0.15},
                font_size = Wsize[1]/40,
                font_name = "letra"
            )
            no = Button(
                text = "No",
                background_normal = lizo,
                background_down = lizo_o,
                size_hint=(0.22, 0.07),
                pos_hint={'center_x': 0.75, 'center_y': 0.15},
                font_size = Wsize[1]/40,
                font_name = "letra"
            )
            seguridad = [seguro, si, no]
            emergentev = Image(source = emergenV, pos_hint = {'center_x':0.5, 'center_y':0.4}, size_hint = (0.95, 0.95))
            emergentea = Image(source = emergenA, pos_hint = {'center_x':0.5, 'center_y':0.4}, size_hint = (0.95, 0.95))
            emergenter = Image(source = emergenR, pos_hint = {'center_x':0.5, 'center_y':0.4}, size_hint = (0.95, 0.95))
            self.nombre_c = TextInput(
                hint_text='Ingresar nombre:',
                background_normal = lizo,
                background_active = lizo_o,
                multiline=False,
                pos_hint={'center_x':0.5, 'center_y':0.60},
                size_hint = (0.7, 0.08),
                font_size = Wsize[1]/40,
                font_name = "letra",
                hint_text_color = (0,0,0,1)
                )
            self.nombre_c.bind(on_focus=self.clear_content)
            self.start_c = TextInput(
                hint_text='Ingresar dias desde el inicio:',
                background_normal = lizo,
                background_active = lizo_o,
                multiline=False,
                pos_hint={'center_x':0.5, 'center_y':0.50},
                size_hint = (0.7, 0.08),
                font_size = Wsize[1]/40,
                font_name = "letra",
                hint_text_color = (0,0,0,1)
                )
            self.start_c.bind(on_focus=self.clear_content)
            self.widf(arg1 = [emergentev, self.nombre_c, self.start_c], arg2 = 'add')
            save = Button(
                text="Guardar generador",
                size_hint=(0.55, 0.067),
                pos_hint={'center_x': 0.5, 'center_y':0.15},
                font_size = Wsize[1]/40,
                background_normal = lizo,
                background_down = lizo_o,
                font_name = "letra"
                )
            
            #el name queda como "None" por el momento dado a que falta confirmar los datos externos del generador
            name = None
            start = 0
            emergente = [emergentev, emergentea, emergenter]
            parameters = [0, 0, 0]
            objeto = [tiempo_actual, tiempo_faltante, spawn, salir, borrar, emergente, lapiz, name, seguridad, start, parameters]
            self.widgets.append(objeto)
            seguirf = partial(self.confirmadd, arg1=largo)
            save.bind(on_press=seguirf)
            self.root.add_widget(save)
            self.user_input = None
            self.user_input2 = None
            cant +=1

    #una vez que el usuario ingresa los parametros externos del generador
    def confirmadd(self, instance, arg1):
            newname = ''
            global cant
            n = 0
            listname = list(self.nombre_c.text)
            #reviso que el nombre dado no supere un largo determinado, para evitar problemas visuales
            if len(listname) > 14:
                for letra in listname:
                    n +=1
                    newname = newname + letra
                    if n == 14:
                        break
                self.user_input = newname
            else:
                self.user_input = self.nombre_c.text
            self.user_input2 = self.start_c.text
            tiempo_actual = datetime.now()
            widget_time = self.widgets[arg1]
            name = self.user_input
            start = self.user_input2
            #para el tiempo que tarde de ingresar los parametros, un valor fijo de reemplazo
            try:
                widget_time[9] = int(start)
            except:
                widget_time[9] = 0
            if name == "" or name == "Ingresar nombre:":
                ahora = datetime.now()
                ahoraa = ahora.strftime('%Y/%m/%d')
                name = f"Generador {ahoraa}"
            
            parameters = [0, 0, 0] #pressure, temperature, gas%
            try:
                info = requests.get('http://apiweb-ivancenyko.vercel.app/bgas').json()
                nameL = name.lower()
                if nameL in info:
                    pressure = info[nameL][0]
                    temperature = info[nameL][1]
                    gas = info[nameL][2]
                    cosas = [pressure, temperature, gas]
                    for i in range(len(parameters)):
                        parameters[i-1] = cosas[i-1]
                        widget_time[10] = parameters
            except:
                        pass
            widget_time[7] = name
            tiempostr = tiempo_actual.strftime('%Y/%m/%d %H:%M:%S')
            spawnf = partial(self.info, arg1=tiempostr)
            salirf = partial(self.salida, arg1=tiempostr)
            borrarf = partial(self.remove_box, arg1=tiempostr)
            editarf = partial(self.editar, arg1=tiempostr)
            confirmf = partial(self.confirm_remove, arg1=tiempostr)
            notf = partial(self.not_remove, arg1=tiempostr)

            widget_time[8][0].text = f"""
Estás seguro que quieres borrar
{name}?
            """
            widget_time[2].bind(on_press=spawnf)
            widget_time[3].bind(on_press=salirf)
            widget_time[4].bind(on_press=borrarf)
            widget_time[6].bind(on_press=editarf)
            widget_time[8][1].bind(on_press=confirmf)
            widget_time[8][2].bind(on_press=notf)

            with open (datos, mode='a', newline='') as file:
                writer = csv.writer(file)
                intime = tiempo_actual.strftime('%Y/%m/%d %H:%M:%S')
                try:
                    i = int(start)
                except:
                    start = 0
                ingreso = (intime, name, start)
                writer.writerow(ingreso)

            self.widf(arg1 = [widget_time[2], widget_time[4], widget_time[6]], arg2 = 'add')
            Clock.schedule_interval(lambda dt: self.update_labels(), 1)
            instance.size_hint = (0.3, 0.2)
            instance.pos_hint = {'center_x':0.15, 'center_y':0.9}
            with open (datos, mode='r') as file:
                read = csv.reader(file)
                data = list(read)
                for line in data:
                    if tiempostr in line:
                        indice = (data.index(line))
                        widget_time = self.widgets[indice]
                ventana = widget_time[5]
                self.widf(arg1 = [self.nombre_c, self.start_c, ventana[0], instance], arg2 = 'rem')
            widget_time[2].text = f'{widget_time[7]}'
            cant -=1

    #actualizacion a traves del tiempo de los parametros de los generadores
    def update_labels(self):
        global tiempo_diasU, tiempo_diasV
        #para cada generador
        for widget_time in self.widgets:
            #calculo del tiempo para maxima eficiencia y vencimiento del generador
            tiempo_actual = datetime.now()
            tiempo_transcurrido = tiempo_actual - widget_time[0]
            tiempo_sec = int(tiempo_transcurrido.total_seconds()) + (float(widget_time[9])*86400)
            tiempo_finU = 1209600 - tiempo_sec
            tiempo_diasU = int(tiempo_finU // 86400)
            tiempo_horasU =int((tiempo_finU - (tiempo_diasU*86400)) // 3600)
            tiempo_transcurrido = tiempo_actual - widget_time[0]
            tiempo_finV = 7776000 - tiempo_sec
            tiempo_diasV = int(tiempo_finV // 86400)
            tiempo_horasV = int((tiempo_finV - (tiempo_diasV*86400)) // 3600)

            catorce = (widget_time[0]+timedelta(days=14)).strftime("%d-%m-%Y")
            noventa = (widget_time[0]+timedelta(days=90)).strftime("%d-%m-%Y")
            #texto predeterminado para la descripcion de cada generador
            print1 = textwrap.fill(f'''

{widget_time[7]}:

El gas tendrá su pico de calidad en {tiempo_diasU} días y {tiempo_horasU} horas ({catorce})

El gas empezará a perder calidad en {tiempo_diasV} días y {tiempo_horasU} horas ({noventa})''', width = 35, replace_whitespace=False)
            
            print2 = textwrap.fill(f'''

{widget_time[7]}:

El gas está en su pico de calidad, y empeará a perder calidad en {tiempo_diasV} días y {tiempo_horasU} horas

({noventa})''', width = 35, replace_whitespace=False)
            print3 = textwrap.fill(f'''

{widget_time[7]}:

El gas está perdiendo calidad desde hace {-tiempo_diasV} días y {tiempo_horasV} horas, y su eficiencia decaerá con cada dia transcurrido

({noventa})''', width = 35, replace_whitespace=False)
            #ahora, se agrega un texto en caso que se tengan los datos de internet, u otro si no
            if widget_time[10][0]:
                print1 = textwrap.fill(print1 + f'''

Presion = {widget_time[10][0]}
Temperatura = {widget_time[10][1]}
% de metano = {widget_time[10][2]}''', width = 35, replace_whitespace=False)
                print2 = textwrap.fill(print2 + f'''

Presion = {widget_time[10][0]}
Temperatura = {widget_time[10][1]}
% de metano = {widget_time[10][2]}''', width = 35, replace_whitespace=False)
                print3 = textwrap.fill(print3 + f'''

Presion = {widget_time[10][0]}
Temperatura = {widget_time[10][1]}
% de metano = {widget_time[10][2]}''', width = 35, replace_whitespace=False)
            else:
                print1 = print1 + '''

Presion no disponible
Temperatura no disponible
% de metano no disponible'''
                print2 = print2 + '''

Presion no disponible
Temperatura no disponible
% de metano no disponible'''
                print3 = print3 + '''

Presion no disponible
Temperatura no disponible
% de metano no disponible'''
            #un print para cada situacion posible del generador
            try:
                if tiempo_diasU > 0 and len(widget_time) > 8:
                    widget_time[1].text = print1

                elif tiempo_diasV > 0 and len(widget_time) > 8:
                    widget_time[1].text = print2

                elif len(widget_time) > 8:
                    widget_time[1].text = print3
            except:
                pass
            #actualizo la posicion de los componentes de cada generador (cuadro, tacho, lapiz)
            widget_time[1].pos_hint={'center_x': 0.5, 'center_y': 0.48}
            widget_time[2].pos_hint={'center_x': 0.5, 'center_y': 0.66-((self.widgets.index(widget_time))*0.0833)}
            widget_time[4].pos_hint={'center_x': 0.85, 'center_y': 0.66-((self.widgets.index(widget_time))*0.0833)}
            widget_time[6].pos_hint={'center_x': 0.15, 'center_y': 0.66-((self.widgets.index(widget_time))*0.0833)}

    #para ver la informacion de cada generador
    def info(self, instance, arg1):
        global cant
        #de vuelta, solo si no hay otra ventana abierta (voy a dejar de mencionarlo a partir de ahora)
        if cant == 0:
            #leo el data para la info
            with open (datos, mode='r') as file:
                read = csv.reader(file)
                data = list(read)
                for line in data:
                    if arg1 in line:
                        tiempo_actual = datetime.now()
                        b = (data.index(line))
                        widget_time = self.widgets[b]
                        ventana = widget_time[5]
                        tiempo_transcurrido = tiempo_actual - widget_time[0]
                        tiempo_sec = int(tiempo_transcurrido.total_seconds()) + (float(widget_time[9])*86400)
                        tiempo_finU = 1209600 - tiempo_sec
                        tiempo_diasU = int(tiempo_finU // 86400)
                        tiempo_finV = 7776000 - tiempo_sec
                        tiempo_diasV = int(tiempo_finV // 86400)

                        #para cada situacion posible del generador, tengo un color diferente de ventana
                        if tiempo_diasU > 0:
                            self.widf(arg1 = [ventana[1], widget_time[3], widget_time[1]], arg2 = 'add')
                        elif tiempo_diasV > 0:
                            self.widf(arg1 = [ventana[0], widget_time[3], widget_time[1]], arg2 = 'add')
                        else:
                            self.widf(arg1 = [ventana[2], widget_time[3], widget_time[1]], arg2 = 'add')
            cant +=1

    #ventana de ayuda
    def tutorial(self, instance, arg1, arg2, arg3):
        global cant
        if cant == 0:
            cant +=1
            self.widf(arg1 = [arg1, arg2, arg3], arg2 = 'add')

    #cierre de la ventana de ayuda
    def watbye(self, instance, arg1, arg2, arg3):
        global cant
        self.widf(arg1 = [arg1, arg2, arg3], arg2 = 'rem')
        cant -=1

    #cierre de la ventana de info
    def salida(self, instance, arg1):
        global cant
        with open (datos, mode='r') as file:
            read = csv.reader(file)
            data = list(read)
            for line in data:
                if arg1 in line:
                    b = (data.index(line))
                    widget_time = self.widgets[b]
                    ventana = widget_time[5]
                    self.widf(arg1 = [widget_time[1], widget_time[3], ventana[0], ventana[1], ventana[2]], arg2 = 'rem')
        cant -=1

    #edicion del nombre del generador
    def editar(self, instance, arg1):
        global cant
        if cant == 0:
            with open (datos, mode='r') as file:
                read = csv.reader(file)
                data = list(read)
                for line in data:
                    if arg1 in line:
                        b = (data.index(line))
                        widget_time = self.widgets[b]
                        ventana = widget_time[5]
                        self.root.add_widget(ventana[0])
            #pido el nuevo nombre
            self.newname = TextInput(
                text=f'{widget_time[7]}',
                background_normal = lizo,
                background_active = lizo_o,
                multiline=False,
                pos_hint={'center_x':0.5, 'center_y':0.5},
                size_hint = (0.7, 0.08),
                font_size = Wsize[1]/35,
                font_name = "letra"
                )
            self.root.add_widget(self.newname)
            save = Button(
                text="Guardar nombre",
                background_normal = lizo,
                background_down = lizo_o,
                size_hint=(0.5, 0.067),
                pos_hint={'center_x': 0.5, 'center_y':0.15},
                font_size=Wsize[1]/40,
                font_name = "letra"
                )
            guardarf = partial(self.boton_guardar, arg1=arg1)
            save.bind(on_press=guardarf)
            self.root.add_widget(save)
            self.user_input = None
            cant +=1

    #una vez que tengo el nuevo nombre
    def boton_guardar(self, instance, arg1):
        global cant
        n = 0
        newname = ''
        listname = list(self.newname.text)
        if len(listname) > 18:
            for letra in listname:
                n +=1
                newname = newname + letra
                if n == 18:
                    break
            self.user_input = newname
        else:
            self.user_input = self.newname.text
        with open (datos, mode='r') as file:
            read = csv.reader(file)
            data = list(read)
            for line in data:
                if arg1 in line:
                    indice = (data.index(line))
                    widget_time = self.widgets[indice]
        with open(datos, mode='w', newline='') as file:
            writer = csv.writer(file)
            for line in data:
                if arg1 in line:
                    line[1] = self.user_input
                    widget_time[7] = line[1]
            writer.writerows(data)
            ventana = widget_time[5]
        self.widf(arg1 = [ventana[0], instance, self.newname], arg2 = 'rem')
        widget_time[2].text = f'{widget_time[7]}'
        cant -=1

    #para sacar los generadores
    def remove_box(self, instance, arg1):
        global cant
        if cant == 0:
            with open (datos, mode='r') as file:
                read = csv.reader(file)
                data = list(read)
                for line in data:
                    if arg1 in line:
                        indice = data.index(line)
                        widget_time = self.widgets[indice]
                        self.widf(
                            arg1 = [widget_time[5][0], widget_time[8][0], widget_time[8][1], widget_time[8][2]],
                            arg2 = 'add'
                            )
            cant +=1

    #SEGURO que quiere sacar el generador?
    def confirm_remove(self, instance, arg1):
        global cant
        with open (datos, mode='r') as file:
                read = csv.reader(file)
                data = list(read)
                for line in data:
                    if arg1 in line:
                        indice = data.index(line)
                        widget_time = self.widgets[indice]
                        self.widf(arg1 = [widget_time[1], widget_time[2], widget_time[4], widget_time[6]], arg2 = 'rem')
                        with open (datos, mode='r') as file:
                            read = csv.reader(file)
                            data = list(read)
                            del data[indice]
                        with open(datos, mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(data)
                        del self.widgets[indice]
                        self.widf(
                            arg1 = [widget_time[5][0], widget_time[8][0], widget_time[8][1], widget_time[8][2]],
                            arg2 = 'rem'
                            )
                        cant -=1

    #si no estabas SEGURO
    def not_remove(self, instance, arg1):
        global cant
        with open (datos, mode='r') as file:
                read = csv.reader(file)
                data = list(read)
                for line in data:
                    if arg1 in line:
                        indice = data.index(line)
                        widget_time = self.widgets[indice]
                        self.widf(
                            arg1 = [widget_time[5][0], widget_time[8][0], widget_time[8][1], widget_time[8][2]],
                            arg2 = 'rem'
                        )
                        cant -=1

    #funcion para agregar o remover widgets mas eficientemente (el momento de implementarlo me ahorro 30 lineas)
    def widf(self, arg1, arg2):
        for wid in arg1:
            if arg2 == 'rem':
                self.root.remove_widget(wid)
            else:
                self.root.add_widget(wid)
    
    #para borrar el texto predeterminado en las ventanas de inputs
    def clear_content(self, instance):
        instance.text=''

#inicia la app
if __name__ == "__main__":
    Bgas().run()