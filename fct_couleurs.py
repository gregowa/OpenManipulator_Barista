#!/usr/bin/env python3

import rospy
#from geometry_msgs.msg import Point
import cv2
import numpy as np
import time
#import argparse
#from std_msgs.msg import Int32
import move_robot

  
  # Fonction de traitement d'image pour détecter une couleur sur l'image  
def detect_color(cap, color_id):
    ret, frame = cap.read()
    if not ret:
        rospy.logerr("Erreur : Impossible de lire l'image de la caméra.")
        return []

    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if color_id == 1:  # Rouge
        lower_1 = np.array([0, 120, 70])
        upper_1 = np.array([10, 255, 255])
        lower_2 = np.array([170, 120, 70])
        upper_2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_1, upper_1)
        mask2 = cv2.inRange(hsv, lower_2, upper_2)
        mask = cv2.bitwise_or(mask1, mask2)
    elif color_id == 2:  # Bleu
        lower = np.array([100, 70, 30])
        upper = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
    elif color_id == 3:  # Jaune
        lower = np.array([20, 100, 100])
        upper = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
    elif color_id == 4:  # Vert foncé
        lower = np.array([40, 150, 20])
        upper = np.array([80, 255, 100])
        mask = cv2.inRange(hsv, lower, upper)
    else:
        rospy.logerr("Erreur : Identifiant de couleur invalide.")
        return []
	
    # Apllication d'un filtre et recherches d'un contour fermé de la couleur spécifiée
    mask = cv2.GaussianBlur(mask, (9, 9), 0)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    coordinates = [(1000,1000)]
    x_centered = 1000

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 10000:
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            circularity = (4 * np.pi * area) / (perimeter * perimeter)
            if circularity > 0.5:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    x_centered = cX - frame_width // 2
                    y_centered = cY - frame_height // 2
                else:
                    x_centered, y_centered = 0, 0
                coordinates.append((x_centered, y_centered))
                
                # Dessiner les contours et le point de centre
                cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
                cv2.circle(frame, (cX, cY), 7, (255, 0, 0), -1)
                cv2.putText(frame, f"({cX}, {cY})", (cX + 10, cY + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Affichage du flux vidéo avec les annotations
    #cv2.imshow('Retour caméra', frame)

    return x_centered

# Fonction de recherche d'un gobelet de couleur
# Balaye l'espace autour du robot (trajectoire circulaire) 
# S'arrête quand la couleur est détectée

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

if __name__ == "__main__":
    main()
