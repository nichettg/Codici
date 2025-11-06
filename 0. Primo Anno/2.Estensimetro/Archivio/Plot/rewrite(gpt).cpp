#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>

using namespace std;

int main() {
    ifstream inputFile("allungamento.txt"); // File di input
    ofstream outputFile("media_allungamento.txt"); // File di output
    
    if (!inputFile) {
        cerr << "Errore nell'apertura del file di input" << endl;
        return 1;
    }
    
    map<int, vector<int>> dataMap; // Mappa per memorizzare i dati
    string line;
    
    while (getline(inputFile, line)) {
        stringstream ss(line);
        int x, y;
        if (ss >> x >> y) {
            dataMap[x].push_back(y); // Inserisce il valore nella mappa
        }
    }
    
    inputFile.close();
    
    // Scrittura delle medie nel file di output
    for (const auto& pair : dataMap) {
        int sum = 0;
        for (int val : pair.second) {
            sum += val;
        }
        double media = static_cast<double>(sum) / pair.second.size();
        outputFile << pair.first << "\t" << media << endl;
    }
    
    outputFile.close();
    cout << "File media_output.txt generato con successo!" << endl;
    return 0;
}