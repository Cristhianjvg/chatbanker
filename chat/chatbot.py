import nltk
import numpy as np
import random
import string
import warnings
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

warnings.filterwarnings("ignore")

flag = True
f = open('static/chatbot.txt', 'r', errors='ignore')
raw=f.read()
nlp = spacy.load('es_core_news_sm')

# raw=raw.lower()# convertir en minúscula
# nltk.download('punkt') # Instalar módulo punkt si no está ya instalado (solo ejecutar la primera vez)
# nltk.download('wordnet') # Instalar módulo wordnet si no está ya instalado (solo ejecutar la primera vez)
# sent_tokens = nltk.sent_tokenize(raw)# Convierte el CORPUS a una lista de sentencias
# word_tokens = nltk.word_tokenize(raw)# Convierte el CORPUS a una lista de palabras
# lemmer = nltk.stem.WordNetLemmatizer()

#WordNet diccionario semántico incluido en NLTK
# def LemTokens(tokens):
    
#     return [lemmer.lemmatize(token) for token in tokens]

# remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
# def LemNormalize(text):
#     return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    
SALUDOS_INPUTS = ("hola", "buenas", "saludos", "qué tal", "hey","buenos dias",)
SALUDOS_OUTPUTS = ["Hola", "Hola, ¿Qué tal?", "Hola, ¿Cómo te puedo ayudar?", "Hola, encantado de hablar contigo"]

def saludos(sentence):
    for word in sentence.split():
        if word.lower() in SALUDOS_INPUTS:
            return random.choice(SALUDOS_OUTPUTS)

def respuesta_predefinida(user_response):
    # Aquí puedes agregar preguntas y respuestas predefinidas
    preguntas = ["hola","¿Cuál es tu nombre?", "¿Cómo estás?", "¿Qué puedes hacer?", "¿Cuándo fue construido el Titanic?"]
    respuestas = ["hola","Mi nombre es ROBOT.", "Estoy bien, gracias por preguntar.", "Puedo responder preguntas sobre tus vacaciones en el crucero.", "El Titanic fue construido en Belfast, Irlanda del Norte, y se completó en 1911."]
    
    for i, pregunta in enumerate(preguntas):
        similitud = nlp(user_response).similarity(nlp(pregunta))
        if similitud > 0.7:  # Puedes ajustar el umbral según tus necesidades
            return respuestas[i]
    return 

#Función para determinar la similitud del texto insertado y el corpus
def response(user_response):
    


