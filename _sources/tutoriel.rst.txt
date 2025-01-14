Installation
============

Cette section explique comment installer LaTeX.

Configuration de la Raspberry
----------------------

Pour ce projet, nous sommes partis d'une Rasberry Pi 4 et d'une carte SD neuve sur laquelle aucun système d'exploitation n'avait été installé. Les étapes de configuration de la Rasberry Pi sont détaillés dans cette partie.

1. Installation de Ubuntu Lite via Pi Imager : la version Desktop souhaitée pour utiliser le bras robot OpenManipulator sous ROS Noetic n'étant pas disponible, on doit installer la version Lite (sans interface graphique).
2. Branchement de la Rasberry à un clavier, un écran et une souris
3. Création d'un mot de passe
4. Configuration du clavier en azerty
5. Configuration de la connexion internet :  Modifier le fichier netplan avec le nom du réseau auquel se connecter + sudo netplan apply une fois les modifications terminées
6. Vérifier que la connexion est active : Commande ip a pour voir si la connexion est active, si à l'état down : sudo ip linksetwlan0 up
7. Récupérer les mises à jour nécessaires : sudo apt update sudo apt upgrade
8. sudo kill-9 <PID> : pour arrêter les processus qui tournent et produisent des erreurs (PID : remplacer par l'ID du processus obtenu avec la commande ps -e | grep <process\_name>)
9. Installer Ubuntu desktop et reboot la Rasberry pour que la configuration se mette à jour
10. Installer ROS + VS code et Python directement dans VS code


Configuration pour la PiCamera
----------------------

VSCode est un éditeur de code open-source développé par Microsoft. Il est très populaire parmi les développeurs pour sa facilité d'utilisation et ses nombreuses fonctionnalités et comporte une extension pour LaTeX : *LaTeX Workshop*.

.. note::
   Pour installer VSCode, vous devez d'abord télécharger le logiciel sur le site officiel.
   `<https://code.visualstudio.com/download>`_

.. warning::
   Lors de l'installation, cochez la case *Add to PATH* pour ajouter VSCode à votre PATH.

Configuration pour l’OpenManipulator
------------------------------

Il existe une extension pour VSCode appelée *LaTeX Workshop* qui facilite l'utilisation de LaTeX dans VSCode. Pour l'installer, suivez les étapes suivantes :
   - Ouvrez VSCode.
   - Cliquez sur l'icône des extensions dans la barre latérale.
   - Recherchez *LaTeX Workshop*.
   - Cliquez sur *Install*.
   - Redémarrez VSCode.

.. note::
   James-Yu.latex-workshop