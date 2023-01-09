FROM python:3.10

# installer les bibliothèques nécessaires
RUN pip install flask wordcloud PyPDF2 docx2txt itsdangerous

# copier le code de l'application dans le répertoire de travail si on utilise pas de volume
# COPY . /app
# WORKDIR /app

# exposer le port 5000 sur lequel l'application Flask écoute
EXPOSE 5000

# définir l'entrypoint de l'application
ENTRYPOINT ["python"]
CMD ["app.py"]