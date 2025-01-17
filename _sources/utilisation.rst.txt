Utilisation
==========

1. Ouvrir un nouveau terminal et **lancer ROS** : roscore
2. Reconstruire l'espace de travail depuis le dossier catkin_ws :  

.. code-block::
    catkin_make  
    clean catkin_make
    
3. Recharger l'espace de travail et permet d'éxecuter la commande (à exécuter depuis catkin_ws, à faire à chaque fois que l'on lance un nouveau noeud ROS).

.. code_block::
    source devel/setup.bash 
    
4. Ouvrir un nouveau terminal et lancer le contrôleur de l'OpenManipulator} : 

.. code-block::
    roslaunch open_manipulator_controller open_manipulator_controller.launch . 

A l'exécution de cette commande, les moteurs devraient se raidir et des informations devraient défiler dans le terminal. 
Si les moteurs ne se raidissent pas, vérifier que la carte d'alimentation des moteurs est bien alimentée et que le bouton ON/OFF est bien enclenché.
5. Ouvrir un nouveau terminal et lancer la télécommande pour piloter l'OpenManipulator : 

.. code-block::
    roslaunch open_manipulator_teleop open_manipulator_teleop_keyboard.launch}

6. Tester l'ouverture de la pince par exemple, à l'aide de la télécommande teleop.


Création de noeuds ROS
______________________

Cette partie détaille la démarche pour implémenter ses propres fonctions pour le pilotage du robot. Les fonctions sont écrites en Python et seront placées dans des fichiers qui constitueront ensuite les différents noeuds à interfacer sous ROS.