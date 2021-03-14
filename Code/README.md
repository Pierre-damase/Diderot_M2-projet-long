Ce programme contient les différents jupyter notebook et programme mis en place, que ce soit en python ou en Julia.

**Julia**

* `Prot`: module qui contient l'ensemble des méthodes mises en place en Julia

* `main.jl`: fonction mise en place pour pouvoir éxécuter **Prot** dans le terminal

  * *cf*. la section Julia de https://github.com/Pierre-damase/Projet-julia/blob/master/README.md pour l'éxécution de ce programme.

* `benchmark_julia.jl`: programme d'évaluation des performances (temps d'éxécution) des méthodes mises en place dans **Prot**
  
  * Exécution: `julia benchmark_julia.jl`
  * Génère le fichier `benchmark-julia.txt` sauvegardé dans le fichier ./data

* `prot-jl.ipynb`: exemple intéractif de l'application du module **Prot**

***

**Python**

* `prot_py`: module qui contient l'ensemble des méthodes mises en place en python

  * *cf*. la section Python de https://github.com/Pierre-damase/Projet-julia/blob/master/README.md pour l'éxécution de ce module.

* `benchmark_python.py`: programme d'évaluation des performances (temps d'éxécution) des méthodes mises en place dans **prot_py**

  * Exécution: `python benchmark_python.jl`
  * Génère le fichier `benchmark-python.json` sauvegardé dans le fichier ./data

* `prot-py.ipynb`: exemple intéractif de l'application du module **prot_py**, génération des sous-structures pour le benchmark et réalisation des graphiques pour le benchmark

***

**data**

  * `alignements`: sauvegarde des alignements de séquences au format txt avec respect du format fasta, i.e. 80 caractères maximum par ligne 
  * `contact_maps`: sauvegarde des cartes de contacts au format .png (python) ou .txt (Julia)
  * `pdb`: contient les structures pdb téléchargées, `pdb/Becnhmark` contient les structures pdb pour le benchmark
  * `benchmark-julia.txt`: fichier généré par `benchmark_julia.jl`
  * `benchmark-python.json`: fichier généré `benchmark_python.py`
