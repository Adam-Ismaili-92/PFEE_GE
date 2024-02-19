# PFEE_GE

AUTHORS : 
- Adam ISMAILI
- Louis RIBAULT
- Rémi MONTEIL
- William HUANG

Notre projet, en collaboration avec l'entreprise "GE HEALTHCARE", consiste en la génération de modèles numériques corps focalisés sur les os.

Pour cela, nous avons réalisé une segmentation par classe, un calcul de densités/coefficients d'attenuation par voxel, et un calcul de positions par volume.

Le dataset est trouvable sur le site [wiki.cancerimagingarchive.net](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=61080890).

Le notebook contient l'essentiel de la pipeline du projet.

Il présente les fonctions suivantes : 
- "print_3_slices" permettant d'afficher 3 slices d'un volume suivant l'indice de la slice de départ et l'axe de coupe (allant de 1 à 3).
- "load_volume_data" permettant de charger un volume nii et son tableau de donnée à partir de son path.
- "segmentation_bone_class" permettant la segmentation des os, à partir d'un flou gaussien, d'un seuillage hystérésis (bas : 200 HU, haut : 500 HU), de morphologie mathématiques (closing), et d'un épaississement des contours.
- "segmentation_tissue_class" permettant la segmentation des tissues, à partir d'un seuillage à -120 HU, de morphologie mathématiques (closing), et de remplissage des contours.
- "segmentation_air_class" permettant la segmentation de l'air/des poumons, à partir d'un seuillage à -120 HU et de morphologie mathématiques (closing).
- "segmentation_class" regroupant toutes les fonctions de segmentation précédentes et sommant leur résultat pour une segmentation de classe complète, allant de 0 à 4 (0 : background, 1 : air, 2 : tissue, 3 : os trabéculaire, 4 : os cortical).
- "segmentation_densities" permettant le calcul des valeurs de densités pour chaque voxel.
- "segmentation_positions" permettant le calcul des positions (repère + taille d'un voxel en mètres) pour chaque volume. Le repère est acquis en calculant la moyenne des indices des voxels du poumon droit. A NOTER : Le repère est pour l'instant toujours situé sur le poumon droit.
- "segmentation_pipeline" regroupant toutes les fonctions de segmentation de classe et de calcul de densités/positions en une pipeline complète. L'objet retourné est une instance de la classe "segmentation". "segmentation.classes" permet d'obtenir un volume de segmentation de classes, et "segmentation.densities()" permet d'obtenir un volume de densités, "segmentation.densities(False) permet d'obtenir un volume de coefficients d'atténuation, "segmentation.positions" permet d'obtenir un tuple de positions ("segmentation.positions[0]" pour obtenir la taille d'un voxel, "segmentation.positions[1]" pour obtenir le repère).

Ces fonctions sont réparties dans les fichiers de l'application situés dans le dossier "App/". L'application est exécutable par la commande "python segmentation_app.py".

Notre dossier git présente les fichiers suivants :
- "PFEE_Pipeline.ipynb" est le notebook contenant la pipeline complète du projet.
- "App/" est le dossier contenant les fichiers permettant de lancer l'application du projet.
- "OrganSegmentations/" est le dossier contenant des volumes d'entrée à tester pour l'application ou le notebook.
- "loaded_3D_image_examples/" est le dossier où sont chargés les volumes segmentés resultants du notebook.
- "result/" est le dossier où sont chargés les fichiers résultants de l'application.
- "linear_relationship_densities.png" est le schéma utilisé dans le notebook pour illustrer les relations linéaires entre la densité et les valeurs HU.
- "pipeline_schema.png" est le schéma utilisé dans le notebook pour illustrer le déroulement de la pipeline.
