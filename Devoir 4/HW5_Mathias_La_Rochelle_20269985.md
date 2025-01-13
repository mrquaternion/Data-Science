# HW5 Réponses courtes / HW5 Short Answers


**Name:** Mathias La Rochelle

**Matricule \#:** 20269985

**Veuillez écrire vos réponses courtes ci-dessous et les inclure dans votre soumission de gradescope. / Please write your short answers below and include this as part of your gradescope submission.**

**Le titre du rapport doit être HW5_{Votre_Nom}\_{Matricule_\#} / The title of the report should be HW5_{Your_Name}\_{Matricule_\#}**


## Question 2
J'utilisais déjà l'argument `--cache-from` alors pour moi, il y a toujours une seule image qui était construite à chaque fois que je soumettais un build. Mais de ce que j'ai compris, sans cet argument passé dans le fichier `cloudbuild.yaml`, deux images se construisaient à chaque fois (`build-image` et un des 4 autres images) ce qui devait alonger la période du processus de build. Cela ne doit pas être le cas quand nous avons besoin de construire notre `build-image` une seule fois, ce qui est notre cas. C'est à ce moment que nous pouvons utiliser le cache présent de `BASE_IMAGE_URI` du dernier build.

## Question 4
Je pourrais créer une image Docker qui contiendrait le modèle ResNet pré-téléchargé. Il sera donc mis dans le cache et comme à la Question 2, cela évitera de le téléchargé à chaque fois qu'un nouveau service sera déployé. Le build initial sera un peu plus long que les autres mais cela permettra d'avoir le modèle déjà dans notre conteneur.

## Question 5
Déployer les services backend et frontend séparément réflète (de proche) l'architecture à 3 niveaux (3-tier architecture, merci Génie logiciel). Cette approche permet d'anticiper toute modification qui sera fait au code des deux services. Séparés, ces modules ne dépendent pas l'un de l'autre et donc il est plus facile de faire des maintenances ou de scale les services sans que les bugs de l'un affecte l'autre. Ça permet aussi d'avoir plusieurs personnes à travailler parallèlement.

## Question 7
En fait, dans le cas de la version 1 de notre application, ce n'est pas un problème car il n'y aura jamais de conflits d'états une personne ou plus décident d'utiliser l'interface. Alors que dans la version 2, il y a plusieurs "états". Quand l'application Flask sera initialisée avec le modèle sélectionné par le premier utilisateur, il y aura des conflits si les autres utilisateurs sélectionnent par la suite un modèle différent au sien.

Pour corriger ce problème, nous pouvons, au niveau du frontend, allouer la gestion de sessions. Une session permet de stocker l'information relié à un utilisateur. Bien sûr dans notre cas, nous avons seulement besoin de stocker ces informations temporaires étant donné qu'elles ne sont pas nécessaires au fonctionnement ultérieur de l'application pour l'utilisateur en question. Dans ce contexte, la donnée propre à l'utilisateur serait le modèle qu'il aurait choisi dans l'interface.

Pour le backend, l'approche sera différente. On pourrait mettre en cache chaque modèle pour éviter qu'il soit chargé plus qu'une seule fois. De plus, chaque modèle va ainsi pouvoir continuer d'être disponible pour plusieurs requêtes d'utilisateurs.

## Question 8
De ce que je comprends, le code dans le modèle `v3` tente de résoudre le problème de la question précédente. Une passerelle API permet d'avoir une entrée unique pour toutes les requêtes des utilisateurs et ainsi les rediriger vers les microservices (architecture micro-services, merci Génie logiciel encore une fois). Dans notre cas, les microservices sont les différents modèles auquels un utilisateur peut avoir accès. De cette façon, chaque utilisateur va pouvoir utiliser l'interface de l'application et utiliser des modèles qui ne sont pas nécessairement les mêmes sans que de conflits ne se fassent.

## Question 9
Source unique de mes réponses : https://www.ibm.com/think/topics/quantization

La quantification est un bon outil d'optimisation pour réduire la charge de calcul et l'augmentation de la vitesse d'inférence des LLM. L'idée générale provient du fait que le processus de quantification tourne autour de la réduction des poids à un type de donnée moins précis (genre de `double` à `float`). Moins de précision (chiffres significatifs) amenera à un temps d'exécution plus faible.

Mais ce processus peut être très désavantageux. La quantification entraîne principalement une perte de précision dans les poids ce qui affectera l'exactitude des prédictions du LLM, ce que nous ne voulons généralement pas (dépend du contexte bien évidemment). Aussi, le processus de quantification est très demandant en termes de ressources (surtout QAT). Cependant il est plus facile à implémenter PTQ mais la perte de précision est plus grande que QAT alors son utilisation doit peut-être être remise en question. Dans les deux cas, il ne faut pas être surpris que le temps de calcul sera supérieur comparé à si on n'avait pas implémenté le processus de quantification.