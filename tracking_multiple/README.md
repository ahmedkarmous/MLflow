# scénario 1: 
Deux chercheurs enregistrent leurs données de tracking dans le même dossier

### scénario 1.1:
Deux chercheurs travaillent sur deux expérimentations différentes (noms différents):
- chaque expérimentation sera enregistré dans son propre dossier (ayant comme nom l'id de l'expérimentation)

### scénario 1.2: 
Deux chercheurs travaillent sur la même expérimentation (même nom)
- les runs des expérimentations (un dossier pour chaque run) seront enregistrés dans le même dossier (ayant comme nom l'id de l'expérimentation)


/!\ il faut ajouter les if (si les fichiers existent) dans logFromDir

- le chercheur peut importer une ou plusieurs experimentations
- les runs peuvent avoir le même nom (à régler)

détailler les scénarios: 
* X choisit une expérimentation à ajouter :
    - il spécifie son nom
    - il spécifie si c'est une nouvelle experimentation (elle n'existe pas sur le serveur)
    --->    - si elle existe dans son dossier local
            - si elle n'existe pas
            - si elle existe dans le serveur et qu'il a spécifé qu'elle est une nouvelle exp 
            - si elle n'existe pas mais il a specifié qu'elle n'est pas une nouvelle exp



des cas gérés: 
- exp spécifiée pas trouvée
- exp spécifiée trouvée mais sans runs
- exp nouvelle porte le nom d'une exp existante

cas à gérer (si c'est nécessaire) (si cela ne se fait pas, on peut ajouter les mêmes exp et les même runs plusieurs fois):
    - plusieurs exécutions (runs) avec le même nom
    - mlflow l'autorise
    - ce cas est géré pour les exp car si ce n'était pas géré, mlflow va    ajouter les exécutions de cet exp dans l'exp existante alors que le chercheur l'ajoute comme une nouvelle 
    - interdire cela va augmenter la complexité du code (il faut chercher le run selon le nom pour chacun avant de l'ajouter)
