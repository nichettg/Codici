#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main () {
    cout<<"Inserire il nome del file di input: ";
    string nomei;
    cin>>nomei;
    cout<<"Inserire il nome del file di output: ";
    string nomeo;
    cin>>nomeo;

    ifstream input (nomei);
    ofstream output (nomeo);
    if (!input) {
        cout<<"Errore apertura file input"<<'\n';
        return 1;
    }
    if (!output) {
        cout<<"Errore apertura file output"<<'\n';
        return 1;
    }

    string a;
    while (input>>a) {
        output<<a<<'\n';
    }

    return 0;
}