#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <cstdio>

using namespace std;

void elaboraFile(const vector<string>& inFile, const vector<string>& outFile) {
    for (size_t i = 0; i < inFile.size(); i++) {
        ifstream input(inFile[i]); //prende i nomi dei file da elaborare da una vettore di stringhe contenuto nel main
        ofstream output(outFile[i]);

        if (!input) {
            cerr << "Errore nell'apertura dei file di input: " << inFile[i]<< endl;
            return;
        }

        if (!output) {
            cerr<< "Errore nell'apertura del file di output: "<< outFile[i]<< endl;
            return;
        }

        string riga;
        int contatoreRighe = 0;

        while (getline(input, riga)) {
            if (contatoreRighe < 2) { //ignora le prime due righe e le copia nel file di output (titolo dell'esperienza e contenuto delle colonne)
                output << riga << endl;
            } 
            
            else { //sostituisce le virgole decimali con punti e spazi e tab con virgole
                for (char& c : riga) {
                    if (c == ',') c = '.';
                    if (c == '	' || c == '\t') c = ',';
                }
                output << riga << endl;
            }
            contatoreRighe++;
        }

        input.close();
        output.close();

        const char* eliminato = inFile[i].c_str(); //passaggio della stringa con il nome del file da eliminare a puntatore, perchè "remove" funziona solo con puntatori
        if (remove(eliminato) != 0) { //rimuove i file di input
            perror(("Errore nella rimozione del file: " + inFile[i]).c_str());
        }
        else {
            cout << "File " << inFile[i] << " eliminato con successo\n";
        }
    }
}

int main(){ //vettori di stringhe contenenti i nomi dei file di input e quelli dei file di output
    vector<string> inputFiles= {
        "../Raw/tors_0.85hz.txt",
        "../Raw/tors_0.91hz.txt",
        "../Raw/tors_0.92hz.txt",
        "../Raw/tors_0.93hz.txt",
        "../Raw/tors_0.94hz.txt",
        "../Raw/tors_0.95hz.txt",
        "../Raw/tors_0.96hz.txt",
        "../Raw/tors_0.955hz.txt",
        "../Raw/tors_0.965hz.txt",
        "../Raw/tors_0.9575hz.txt",
        "../Raw/tors_0.9625hz.txt",
        "../Raw/tors_0.96063hz.txt",
        "../Raw/tors_0.96125hz.txt",
        "../Raw/tors_0.96183hz.txt",
        "../Raw/tors_1.5hz.txt",
        "../Raw/tors_2_0.97hz.txt"
    };

    vector<string> outputFiles= {
        "../Raw/tors_0.85hz.csv",
        "../Raw/tors_0.91hz.csv",
        "../Raw/tors_0.92hz.csv",
        "../Raw/tors_0.93hz.csv",
        "../Raw/tors_0.94hz.csv",
        "../Raw/tors_0.95hz.csv",
        "../Raw/tors_0.96hz.csv",
        "../Raw/tors_0.955hz.csv",
        "../Raw/tors_0.965hz.csv",
        "../Raw/tors_0.9575hz.csv",
        "../Raw/tors_0.9625hz.csv",
        "../Raw/tors_0.96063hz.csv",
        "../Raw/tors_0.96125hz.csv",
        "../Raw/tors_0.96183hz.csv",
        "../Raw/tors_1.5hz.csv",
        "../Raw/tors_2_0.97hz.csv"
    };

    elaboraFile(inputFiles, outputFiles);

    return 0;
}