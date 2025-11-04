#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>

struct Data {
    int force;
    int elongation;
};

void processFile(const std::string& inputFilename) {
    std::ifstream inputFile(inputFilename);
    if (!inputFile) {
        std::cerr << "Errore nell'apertura del file di input: " << inputFilename << std::endl;
        return;
    }
    
    std::string outputFilename = inputFilename.substr(0, inputFilename.find_last_of('.')) + "_o.txt";
    std::ofstream outputFile(outputFilename);
    if (!outputFile) {
        std::cerr << "Errore nell'apertura del file di output: " << outputFilename << std::endl;
        return;
    }
    
    std::vector<Data> dataset;
    std::string line;
    
    while (std::getline(inputFile, line)) {
        std::istringstream iss(line);
        Data data;
        if (iss >> data.force >> data.elongation) {
            dataset.push_back(data);
        }
    }
    
    inputFile.close();
    
    for (size_t i = 0; i < dataset.size() - 1; ++i) {
        int diff = dataset[i + 1].elongation - dataset[i].elongation;
        outputFile << dataset[i].force << "\t" << diff << "\n";
    }
    
    outputFile.close();
    std::cout << "File " << outputFilename << " generato con successo!" << std::endl;
}

int main() {
    std::vector<std::string> filenames = {"dati1a.txt", "dati1b.txt", "dati2a.txt", "dati2b.txt", "dati3a.txt", "dati3b.txt", "dati4a.txt", "dati4b.txt"};
    
    for (const auto& filename : filenames) {
        processFile(filename);
    }
    
    return 0;
}
