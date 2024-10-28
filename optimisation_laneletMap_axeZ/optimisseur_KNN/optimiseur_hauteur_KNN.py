import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import csv
import time



#########################################################################################################


input_traj = "traj.csv"
input_lanelet2 = "Test.osm"


#########################################################################################################



def filtre_1d(n):
    return np.ones(n)*(1/n) , n

def convolution_1d_padding(input,kernel=10,mode="full"):
	"""
	entree: tableau 1d (python-list)
	sortie :tableau convolué 1d (python-list)
	"""
	entree = input[:]
	print("entree",len(input))

	filtre,_  = filtre_1d(kernel)
	for i in range(kernel):
		entree.insert(0,entree[0])
		entree.append(entree[-1])
	sortie = np.convolve(entree,filtre,mode)
	# sortie = sortie[:(-(kernel-1))]
	sortie = sortie[(kernel):-((2*kernel-1))]
	# sortie = sortie[(kernel//2):(-(kernel//2-1))]

	print("sortie",len(sortie))
	return sortie

def print_c(clignotant):
    clignotant = str(clignotant)
    # os.system("clear")
    print("\033[5;34;42m"+clignotant+"\033[0m", end='\r')

def print_reussi(reussi):
    reussi = str(reussi)
    print("\033[1;32;47m"+reussi+"\033[0m")


#########################################################################################################

def matching_traj_lanelet(input_traj,points_lanelet) ->dict:
	"""
	min_dega: degalage minimum négligable, dans ce cas là utilise plustot le valeur qui viens de la nuage de points
	"""
	points_traj = []
	ligne1 = True
	dico_id_z = {}
	min_dega = 0.1				#TODO
	zlist_traj = []

	with open(input_traj, encoding='utf-8-sig') as f:
		for row in csv.reader(f, skipinitialspace=True):
			point_traj = []
			if ligne1 :
				ligne1 = False
				continue
                
			point_traj.append(float(row[0]))
			point_traj.append(float(row[1]))
			point_traj.append(float(row[2]))
			points_traj.append(point_traj)
			zlist_traj.append(float(row[2]))
			point_traj = []
                  
	f.close()

	x = np.array(range(len(zlist_traj)))
	y = np.array( zlist_traj )

	plt.xlabel("Numéro",fontdict={'size': 16})
	plt.ylabel("Z",fontdict={'size': 16})
	plt.title("hauteur_de_chaque_points",fontdict={'size': 16})
	plt.xticks([])
	plt.yticks([])
	plt.subplot(2,1,1)
	plt.plot(x, y, color = 'r')

	# return dico_id_z
	print_reussi("Les fichiers sont bien chargés")

	
	"""
	# gilsser le trajectoire ci besoin (avec convolution_1d_padding) TODO
	# zlist_traj_N = convolution_1d_padding(zlist_traj)
	# for i in range(len(points_traj)) :
	# 	points_traj[i][2] = zlist_traj_N[i]

	# y2 = np.array( zlist_traj_N )
	# plt.subplot(2,1,2)
	# plt.plot(x, y2, color = 'g')
	"""


	plt.show()



	print_c("####### En train de Matching  #############")


	for point_lanlet in points_lanelet :
		z_optimised,drapeau = KNN_traj(point_lanlet,points_traj)
		if ((z_optimised-point_lanlet[3])**2)**0.5 >= min_dega and drapeau:
			dico_id_z[point_lanlet[0]] = z_optimised
		else: 
			pass

					
	# print(points_traj)
	return dico_id_z
#########################################################################################################

def KNN_traj(p1,p_s) ->float | bool :
	"""
	p1: point de lanelet2
	p_s: points de trajectoire
	max_distance: un seuil de distance maximum afin de définir qui sont les neighhbours.
	"""
	max_distance = 30			#TODO
	distance = []
	for p2 in p_s:
		distance1 = ((p2[0]-p1[1])**2+(p2[1]-p1[2])**2)**0.5
		distance.append(distance1)
	
	min_value = min(distance)
	if  min_value >= max_distance:
		return 0,False
	else:
		min_idx = distance.index(min_value) 
	
	return (p_s[min_idx][2]-0.26), True




#########################################################################################################
print("####### Chargement les fichiers #############")

start = time.time()

domTree = ET.parse(input_lanelet2)
root = domTree.getroot()


points = []

nodes = root.findall("node")
# tags = root.findall("tag")

for node in nodes:
	point = []
      
	iD = node.get("id")
	iD = int(iD)
	point.append(iD)

	axeX = node[0].get("v")
	axeX = float(axeX)
	point.append(axeX)

	axeY = node[1].get("v")
	axeY = float(axeY)
	point.append(axeY)

	axeZ = node[2].get("v")
	axeZ = float(axeZ)
	point.append(axeZ)
      
	points.append(point)
	point = []
      
# print(points)


dico_id_z = matching_traj_lanelet(input_traj,points)


print_reussi("--------- Création le nouveau Lanelet2 ------------")
#################################### ----OUT PUT---- #######################################################
num_total = 0
num_modifi = 0

for node in nodes:
	num_total += 1
	iD_r = node.get("id")
	iD_r = int(iD_r)
	if iD_r in dico_id_z.keys(): 
		node[2].set("v", str(dico_id_z[iD_r])  )
		num_modifi += 1
	else:
		continue
    
domTree.write("out.osm",encoding="utf8")
print("Il y a %d points 3d total, dont %d points 3d sont déplacés"%(num_total,num_modifi))


end = time.time()
print("Temps d'éxecusion: "+str(end-start)+" s\n")
#########################################################################################################






