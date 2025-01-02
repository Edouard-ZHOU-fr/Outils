import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import json 
import time




#########################################################################################################


input_lanelet2 = "/home/hongyu/python_ws/point_arret/lanelet2_map_YeloDeta_Total_V3_3_PointArrets.osm"

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



#########################################################################################################
print("####### Chargement les fichiers #############")

start = time.time()

domTree = ET.parse(input_lanelet2)

root = domTree.getroot()
nodes = root.findall("node")

points_id = []
arrets_id = 0
database = []
for node in nodes:
    drapeau_Pointarret = False
    arret_name  = ""

    tags = node.findall("tag")
    for tag in tags:
        if tag.get("k") == "Point_arret" :
            arret_name = tag.get("v")
            drapeau_Pointarret  = True
            pass
    if drapeau_Pointarret:
        point_arret = {}
        arrets_id += 1
        latitude = float(node.get("lat"))
        longitude = float(node.get("lon"))
        for tag in tags:
            if tag.get("k") == "ele" :
                altitude = float(tag.get("v"))
                break
        point_arret = {"name":arret_name, "id":arrets_id, "latitude":latitude, 
                       "longitude":longitude,"altitude":altitude}
        database.append(point_arret)

mission_database = {"database":database}
# #########################################################################################################

print(database)
out_json = input_lanelet2.replace(".osm", "__mission_database.json")

with open(out_json,"w") as f:
    json.dump(mission_database, f, indent=4, ensure_ascii=False)
f.close()








