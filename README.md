# Projet Julia

Ce projet est une initiation à Julia. Il a pour but de réaliser l'analyse des structures des protéines avec Julia et de comparer avec ce qui ce fait en Python. Quelques exemples d'application ont été mis en place pour l'hémoglobine humaine (1A01) & bovine (2QSP) tels que la comparaison de séquences, de structures, etc.

## Cheat sheet

Le jupyter notebook `julia-cheat-sheet.ipynb` est un cheat sheet basé sur le livre [**Julia 1.0 Programming**](https://github.com/Pierre-damase/Projet-julia/blob/master/Doc/Julia1.0.pdf). Il présente les particularités de syntaxes de Julia ainsi que des comparaison de code entre Julia et python.

## Analyses

Les programmes mis en place (Julia, Python) permettent de réaliser les analyses suivantes:

- Lecture de fichier .pdb
- Visualisation de structures
- Alignement de séquences
- Comparaison de deux structures - alignement 3D & RMSD
- Carte de contacts

## Prérequis

L'utilisation de [Miniconda3](https://docs.conda.io/en/latest/miniconda.html) est fortement recommandée pour l'utilisation des différents programme mis en place (package python, jupyter lab).

Une instalation de julia est également nécessaire au préalable:

```
sudo apt install julia
```

## Quick start

1. Clone du répertoire github

> Lien HTTPS

```
https://github.com/Pierre-damase/Projet-julia.git
```

2. Initialiser l'environnement conda à partir du fichier julia.yml

L'environnement conda permet l'installation de tous les modules nécessaire pour le programme python ainsi que de jupyter lab.

```
conda env create --file julia.yml
```

3. Activer l'environnement conda

```
conda activate julia
```

4. Set up de Julia

Pour l'utilisation du kernel Julia avec jupyter lab et l'installation des différents packages veuillez exécuter les lignes de commande suivante dans un terminal:

```
julia
using Pkg
Pkg.add("IJulia")
Pkg.add("ArgParse")
Pkg.add("BioAlignments")
Pkg.add("BioStructures")
Pkg.add("Bio3DView")
Pkg.add("NaturalSort")
Pkg.add("Suppressor")
```

## Julia

Les différentes méthodes mise en place ont été codées dans le module **Prot**.

Il faut être situé dans le dossier ./Projet-julia/Code

1. Exemple intéractif

```
jupyter lab prot-jl.ipynb
```

2. Exécution via le script main.jl

```
julia main.jl -i ID -e ARG -a ALIGN -c CUTOFF
```

  - Arguments nécessaires
  
    - **ID**: l'id du/des fichier.s pdb à étudier
    - **ARG**: l'étude à réaliser - **view** pour la visualisation, **align** pour l'alignement de séquences, **rmsd** pour l'alignement de strucutres et le calcul du rmsd et **maps** pour générer la carte de contacts.
  
  - Arguments facultatifs
  
    - **ALIGN**: **global** pour un alignement global des protéines (défaut) & **region** pour un alignement global des régions
    - **CUTOFF**: le cutoff de la carte de contacts - entre 6 et 12A (vaut 10A par défaut)

## Python


Les différentes méthodes mise en place ont été codées dans le module **prot_py**.

Il faut être situé dans le dossier ./Projet-julia/Code

1. Exemple intéractif

```
jupyter lab prot-py.ipynb
```

2. Exécution via le module prot_py

L'instruction -m permet d'éxécuter prot_py en tant que module python.

```
python -m prot_py -i ID -e ARG -a ALIGN -c CUTOFF
```

  - Arguments nécessaires
  
    - **ID**: l'id du/des fichier.s pdb à étudier
    - **ARG**: l'étude à réaliser - **view** pour la visualisation, **align** pour l'alignement de séquences, **rmsd** pour l'alignement de strucutres et le calcul du rmsd et **maps** pour générer la carte de contacts.
  
  - Arguments facultatifs
  
    - **ALIGN**: **global** pour un alignement global des protéines (défaut) & **region** pour un alignement global des régions
    - **CUTOFF**: le cutoff de la carte de contacts - entre 6 et 12A (vaut 10A par défaut)

## Auteur

IMBERT Pierre
