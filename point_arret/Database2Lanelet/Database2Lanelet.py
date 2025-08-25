import xml.etree.ElementTree as ET
import json
import yaml
import time
import mgrs
import math





#########################################################################################################


input_lanelet2 = "/home/hongyu/python_ws/point_arret/Database2Lanelet/lanelet2_map.osm"
input_missionDatabase = "/home/hongyu/python_ws/point_arret/Database2Lanelet/mission_database.json"
useYaw = True	# actuellement le translation n'est pas précis (a cause du lib mgrs sous python unité minmum = 1m)
largeurArret = 2.2
longeurArret = 4

useMapProjector = True # utilise le mapProjector pour verifier le calcule du convertissement MGRS cette etape n'est pas néssesaire
input_mapProjector = "/home/hongyu/python_ws/point_arret/Database2Lanelet/map_projector_info.yaml"

#########################################################################################################

def print_c(clignotant):
    clignotant = str(clignotant)
    # os.system("clear")
    print("\033[5;34;42m"+clignotant+"\033[0m", end='\r')

def print_reussi(reussi):
    reussi = str(reussi)
    print("\033[1;32;47m"+reussi+"\033[0m")

def pretty_xml(element, indent='\t', newline='\n', level=0) -> None:  
	if element: 
		if (element.text is None) or element.text.isspace():  
			element.text = newline + indent * (level + 1)
		else:
			element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
		
	temp = list(element) 
	for subelement in temp:
		if temp.index(subelement) < (len(temp) - 1):  
			subelement.tail = newline + indent * (level + 1)
		else: 
			subelement.tail = newline + indent * level
		pretty_xml(subelement, indent, newline, level=level + 1) 
		
#########################################################################################################

def add_node(root,id_n,lat,lon,c_xMgrs,c_yMgrs,ele,nom_arret,color="red") -> None:
	nom_arret = str(nom_arret)
	ele = str(ele)
	lat = str(lat)
	lon = str(lon)
	id_n = str(id_n)
	c_xMgrs = str(c_xMgrs)
	c_yMgrs = str(c_yMgrs)
	node = ET.SubElement(root,"node")
	node.attrib = {"id":id_n,"lat":lat,"lon":lon}
	tag = ET.SubElement(node,"tag")
	tag.attrib = {"k":"local_x","v":c_xMgrs}
	tag = ET.SubElement(node,"tag")
	tag.attrib = {"k":"local_y","v":c_yMgrs}
	tag = ET.SubElement(node,"tag")
	tag.attrib = {"k":"ele","v":ele}
	tag = ET.SubElement(node,"tag")
	tag.attrib = {"k":"color","v":color}
	tag = ET.SubElement(node,"tag")
	tag.attrib = {"k":"Point_arret","v":nom_arret}
	# pretty_xml(root)


def dataMgrs2LongLat(datamgrs) -> None:
	mgrs_grid = datamgrs[:5]
	cOrigin_xMgrs = int(datamgrs[5:10])
	cOrigin_yMgrs = int(datamgrs[10:])
	return mgrs_grid, cOrigin_xMgrs, cOrigin_yMgrs


def longLat2DataMgrs (mgrs_grid,mgrsX,mgrsY) -> None:
	mgrsX = str(int(mgrsX))
	mgrsY = str(int(mgrsY))
	if len(mgrsX) < 5:
		for i in range(5-len(mgrsX)):
			mgrsX = "0"+mgrsX
	elif len(mgrsX) > 5:
		raise Exception("\n\n\n\n /!\\ Le format de MGRS n'est pas bonne \n\n\n\n")
	if len(mgrsY) < 5:
		for i in range(5-len(mgrsY)):
			mgrsY = "0"+mgrsY
	elif len(mgrsY) > 5:
		raise Exception("\n\n\n\n /!\\ Le format de MGRS n'est pas bonne \n\n\n\n")
	return (mgrs_grid+mgrsX+mgrsY)


def mgrs2LatLong(mgrs_grid,xMgrs,yMgrs):
	c_mgrs = longLat2DataMgrs(mgrs_grid,xMgrs,yMgrs)
	c_Lat = m.toLatLon(c_mgrs)[0]
	c_Long = m.toLatLon(c_mgrs)[1]
	return c_Lat, c_Long


def addBusPoint (rootLanelet,nom_arret, c_xMgrs,c_yMgrs,altitude,color="red") :
	global max_id
	c_Lat,c_Long = mgrs2LatLong(mgrs_grid,c_xMgrs,c_yMgrs)
	max_id += 1 
	# print(nom_arret,c_Lat,c_Long)
	add_node(rootLanelet,id_n=max_id,lat=c_Lat,lon=c_Long,ele=altitude,
	      	nom_arret=nom_arret,c_xMgrs=c_xMgrs,c_yMgrs=c_yMgrs,color=color)
	

def creationBusArea (rootLanelet,pointsBusArea,nom_arret):
	global max_id
	max_id -= 1 #regelage du vector map 
	nom_arret = str(nom_arret)
	idWay = str(max_id)
	max_id += 1 #regelage du vector map 

	way = ET.SubElement(rootLanelet,"way")
	way.attrib = {"id" : idWay}
	for i in pointsBusArea:
		nd = ET.SubElement(way,"nd")
		nd.attrib = {"ref":str(i)}

	tag = ET.SubElement(way,"tag")
	tag.attrib = {"k":"type","v":"bus_stop_area"}
	tag = ET.SubElement(way,"tag")
	tag.attrib = {"k":"area","v":"yes"}
	# pretty_xml(root)

#########################################################################################################
print("####### Chargement les fichiers #############")
start = time.time()
domTree = ET.parse(input_lanelet2)
root = domTree.getroot()
nodes = root.findall("node")
points_id = []

for node in nodes:
	iD = node.get("id")
	iD = int(iD)
	points_id.append(iD)
max_id = max(points_id)
# print(max(points_id))

f = open(input_missionDatabase,) 
arretData = json.load(f) 
f.close()

if useMapProjector:
	with open(input_mapProjector, "r", encoding="utf-8") as y:
		config = yaml.safe_load(y)  # 返回 Python 字典
		cartoMgrs = config["mgrs_grid"]

#########################################################################################################

print_reussi("--------- Creation Bus Area sur la Cartographie ------------")
# max_id = 0 # TODO Supprime
m = mgrs.MGRS()
points_arret = arretData["database"]
for point_arret in points_arret:
	# max_id += 1
	nom_arret = point_arret["name"]
	latitude = point_arret["latitude"]
	longitude = point_arret["longitude"]
	altitude = point_arret["altitude"]
	isYaw = False
	if useYaw:
		try:
			yaw = point_arret["yaw"]
			isYaw = True
			yaw = yaw-(math.pi)
			# yaw = (math.pi)-yaw # TODO

			# print(yaw)
		except:
			print("Pas de donness yaw indiqué dans la base de donnees")
			break
	else:
		pass
	cOrigin_mgrs = m.toMGRS(latitude, longitude)
	mgrs_grid,cOrigin_xMgrs, cOrigin_yMgrs  = dataMgrs2LongLat(cOrigin_mgrs)
	pointsBusArea = []
	if useMapProjector : 
		if mgrs_grid != cartoMgrs :
			raise Exception("\n\n\n\n /!\\ Le MGRS du MapProjector et la programme ne sont pas le meme \n\n\n\n")
	if isYaw :
		c1_xMgrs = cOrigin_xMgrs + ((longeurArret/2)*math.cos(yaw)-(largeurArret/2)*math.sin(yaw))
		c1_yMgrs = cOrigin_yMgrs + ((longeurArret/2)*math.sin(yaw)+(largeurArret/2)*math.cos(yaw))
		c2_xMgrs = cOrigin_xMgrs + ((longeurArret/2)*math.cos(yaw)+(largeurArret/2)*math.sin(yaw))
		c2_yMgrs = cOrigin_yMgrs + ((longeurArret/2)*math.sin(yaw)-(largeurArret/2)*math.cos(yaw))
		c3_xMgrs = cOrigin_xMgrs - ((longeurArret/2)*math.cos(yaw)-(largeurArret/2)*math.sin(yaw))
		c3_yMgrs = cOrigin_yMgrs - ((longeurArret/2)*math.sin(yaw)+(largeurArret/2)*math.cos(yaw))
		c4_xMgrs = cOrigin_xMgrs - ((longeurArret/2)*math.cos(yaw)+(largeurArret/2)*math.sin(yaw))
		c4_yMgrs = cOrigin_yMgrs - ((longeurArret/2)*math.sin(yaw)-(largeurArret/2)*math.cos(yaw))
	else:
		c1_xMgrs = cOrigin_xMgrs + (largeurArret/2)
		c1_yMgrs = cOrigin_yMgrs + (longeurArret/2)
		c2_xMgrs = cOrigin_xMgrs - (largeurArret/2)
		c2_yMgrs = cOrigin_yMgrs + (longeurArret/2)
		c3_xMgrs = cOrigin_xMgrs - (largeurArret/2)
		c3_yMgrs = cOrigin_yMgrs - (longeurArret/2)
		c4_xMgrs = cOrigin_xMgrs + (largeurArret/2)
		c4_yMgrs = cOrigin_yMgrs - (longeurArret/2)

	addBusPoint(root,nom_arret,c1_xMgrs,c1_yMgrs,altitude)
	pointsBusArea.append(max_id)
	addBusPoint(root,nom_arret,c2_xMgrs,c2_yMgrs,altitude)
	pointsBusArea.append(max_id)
	addBusPoint(root,nom_arret,c3_xMgrs,c3_yMgrs,altitude,color="green")
	pointsBusArea.append(max_id)
	max_id += 1 # regelage du vector map pour le 4eme point 
	addBusPoint(root,nom_arret,c4_xMgrs,c4_yMgrs,altitude,color="green")
	pointsBusArea.append(max_id)

	creationBusArea(root, pointsBusArea, nom_arret)

#########################################################################################################

pretty_xml(root)

out_lanelet2 = input_lanelet2.replace(".osm", "_ZoneArrets.osm")
print(out_lanelet2)
domTree.write((out_lanelet2),encoding="utf8")   
end = time.time()
print("Temps d'éxecusion: "+str(end-start)+" s\n")

#########################################################################################################






