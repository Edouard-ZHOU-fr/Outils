#include <iostream>
#include <filesystem>
#include <string>
#include <sstream>
#include <ctime>
#include <limits>  // utiliser pour chercher les max du dossier
#include <cmath> 
#include <fstream>

#include <json.hpp>

namespace fs = std::filesystem;

using json = nlohmann::json;

// 将字符串 "2025-03-05-10-28-34" 转换为 `std::tm`
std::tm stringToTime(const std::string& timeStr) {
    std::tm tmTime = {};
    std::istringstream ss(timeStr);
    ss >> std::get_time(&tmTime, "%Y-%m-%d-%H-%M-%S"); // 解析时间格式
    return tmTime;
}


std::string getPrefix(const std::string& fileName) {
    size_t pos = fileName.find('_'); // 找到第一个 "_"
    return (pos != std::string::npos) ? fileName.substr(0, pos) : fileName;
}

// 提取文件名中的时间部分
std::string extractTimeFromFilename(const std::string& filename) {
    size_t pos = filename.find('_');
    if (pos != std::string::npos && pos + 1 < filename.size()) {
        return filename.substr(pos + 1); // 提取 `_` 之后的时间部分
    }
    return "";
}

void findFilesContaining(const std::string& folderPath, const std::string& partialName,std::string& rp_f_cible) {
    bool found = false;
    
    for (const auto& entry : fs::directory_iterator(folderPath)) {
        std::string fileName = entry.path().filename().string();

        // 检查文件名是否包含 partialName
        if (fileName.find(partialName) != std::string::npos) {
            // std::cout << "Trouvé: " << entry.path() << std::endl;
            rp_f_cible = entry.path();
            found = true;
        }
    }

    if (!found) {
        std::cout << "/!\\ N'est pas trouvé le fichier \"" << partialName << "\" 文件。" << std::endl;
    }
}

bool copyFile(const std::string& sourceFile, const std::string& destinationPath) {
    try {
        fs::copy_file(sourceFile, destinationPath, fs::copy_options::overwrite_existing);
        std::cout << "Le fichier copie réussi: " << sourceFile << " ====> " << destinationPath << std::endl;
        return true;
    } catch (const fs::filesystem_error& e) {
        std::cerr << "/!\\ Le fichier Copie failed: " << e.what() << std::endl;
        return false;
    }
}

// 计算两个时间之间的分钟差
int getMinuteDifference(const std::tm& t1, const std::tm& t2) {
    time_t time1 = mktime(const_cast<std::tm*>(&t1));
    time_t time2 = mktime(const_cast<std::tm*>(&t2));

    // 计算时间差（单位：秒），然后转换为分钟
    double secondsDiff = std::difftime(time1, time2);
    int minutesDiff = static_cast<int>(secondsDiff / 60); // 转换为分钟

    return minutesDiff;
}

// 筛选距离要求时间之前最近的最后一个文件
void findFileClosestBeforeTargetTime(const std::string& folderPath, const std::string& targetTimeStr,std::string& rp_cible, int&  min_deviato,std::string& type_log) {
    std::tm targetTime = stringToTime(targetTimeStr); // 转换为 std::tm

    std::string closestFile;
    int closestTimeDiff = std::numeric_limits<int>::min();  // 初始化为最小值（表示时间差最大的负值）

    for (const auto& entry : fs::directory_iterator(folderPath)) {
        std::string filename = entry.path().filename().string();
        std::string fileTimeStr = extractTimeFromFilename(filename);
        std::string filePrefix = getPrefix(filename);

        if (filePrefix != type_log){
            continue;
        }

        if (!fileTimeStr.empty()) {
            std::tm fileTime = stringToTime(fileTimeStr);
            
            // 计算文件时间与目标时间的时间差
            int minutesDiff = getMinuteDifference(fileTime, targetTime);

            // 寻找距离目标时间之前最近的文件（负时间差最大的文件）
            if ((minutesDiff < 0) && (minutesDiff > closestTimeDiff)) {
                closestTimeDiff = minutesDiff;
                closestFile = filename;
            }
        }
    }

    if (!closestFile.empty()) {
        std::cout << "Le dernier fichier le plus proche de l'heure cible est le fichier： " << closestFile << " (decalage du temps: " << closestTimeDiff << " min)" << std::endl;
        rp_cible = closestFile;
        min_deviato = closestTimeDiff;
    } else {
        std::cout << "Le fichier plus proche n'est pas trouvé, verifiez l'existence svp!" << std::endl;
    }
}

int main() {

    std::string folderPath;
    // std::cout << "Veuillez saisir le repertoire de BlackBox" << std::endl;
    // std::cin >> folderPath;

    std::string targetTimeStr; // 指定的目标时间
    // std::cout << "Veuillez saisir le Temps cible sous format 2025-03-05-13-30-00" << std::endl;
    // std::cin >> targetTimeStr;

    std::tm t_cible = stringToTime(targetTimeStr); // 转换为 std::tm
    std::string rp_d_cible = "";
    std::string rp_f_cible = "";
    std::string partialName = "";
    std::string rp_destin; // 指定的目标时间
    std::string type_log; // 指定的目标时间


    json config;
    int min_deviato = 0;
    int n_fichier;
    std::ifstream file("../config.json"); // 打开 JSON 文件
    if (!file) {
        std::cerr << "Il n'existe pas le fichier JSON !" << std::endl;
        return 1;
    }
    file >> config;


    folderPath = config["source_BlackBox"];
    targetTimeStr = config["temp_incidant"];
    rp_destin = config["Destination"];
    type_log = config["Type"];


    findFileClosestBeforeTargetTime(folderPath, targetTimeStr,rp_d_cible,min_deviato,type_log);
    n_fichier = std::abs(min_deviato/5);
    partialName = rp_d_cible+"_"+std::to_string(n_fichier);
    rp_d_cible = folderPath+rp_d_cible+"/";
    findFilesContaining(rp_d_cible,partialName,rp_f_cible);

    fs::path rp_bb(rp_f_cible);
    std::string nom_bb = rp_bb.filename().string(); // 获取文件名
    rp_destin = rp_destin+nom_bb;


    copyFile(rp_f_cible,rp_destin);
    // std::cout <<  rp_f_cible << "  ============> " << rp_destin << std::endl;

    return 0;
}
