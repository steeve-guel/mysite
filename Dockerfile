# 1. Utiliser une image Python officielle et légère
FROM python:3.14-slim

# 2. Éviter que Python crée des fichiers de cache .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Définir le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 4. Installer les outils système requis pour compiler Pillow (gestion des images)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copier d'abord le fichier requirements.txt pour installer les dépendances
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirement.txt

# 6. Copier tout le reste du code de ton projet (tes dossiers, ton modèle .joblib)
COPY . /app/

# 7. Exposer le port de l'application
EXPOSE 8000

# 8. Commande pour démarrer Django avec le serveur de production Gunicorn
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]