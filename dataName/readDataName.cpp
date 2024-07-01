#include <iostream>
#include <filesystem>
#include <vector>
#include <fstream>

namespace fs = std::filesystem;

void listFiles(const fs::path& path, std::vector<fs::path>& files) {
    for (const auto& entry : fs::directory_iterator(path)) {
        if (fs::is_regular_file(entry.status())) {
            files.push_back(entry.path());
        }
    }
}

void saveFileNames(const std::vector<fs::path>& files, const std::string& outputFilePath) {
    std::ofstream outputFile(outputFilePath);
    if (outputFile.is_open()) {
        for (const auto& file : files) {
            outputFile << file.string() << std::endl;
        }
        outputFile.close();
    } else {
        std::cerr << "Failed to open file: " << outputFilePath << std::endl;
    }
}

int main() {
    fs::path rootPath = "/data/ls/data/"; // 替换成你的主文件夹路径
    std::vector<std::string> subfolders = {"email_txt", "img_m"};

    for (const auto& subfolder : subfolders) {
        fs::path subfolderPath = rootPath / subfolder;
        std::vector<fs::path> files;

        try {
            if (fs::exists(subfolderPath) && fs::is_directory(subfolderPath)) {
                listFiles(subfolderPath, files);
                saveFileNames(files, subfolder + "_filename.txt");
            } else {
                std::cerr << "The path " << subfolderPath << " does not exist or is not a directory." << std::endl;
            }
        } catch (const fs::filesystem_error& e) {
            std::cerr << "Filesystem error: " << e.what() << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "Exception: " << e.what() << std::endl;
        }
    }
    rootPath = "/data/ls/data/img_txt/"; // 替换成你的主文件夹路径
    subfolders = {"img_million", "text"};
    for (const auto& subfolder : subfolders) {
        fs::path subfolderPath = rootPath / subfolder;
        std::vector<fs::path> files;

        try {
            if (fs::exists(subfolderPath) && fs::is_directory(subfolderPath)) {
                listFiles(subfolderPath, files);
                saveFileNames(files, "img_txt-" + subfolder + "_filename.txt");
            } else {
                std::cerr << "The path " << subfolderPath << " does not exist or is not a directory." << std::endl;
            }
        } catch (const fs::filesystem_error& e) {
            std::cerr << "Filesystem error: " << e.what() << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "Exception: " << e.what() << std::endl;
        }
    }

    return 0;
}

