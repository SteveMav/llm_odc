# Exercice 1 : Conception d'Agents avec LangGraph et LangChain

Ce projet présente plusieurs démonstrations de patrons de conception d'agents (Agentic Design Patterns) construits avec **LangGraph** et **LangChain**, connectés à un LLM local.

## Table des Contents
- [Description](#description)
- [Architecture & Patrons de Conception](#architecture--patrons-de-conception)
- [Prérequis](#prérequis)
- [Installation et Configuration](#installation-et-configuration)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)

---

## Description

L'objectif de ce projet est de concevoir et structurer des flux de travail autonomes basés sur des graphes d'états (State Graphs). Le projet utilise un modèle de langage (Qwen) hébergé localement avec **LM Studio** pour exécuter les tâches sans dépendre d'API payantes en ligne.

---

## Architecture & Patrons de Conception

Les exemples sont principalement implémentés dans le notebook `workshop(1).ipynb` et couvrent :

1. **Sortie Structurée (Structured Output)** :
   Utilisation de modèles Pydantic pour forcer le LLM à formater sa réponse sous forme d'un objet JSON strict (par exemple pour générer des requêtes de recherche et des justifications).

2. **Patron 1 : Prompt Chaining (Enchaînement de Prompts)** :
   - Génération d'une blague sur un thème donné.
   - Routage conditionnel automatique (`check_punchline`) : le graphe vérifie la présence d'une punchline. Si elle est manquante, il redirige la blague vers un nœud d'amélioration (`improve_joke`), puis de finition (`polish_joke`).

3. **Patron 2 : Parallélisation (Parallelization)** :
   - Exécution de 3 appels LLM parallèles pour générer simultanément une blague, une histoire et un poème.
   - Un nœud agrégateur (`aggregator`) attend la complétion des trois tâches pour fusionner les résultats dans l'état final.

4. **Patron 3 : Générateur-Évaluateur (Generator-Evaluator)** :
   - Un générateur produit une blague.
   - Un évaluateur analyse la blague de manière structurée (`grade` et `feedback`).
   - Le dictionnaire d'état transmet les retours au générateur pour réécrire la blague en boucle si elle n'est pas jugée drôle.

---

## Prérequis

- **Python** `>= 3.14`
- Le gestionnaire de paquets **uv** (recommandé pour une installation rapide et la gestion du fichier de verrouillage `uv.lock`)
- **LM Studio** configuré avec le modèle `qwen3-1.7b@q6_k` (ou un autre modèle équivalent).

---

## Installation et Configuration

### 1. Cloner et installer les dépendances
Utilisez `uv` pour synchroniser le projet et installer l'environnement virtuel automatiquement :
```bash
# Installer l'environnement virtuel et les dépendances
uv sync
```

Les dépendances majeures déclarées dans `pyproject.toml` sont :
- `langchain`
- `langgraph`
- `langchain-openai`
- `notebook` (Jupyter)

### 2. Configurer LM Studio
1. Téléchargez et ouvrez **LM Studio**.
2. Récupérez le modèle `qwen3-1.7b@q6_k` (ou le modèle de votre choix).
3. Lancez le **Local Server** sur le port `1234` (l'API de base doit correspondre à `http://127.0.0.1:1234/v1`).

---

## Utilisation

Pour lancer et explorer les notebooks de démonstration :

```bash
# Lancer l'interface Jupyter Notebook
uv run jupyter notebook
```

Ouvrez ensuite le fichier principal [workshop(1).ipynb](file:///C:/Users/Salem/Documents/aiot/exercice%201/workshop(1).ipynb) depuis l'interface de votre navigateur.

---

## Structure du Projet

- **`workshop(1).ipynb`** : Le notebook principal contenant les implémentations pas à pas des graphes LangGraph et des sorties structurées.
- **`v.ipynb`** : Un notebook de test pour valider l'extraction structurée Pydantic.
- **`main.py`** : Script d'entrée standard simple servant de test d'exécution.
- **`pyproject.toml`** : Fichier de configuration du projet et liste des dépendances Python.
- **`uv.lock`** : Fichier de verrouillage des dépendances généré par `uv`.
- **`README.md`** : Ce document.
