#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <iomanip>
#include <fstream>
using namespace std;

double f_media(vector <double>);
double f_dev(vector<double>, double);
double arrotonda (double valore);

int main() {
    
    string iname;

    //input
    cout<<"Inserire il nome del file di input: ";
    cin>>iname;
    cout<<endl;

    ifstream input(iname);
    if (!input) {
        cout<<"Errore nell'apertura del file di input "<<iname<<endl;
        return 1;
    }

    ofstream output1("plot.txt");
    if (!output1) {
        cout<<"Errore nell'apertura del file di output plot.txt"<<endl;
        return 1;
    }

    //secondo output
    ofstream output2("processed_data.txt");
    if (!output2) {
        cout<<"Errore nell'apertura del file di output 'processed_data.txt'"<<endl;
        return 1;
    }

    //raccolta dati valori input
    vector <double> valori;
    double valore;

    while (input>>valore) {
        valori.push_back(valore);
    }

    //calcolo di minimo e massimo per determinare il dominio dei valori nel file input
    double max_valore=valori.at(0), min_valore=valori.at(0);
    for (int j=0; j<valori.size(); ++j) {
        if (max_valore <= valori.at(j)) {
            max_valore = valori.at(j);
        }
        if (min_valore >= valori.at(j)) {
            min_valore = valori.at(j);
        }
    }

    cout<<"Il numero di dati è "<<valori.size()<<endl;
    cout<<"Il range delle frequenze è ["<<min_valore<<","<<max_valore<<"]"<<endl;
    cout<<"Il numero di frequenze distinte osservate è "<<(max_valore-min_valore)*100<<endl;

    //numero bin
    int nbin;
    cout<<"Inserire il numero di bin: ";
    cin>>nbin;
    cout<<endl;

    //ampiezza bin
    double abin = (max_valore - min_valore)/nbin;
    cout<<"L'ampiezza dei bin è "<<abin<<endl;

    //dati plot
    cout<<"Intervalli:"<<endl;
    for (int e=0; e<nbin; ++e) { //il <= è per comprendere nella rappresentazione anche il max

        //estremi
        double min = min_valore + e*abin;
        double max = min_valore + (e+1)*abin;
       
        //prima colonna output
        double media = (min + max) / 2;
        output1<<fixed<<setprecision(2)<<media<<"\t";

        //seconda colonna output
        int somma=0;
        for (auto t: valori) {  
            if ( t >= min && t < max)
            somma++;
        }

        cout<<min<<"\t"<<max<<endl;

        output1<<somma<<endl;
        
    }

    //dati 'processed_data.txt'
    double media=f_media(valori);
    double dev=f_dev(valori,media);
    output2<<"Numero valori: "<<valori.size()<<endl
    <<"Ampiezza bin: "<<abin<<endl
    <<"Media: "<<media<<endl
    <<"Deviazione standard campionaria: "<<dev<<endl<<endl;

    output2<<"a= "<<valori.size()*abin<<endl
    <<"b= "<<media<<endl
    <<"c= "<<dev<<endl<<endl;
    
    int somma_somme = 0;
    for (double i=min_valore; i<=max_valore; i += 0.01) {
        double k = arrotonda(i);
        int somma=0;
        for (auto c: valori) {
            if (k==c) {
                somma += 1;
            }
        }
        somma_somme += somma;
        output2<<fixed<<setprecision(2)<<k<<"\t"<<somma<<endl;        
    }

    output2<<endl<<"La somma totale delle frequenze è "<<somma_somme;

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
        somma += pow ( c - m,2) ;
    }

    return sqrt (somma/(v.size () - 1));
}

//funzione arrotondamento
double arrotonda (double valore) {
    return round(valore*100.0) / 100.0;
}