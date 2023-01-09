from flask import Flask, request, make_response, redirect, render_template
from itsdangerous import URLSafeTimedSerializer
from wordcloud import WordCloud
from tempfile import NamedTemporaryFile
from io import BytesIO
import random
import string
import time
import os
import shutil
import PyPDF2
from PyPDF2 import PdfReader
import docx2txt

# générer une clé secrète aléatoire
secret_key = os.urandom(24)
# générer un identifiant d'utilisateur unique (pour le test, sinon utiliser un id / utilisateur)
user_id = 1

app = Flask(__name__)

# instancier l'objet qui génère les identifiants de session
serializer = URLSafeTimedSerializer(secret_key)

# définir la fonction qui génère un identifiant de session
def generate_session_id():
    # générer un identifiant de session unique
    session_id = serializer.dumps([user_id, time.time()])
    return session_id

# définir la fonction qui vérifie un identifiant de session
def verify_session_id(session_id):
    # vérifier si l'identifiant de session est valide
    try:
        user_id, timestamp = serializer.loads(session_id, max_age=3600)
    except:
        return False
    return True

def generate_random_filename(length=20):
    # générer une chaîne aléatoire de caractères
    letters = string.ascii_lowercase
    filename = ''.join(random.choice(letters) for i in range(length))
    return filename + '.png'

def extract_text_from_pdf(file):
    # lire le fichier PDF en mémoire
    with BytesIO(file.read()) as data:
        # créer un lecteur PDF
        reader = PdfReader(data)
        # extraire le texte du PDF
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

wordclouds = {}
@app.route('/upload', methods=['POST'])
def upload_file():
    # ...
    # vérifier si le fichier existe dans la requête
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    # vérifier si l'utilisateur a bien sélectionné un fichier
    if file.filename == '':
        return redirect(request.url)
    if file:
        # enregistrer le fichier dans un fichier temporaire
        temp_file = NamedTemporaryFile(delete=False)
        file.save(temp_file.name)
        # extraire le texte du fichier
        if file.filename.endswith('.pdf'):
            # ouvrir le fichier PDF et extraire le texte
            text = extract_text_from_pdf(temp_file)
        elif file.filename.endswith('.docx'):
            # utiliser docx2txt pour extraire le texte du fichier Word
            text = docx2txt.process(temp_file.name)
        else:
            return 'Le fichier doit être au format PDF ou Word (.pdf ou .docx).'

        # générer le nuage de mots
        wordcloud = WordCloud().generate(text)
        # enregistrer le nuage de mots dans un fichier image avec un nom de fichier aléatoire
        image_file = generate_random_filename()
        wordcloud.to_file(image_file)
        # générer un identifiant de session pour l'utilisateur
        session_id = generate_session_id()
        # ajouter le nom du fichier au dictionnaire des nuages de mots en utilisant l'identifiant de session comme clé
        wordclouds[session_id] = image_file
        # enregistrer l'identifiant de session dans un cookie
        response = make_response(redirect('/wordcloud'))
        response.set_cookie('session_id', session_id)
        return response

@app.route('/wordcloud')
def show_wordcloud():
    # récupérer l'identifiant de session depuis le cookie
    session_id = request.cookies.get('session_id')
    # vérifier si l'identifiant de session est valide
    if not verify_session_id(session_id):
        return 'Votre session a expiré ou est invalide.', 404
    # récupérer le nom du fichier du nuage de mots généré par l'utilisateur
    image_file = wordclouds.get(session_id)
    if image_file is None:
        return 'Aucun nuage de mots n\'a été généré pour votre session.', 404
    # lire l'image du nuage de mots
    with open(image_file, 'rb') as f:
        image = f.read()
    # renvoyer l'image au navigateur
    return image, 200, {'Content-Type': 'image/png'}

@app.route('/')
def home():
    return render_template('index.html')

# les autres routes de l'application (upload, wordcloud) restent inchangées

if __name__ == '__main__':
    app.run()