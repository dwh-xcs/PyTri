# Instale a versão estável 2.91:
# pip install pyttsx3==2.91

import pyttsx3

engine = pyttsx3.init() # Inicializando a lib.

# # Obtendo a taxa de fala atual.
# rate = engine.getProperty('rate')
# print(f'Taxa de fala atual: {rate}') # Imprime a taxa de voz atual.

engine.setProperty('rate', 230) # Definindo uma nova taxa de fala (230 velocidade).

# # Obtendo o nível de volume atual. 
# volume = engine.getProperty('volume')   
# print(f'Nível de volume atual: {volume}') # Imprime o nível de volume atual.
# engine.setProperty('volume', 1.0) # Volume máximo.


# # Obtendo a lista de vozes disponíveis.
# voices = engine.getProperty('voices') 
# engine.setProperty('voice', voices[0].id) # Selecionando uma voz (0 para masculino, 1 para feminino, etc.).

# # Teste com texto estático a ser falado.
# engine.say("Olá, mundo!") 
# engine.say(f'Meu nome é Maria, tudo bem?') 
# engine.runAndWait() 

# Teste com texto em Lopping.
list_frase = [
    'Olá mundo!', 
    'Meu nome é Maria.',
    'Tudo bem?',
    'Esse é o teste com Lopping.',
    'E a biblioteca pyttsx3.']

for frase in list_frase:
    engine.say(frase) 
    engine.runAndWait()

