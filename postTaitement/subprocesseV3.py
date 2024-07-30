import subprocess, signal
import os
import time
import sys,shutil
import psutil


def print_c(clignotant):
    clignotant = str(clignotant)
    # os.system("clear")
    print("\033[5;34;42m"+clignotant+"\033[0m")

    pass

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def main():

#####################################################################################################################################################

    time_s = 0
    n_bag = 10
    nm_bag = 10
    n_pcd = 1000
    duration = 5
    ratio = 0.1
    g_zone = "30TXS"
    r_pc = "/media/milla/datalogger/YeloDeta/rosbag2_2024_05_02-14_15_37/les_nuages_de_points/testDeBag10/"
    r_rosbag = "/media/milla/datalogger/YeloDeta/rosbag2_2024_05_02-14_15_37/ROS1BAG/"


#####################################################################################################################################################



    rviz = "roslaunch hdl_graph_slam hdl_graph_slam_floam.launch enable_gps:=true gnss_topic:=/fixposition/converter/gpsfix"

    # noetic = "noetic"
    # rostime = "rosparam set use_sim_time true"
    # setup  = "source ~/ros/mapping_ws/devel/setup.bash" 
    # g_zone: grid de la zone MGRS
    # ratio: rate de ROS 
    n_pc = n_pcd
    drapeau = True

    while True:
        if nm_bag <= 0:
            print("88888888888888888888888")

            break
        if time_s >= 300:
            n_bag += 1
            n_pcd += 100
            n_pc = n_pcd

            time_s = 0

            nm_bag = nm_bag - 1



        rosbag = f"rosbag play "+r_rosbag+f"output_ros{n_bag}.bag -s {time_s} --clock -r {ratio} /tf:=/tf_old"
        enregistement2 = f"rosservice call /hdl_graph_slam/save_map \"utm: false \nresolution: 0.0 \ndestination: \'"+r_pc+f"maps{n_pc}.pcd\'\" "
        conertissement2 = f"roslaunch utils pcd_utm2mgrs.launch map_name:=\"maps{n_pc}\" map_path:=\""+r_pc+f"\" zone:=\"{g_zone}\" utm_file_path:=\""+r_pc+f"maps{n_pc}.pcd.utm\""
        clear1 = f"rm "+r_pc+f"maps{n_pc}.pcd"
        clear2 = f"rm "+r_pc+f"maps{n_pc}.pcd.utm"





        if drapeau:
            # start = time.time()

            processe1 = subprocess.Popen(rviz, shell=True, stdout=subprocess.PIPE) 
            print_c("Ouvert Rviz")
            pid1 = processe1.pid
            time.sleep(3)

            # print(pid1)
            processe2 = subprocess.Popen(rosbag, shell=True, stdout=None)
            print_c("Ouvert rosbag")
            print(rosbag)
            print("time start: %d",time_s)

            start = time.time()

            pid2 = processe2.pid
            drapeau = False


        actuel = time.time()
        temps_execution = actuel-start
        if (temps_execution*ratio) >= duration:

            # print("000000000000000000000000")
            kill(processe2.pid)
            processe2.wait()
            print_c("Ferme rosbag")

            processe3 = subprocess.Popen(enregistement2, shell=True, stdout=subprocess.PIPE)
            print_c("Enregistement")
            processe3.wait()
            processe4 = subprocess.Popen(conertissement2, shell=True, stdout=subprocess.PIPE)
            print_c("Convertissement")
            n_pc+=1
            time_s += (duration-1)
            processe4.wait()


            kill(processe1.pid)
            print_c("Ferme Rviz")
            processe1.wait()


            proc5 = subprocess.Popen(clear1, shell=True, stdout=subprocess.PIPE)
            proc6 = subprocess.Popen(clear2, shell=True, stdout=subprocess.PIPE)
            proc5.wait()
            proc6.wait()




            drapeau = True
            time.sleep(3)
            print("2222222222222222222222222222")
            # nm_bag = nm_bag - 1


    # domTree.write("out.osm",encoding="utf8")
    os.killpg(os.getpgid(processe1.pid),signal.SIGKILL)

 
if __name__=="__main__":
    main()
    pass
