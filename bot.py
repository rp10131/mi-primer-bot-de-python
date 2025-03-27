import discord, random, os, asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Cargar las variables del archivo .env y funciones
load_dotenv()
gen_pass(10)

TOKEN = os.getenv("DISCORD_TOKEN")

# La variable intents almacena los privilegios del bot
intents = discord.Intents.default()
# Activar el privilegio de lectura de mensajes
intents.message_content = True
# Crear un bot en la variable cliente y transferirle los privilegios
client = commands.Bot(command_prefix='y-', intents=intents)
last_message_time = datetime.now()

@client.event
async def on_ready():
    juego = ['Ping Pong', 'Piedra, Papel o Tijera', 'Sopa de Tortuga']
    viendo = ['Discord', 'la fortuna de los miembros conectados', 'y-y.help']
    haciendo = random.randint(1,2)
    if haciendo == 1:
        activity = discord.Game(name=random.choice(juego))
    else:
        activity = discord.Activity(type=discord.ActivityType.watching, name=random.choice(viendo))

    await client.change_presence(activity=activity)
    print(f'Hemos iniciado sesión como {client.user}\n{activity}')
    check_inactivity.start()

@client.event
async def on_message(message):
    global last_message_time

    if message.author == client.user:
        return
    else:
        last_message_time = datetime.now()
    if message.content.startswith('hola'):
        await message.channel.send("Hola!")
    elif message.content.startswith('adiós'):
        await message.channel.send("\U0001f642")
    elif message.content.startswith('!ping'):
        await message.channel.send("Pong!")
    if (message.content == 'y-tortuga'):
        await message.add_reaction("\U0001F422")
        await message.channel.send("Un hombre pidió sopa de tortuga en un restaurante con vista al mar. El hombre tomó un sorbo de sopa, confirmó que era auténtica sopa de tortuga, pagó la cuenta, se fue a casa y luego se suicidó. ¿Por qué?")
        await message.channel.send("Cómo jugar: Ingresa tu pregunta con el siguiente formato: y-tortuga <preguna>. Yumemibot responderá con 'Sí' o 'No' o 'Es irrelevante'.")
    if message.content == 'y-piedrapapel':
        await message.channel.send("Juguemos Piedra Papel o Tijera! Tu mensaje debe verse así: y-piedrapapel <opción>")

    await client.process_commands(message)

@tasks.loop(seconds=60)  # Verifica cada minuto
async def check_inactivity():
    global last_message_time
    current_time = datetime.now()
    if current_time - last_message_time > timedelta(minutes=60):
        channel = discord.utils.get(client.get_all_channels(), name="💀〣spam")
        if channel:
            await channel.send("¡Hola! Parece que hace rato no hay mensajes 😊")
            print(last_message_time)
            last_message_time = datetime.now()

@client.command(name="piedrapapel", help='juega al juego Piedra Papel o Tijera; puede funcionar con solo "y-piedrapapel"')
async def piedra_papel_tijera(ctx, eleccion: str):
    opciones = ["piedra", "papel", "tijera"]
    if eleccion.lower() not in opciones:
        await ctx.send("Por favor, elige entre piedra, papel o tijera.")
        return
    elif eleccion.lower() == 'yumemi':
        await ctx.send(">.<")
        return

    eleccion_bot = random.choice(opciones)
    mensaje = f"🤖 Yo elijo **{eleccion_bot}**. Tú eliges **{eleccion.lower()}**."

    if eleccion.lower() == eleccion_bot:
        resultado = "¡Empatamos! :o"
    elif (eleccion.lower() == "piedra" and eleccion_bot == "tijera") or \
         (eleccion.lower() == "papel" and eleccion_bot == "piedra") or \
         (eleccion.lower() == "tijera" and eleccion_bot == "papel"):
        resultado = "¡Ganaste! :)"
    else:
        resultado = "¡Perdiste! ;v;"

    await ctx.send(f"{mensaje}\n{resultado}")

@client.command(name="tortuga", help='juega al juego Sopa de Tortuga; puede funcionar con solo "y-tortuga"')
async def sopa_de_tortuga(ctx, eleccion: str):
    opciones = ['Sí', 'No', 'Es irrelevante']
    if eleccion != '':
        await ctx.send(f"Creo que.. {random.choice(opciones)}")

@client.command(name="saludo", help='Envía un mensaje de saludo así nada más')
async def saludo(ctx):
    # El bot envía un mensaje
    mensaje = await ctx.send("¡Hola a todos!")
    
    # Reacciona al mensaje que acaba de enviar
    await mensaje.add_reaction("👋")

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
        f'Sabías que {meses[mes_actual - 1]} es tu mes de suerte? 🍀', 'Mañana deberás cuidarte de las cucarachas!', 
        f'{ctx.author.name}, tu creatividad florecerá pronto! 🎨', f'Crearás un bot de discord este {meses[(mes_actual + random.randint(-1, 2)) % 12]} 😯', 
        'Un giro inesperado en tu vida te llevará a descubrir tu verdadera pasión! Probablemente después de pedir pizza', 'La fortuna sonríe a quienes la buscan... excepto si la buscan en Google Maps', 
        'Una fuerza misteriosa te guiará a encontrar el último calcetín perdido... o a comprar uno nuevo!', 'Tus esfuerzos darán frutos muy pronto. Literalmente, planta ese árbol de limón', 
        'Pronto recibirás un mensaje importante... de una cadena de WhatsApp que lleva años circulando, claro', 
        'Tu café será perfecto- pero olvidarás tomarlo', 'La respuesta a una pregunta filósofica te llegará pronto',
        f'Lo creas o no... verano {datetime.now().year} ha de ser tu verano más fresco', f'{ctx.author.name}... sólo hazlo ya! sólo hazlo ya!',
        'Hmmm, se me hace que tienes que dejar el teléfono o la PC por un rato', f'Algo te hará amar la historia en {meses[(mes_actual + random.randint(-3, 3)) % 12]} 🤔'
    ]

    await ctx.send(f"🔮 {ctx.author.mention}! Tu fortuna: {random.choice(opciones)}")

@client.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@client.command(name='adivinar', help='Escoge un número del 1 al 10 y el usuario tiene que adivinar cuál es.')
async def adivinar(ctx):
    await ctx.send('Adivina un número entre el 1 y el 10!')
    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()

    answer = random.randint(1, 10)

    try:
        guess = await client.wait_for('message', check=is_correct, timeout=8.0)
    except asyncio.TimeoutError:
        return await ctx.send(f'Lo lamento, te tardaste demasiado. Era {answer}')

    if int(guess.content) == answer:
        await ctx.send('Estas en lo correcto!')
    else:
        await ctx.send(f'Uy. En realidad es {answer}')

@client.command(name='y.help', help='Lista de ayuda creada antes de saber que "help" está por defecto...')
async def lista_comandos(ctx):
    embed = discord.Embed(title="✯y u me m i b o t ・ c o m m a n d s✯", description="Aquí están los comandos organizados por categorías:", color=discord.Color.blue())
    
    # Categoría: Otro
    embed.add_field(name="**Otros**", value="`saludo` - Envía un saludo amistoso así nada más.\n `embed` - envía un embed vacío", inline=False)
    
    # Categoría: Diversión
    embed.add_field(name="**Diversión**", value="`fortuna` - Predice tu fortuna en un futuro cercano.\n `piedrapapel` - juega al juego Piedra Papel o Tijera; puede funcionar con solo 'y-piedrapapel'\n `tortuga` - juega al juego Sopa de Tortuga; puede funcionar con solo 'y-tortuga'\n `heh` - risas. Es posible cambiar la cantidad de 'heh' con 'y-heh <número>'", inline=False)
    embed.add_field(name="**Notas**", value="El prefijo del bot es `y-`\n Yumemibot es capaz de responder a mensajes que no son comandos (y por lo tanto, no usan el prefijo) en algunos casos.", inline=False)

    await ctx.send(embed=embed)

client.run(TOKEN)
