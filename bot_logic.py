import random, requests,os

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>"
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return password

# comando "y-animal"
def get_image(animal):
    if animal == None:
        animales = [obtener_url_de_pato(), obtener_url_de_perro(), obtener_url_de_zorro(), obtener_url_de_gato(),obtener_url_de_oso()]
        validos = [img for img in animales if img]
        if not validos:
            return "No se pudo obtener una imagen en este momento."
        return random.choice(validos)
    elif animal in ['pato', 'perro', 'zorro', 'gato', 'oso']:
        return globals()[f"obtener_url_de_{animal}"]()  # Llama dinámicamente la función correspondiente
    else:
        return f"Lo siento, no tengo imágenes para '{animal}'. Prueba con pato, perro, zorro, gato u oso 🐻"

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
    url = 'https://cataas.com/cat'
    return url

def obtener_url_de_oso():
    x = random.randint(300,500)
    y = random.randint(300,500)
    url = f"https://placebear.com/{x}/{y}"
    return url

# comandos de y-meme
def meme(estilo):
    global estilo_2
    estilo_2 = estilo

    memes = os.listdir(f"images/{estilo}")
    img_name = random.choice(memes)
    return probabilidad(img_name)

def probabilidad(imagen):
    quinto_de_probabilidad = [
        'microondas.webp', 'Screenshot_20241129_182944.webp', 
        'IMG_2727.webp','d99fe7080655645c6367d908f443760f.webp', 'plan_incre.webp'
    ]
    if imagen in quinto_de_probabilidad:
        si_o_no = random.randint(1,5)
        if si_o_no != 1:
            print(f"Se hizo la probabilidad ({si_o_no})|{imagen}" )
            return meme(estilo_2)
        else:
            print(si_o_no)
            return imagen
    else:
        return imagen