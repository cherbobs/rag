# Projet RAG avec Ollama

Ce projet implémente un système de **génération augmentée par récupération (RAG)** en utilisant **Ollama** pour répondre à des questions basées sur des documents. Les utilisateurs peuvent interroger un modèle directement ou enrichir leurs questions avec un contexte extrait de documents locaux.

---

## **Table des matières**
- [Prérequis](#prérequis)
- [Structure des fichiers](#structure-des-fichiers)
- [Utilisation](#utilisation)
  - [Mode sans RAG](#mode-sans-rag)
  - [Mode avec RAG](#mode-avec-rag)
- [Commandes utiles](#commandes-utiles)
- [Dépannage](#dépannage)

---

## **Prérequis**

Avant d'exécuter le projet, assurez-vous que les conditions suivantes sont remplies :

1. **Environnement Python** :
   - Installez Python 3.8 ou une version ultérieure.
   - Créez un environnement virtuel :
     ```bash
     python -m venv .venv
     source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
     ```

2. **Installation des dépendances** :
   Installez les dépendances nécessaires via `pip` :
   ```bash
   pip install torch ollama numpy
   ```

3. **Serveur Ollama actif** :
   Assurez-vous que le serveur Ollama est démarré avant d'exécuter le script :
   ```bash
   ollama serve

4. **Modèles installés sur Ollama** :
   Vérifiez les modèles disponibles sur le serveur Ollama :
   ```bash
   ollama list

   Téléchargez les modèles nécessaires si besoin :
   ```bash
   ollama pull llama2


## **Structure des fichiers**
* **`localrag.py`** : Le script principal, permettant deux modes d'utilisation :  
  * **Sans RAG (`--mode no-rag`)** : Pose des questions directement au modèle.  
  * **Avec RAG (`--mode rag`)** : Utilise les documents locaux pour enrichir les réponses.  
* **`vault.txt`** : Un fichier texte contenant les documents locaux utilisés dans le mode **RAG**. Chaque ligne représente un document ou un fragment.

## **Utilisation**

### **Mode sans RAG**

Dans ce mode, les questions sont posées directement au modèle, sans utiliser de contexte supplémentaire :

bash

`python localrag.py --mode no-rag`

### **Mode avec RAG**

Dans ce mode, les réponses sont générées en utilisant le contenu de `vault.txt` comme contexte :

bash

`python localrag.py --mode rag`

---

## **Commandes utiles**

### **Lister les modèles disponibles**

bash

`ollama list`

### **Télécharger un modèle**

bash

`ollama pull <nom_du_modèle>`

Exemple :

bash

`ollama pull llama2`

### **Tester un modèle directement**

bash

`ollama generate -m <nom_du_modèle> "<votre_question>"`

Exemple :

bash

`ollama generate -m llama2 "Quel est le step ?"`

---

## **Dépannage**

### **Problème : Port déjà utilisé**

Si le port `11434` est occupé, identifiez le processus qui l'utilise :

bash

`netstat -ano | findstr :11434`

Terminez le processus correspondant avec son PID :

bash

`taskkill /PID <PID> /F`

Relancez ensuite le serveur Ollama :

bash

`ollama serve`

### **Problème : Modèle introuvable**

Si un modèle comme `llama2` ou `mistral` n'est pas trouvé :

Assurez-vous que le modèle est téléchargé :  
bash

`ollama pull llama2`

Vérifiez que le nom du modèle dans `localrag.py` correspond exactement à celui listé par `ollama list`.

---

## **Contributeurs**

* Développeur : \[cherbobs\]  
* Contact : \[e_cherbonnier@hetic.eu\]

