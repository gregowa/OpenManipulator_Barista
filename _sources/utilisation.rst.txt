Utilisation
==========

1. Ouvrir un nouveau terminal et **lancer ROS** : 

.. code-block::

    roscore

2. Reconstruire l'espace de travail depuis le dossier catkin_ws :  

.. code-block::

    catkin_make  
    clean catkin_make
    
3. Recharger l'espace de travail et permet d'exécuter la commande (à exécuter depuis catkin_ws, à faire à chaque fois que l'on lance un nouveau noeud ROS).

.. code_block::

    source devel/setup.bash 

4. Ouvrir un nouveau terminal et lancer le contrôleur de l'OpenManipulator : 

.. code-block::

    roslaunch open_manipulator_controller open_manipulator_controller.launch 

A l'exécution de cette commande, les moteurs devraient se raidir et des informations devraient défiler dans le terminal. 
Si les moteurs ne se raidissent pas, vérifier que la carte d'alimentation des moteurs est bien alimentée et que le bouton ON/OFF est bien enclenché.

5. Ouvrir un nouveau terminal et lancer la télécommande pour piloter l'OpenManipulator : 

.. code-block::

    roslaunch open_manipulator_teleop open_manipulator_teleop_keyboard.launch}

6. Tester l'ouverture de la pince par exemple, à l'aide de la télécommande teleop.


Création de noeuds ROS
______________________

Cette partie détaille la démarche pour implémenter ses propres fonctions pour le pilotage du robot. Les fonctions sont écrites en Python et seront placées dans des fichiers qui constitueront ensuite les différents noeuds à interfacer sous ROS.

* Créer un package dans un fichier au format XML placé dans le dossier source du projet (contenant le code des différents noeuds)

.. code-block::

    <?xml version="1.0"?>
    <package format="2">
    <name>robot_barista</name>
    <version>0.0.0</version>
    <description>The robot_barista package</description>

    <!-- One maintainer tag required, multiple allowed, one person per tag -->
    <!-- Example:  -->
    <!-- <maintainer email="jane.doe@example.com">Jane Doe</maintainer> -->
    <maintainer email="ubuntu@todo.todo">ubuntu</maintainer>


    <!-- One license tag required, multiple allowed, one license per tag -->
    <!-- Commonly used license strings: -->
    <!--   BSD, MIT, Boost Software License, GPLv2, GPLv3, LGPLv2.1, LGPLv3 -->
    <license>TODO</license>


    <!-- Url tags are optional, but multiple are allowed, one per tag -->
    <!-- Optional attribute type can be: website, bugtracker, or repository -->
    <!-- Example: -->
    <!-- <url type="website">http://wiki.ros.org/robot_barista</url> -->

* On pourra ensuite créer un launch file, ce fichier permet d'exécuter plusieurs noeuds ROS à la fois.
Exemple de launch file pour turtlesim : 

.. code-block::

    <launch>
    <node pkg="turtlesim" exec="turtlesim_node" name="sim" namespace="turtlesim1"/>
    <node pkg="turtlesim" exec="turtlesim_node" name="sim" namespace="turtlesim2"/>
    <node pkg="turtlesim" exec="mimic" name="mimic">
        <remap from="/input/pose" to="/turtlesim1/turtle1/pose"/>
        <remap from="/output/cmd_vel" to="/turtlesim2/turtle1/cmd_vel"/>
    </node>
    </launch>


Exemple de fonction écrite en Python et pouvant être implémentée dans un noeud ROS

.. code-block::
    
    def recherche_gobelet(color_id):
    # récupération du flux vidéo
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        rospy.logerr("Erreur : Impossible d'ouvrir la caméra.")
        return

    last_time = time.time()
    print("Appuyez sur 'q' pour quitter.")

    try:
        while True:
            x_coord = detect_color(cap, color_id)
            print(x_coord)
            # Tant que la couleur n'est pas détectée au centre de l'image (à +/- 150 pixels)
            if not (-150 <= x_coord <= 150):
                move_robot.move_joints_relative(-0.05, 0.0, 0.0, 0.0, 1.0) # Trajectoire circulaire
            else:
                break
            key = cv2.waitKey(5) & 0xFF
            if key == ord('q'):
                break
            time.sleep(0.35)
    except KeyboardInterrupt:
        print("Arrêt du programme.")
    finally:
        cap.release()
        cv2.destroyAllWindows()