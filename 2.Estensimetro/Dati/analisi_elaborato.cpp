#include <iostream>
#include <cmath>
#include <fstream>
#include <vector>
using namespace std;

ifstream input ("fit_analitico.txt");

double f_media(const vector<double>&, const vector <double>&);
double f_inc(const vector<double>&);
double f_comp(double,double,double,double);

vector <double> dati_all, dati_acc, s_all, s_acc;

int main () {

    double a, b, c, d, e, f, g, h;
    while (input>>a>>b>>c>>d>>e>>f>>g>>h) {
        dati_all.push_back(c);
        s_all.push_back(d);
        dati_acc.push_back(g);
        s_acc.push_back(h);
    }

    double k_all = f_media(dati_all, s_all);
    double sk_all = f_inc(s_all);
    double k_acc = f_media(dati_acc, s_acc);
    double sk_acc = f_inc(s_acc);
    double comp_all_acc = f_comp(k_all,sk_all,k_acc,sk_acc);

    cout << "Fit analitico " << '\n'
    << "k allungamento = " << k_all << " +/- " << sk_all << '\n'
    << "k accorciamento = " << k_acc << " +/- " << sk_acc << '\n'
    << "Compatibilità (all-acc): " << comp_all_acc << '\n' << '\n';

    //media ponderata kacc e kall
    vector <double> vk = {k_all,k_acc};
    vector <double> vsk = {sk_all, sk_acc};
    double k = f_media(vk,vsk);
    double sk = f_inc(vsk);
    cout << "k = " << k << " +/- " << sk << '\n' << '\n';

    //gnuplot
    const double k_all_gnu = 4.4024e-05;
    const double sk_all_gnu = 9.79e-08;
    const double k_acc_gnu = 4.44757e-05;
    const double sk_acc_gnu = 9.231e-08;
    double comp_all_acc_gnu = f_comp(k_all_gnu,sk_all_gnu,k_acc_gnu,sk_acc_gnu);

    cout << "Fit gnuplot" << '\n'
    << "k allungamento = " << k_all_gnu << " +/- " << sk_all_gnu << '\n'
    << "k accorciamento = " << k_acc_gnu << " +/- " << sk_acc_gnu << '\n'
    << "Compatibilità (all-acc): " << comp_all_acc_gnu << '\n' << '\n';
    vector <double> vk_gnu = {k_all_gnu,k_acc_gnu};
    vector <double> vsk_gnu = {sk_all_gnu, sk_acc_gnu};
    double k_gnu = f_media(vk_gnu,vsk_gnu);
    double sk_gnu = f_inc(vsk_gnu);
    cout << "k = " << k_gnu << " +/- " << sk_gnu << '\n' << '\n'<<'\n';

    //compatibilità fit analitico e fit gnuplot
    double comp_finale = f_comp(k,sk,k_gnu,sk_gnu);
    cout << "Compatiblità tra k del fit analitico e k del fit gnuplot = " << comp_finale <<'\n';
    return 0;
}

//funzione media ponderata
double f_media(const vector <double>& v, const vector <double>& vs) {
    double sumn = 0.;
    double sumd = 0.;
    for (int i = 0; i < v.size(); i++) {
        sumn += v.at(i)/ pow(vs.at(i), 2);
    }
    for (auto & c : vs) {
        sumd += 1/ pow(c, 2);
    }

    return sumn/sumd;
}

//funzione incertezza media ponderata
double f_inc(const vector <double>& vs) {
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