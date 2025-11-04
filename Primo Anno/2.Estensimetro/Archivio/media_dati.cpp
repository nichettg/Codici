//programma che legga in input un file del tipo F,x e calcoli la media delle x e la sua deviazione standard

#include <iostream>
#include <cmath>
#include <fstream>
#include <vector>
using namespace std;

ifstream input1 ("allungamento.txt");
ifstream input2 ("accorciamento.txt");
ofstream output1 ("medie_allungamento.txt");
ofstream output2 ("medie_accorciamento.txt");

double f_media (const vector<double>&);
double f_dev (const vector<double>&,double);

vector<double> dati_all, dati_acc;
vector<int> dati_F;

int main () {

    if (!input1 || !input2) {
        cerr<<"Errore apertura file input"<<'\n';
        return 1;
    }

    int a;
    double b,c,d;
    while (input1>>a>>b) {
        dati_all.push_back(b);
        dati_F.push_back(a);
    }
    while (input2>>c>>d) {
        dati_acc.push_back(-d);
    }

    for (int i = 0; i < 11; i++) {
        vector<double> v_all = {dati_all[i],dati_all[i+11],dati_all[i+22],dati_all[33]};
        vector<double> v_acc = {dati_acc[i],dati_acc[i+11],dati_acc[i+22],dati_acc[33]};
        double media_all = f_media(v_all);
        double media_acc = f_media(v_acc);
        double dev_all = f_dev(v_all, media_all);
        double dev_acc = f_dev(v_acc, media_acc);
        v_all.clear();
        v_acc.clear();
        output1<<dati_F[i]<<'\t'<<'\t'<<media_all<<'\t'<<'\t'<<dev_all/sqrt(4)<<'\n';   // F    x medio     dev std media
        output2<<dati_F[i]<<'\t'<<'\t'<<media_acc<<'\t'<<'\t'<<dev_acc/sqrt(4)<<'\n';
        media_all=0.;
        media_acc=0.;
        dev_all=0.;
        dev_acc=0.;
    }
    return 0;
}

//funzione media
double f_media (const vector <double> & v) {
    double somma = 0.;
    for (auto & c : v) {
        somma += c;
    }
    return somma/v.size();
}

//funzione deviazione standard
double f_dev (const vector <double> & v, double m) {
    double somma = 0.;
    for (auto & c : v) {
        somma += pow(c - m, 2);
    }
    return sqrt(somma/(v.size()-1));
}