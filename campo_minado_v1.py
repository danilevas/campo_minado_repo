from tkinter import *
import math
import random
from PIL import ImageTk,Image

root = Tk()
root.title("Campo Minado do Dani!")
root.configure(bg='#BDBDBD')

tamanho_x = 15
tamanho_y = 7.5

path = "C:/Programas/Projetos Pessoais/tkinter/campo_minado/"
imagens = [
    Image.open(path + "icones/flag resized.png"),
    Image.open(path + "icones/1.png"),
    Image.open(path + "icones/2.png"),
    Image.open(path + "icones/3.png"),
    Image.open(path + "icones/4.png"),
    Image.open(path + "icones/5.png"),
    Image.open(path + "icones/6.png"),
    Image.open(path + "icones/7.png"),
    Image.open(path + "icones/8.png"),
    Image.open(path + "icones/fundo.png"),
    Image.open(path + "icones/fundo.png")
]
imagens_prontas = []

for i in range(len(imagens)):
    # Load an image in the script
    img = imagens[i]

    tkimage = ImageTk.PhotoImage(img)
    h = tkimage.height()
    w = tkimage.width()

    # Resize the Image using resize method
    if i == 0 or i == 10:
        resized_image = img.resize((int(tamanho_x*2), int(tamanho_x*2)), Image.ANTIALIAS)
    else:
        resized_image = img.resize((int(tamanho_x*2.3), int(tamanho_x*2.3)), Image.ANTIALIAS)
    imagens_prontas.append(ImageTk.PhotoImage(resized_image))

botoes = []
numeros = []
colunas = 10
linhas = 10
bombas = 10
lugar_bombas = []
marcados = []

def desabilita(label):
    label.configure(borderwidth=1, highlightbackground = "#7F7F7F", highlightcolor= "#7F7F7F")

def desabilitado(label):
    if label["borderwidth"] == 1:
        return True
    else:
        return False

def marca(indice):
    label = botoes[indice]
    label.configure(image=imagens_prontas[0])
    marcados.append(indice)

def desmarca(indice):
    label = botoes[indice]
    label.configure(image=imagens_prontas[10])
    marcados.remove(indice)

def marcado(indice):
    if indice in marcados:
        return True
    else:
        return False

def coloca_icone(label, numero):
    label.configure(image=imagens_prontas[numero], padx=tamanho_x-1)

def revelar_vizinhos(indice):
    inicio = True
    fila = [indice]
    while fila:
        atual = fila.pop(0)
        desabilita(botoes[atual])
            
        if (inicio == True) or (inicio == False and numeros[atual] == 0 ):
            inicio = False
            for vizinho in obter_vizinhos(atual):
                if (not desabilitado(botoes[vizinho])) and vizinho not in lugar_bombas and not bloqueado(vizinho, atual): # mudança
                    fila.append(vizinho)
                    desabilita(botoes[vizinho])
                    if numeros[vizinho] > 0:
                        coloca_icone(botoes[vizinho], numeros[vizinho])
                    else:
                        coloca_icone(botoes[vizinho], 9)

def bloqueado(vizinho, atual):
    diagonais = [atual + colunas + 1, atual + colunas - 1, atual - colunas + 1, atual - colunas - 1]
    if vizinho not in diagonais:
        return False
    else:
        if vizinho == diagonais[0] and (atual + colunas not in lugar_bombas and atual + 1 not in lugar_bombas):
            return False
        elif vizinho == diagonais[1] and (atual + colunas not in lugar_bombas and atual - 1 not in lugar_bombas):
            return False
        elif vizinho == diagonais[2] and (atual - colunas not in lugar_bombas and atual + 1 not in lugar_bombas):
            return False
        elif vizinho == diagonais[3] and (atual - colunas not in lugar_bombas and atual - 1 not in lugar_bombas):
            return False
        else:
            return True

def clique_botao(indice):
    label = botoes[indice]
    # A label abaixa quando é clicada
    label.config(relief=SUNKEN)

def desclique_botao(indice):
    label = botoes[indice]
    label.config(relief=RAISED)
    
    if indice in lugar_bombas:
        # VOCÊ PERDEU!
        label.configure(text="B!", padx=tamanho_x*0.65)
        for botao in botoes:
            if botao != label:
                botao.configure(state=DISABLED) # Para ninguém poder clicar mais em nada depois que o jogo termina
        root.after(2000, root.destroy)  # Delay for 2 seconds before closing the window
    else:
        if numeros[indice] > 0:
            coloca_icone(label, numeros[indice])
        else:
            coloca_icone(label, 9)
        desabilita(label)
        revelar_vizinhos(indice)

def obter_vizinhos(indice):
    vizinhos = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == dy == 0:
                continue
            linha = indice // colunas
            coluna = indice % colunas
            nova_linha = linha + dy
            nova_coluna = coluna + dx
            if 0 <= nova_linha < linhas and 0 <= nova_coluna < colunas:
                vizinhos.append(nova_linha * colunas + nova_coluna)
    return vizinhos

def bandeirinha(indice):
    # label = botoes[indice]
    if not marcado(indice):
        marca(indice)
        checa_ganhou()
    else:
        desmarca(indice)

def checa_ganhou():
    marcados.sort()
    if lugar_bombas == marcados:
        # VOCÊ GANHOU!
        for indice in range(linhas * colunas):
            botoes[indice].configure(bg="blue")
            root.after(2000, root.destroy)  # Delay for 2 seconds before closing the window

# Sorteando as bombas
for i in range(bombas):
    local_bomba = random.randint(0, (colunas * linhas) - 1)
    if local_bomba not in lugar_bombas:
        lugar_bombas.append(local_bomba)
lugar_bombas.sort()

# Colocando os números nos quadrados sem bomba
for i in range(colunas * linhas):
    num = 0
    for vizinho in obter_vizinhos(i):
        if vizinho in lugar_bombas:
            num += 1
    numeros.append(num)

# Definindo os botões
for i in range(colunas * linhas):
    if i in lugar_bombas:
        botao = Label(root, relief=RAISED, padx=tamanho_x, pady=tamanho_y, borderwidth=3, bg="#BDBDBD")
    else:
        botao = Label(root, relief=RAISED, padx=tamanho_x, pady=tamanho_y, borderwidth=3, bg="#BDBDBD")
    botao.bind("<Button-1>", lambda event, i=i: clique_botao(i))
    botao.bind("<ButtonRelease-1>", lambda event, i=i: desclique_botao(i))
    botao.bind("<Button-3>", lambda event, i=i: bandeirinha(i))
    botoes.append(botao)

# Colocando os botões na tela
for i in range(colunas * linhas):
    botoes[i].grid(row=math.floor(i / colunas), column=i % colunas)

root.mainloop()