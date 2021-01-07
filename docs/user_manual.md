# Plugin QGIS
## Barre d'outils
Le plugin, une fois installé, ajoute une barre d'outils à l'interface QGIS,
composée de plusieurs boutons qui permettent d'effectuer différentes
opérations.

<figure>
  <img src="../assets/toolbar.png" width="300" />
  <figcaption>Barre d'outils du plugin</figcaption>
</figure>

Les outils sont, dans l'ordre :

- Connection DB
- Créer un nouveau comptage
- Modifier un comptage
- Importation données
- Validation données
- Filtrage
- Importation fichiers ICS
- Réglages

## Utilisation
### Connection DB
<figure>
  <img src="../assets/power.png" width="80" />
  <figcaption>Bouton connection DB</figcaption>
</figure>

Le bouton `Connection DB` ouvre une connexion à la base de données et charge
les couches de l'application dans QGIS.

<figure>
  <img src="../assets/layers.png" width="300" />
  <figcaption>Couches dans QGIS</figcaption>
</figure>

### Créer un nouveau comptage
<figure>
  <img src="../assets/measure.png" width="80" />
  <figcaption>Bouton creation nouveau comptage</figcaption>
</figure>

Pour créer un nouveau comptage (élément dans la couche `comptage`), il
existe l'outil `Créer un nouveau comptage` qui simplifie l'opération par
rapport à l'insertion manuelle dans la table.

Pour créer un nouveau comptage à l'aide de l'outil, vous devez commencer par
sélectionner un tronçon sur la carte en utilisant les outils de sélection de
géométrie QGIS normaux. Pour simplifier la recherche du tronçon à
sélectionner, vous pouvez utiliser l'outil de recherche dans la couche
`tronçon`.

Une fois que vous avez sélectionné le tronçon pour lequel vous voulez créer
le comptage, en appuyant sur le bouton `Créer un nouveau comptage` vous
pouvez entrer les données du comptage et les sauvegarder dans la base de
données.

<figure>
  <img src="../assets/create_measure.gif" width="800" />
  <figcaption>Creation d'un nouveau comptage</figcaption>
</figure>

### Modifier comptage
<figure>
  <img src="../assets/select_edit.png" width="80" />
  <figcaption>Bouton modifier comptage</figcaption>
</figure>

Après avoir sélectionné un tronçon sur la carte, appuyer sur le bouton
`Modifier comptage` affiche le tableau d'attributs de la couche `comptage` avec
les comptages du tronçon sélectionné où vous pouvez éditer les données du
comptage.

<figure>
  <img src="../assets/edit_measure.gif" width="800" />
  <figcaption>Modification d'un comptage</figcaption>
</figure>

### Importation
<figure>
  <img src="../assets/import.png" width="80" />
  <figcaption>Bouton importation données</figcaption>
</figure>

### Validation
<figure>
  <img src="../assets/validate.png" width="80" />
  <figcaption>Bouton validation</figcaption>
</figure>

### Filtrage
<figure>
  <img src="../assets/filter.png" width="80" />
  <figcaption>Bouton filtrage</figcaption>
</figure>

### Importation fichiers ICS
<figure>
  <img src="../assets/calendar.png" width="80" />
  <figcaption>Bouton importation fichiers ICS</figcaption>
</figure>

### Réglages
<figure>
  <img src="../assets/settings.png" width="80" />
  <figcaption>Bouton réglages</figcaption>
</figure>

### Exporter la configuration
### Créer un rapport
### Créer un plan de pose
### Visualiser les graphiques d'un comptage
