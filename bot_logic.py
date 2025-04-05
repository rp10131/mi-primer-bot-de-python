import random, requests,os

# comando "y-animal"
def get_image(animal):
    if animal == None: # Si no especifica el animal:
        # Obtiene un valor aleatorio de cada función que obtiene urls.
        animales = [obtener_url_de_pato(), obtener_url_de_perro(), obtener_url_de_zorro(), obtener_url_de_gato(),obtener_url_de_oso()]
        validos = [img for img in animales if img] # Revisa las imágenes que sí se obtuvieron.
        if not validos:
            return "No se pudo obtener una imagen en este momento."
        return random.choice(validos) # Regresa a bot.py una de las imágenes obtenidas.
    elif animal in ['pato', 'perro', 'zorro', 'gato', 'oso']: # Cuando el animal especificado sí está ahí.
        return globals()[f"obtener_url_de_{animal}"]()  # Llama dinámicamente la función correspondiente.
    else:
        return f"Lo siento, no tengo imágenes para '{animal}'. Prueba con pato, perro, zorro, gato u oso 🐻" # No se encontró el animal.

# APIs exteriores.
def obtener_url_de_pato():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

def obtener_url_de_perro():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

def obtener_url_de_zorro():
    url = 'https://randomfox.ca/floof/'
    res = requests.get(url)
    data = res.json()
    return data['link']

def obtener_url_de_gato():
    url = 'https://cataas.com/cat' # El enlace automaticamente devuelva fotos de gatos aleatorias.
    return url

def obtener_url_de_oso(): # Las imagenes cambian dependiedo de las medidas.
    x = random.randint(300,500)
    y = random.randint(300,500)
    url = f"https://placebear.com/{x}/{y}"
    return url
###
# comandos de y-meme
def meme(estilo):
    global estilo_2
    estilo_2 = estilo # almacena el estilo que recibió´la función para poder usarla en otro lugar.

    memes = os.listdir(f"images/{estilo}") # obtiene las imagenes en la subcarpeta.
    img_name = random.choice(memes) # escoge una de esas imágenes.
    return probabilidad(img_name) # la función "probabilidad" decide si enviar la imagen o no.

def probabilidad(imagen):
    quinto_de_probabilidad = [
        'microondas.webp', 'Screenshot_20241129_182944.webp', 
        'IMG_2727.webp','d99fe7080655645c6367d908f443760f.webp', 'plan_incre.webp'
    ] # imágenes con un quinto de probabilidad de que se envien
    if imagen in quinto_de_probabilidad:
        si_o_no = random.randint(1,5)
        if si_o_no != 1: # la imagen no se envía.
            print(f"Se hizo la probabilidad ({si_o_no})|{imagen}" )
            return meme(estilo_2) # llama a la función "meme" para escoja una nueva imagen.
        else: # la imagen se envía.
            print(si_o_no)
            return imagen
    else:
        return imagen
