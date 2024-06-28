# scénario 1: 
Deux chercheurs enregistrent leurs données de tracking dans le même dossier

### scénario 1.1:
Deux chercheurs travaillent sur deux expérimentations différentes (noms différents):
- chaque expérimentation sera enregistré dans son propre dossier (ayant comme nom l'id de l'expérimentation)

### scénario 1.2: 
Deux chercheurs travaillent sur la même expérimentation (même nom)
- les runs des expérimentations (un dossier pour chaque run) seront enregistrés dans le même dossier (ayant comme nom l'id de l'expérimentation)


/!\ il faut ajouter les if (si les fichiers existent) dans logFromDir