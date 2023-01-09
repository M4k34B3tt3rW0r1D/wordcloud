# wordcloud - Nuage de mot
### en
What does that code ?
This web application allow a user to load a docx or pdf file and generate a wordcloud from it.
The code is very simple and needs customization if you want something to your image. 
### fr
A quoi sert ce code ?
Cette application web permet à un utilisateur de charger un fichier docx ou pdf et de générer un nuage de mots à partir de celui-ci.
Le code est très simple et nécessite une personnalisation si vous voulez quelque chose à votre image et plus robuste. 

## Getting Started
To run the code :
Pour executer le code:
```shell
python app.py
```
## Docker ?
### en
you can also run the app in a docker container by mounting a volume
first you'll need to build the image, then run in a container

### fr
vous pouvez aussi exécuter l'application dans un conteneur docker en montant un volume
Vous devrez d'abord construire l'image, puis l'exécuter dans un conteneur.
```shell
docker build -t myapp .
docker run -p 5000:5000 -v /path/to/app:/app myapp
```

# Author
Cyberlife
M4k34B3tt3rW0r1D