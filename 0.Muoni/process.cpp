#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <string>
using namespace std;

string nome;
ifstream input("muoni.txt");
ofstream output(nome);

vector<int> valori;
vector<int> angoli;
vector<int> somme;

int main() {
   
    //input
    if (!input) {
        cout<<"Errore apertura file input"<<endl;
        return 1;
    }
    cout<<"Lettura da file input: 'muoni.txt'"<<endl;
    
    //output
    cout<<"Digitare il nome del file di output: ";
    cin>>nome;
    cout<<endl;
    ofstream output(nome);
    if(!output) {
        cout<<"Errore apertura file output"<<endl;
        return 1;
    }

    //raccolta dati input in due vettori "angoli" e "valori"  
    int a,v1,v2,v3,v4;
    while(input>>a>>v1>>v2>>v3>>v4) {
        angoli.push_back(a);
        valori.push_back(v1);
        valori.push_back(v2);
        valori.push_back(v3);
        valori.push_back(v4);
    }

    //raccolta somme dei valori presi a gruppi di 4 in un vettore "somme"
    for (int t=0; t<valori.size(); t+=4) {
        int somma=0;
        for (int i=t; i<4+t && i < valori.size(); ++i) {
            somma += valori.at(i);
        }
        somme.push_back(somma);
    }

    //stampa in file di output
    for (int d=0; d<angoli.size(); ++d) {
        
        double media = somme.at(d)/4.;

        double sommatoria=0.;
        for (int g=0; g<4 && g+(4*d) < valori.size(); ++g) {
            sommatoria += pow(valori.at(g+(4*d))-media, 2);
        }
        double dev = sqrt(sommatoria/3.);

        output<<angoli.at(d)<<"\t"<<media<<"\t"<<dev<<endl;
    }

    return 0;
}