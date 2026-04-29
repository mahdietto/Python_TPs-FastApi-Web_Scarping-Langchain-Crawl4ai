#  Advanced Python TPs

Ce repository contient les travaux pratiques réalisés dans le cadre du module **Advanced Python**.

##  Structure du projet

```
advanced-python-tp/
│
├── tp1_fastapi_postgresql/
├── tp2_web_scraping/
├── tp3_langchain/
├── tp4_crawl4ai/
```

---

#  TP1 — FastAPI + PostgreSQL

##  Objectif

Créer une API REST avec FastAPI connectée à une base de données PostgreSQL.

##  Fonctionnalités

* Création de questions avec choix (POST)
* Récupération des questions (GET)
* Suppression (DELETE)
* Utilisation de SQLAlchemy (ORM)

##  Lancer le projet

```
uvicorn main:app --reload
```

---

#  TP2 — Web Scraping

##  Objectif

Extraire et analyser des données depuis un site web.

##  Fonctionnalités

* Scraping avec requests & BeautifulSoup
* Analyse de mots-clés
* Génération de graphique (matplotlib)
* API FastAPI (`/scraping`)

##  Lancer

```
python scraper.py
```

ou

```
uvicorn api_scraper:app --reload
```

---

#  TP3 — LangChain

##  Objectif

Utiliser les modèles LLM avec LangChain.

##  Contenu

* Génération simple avec LLM
* Prompt Templates
* Structured Output (Pydantic)
* AI Agent avec outils (Search + Calculator)

##  Configuration

Ajouter votre clé API :

```
GROQ_API_KEY=your_key_here
```

---

#  TP4 — Crawl4AI

##  Objectif

Crawler des pages web avec différentes stratégies.

##  Contenu

* Crawl simple (single page)
* Crawl séquentiel (multi-pages)
* Crawl parallèle (asyncio)

##  Installation

```
pip install crawl4ai
crawl4ai-setup
```

---

# Installation globale

```
pip install -r requirements.txt
```

---

#  Auteur

* Nom : Fedi Saadly
* Formation : ISET Tozeur — Technologies de l'Informatique

---

#  Remarque

Ce projet couvre :

* API Development (FastAPI)
* Databases (PostgreSQL)
* Web Scraping
* AI (LangChain)
* Async Crawling (Crawl4AI)

---

#  Conclusion

Projet complet couvrant plusieurs technologies avancées en Python, avec une approche pratique et modulaire.
