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


il faut écrire un jeu de test 


