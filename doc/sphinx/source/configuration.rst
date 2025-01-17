Configuration
============

Cette section explique comment installer et configurer les différents éléments du projet.

Configuration de la Raspberry
----------------------

Pour ce projet, nous sommes partis d'une Rasberry Pi 4 et d'une carte SD neuve sur laquelle aucun système d'exploitation n'avait été installé. Les étapes de configuration de la Rasberry Pi sont détaillés dans cette partie.

1. Installation de Ubuntu Lite via Pi Imager : la version Desktop souhaitée pour utiliser le bras robot OpenManipulator sous ROS Noetic n'étant pas disponible, on doit installer la version Lite (sans interface graphique).
2. Branchement de la Rasberry à un clavier, un écran et une souris
3. Création d'un mot de passe
4. Configuration du clavier en azerty
5. Configuration de la connexion internet :  Modifier le fichier netplan avec le nom du réseau auquel se connecter + sudo netplan apply une fois les modifications terminées
6. Vérifier que la connexion est active : Commande ip a pour voir si la connexion est active, si à l'état down :

.. code-block::

   sudo ip linksetwlan0 up

7. Récupérer les mises à jour nécessaires : 

.. code-block::

	sudo apt update
	sudo apt upgrade

8. sudo kill-9 <PID> : pour arrêter les processus qui tournent et produisent des erreurs (PID : remplacer par l'ID du processus obtenu avec la commande ps -e | grep <process\_name>)
9. Installer Ubuntu desktop et reboot la Rasberry pour que la configuration se mette à jour
10. Installer ROS + VS code et Python directement dans VS code


Configuration pour la PiCamera
----------------------

Pour la PiCamera, les étapes d'installation sont détaillées dans ce tutoriel : 
`<https://chuckmails.medium.com/enable-pi-camera-with-raspberry-pi4-ubuntu-20-10-327208312f6e>`_.

.. note::

	La résolution de l'erreur suivante est également détaillée : “Your firmwave appears to be out of date (no start_x.elf). Please update”

Configuration pour l'OpenManipulator
----------------------

1. Installation de ros2launch
2. Installation des outils pour OpenManipulator
3. Aller au bashrc

.. code-block::
	source~/.bashrc 

4. sudo apt-get install ros-noetic-ros-controllers ros-noetic-gazebo* ros-noetic-moveit* ros-noetic-industrial-core
5. sudo apt install ros-noetic-dynamixel-sdk ros-noetic-dynamixel-workbench*
6. sudo apt install ros-noetic-robotis-manipulator
7. Installer catkin et configurer le dossier catkin_ws/src

**Erreur** rencontrée lors du catkin_make

**Solution** : installation de python3-catkin-tools + réinstallation de tous les packages ROS Noetic. 
Attention, l'installation peut bloquer en court de route à cause de ressources insuffisantes 
(blocage à 50-60% de l'installation dans notre cas). 
Pour éviter de faire surchauffer la carte et de permettre à l'installation d'aboutir : 

* Utiliser une alimentation sur secteur (chargeur USB-C 2A) plutôt que sur le port USB d'un ordinateur.
* Changement de la fréquence d'horloge du CPU à 1500 Hz + catkin_make avec l'option -j1 (réduit le nombre de tâches parallèles) : résoud le problème et va au bout de l'installation dans notre cas.