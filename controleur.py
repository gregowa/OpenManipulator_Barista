#!/usr/bin/env python3
import rospy
from time import sleep 
from std_msgs.msg import Int32
import fct_couleurs
import move_robot
import cv2

# Fonction service d'un cocktail
# id0, id1, id2 : numéro des ingrédients = couleurs à détecter
def coktail(id0,id1,id2):
	ingredients = [id0,id1,id2]
	for ing in ingredients:
		move_robot.home_pos(1.0)
		sleep(1)
		fct_couleurs.recherche_gobelet(ing)
		sleep(1)
		move_robot.effector_open()
		move_robot.take_pos(2.0)
		sleep(1)
		move_robot.serv_pos(2.0)
		sleep(3)
		move_robot.throw_pos(1.0)
		sleep(1)
		move_robot.home_pos(1.0)

# Programme principal	
def main():
	choice = -1
	while choice != 100:    
		# Interface graphique		
		print("Sélectionneez un programme :")
		print("0: home to serv")
		print("\n CHOIX D'UN COCKTAIL : \n")
		print("1: Mojito")
		print("2: Gin Tonic")
		print("3: Long Island \n")
		print("10: Position service")
		print("11: Ouvrir pince")
		print("12: Fermer pince")
		print("100: quitter")
		choice = int(input("Entrez le n de programmme :"))
		
		if choice == 0:
			move_robot.home_pos(1.0)
			print("Robot en position initiale")
		elif choice == 1:
			print("Vous avez choisi un Mojito")
			coktail(1,2,3)
			print("Boisson prête")
		elif choice == 2:
			print("Vous avez choisi un Gin Tonic")
			coktail(1,3,4)
			print("Boisson prête")
		elif choice == 3:
			print("Vous avez choisi un Long Island")
			coktail(2,3,4)
			print("Boisson prête")
		elif choice == 10:
			move_robot.serv_pos(3.0)
		elif choice == 11:
			move_robot.effector_open()
		elif choice == 12:
			move_robot.effector_close()
		elif choice == 13:
			fct_couleurs.recherche_gobelet(1)
			

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
		
