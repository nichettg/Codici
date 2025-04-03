#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
using namespace std;

/*
dati 1, indici: 0-21
dati 2, indici: 22-43
dati 3, indici: 44-65
dati 4, indici: 66-87
*/

double f_media (vector <int> &, int, int);
double f_dev (vector <int> &, double, int, int);
double f_cov (vector <int> &, vector <int> &, double, double, int, int);
double f_sk (double, double, double, double, double, int);
double f_sK (double, double);

/*double arrotonda(double num, int cifre) {
    double fattore = pow(10, cifre);
    return round(num * fattore) / fattore;
}*/

ifstream input("datiTOT.txt");
ofstream output("data_processed.txt");
ofstream output2("k^-1.txt");
ofstream output3("k^-1sigma.txt");

int main () {
    
    //file di input esterno
    if (!input) {
        cout<<"Errore nell'apertura del file input: datiTOT.txt"<<endl;
        return 1;
    }

    //raccolta dati in vettori
    int a, b, F, x;
    vector <int> dati_F;
    vector <int> dati_x;
    vector <int> dati_F_all;
    vector <int> dati_F_acc;
    vector <int> dati_x_all;
    vector <int> dati_x_acc;

    while (input>>a>>b) {
        F=abs(a);
        x=abs(b);

        dati_F.push_back(F);
        dati_x.push_back(x);
        
        if (a>0) {
            dati_F_all.push_back(a);
        }
        if (a<0) {
            dati_F_acc.push_back(abs(a));
        }

        if (b>0) {
            dati_x_all.push_back(b);
        }
        if (b<0) {
            dati_x_acc.push_back(abs(b));
        }
    }

    for (int k=0; k<4; k++) {
        dati_F_all.push_back(0);
        dati_F_acc.push_back(0);
        dati_x_all.push_back(0);
        dati_x_acc.push_back(0);
    }

    //********************************************************************************************************
    //elaborazione dati con funzioni
    //********************************************************************************************************

    //quattro serie di dati
    output<<"Elaborazione delle quattro serie di dati:"<<'\n';
    for (int i=0; i<=66; i+=22) {

        output<<'\n'<<"Serie "<<(i / 22 + 1)<<":"<<'\n';

        //allungamento
        double media_Fa = f_media(dati_F, i, i+10); //in gp
        double dev_Fa = f_dev(dati_F, media_Fa, i, i+10) * 9.81e-3; //in N
        double media_xa = f_media(dati_x, i, i+10); //in micron
        double dev_xa = f_dev(dati_x, media_xa, i, i+10) * 1e-6; //in m
        double cova = f_cov(dati_x, dati_F, media_xa, media_Fa, i, i+10) * 9.81e-3 * 1e-6; //in N*m

        double ka = (media_Fa / media_xa) * 9.81e-3/1e-6; //in N/m
        double ska = f_sk(media_Fa, media_xa, dev_Fa, dev_xa, cova, 11); //in N/m
        double Ka = (media_xa / media_Fa) * 1e-6/9.81e-3; //in m/N
        double sKa = f_sK(ka, ska); //in m/N

        //accorciamento
        double media_Fb = f_media(dati_F, i+11, i+21); //in gp
        double dev_Fb = f_dev(dati_F, media_Fb, i+11, i+21) * 9.81e-3; //in N
        double media_xb = f_media(dati_x, i+11, i+21); //in micron
        double dev_xb = f_dev(dati_x, media_xb, i+11, i+21) * 1e-6; //in m
        double covb = f_cov(dati_x, dati_F, media_xb, media_Fb, i+11, i+21) * 9.81e-3 * 1e-6; //in N*m

        double kb = (media_Fb / media_xb) * 9.81e-3/1e-6; //in N/m
        double skb = f_sk(media_Fb, media_xb, dev_Fb, dev_xb, covb, 11); //in N/m
        double Kb = (media_xb / media_Fb) * 1e-6/9.81e-3; //in m/N
        double sKb = f_sK(kb, skb); //in m/N      

        //allungamento e accorciamento unite
        double media_F = f_media(dati_F, i, i+21); //in gp
        double dev_F = f_dev(dati_F, media_F, i, i+21) * 9.81e-3; //in N
        double media_x = f_media(dati_x, i, i+21); //in micron
        double dev_x = f_dev(dati_x, media_x, i, i+21) * 1e-6; //in m
        double cov = f_cov(dati_x, dati_F, media_x, media_F, i, i+21) * 9.81e-3 * 1e-6; //in N*m

        double k = (media_F / media_x) * 9.81e-3/1e-6; //in N/m
        double sk = f_sk(media_F, media_x, dev_F, dev_x, cov, 22); //in N/m
        double K = (media_x / media_F) * 1e-6/9.81e-3; //in m/N
        double sK = f_sK(k, sk); //in m/N

        output<<"\n\t§ Allungamento"
        <<"\n\tk = " <<ka<< " N/m"
        <<"\n\tIncertezza k = " <<ska<< " N/m"
        <<"\n\t1/k = " <<Ka<< " m/N"
        <<"\n\tIncertezza 1/k = " <<sKa<< " m/N"

        <<'\n'<<'\n'<<'\t'<<"§ Accorciamento"
        <<'\n'<<'\t'<<"k = "<<kb<<" N/m"
        <<'\n'<<'\t'<<"Incertezza k = "<<skb<<" N/m"
        <<'\n'<<'\t'<<"1/k = "<<Kb<<" m/N"
        <<'\n'<<'\t'<<"Incertezza 1/k = "<<sKb<<" m/N"

        <<'\n'<<'\n'<<'\t'<<"§ Unione allungamento e accorciamento"
        <<'\n'<<'\t'<<"k = "<<k<<" N/m"
        <<'\n'<<'\t'<<"Incertezza k = "<<sk<<" N/m"
        <<'\n'<<'\t'<<"1/k = "<<K<<" m/N"
        <<'\n'<<'\t'<<"Incertezza 1/k = "<<sK<<" m/N"<<'\n';

        output2<<Ka<<'\t'<<sKa<<'\n'
        <<Kb<<'\t'<<sKb<<'\n'
        <<K<<'\t'<<sK<<'\n'<<'\n';
    }

    //unione delle quattro serie di dati
    output<<'\n'<<'\n'<<"Elaborazione della serie di dati generata dall'unione delle quattro precedenti:"<<'\n';

    //allungamento
    double media_Fa = f_media(dati_F_acc, 0, 43); //in gp
    double media_xa = f_media(dati_x_acc, 0, 43); //in micron
    double dev_Fa = f_dev(dati_F_acc, media_Fa, 0, 43) *9.81e-3; //in N
    double dev_xa = f_dev(dati_x_acc, media_xa, 0, 43) *1e-6; //in m
    double cova = f_cov(dati_F_acc, dati_x_acc, media_Fa, media_xa, 0, 43) * 9.81e-3*1e-6; //in N*m

    double ka = (media_Fa / media_xa) * 9.81e-3/1e-6; //in N/m
    double ska = f_sk(media_Fa, media_xa, dev_Fa, dev_xa, cova, 44); //in N/m
    double Ka = (media_xa / media_Fa) * 1e-6/9.81e-3; //in m/N
    double sKa = f_sK(ka, ska); //in m/N

    output<<'\n'<<"§ Allungamento"
    <<'\n'<<'\n'<<'\t'<<"Media F = "<<media_Fa * 9.81e-3<<" N"
    <<'\n'<<'\t'<<"Deviazione Standard F = "<<dev_Fa/sqrt(44)<<" N"
    <<'\n'<<'\t'<<"Media x = "<<media_xa * 1e-6<<" m"
    <<'\n'<<'\t'<<"Deviazione Standard x = "<<dev_xa/sqrt(44)<<" m"
    <<'\n'<<'\t'<<"COV[F,x] = "<<cova<<" N*m"
    <<'\n'<<'\t'<<"Coefficiente correlazione Pearson = "<<cova/(dev_xa * dev_Fa)

    <<'\n'<<'\n'<<'\t'<<"k = "<<ka<<" N/m"
    <<'\n'<<'\t'<<"Incertezza k = "<<ska<<" N/m"
    <<'\n'<<'\t'<<"1/k = "<<Ka<<" m/N"
    <<'\n'<<'\t'<<"Incertezza 1/K = "<<sKa<<" m/N";

    //accorciamento
    double media_Fb = f_media(dati_F_all, 0, 43); //in gp
    double media_xb = f_media(dati_x_all, 0, 43); //in micron
    double dev_Fb = f_dev(dati_F_all, media_Fb, 0, 43) *9.81e-3; //in N
    double dev_xb = f_dev(dati_x_all, media_xb, 0, 43) *1e-6; //in m
    double covb = f_cov(dati_F_all, dati_x_all, media_Fb, media_xb, 0, 43) * 9.81e-3*1e-6; //in N*m

    double kb = (media_Fb / media_xb) * 9.81e-3/1e-6; //in N/m
    double skb = f_sk(media_Fb, media_xb, dev_Fb, dev_xb, covb, 44); //in N/m
    double Kb = (media_xb / media_Fb) * 1e-6/9.81e-3; //in m/N
    double sKb = f_sK(kb, skb); //in m/N

    output<<'\n'<<'\n'<<"§ Accorciamento"
    <<'\n'<<'\n'<<'\t'<<"Media F = "<<media_Fb * 9.81e-3<<" N"
    <<'\n'<<'\t'<<"Deviazione Standard F = "<<dev_Fb/sqrt(44)<<" N"
    <<'\n'<<'\t'<<"Media x = "<<media_xb * 1e-6<<" m"
    <<'\n'<<'\t'<<"Deviazione Standard x = "<<dev_xb/sqrt(44)<<" m"
    <<'\n'<<'\t'<<"COV[F,x] = "<<covb<<" N*m"
    <<'\n'<<'\t'<<"Coefficiente correlazione Pearson = "<<covb/(dev_xb * dev_Fb)

    <<'\n'<<'\n'<<'\t'<<"k = "<<kb<<" N/m"
    <<'\n'<<'\t'<<"Incertezza k = "<<skb<<" N/m"
    <<'\n'<<'\t'<<"1/k = "<<Kb<<" m/N"
    <<'\n'<<'\t'<<"Incertezza 1/K = "<<sKb<<" m/N";

    //unione
    double media_FTOT = f_media(dati_F, 0, 87); //in gp
    double media_xTOT = f_media(dati_x, 0, 87); //in micron
    double dev_FTOT = f_dev(dati_F, media_FTOT, 0, 87) *9.81e-3; //in N
    double dev_xTOT = f_dev(dati_x, media_xTOT, 0, 87) *1e-6; //in m
    double covTOT = f_cov(dati_F, dati_x, media_FTOT, media_xTOT, 0, 87) * 9.81e-3*1e-6; //in N*m

    double kTOT = (media_FTOT / media_xTOT) * 9.81e-3/1e-6; //in N/m
    double skTOT = f_sk(media_FTOT, media_xTOT, dev_FTOT, dev_xTOT, covTOT, 88); //in N/m
    double KTOT = (media_xTOT / media_FTOT) * 1e-6/9.81e-3; //in m/N
    double sKTOT = f_sK(kTOT, skTOT); //in m/N

    output<<'\n'<<'\n'<<"§ Unione allungamento e accorciamento"
    <<'\n'<<'\n'<<'\t'<<"Media F = "<<media_FTOT * 9.81e-3<<" N"
    <<'\n'<<'\t'<<"Deviazione Standard F = "<<dev_FTOT/sqrt(44)<<" N"
    <<'\n'<<'\t'<<"Media x = "<<media_xTOT * 1e-6<<" m"
    <<'\n'<<'\t'<<"Deviazione Standard x = "<<dev_xTOT/sqrt(44)<<" m"
    <<'\n'<<'\t'<<"COV[F,x] = "<<covTOT<<" N*m"
    <<'\n'<<'\t'<<"Coefficiente correlazione Pearson = "<<covTOT/(dev_xTOT * dev_FTOT)

    <<'\n'<<'\n'<<'\t'<<"k = "<<kTOT<<" N/m"
    <<'\n'<<'\t'<<"Incertezza k = "<<skTOT<<" N/m"
    <<'\n'<<'\t'<<"1/k = "<<KTOT<<" m/N"
    <<'\n'<<'\t'<<"Incertezza 1/K = "<<sKTOT<<" m/N";

    output3<<Ka<<'\t'<<sKa<<'\n'
    <<Kb<<'\t'<<sKb<<'\n'
    <<KTOT<<'\t'<<sKTOT;

    return 0;
}




//******************************************************************************************************************
//funzioni
//******************************************************************************************************************

//funzione media (vettore di dati, indice inizio, indice fine)
double f_media (vector <int> & v, int i, int f) {
    int somma = 0;
    int d = 0;
    for (int n = i ; n <= f; n++) {
        somma += v.at(n);
        d++;
    }
    return somma/d;
}

//funzione deviazione standard (vettore di dati, double media, indice inizio, indice fine)
double f_dev (vector <int> & v, double m, int i, int f) {
    double somma = 0.;
    int d = 0;
    for (int n = i; n <= f; n++ ) {
        somma += pow(v.at(n) - m, 2);
        d++;
    }
    return sqrt(somma/(d-1));
}

//funzione covarianza (vettore di dati 1, vettore di dati 2, double media 1, double media 2, indice inizio, indice fine)
double f_cov (vector <int> & v1, vector <int> & v2, double m1, double m2, int i, int f) {
    double somma = 0.;
    int d = 0;
    for (int n = i; n <= f; n++) {
        somma += (v1.at(n) - m1)*(v2.at(n) - m2);
        d++;
    }
    return somma/(d-1);
}

//funzione equazione sk (F medio, x medio, dev F campionaria, dev x campionaria, cov Fx, numerosità)
double f_sk (double F0, double x0, double sF, double sx, double cov, int n) {
    double x = x0 * 1e-6; //micron -> m
    double F = F0 * 9.81e-3; //gp -> N
    //double q = ((pow(sF,2)/pow(x,2)) + pow(F,2)*pow(sx,2)/pow(x,4) - 2*(F/pow(x,3))*cov*n)/n;
    double q = ((pow(sF,2)/pow(x,2)) + pow(F,2)*pow(sx,2)/pow(x,4))/n;

    if (q<=0) {
        cerr<<"Radice di numero negativo"<<'\n';
        return 1;
    }

    return sqrt(q);
}

//funzione equazione sK (sk)
double f_sK (double k, double sk) {
    return sk/pow(k,2);
}