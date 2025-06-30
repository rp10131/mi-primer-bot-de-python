import discord, random, os, asyncio, math # "os" es el sistema operativo. Asyncio: https://docs.python.org/3/library/asyncio.html
from discord.ext import commands, tasks # tasks se usa para mensajes programados/automatizados.
from bot_logic import gen_pass, get_image, meme # bot_logic es un archivo .py local creado para ayudar a organizar los comandos.
from dotenv import load_dotenv # info: https://www.geeksforgeeks.org/using-python-environment-variables-with-python-dotenv/
from datetime import datetime, timedelta # paquete que se usa para obtener meses, el año, hora, etc.

# Cargar las variables del archivo .env y funciones.
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN") # Obtiene la variable DISCORD_TOKEN del archivo .env

# La variable intents almacena los privilegios del bot que el desarrollador le puso por defecto.
intents = discord.Intents.default()
# Activar el privilegio de lectura de mensajes.
intents.message_content = True
# Crear un bot en la clase Bot (commands.Bot) y transferirle los privilegios.
client = commands.Bot(command_prefix='y-', intents=intents) # "client" puede tener cualquier nombre.
last_message_time = datetime.now()

@client.event
async def on_ready(): # Cuando se abre el archivo .py del código del bot en la consola.
    await client.change_presence(activity=actividad()) # La actividad es la variable "presencia", llamada usando la función actividad()
    check_inactivity.start() # Comienza a verificar si ha pasado mucho tiempo desde el último mensaje.
    cambiar_estado.start() # Comienza a cambiar la actividad cada determinado tiempo.
    print(f'\n{client.user} está en línea! \nActividad: {presencia}\nLatencia: {round(client.latency * 1000)}ms') # El bot está en línea.

def actividad():
    global presencia # global sirve para mostrar/usar la variable en sitios fuera de donde se llamó a la función, como "print()".
    juego = ['Ping Pong', 'Piedra, Papel o Tijera', 'Sopa de Tortuga']
    viendo = ['Discord', 'la fortuna de los miembros conectados', 'y-y.help']
    haciendo = random.randint(1,2) # Escoge el tipo de actividad que aparecerá en el estado del bot. 
    if haciendo == 1:
        presencia = discord.Game(name=random.choice(juego)) # El estado es "Jugando a _".
        return presencia # regresa la variable "presencia" a la línea de código que llamó a la función.
    else:
        presencia = discord.Activity(type=discord.ActivityType.watching, name=random.choice(viendo)) # El estado es "Viendo _".
        return presencia # regresa la variable "presencia" a la línea de código que llamó a la función.

@tasks.loop(hours=1.5) # Se repite cada hora y media.
async def cambiar_estado():
    await client.change_presence(activity=actividad()) # La actividad es la variable "presencia", llamada usando la función actividad()
    print(f'\nEl estado cambió a {presencia} a las {datetime.now()}') # Muestra "presencia" y la hora en la que cambió.

@tasks.loop(seconds=60)  # Clase Tasks. Verifica cada minuto.
async def check_inactivity():
    global last_message_time
    current_time = datetime.now() # Hora y fecha actuales.
    if current_time - last_message_time > timedelta(minutes=60): # Si ha pasado más de una hora desde el último mensaje.
        channel = discord.utils.get(client.get_all_channels(), name="nombre-del-canal") # Se puede cambiar el nombre del canal.
        if channel:
            await channel.send("¡Hola! Parece que hace rato no hay mensajes 😊")
            print(last_message_time) # En la consola aparece la fecha del último mensaje.
            last_message_time = datetime.now() # El mensaje del bot se convierte en el más reciente y se guardan la fecha y hora.
            
@client.event
async def on_message(message): # Cuando hay mensajes en el servidor de Discord.
    global last_message_time

    if message.author == client.user:
        return # No queremos que el bot responda a sus propios mensajes.
    else:
        last_message_time = datetime.now() # La fecha y hora de la última vez que alguien envió un mensaje.
    if message.content.startswith('hola'): # Mensaje de alguien.
        await message.channel.send("Hola!") # Respuesta del bot.
    elif message.content.startswith('adiós'):
        await message.channel.send("\U0001f642") # Emoji en unicode.
    elif message.content.startswith('!ping'):
        await message.channel.send(f"Pong!\nLatencia: {round(client.latency * 1000)}ms")
    if (message.content == 'y-tortuga'): # El comando cuando no se le dan argumentos.
        await message.add_reaction("\U0001F422") # Añade una reacción al mensaje del usuario.
        await message.channel.send("Un hombre pidió sopa de tortuga en un restaurante con vista al mar. El hombre tomó un sorbo de sopa, confirmó que era auténtica sopa de tortuga, pagó la cuenta, se fue a casa y luego se suicidó. ¿Por qué?")
        await message.channel.send("Cómo jugar: Ingresa tu pregunta con el siguiente formato: y-tortuga <preguna>. Yumemibot responderá con 'Sí' o 'No' o 'Es irrelevante'.")
    if message.content == 'y-piedrapapel': # El comando cuando no se le dan argumentos.
        await message.channel.send("Juguemos Piedra Papel o Tijera! Tu mensaje debe verse así: y-piedrapapel <opción>")

    await client.process_commands(message) # Esto es necesario para que el bot pueda responder a comandos además de a eventos.
    
@client.command(name="piedrapapel", help='juega al juego Piedra Papel o Tijera; puede funcionar con solo "y-piedrapapel"')
async def piedra_papel_tijera(ctx, eleccion: str): # "eleccion" es un argumento string que tiene que introducir el usuario.
    opciones = ["piedra", "papel", "tijera"]
    if eleccion.lower() == 'bot': # Diversión.
        await ctx.send(">.<")
    if eleccion.lower() not in opciones: # Si el argumento no está en la lista.
        await ctx.send("Por favor, elige entre piedra, papel o tijera.")
        return
    eleccion_bot = random.choice(opciones)
    mensaje = f"🤖 Yo elijo **{eleccion_bot}**. Tú eliges **{eleccion.lower()}**." # La elección del bot y el usuario. En minúsculas.

    if eleccion.lower() == eleccion_bot: # Empate.
        resultado = "¡Empatamos! :o"
    elif (eleccion.lower() == "piedra" and eleccion_bot == "tijera") or \
         (eleccion.lower() == "papel" and eleccion_bot == "piedra") or \
         (eleccion.lower() == "tijera" and eleccion_bot == "papel"):
        resultado = "¡Ganaste! :)" # Verifica si el usuario ganó.
    else: # El usuario perdió.
        resultado = "¡Perdiste! ;v;"

    await ctx.send(f"{mensaje}\n{resultado}")

@client.command(name="tortuga", help='juega al juego Sopa de Tortuga; puede funcionar con solo "y-tortuga"')
async def sopa_de_tortuga(ctx, idea: str): # "idea" es un argumento string que puede tener cualquier valor.
    opciones = ['sí', 'no', 'es irrelevante']
    opciones2 = ['Emm...', 'Definitivamente', 'Creo que...', 'Se me hace que', 'Vaya idea!!']
    if idea != '': # si hay un argumento:
        await ctx.send(f"{random.choice(opciones2)} {random.choice(opciones)}") # Responde con un objeto de aleatorio de ambas listas.

@client.command(name='fortuna', help='Adivina la fortuna del usuario')
async def adivinar_la_fortuna(ctx):
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    mes_actual = datetime.now().month  # Obtiene el número del mes (1 para enero, 2 para febrero, etc.)
    opciones = [
        'Pronto encontrarás algo que pensabas perdido', 'Alguien te enviará memes que te cambiarán la vida', 
        'Tu próxima comida será la mejor de la semana', 'Muchos dulces te esperarán muy pronto', 
        f'El número {random.randint(1,100)} será crucial para ti esta semana', 'Una taza de café de esta semana te dará más energía de lo usual', 
        f'Sabías que {meses[mes_actual - 1]} es tu mes de suerte? 🍀', 'Mañana deberás cuidarte de las cucarachas!', # "mes_actual - 1" es igual al mes actual en la lista, ya que comienza con el índice 0.
        f'{ctx.author.name}, tu creatividad florecerá pronto! 🎨', f'Crearás un bot de discord este {meses[(mes_actual + random.randint(-1, 2)) % 12]} 😯', # Escoge un mes de la lista. Si el índice es inexistente ahí, se reinician los valores de la lista. 
        'Un giro inesperado en tu vida te llevará a descubrir tu verdadera pasión! Probablemente después de pedir pizza', 'La fortuna sonríe a quienes la buscan... excepto si la buscan en Google Maps', 
        'Una fuerza misteriosa te guiará a encontrar el último calcetín perdido... o a comprar uno nuevo!', 'Tus esfuerzos darán frutos muy pronto. Literalmente, planta ese árbol de limón', 
        'Pronto recibirás un mensaje importante... de una cadena de WhatsApp que lleva años circulando, claro', 
        'Tu café será perfecto- pero olvidarás tomarlo', 'La respuesta a una pregunta filósofica te llegará pronto',
        f'Lo creas o no... verano {datetime.now().year} ha de ser tu verano más fresco', f'{ctx.author.name}... sólo hazlo ya! sólo hazlo ya!',
        'Hmmm, se me hace que tienes que dejar el teléfono o la PC por un rato', f'Algo te hará amar la historia en {meses[(mes_actual + random.randint(-3, 3)) % 12]} 🤔'
    ] # Opciones para la fortuna.

    await ctx.send(f"🔮 {ctx.author.mention}! Tu fortuna: {random.choice(opciones)}") # Menciona al usuario y le da una fortuna aleatoria.

@client.command()
async def heh(ctx, count_heh = 5): # El argumento por defecto es 5. Se puede cambiar: "y-heh <número>".
    await ctx.send("he" * count_heh) # Multiplica "he" por el argumento y lo envía en un solo mensaje.

@client.command(name='adivinar', help='Escoge un número del 1 al 6 y el usuario tiene que adivinar cuál es.')
async def adivinar(ctx):
    await ctx.send('Adivina un número entre el 1 y el 6!')
    def is_correct(m): # Cuando hay mensaje (m) de respuesta para adivinar:
        return m.author == ctx.author and m.content.isdigit() # El autor del mensaje es el del comando; el mensaje es un número.

    answer = random.randint(1, 6) # Escoge un número aleatorio.

    try:
        guess = await client.wait_for('message', check=is_correct, timeout=8.0) # Son 8 segundos. Si hay mensaje, verifica si es correcto.
    except asyncio.TimeoutError:
        return await ctx.send(f'Lo lamento, te tardaste demasiado. Era {answer}') # Si el usuario tarda mucho.

    if int(guess.content) == answer: # Si lo que escribió el usuario es igual al número del bot
        await ctx.send('Estas en lo correcto!')
    else:
        await ctx.send(f'Uy. En realidad es {answer}')
        
@client.command(name='ecuación', help='Resuelve una ecuación cuadrática. Hay valores por defecto.')
async def square_x(ctx, a: float = 1, b: float = 0, c: float = 0): # Float sirve por si el usuario ingresa decimales.
    if a == 0:
        await ctx.send("El coeficiente 'a' no puede ser 0 en una ecuación cuadrática.") # Si no ya no sería una ecuación cuadrática xd
        return
    
    if a == 1 and b == 0 and c == 0: # Si se usan los valores que están por defecto o si no se ingresan valores:
        await ctx.send("Ecuación cuadrática: ax^2 + bx + c = 0\n Puedes cambiar los valores de a, b y c! Intentaré despejar x")
    else:
        discriminante = b**2 - (4 * (a*c)) # El interior de la raíz cuadrada en la fórmula general.
        if discriminante > 0: # Dos soluciones reales
            raiz1 = (-b + math.sqrt(discriminante)) / (2 * a) # sqrt (square root/raíz cuadrada) proviene de la librería math.
            raiz2 = (-b - math.sqrt(discriminante)) / (2 * a)
            await ctx.send(f"Las raíces son: x1 = {raiz1}, x2 = {raiz2}")
        elif discriminante == 0: # Una solución real
            raiz = -b / (2 * a)
            await ctx.send(f"La raíz es: x = {raiz}")
        else: # Soluciones complejas (números imaginarios).
            parte_real = -b / (2 * a)
            parte_imaginaria = math.sqrt(-discriminante) / (2 * a)
            await ctx.send(f"Las raíces son complejas: x1 = {parte_real} + {parte_imaginaria}i, x2 = {parte_real} - {parte_imaginaria}i")

@client.command(name='meme', help='Envía memes.')
async def mem(ctx, estilo: str = None): # "estilo" es el potencial nombre de las subcarpetas que almacenan memes de varias cosas.
    lista_estilos = ['animal','app','arte_clásico','ciencia','programación','TV','vida','otro'] # Nombres de subcarpetas.
    try:
        if estilo == None or estilo not in lista_estilos: # Si "estilo" está vacío o no está en la lista:
            estilo = random.choice(lista_estilos) # Se le asigna un valor aleatorio de la lista_estilos.
            
        imagen = meme(estilo) # En la función "meme" de bot_logic de obtiene un meme en base al estilo.

        with open(f'images/{estilo}/{imagen}', 'rb') as f: # Busca la imagen.
            picture = discord.File(f) # Hace que discord pueda enviarla.
        # A continuación, podemos enviar este archivo como parámetro.
        await ctx.send(file=picture)
    except Exception as e:
        print('Hubo un error:', e)
        await ctx.send('Parece que no funcionó')

@client.command('animal',help='Envía una foto aleatoria de un animal. Se puede escoger el animal en cuestión.')
async def duck(ctx, animal: str = None): # "animal" es un parámetro que está vacío por defecto.
    image_url = get_image(animal) # obtiene una url de la función get_image() en bot_logic usando el valor del parámetro.
    print(image_url)
    await ctx.send(image_url)
    
@client.command(name='juego', help='Muestra un juego para jugar en un buscador.')
async def juego(ctx):
    juego = { # diccionario contenedor de juegos y sus datos.
        'Cookie Clicker': {'title': 'Cookie Clicker', 'descripcion': 'Idle clicker en el que haces galletas.', 'link': 'https://cookieclicker.com/', 'imagen': 'https://static.wikia.nocookie.net/cookieclicker/images/5/5a/PerfectCookie.png/revision/latest/scale-to-width-down/250?cb=20130827014912.png'},
        'Yume Nikki Online': {'title': 'Yume Nikki Online', 'descripcion': 'Sitio web para jugar Yume Nikki y fangames en línea.', 'link': 'https://ynoproject.net/', 'imagen': 'https://yume.wiki/images/6/6e/Minnatsuki_profile.png'},
        'skribbl': {'title': 'skribbl', 'descripcion': 'Multiplayer en el que dibujas palabras.', 'link': 'https://skribbl.io/', 'imagen': 'https://iemlabs.com/blogs/wp-content/uploads/sites/4/2023/08/skribbl-io-1.webp'},
        'Gartic Phone': {'title': 'Gartic Phone', 'descripcion': 'Teléfono descompuesto que mezcla frases y dibujos.', 'link': 'https://garticphone.com/', 'imagen': 'https://www.gamenora.com/upload/games/thumbnails/Gartic%20Phone.webp'},
        'Death by AI': {'title': 'Death by AI', 'descripcion': 'Sobrevive a arenas ficticias creadas por IA.', 'link': 'https://deathbyai.gg/', 'imagen': 'https://browsercraft.com/images/games/covers/death-by-ai.jpg'},
        'Sort the Court': {'title': 'Sort the Court!','descripcion': 'Das respuestas de sí o no a varias preguntas e influyes en el destino de un reino.', 'link': 'https://graebor.itch.io/sort-the-court', 'imagen': 'https://img.itch.zone/aW1hZ2UvNDczNjcvMjA1ODcxLnBuZw==/original/VFJ3Yl.png'},
        'Trolley': {'title': 'Absurd Trolley Problems', 'descripcion': 'Problemas de pensamiento por trenes.', 'link': 'https://neal.fun/absurd-trolley-problems/', 'imagen':'https://th.bing.com/th/id/OIP.rWtcO9IzkeEumyKidZ4myAHaC9?rs=1&pid=ImgDetMain'},
        'FNF': {'title': "Friday Night Funkin'", 'descripcion': 'Juego rítmico del 2020.', 'link': 'https://ninja-muffin24.itch.io/funkin', 'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Friday_Night_Funkin%27_logo.svg/1024px-Friday_Night_Funkin%27_logo.svg.png'},
        'PASSWORD': {'title': 'The Password Game', 'descripcion': '"Generador" de contraseñas las cuales tienen que seguir varias reglas.', 'link': 'https://neal.fun/password-game/', 'imagen': 'https://i.gzn.jp/img/2023/06/29/the-password-game/01.png'},
        'Akinator': {'title': 'Akinator', 'descripcion': 'Un genio intenta adivinar algún personaje en el que pienses.', 'link': 'https://akinator.com/', 'imagen': 'https://es.akinator.com/assets/img/akinator.png'},
        'QuickDraw': {'title': 'Quick, Draw!', 'descripcion': 'Una IA intenta adivinar qué son tus dibujos.', 'link':'https://quickdraw.withgoogle.com/', 'imagen': 'https://upload.wikimedia.org/wikipedia/en/0/0b/Quick%2C_Draw%21_cover.png'},
        'ChampionIsland': {'title': 'Doodle Champion Island Games', 'descripcion': 'Minijuegos varios sobre deportes.', 'link': 'https://doodles.google/doodle/doodle-champion-island-games-begin/', 'imagen': 'https://www.google.com/logos/doodles/2021/doodle-champion-island-games-begin-6753651837108462.2-2xa.gif'}
    }
    juego_random = random.choice(list(juego.keys())) # Escoge uno de los keys del diccionario (Cookie Clicker, Yume Nikki Online, etc.)
    # Crear el objeto embed
    embed = discord.Embed(
        title=juego[juego_random]['title'], # Obtiene el valor 'title' del subdiccionario del key elegido.
        description=juego[juego_random]['descripcion'], # Mismo caso. Por eso, todos los subdiccionarios tienen que usar los mismos valores.
        color=discord.Color.blue()
    )

    # Añadir un pie de página, imagen y autor
    embed.set_image(url=juego[juego_random]['imagen'])  # Imagen en el embed. Solo acepta URLs.
    embed.add_field(name="**Link**", value=juego[juego_random]['link']) # A pesar de estar aquí, esta parte aparece arriba de la imagen.

    # Enviar el mensaje embed
    await ctx.send(embed=embed) # Envía el embed.

@client.command(name='unión', help='Muestra la fecha en la que un miembro se unió al servidor.')
async def joined(ctx, member: discord.Member): # "discord.Member" implica que quien use el comando tiene que escribir el usuario del miembro
    mensaje = await ctx.send(f'{member.name} se unió a {member.guild} el {discord.utils.format_dt(member.joined_at)}')
    await mensaje.add_reaction("👋") # Reacciona a su propio mensaje gracias a que "mensaje" almacenó cuál fue el que hizo.

@client.command(name='y.help', help='Lista de ayuda creada antes de saber que "help" está por defecto...')
async def lista_comandos(ctx):
    embed = discord.Embed(title="✯b o t ・ c o m m a n d s✯", description="Aquí están los comandos organizados por categorías:", color=discord.Color.blue())
    
    # Categoría: Otro
    embed.add_field(name="**Otros**", value="`juego` - envía un juego online para jugar en el buscador.\n `ecuación` - resuelve ecuaciones cuadráticas: 'y-ecuación <a> <b> <c>'.\n `unión` - Muestra la fecha en la que un miembro se unió al servidor.", inline=False)
    
    # Categoría: Diversión
    embed.add_field(name="**Diversión**", value="`fortuna` - Predice tu fortuna en un futuro cercano.\n `piedrapapel` - juega al juego Piedra Papel o Tijera; puede funcionar con solo 'y-piedrapapel'\n `tortuga` - juega al juego Sopa de Tortuga; puede funcionar con solo 'y-tortuga'\n `heh` - risas. Es posible cambiar la cantidad de 'heh' con 'y-heh <número>'\n`meme` - Muestra un meme de programación.\n`animal` - Envía una foto aleatoria de un animal. Opcionalmente, se puede escoger el animal usando 'y-animal <animal>'; en ese caso, cualquier valor no registrado tendrá de respuesta la lista de los que sí están.", inline=False)
    embed.add_field(name="**Notas**", value="El prefijo del bot es `y-`\n Yumemibot es capaz de responder a mensajes que no son comandos (y por lo tanto, no usan el prefijo) en algunos casos.", inline=False)

    await ctx.send(embed=embed)

client.run(TOKEN) # El bot se pone en parcha
