import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import json 
import time




#########################################################################################################


input_lanelet2 = "/home/hongyu/python_ws/point_arret/lanelet2_map_YeloDeta_Total_V3_3.osm"
in_mission_database = "/home/hongyu/python_ws/point_arret/mission_database.json"

#########################################################################################################



def print_c(clignotant):
    clignotant = str(clignotant)
    # os.system("clear")
    print("\033[5;34;42m"+clignotant+"\033[0m", end='\r')

def print_reussi(reussi):
    reussi = str(reussi)
    print("\033[1;32;47m"+reussi+"\033[0m")


#########################################################################################################
def pretty_xml(element, indent='\t', newline='\n', level=0) -> None:  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作



def add_node(root,id_n,lat,lon,ele,nom_arret) -> None:
	nom_arret = str(nom_arret)
	ele = str(ele)
	lat = str(lat)
	lon = str(lon)
	id_n = str(id_n)

	node = ET.SubElement(root,"node")
	node.attrib = {"id":id_n,"lat":lat,"lon":lon}
	tag = ET.SubElement(node,"tag")
	tag.attrib = {"k":"ele","v":ele}
	tag = ET.SubElement(node,"tag")
	tag.attrib = {"k":"color","v":"red"}
	tag = ET.SubElement(node,"tag")
	tag.attrib = {"k":"Point_arret","v":nom_arret}

	pretty_xml(root)

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
print(max(points_id))


#########################################################################################################
f = open(in_mission_database,) 
data = json.load(f) 
f.close()

print_reussi("--------- Création le nouveau Lanelet2 ------------")

points_arret = data["database"]
for point_arret in points_arret:
	max_id += 1
	nom_arret = point_arret["name"]
	latitude = point_arret["latitude"]
	longitude = point_arret["longitude"]
	altitude = point_arret["altitude"]
	add_node(root,id_n=max_id,lat=latitude,lon=longitude,ele=altitude,
          	nom_arret=nom_arret)




out_lanelet2 = input_lanelet2.replace(".osm", "_PointArrets.osm")
print(out_lanelet2)
domTree.write((out_lanelet2),encoding="utf8")   
end = time.time()
print("Temps d'éxecusion: "+str(end-start)+" s\n")
#########################################################################################################







