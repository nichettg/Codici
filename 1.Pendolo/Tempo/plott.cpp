#include <iostream>
#include <fstream>
#include <cmath>
#include <iomanip>
#include <string>
#include <vector>
using namespace std;

double f_media (vector <double>);
double f_dev (vector <double>, double);

int main () {

    cout<<"Inserire il nome del file di input: ";
    string nomei;
    cin>>nomei;

    ifstream input (nomei);
    if (!input) {
        cout<<"Errore nell'apertura del file di input"<<endl;
    }

    ofstream output ("plot.txt");
    if (!output) {
        cout<<"Errore nell'apertura del file di output"<<endl;
    }

    //raccolta dati
    vector <double> dati;
    double somma=0.;
    double dato;

    while (input>>dato) {
        dati.push_back(dato);
        output<<fixed<<setprecision(2);
        somma+=dato;
        output<<somma<<"\t"<<dato<<"\t"<<"0.05"<<endl;
    }

    double media = f_media(dati);
    double dev = f_dev(dati, media);

    cout<<"Media: "<<media<<endl;
    cout<<"Deviazione standard: "<<dev<<endl;

    return 0;
}

//funzione media
double f_media(vector <double> v) {
    double somma = 0.;
    for (auto c: v) {
        somma += c;
    }

    return somma/v.size();
}

//funzione deviazione standard
double f_dev(vector<double> v, double m) {
    double somma = 0.;
    for (auto c: v) {
        somma += pow ( c - m,2);
    }

    return sqrt (somma/(v.size () - 1));
}
