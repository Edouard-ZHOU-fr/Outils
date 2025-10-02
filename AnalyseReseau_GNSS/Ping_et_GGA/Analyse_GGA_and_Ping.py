import re
import math
import csv
import matplotlib.pyplot as pl
import matplotlib.patches as mpatches
import numpy as np
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import time

inputFileName = 'GGA_Ping.txt'

displayChoice = 1 # 1 : display GNSS-RTK quality / 2 : display Ping quality
zoomLevel = 18 # Adjust between 10 and 18 depending on output map size.

nb_satellite = 12 # nombre de satelitte utilisé, if this value is below 12 this will be red
RTKGreen = 4 # if RTK status is at this value it will be display as green points. Otherwise it will be red points.
HdopGreen = 2 # if Hdop is below this value it will be display as green if RTK is also green. Above it will be orange.

PingGreen = 30 # Below this value ping will be display as green points.
PingOrange = 100 # Below this value ping will be display as orange points. Abode it will be display as red points.


###########################################################################################################################################################
###########################################################################################################################################################


def convert_GGA_Bag(inputFileName = "GGA_Ping.txt",outputFileName = "xxx.csv",exportMoreGGA = False ):
        
    outputFileName = inputFileName.replace(".txt", ".csv")
    # Initialize a few things
    output=[]
    newPing = 0
    newGGA = 0

    # Read input text file
    textFile = open(inputFileName, "r")
    rawLines = textFile.readlines()
    textFile.close()

    # Create a header in the output array
    output.append(['timestamp', 'latitude', 'longitude', 'RTK', 'satellite', 'hdop', 'ping'])

    # For each new GGA and Ping line, add a line in the output array
    for i in rawLines:
        line = re.split(' |,',i)

        if line[0] == '64':
            # Line contains Ping
            ping = float(line[6].replace('time=',''))
            newPing = 1
        elif line[0] == '$GPGGA' or line[0] == '$GNGGA':
            # Line contains GGA
            timestamp = float(line[1])
            latDeci = float(line[2])
            latNS = (line[3])
            if latNS == "N":
                latitude = math.floor(latDeci/100) + (latDeci/100 - math.floor(latDeci/100))/0.6
            elif latNS == "S":
                latitude = -(math.floor(latDeci/100) + (latDeci/100 - math.floor(latDeci/100))/0.6)
            else:
                raise Exception("\n\n\n\n /!\\ Le format de GPGGA n'est pas bonne veuillez verifier le Format(Miniscule peut etre)\n\n\n\n")
            lonDeci = float(line[4])
            lonEW = (line[5])
            if lonEW == "E":
                longitude = math.floor(lonDeci/100) + (lonDeci/100 - math.floor(lonDeci/100))/0.6
            elif lonEW == "W":
                longitude = -(math.floor(lonDeci/100) + (lonDeci/100 - math.floor(lonDeci/100))/0.6)
            else:
                raise Exception("\n\n\n\n /!\\ Le format de GPGGA n'est pas bonne veuillez verifier le Format(Miniscule peut etre)\n\n\n\n")

            RTK = int(line[6])
            satellite = int(line[7])
            hdop = float(line[8])
            newGGA = 1

        # If there is a new GGA and Ping line, create a new line in the output array
        if newPing == 1 and newGGA ==1:
            output.append([timestamp, latitude, longitude, RTK, satellite, hdop, ping])
            newGGA = 0
            if exportMoreGGA == False:
                newPing = 0

    # Write results in the output file
    with open(outputFileName, 'w', newline='') as f:
        csv.writer(f, delimiter=';').writerows(output)

    # Display total computing time
    print("Convertion réussi et terminé")
    return outputFileName


###########################################################################################################################################################

start_time = time.time()

# convertir fichier txt à csv au faorma: timestamp;latitude;longitude;RTK;satellite;hdop;ping
inputFileName = convert_GGA_Bag(inputFileName=inputFileName)


# Read input text file
textFile = open(inputFileName, "r")
rawLines = textFile.readlines()
textFile.close()

# For each line, define points color depending on RTK, Hdop or Ping values.
size = len(rawLines)
data = np.empty(shape=(size-1,4), dtype=object) # columns are : latitude / longitude / color for RTK / color for Ping

for i in range(size-1):
    line = re.split(';|,',rawLines[i+1])
    data[i,0] = float(line[1]) # latitude
    data[i,1] = float(line[2]) # longitude

    if int(line[4]) >= nb_satellite:
        if int(line[3]) == RTKGreen :
            if float(line[5]) <= HdopGreen:
                data[i,2] = 'green' # color RTK set as green
            else:
                data[i,2] = 'orange' # color RTK set as orange
        else:
            if float(line[5]) <= HdopGreen:
                data[i,2] = 'orange' # color RTK set as green
            else:
                data[i,2] = 'red' # color RTK set as red
    else:
        data[i,2] = 'red' # color RTK set as red

    
    if float(line[6]) <= PingGreen:
        data[i,3] = 'green' # color Ping set as green
    elif float(line[6]) <= PingOrange:
        data[i,3] = 'orange' # color Ping set as orange
    else:
        data[i,3] = 'red' # color Ping set as red


# Define boundaries for latitude and longitude
latitude = data[:,0]
longitude = data[:,1]
colorRTK = data[:,2]
colorPing = data[:,3]

lonMin = min(longitude)
lonMax = max(longitude)
latMin = min(latitude)
latMax = max(latitude)

midLon = (lonMax - lonMin)*0.1
midLat = (latMax - latMin)*0.1

lonMin = lonMin - midLon
lonMax = lonMax + midLon
latMin = latMin - midLat
latMax = latMax + midLat


# Plot results with Cartopy
request = cimgt.OSM()
fig = pl.axes(projection=request.crs)
fig.add_image(request, zoomLevel) # Set zoom level



# Display points
if displayChoice == 1: # Display RTK quality
    pl.scatter(longitude, latitude, s=10, alpha = 1, color=colorRTK, transform=ccrs.PlateCarree())
    fig.set_title('RTK quality')
    greenPatch = mpatches.Patch(color='green', label='RTK is good')
    orangePatch = mpatches.Patch(color='orange', label='RTK is weak or Hdop is weak')
    redPatch = mpatches.Patch(color='red', label='No RTK correction or doubt')
if displayChoice == 2: # Display Ping quality
    pl.scatter(longitude, latitude, s=10, alpha = 1, color=colorPing, transform=ccrs.PlateCarree())
    fig.set_title('4G/5G network quality')
    greenPatch = mpatches.Patch(color='green', label='Ping < %d ms' % PingGreen)
    orangePatch = mpatches.Patch(color='orange', label='%d < Ping < %d ms' % (PingGreen, PingOrange))
    redPatch = mpatches.Patch(color='red', label='Ping > %d ms' % PingOrange)


# Add custom legend
pl.legend(handles=[greenPatch, orangePatch, redPatch], loc='upper left', handlelength=1, fontsize="7")


# Display total computing time
print("--- %.3f seconds ---" % (time.time() - start_time))

pl.show()
