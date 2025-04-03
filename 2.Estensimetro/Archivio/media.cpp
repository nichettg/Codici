#include <vector>
#include <iostream>
#include <cmath>
#include <fstream>
using namespace std;

//codice di calcolo della media ponderata delle 4 serie di dati 
//e di calcolo della compatibilità di queste con la serie sigma

ifstream input ("k^-1.txt");
ifstream input2 ("k^-1sigma.txt");
ifstream input3 ("k^-1fit.txt");

double f_media(vector <double>, vector <double>);
double f_inc(vector <double>);
double f_comp(double,double,double,double);

double Ka, sKa, Kb, sKb, K, sK;
vector <double> vKa, vsKa, vKb, vsKb, vK, vsK;
double zKa, szKa, zKb, szKb, zK, szK;
double fKa, sfKa, fKb, sfKb, fK, sfK;

int main () {

    if (!input || !input2 || !input3) {
        cerr<<"Errore apertura file input"<<'\n';
        return 1;
    }

    while (input>>Ka>>sKa>>Kb>>sKb>>K>>sK) {
        vKa.push_back(Ka);
        vsKa.push_back(sKa);
        vKb.push_back(Kb);
        vsKb.push_back(sKb);
        vK.push_back(K);
        vsK.push_back(sK);
    }

    input2>>zKa>>szKa>>zKb>>szKb>>zK>>szK;
    input3>>fKa>>sfKa>>fKb>>sfKb>>fK>>sfK;

    cout<<"Serie sigma: \n"<<"1/k allungamento = "<<zKa<<" +- "<<szKa<<'\n'
    <<"1/k accorciamento = "<<zKb<<" +- "<<szKb<<'\n'
    <<"1/k unione = "<<zK<<" +- "<<szK<<'\n'<<'\n';

    double mKa = f_media(vKa, vsKa);
    double smKa = f_inc(vsKa);
    double mKb = f_media(vKb, vsKb);
    double smKb = f_inc(vsKb);
    double mK = f_media(vK, vsK);
    double smK = f_inc(vsK);

    cout<<"Medie ponderate:\n"<<"1/k allungamento = "<<f_media(vKa, vsKa)<<" +- "<<f_inc(vsKa)<<'\n'
    <<"1/k accorciamento = "<<f_media(vKb, vsKb)<<" +- "<<f_inc(vsKb)<<'\n'
    <<"1/k unione = "<<f_media(vK, vsK)<<" +- "<<f_inc(vsK)<<'\n'<<'\n';

    cout<<"Fit lineare: \n"<<"1/k allungamento = "<<fKa<<" +- "<<sfKa<<'\n'
    <<"1/k accorciamento = "<<fKb<<" +- "<<sfKb<<'\n'
    <<"1/k unione = "<<fK<<" +- "<<sfK<<'\n'<<'\n';

    cout<<"\nCompatibilità j:\n"
    <<"j allungamento/accorciamento serie sigma = "<<f_comp(zKa,szKa,zKb,szKb)<<'\n'
    <<"j allungamento/accorciamento medie ponderate = "<<f_comp(mKa,smKa,mKb,smKb)<<'\n'
    <<"j allungamento/accorciamento fit lineare = "<<f_comp(fKa,sfKa,fKb,sfKb)<<'\n'
    <<"j tra k della serie sigma e k media ponderata = "<<f_comp(zK,szK,mK,smK)<<'\n'
    <<"j tra k della serie sigma e k fit lineare = "<<f_comp(zK,szK,fK,sfK)<<'\n'
    <<"j tra k media ponderata e k fit lineare = "<<f_comp(mK,smK,fK,sfK)<<'\n';
    return 0;
}



//funzione media ponderata
double f_media(vector <double> v, vector <double> vs) {
    double sumn = 0.;
    double sumd = 0.;
    for (int i = 0; i < 4; i++) {
        sumn += v.at(i)/ pow(vs.at(i), 2);
    }
    for (auto & c : vs) {
        sumd += 1/ pow(c, 2);
    }

    return sumn/sumd;
}

//funzione incertezza media ponderata
double f_inc(vector <double> vs) {
    double sum = 0.;
    for (auto & c : vs) {
        sum += 1/ pow(c, 2);
    }
    return sqrt(1/sum);
}

//funzione compatibilità
double f_comp(double a, double sa, double b, double sb) {
    return abs(a+b)/sqrt(sa*sa + sb+sb);
}