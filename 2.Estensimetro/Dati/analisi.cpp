#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <string>

using namespace std;

ifstream input1a ("dati1a.txt");
ifstream input1b ("dati1b.txt");
ifstream input2a ("dati2a.txt");
ifstream input2b ("dati2b.txt");
ifstream input3a ("dati3a.txt");
ifstream input3b ("dati3b.txt");
ifstream input4a ("dati4a.txt");
ifstream input4b ("dati4b.txt");
ofstream output2 ("fit_gnuplot.txt");
ofstream output3 ("fit_analitico.txt");
ofstream output4 ("elaborato.txt");

double f_delta(const vector<double>&);
double f_a(const vector<double>&, const vector<double>&, double);
double f_b(const vector<double>&, const vector<double>&, double);
double f_ia(const vector<double>&, double, double);
double f_ib(const vector<double>&, double, double);
double f_media(const vector<double>&);
double f_dev(const vector<double>&, double);
double f_devres (const vector <double> &, const vector <double> &, double, double);
double f_covpar (double, int, double, double);
double f_pearson (double, double, double);
double f_errpost (const vector <double> &,const vector <double> &, double, double);
void chi_quadro (const vector <double> &, const vector <double> &, double, double, double);

vector <double> dati_F, dati_Fm, dati_x1a, dati_x1b, dati_x2a, dati_x2b, dati_x3a, dati_x3b, dati_x4a, dati_x4b;

int main() {

    const double sy = (10e-6) / (2 * sqrt(6)); //incertezza sperimentale allungamenti x (m)

    if (!input1a) {
        cerr<<"Errore apertura file input"<<'\n';
        return 1;
    }

    double F,x;
    while (input1a >> F >> x) {
        dati_F.push_back(F*9.81e-3); //cambio unità di misura gp -> N e micron -> m, tutti i calcoli e risultati saranno in N e m
        dati_x1a.push_back(x*1e-6);
    }
    while (input1b >> F >> x) {
        dati_Fm.push_back(F*9.81e-3);
        dati_x1b.push_back(x*1e-6);
    }
    while (input2a >> F >> x) {
        dati_x2a.push_back(x*1e-6);
    }
    while (input2b >> F >> x) {
        dati_x2b.push_back(x*1e-6);
    }
    while (input3a >> F >> x) {
        dati_x3a.push_back(x*1e-6);
    }
    while (input3b >> F >> x) {
        dati_x3b.push_back(x*1e-6);
    }
    while (input4a >> F >> x) {
        dati_x4a.push_back(x*1e-6);
    }
    while (input4b >> F >> x) {
        dati_x4b.push_back(x*1e-6);
    }
    
    //vettore contenitore dei vettori dati_x
    vector <vector<double>> v = {dati_x1a, dati_x1b, dati_x2a, dati_x2b, dati_x3a, dati_x3b, dati_x4a, dati_x4b};    
    
    // y = a + bx

    for (int i = 0; i < 8; i++) { //ciclo ripetuto per ogni serie

        double a = 0., b = 0., devres_F = 0., sa1 = 0., sb1 = 0., sa2 = 0., sb2 = 0., sab = 0., err = 0., media_F = 0., dev_F = 0., pearson = 0.;

        if (i % 2 == 0) { //non dispari (cioè allungamenti)
            double delta = f_delta(dati_F);
            if (delta <= 0) {
                cerr<<"Errore calcolo delta:    delta = "<<delta<<'\n';
                return 1;
            }
            media_F = f_media(dati_F);
            dev_F = f_dev(dati_F, media_F);
            a = f_a(dati_F, v[i], delta);
            b = f_b(dati_F, v[i], delta);
            devres_F = f_devres(dati_F, v[i], a, b);
            sa1 = f_ia(dati_F, delta, sy);
            sb1 = f_ib(v[i], delta, sy);
            sa2 = f_ia(dati_F, delta, devres_F);
            sb2 = f_ib(v[i], delta, devres_F);
            sab = f_covpar(media_F,dati_F.size(),sy,dev_F);
            pearson = f_pearson(sab, sa1, sb1);
            err = f_errpost(dati_F, v[i], a, b);


            output4 << "************************************************************" << '\n'
            << "Serie " << (i+2)/2 << " allungamento" << '\n'
            << "************************************************************" << '\n' << '\n'
            << "Regressione lineare y = a + bx______________________________" << '\n'
            << "a = "<< a << " +/- " << sa1 << '\n' //elaborato.txt
            << "b = " << b << " +/- " << sb1 << '\n'
            << '\t' << "Correlazione tra i parametri di interpolazione = " << sab << '\n'
            << '\t' << "Indice di correlazione dei parametri = " << pearson << '\n' << '\n'
            << "Test errore a posteriori____________________________________" << '\n'
            << "Errore a posteriori = " << err << '\n'
            << "Errore ascisse (sy) = " << sy << '\n';
            if (err > sy) {
                output4 << '\t' << "Sottostima di sy, incertezze sperimentali piccole" << '\n' << '\n';
            }
            else if (err < sy) {
                output4 << '\t' << "Sovrastima di sy, incertezze sperimentali grandi (overfitting)" << '\n' <<'\n';
            }

            chi_quadro (dati_F, v[i], a, b, sy);
            output4 << '\n' << '\n';
        }
        else { //dispari (cioè accorciamenti)
            double delta = f_delta(dati_F);
            if (delta <= 0) {
                cerr<<"Errore calcolo delta:    delta = "<<delta<<'\n';
                return 1;
            }
            media_F = f_media(dati_F);
            dev_F = f_dev(dati_F, media_F);
            a = f_a(dati_Fm, v[i], delta);
            b = f_b(dati_Fm, v[i], delta);
            devres_F = f_devres(dati_Fm, v[i], a, b);
            sa1 = f_ia(dati_Fm, delta, sy);
            sb1 = f_ib(v[i], delta, sy);
            sa2 = f_ia(dati_Fm, delta, devres_F);
            sb2 = f_ib(v[i], delta, devres_F);
            sab = f_covpar(media_F,dati_Fm.size(),sy,dev_F);
            pearson = f_pearson(sab, sa1, sb1);
            err = f_errpost(dati_Fm, v[i], a, b);


            output4 << "************************************************************" << '\n'
            << "Serie " << (i+1)/2<< " accorciamento" << '\n'
            << "************************************************************" << '\n' << '\n'
            << "Regressione lineare y = a + bx______________________________" << '\n'
            << "a = "<< a << " +/- " << sa1 << '\n' //elaborato.txt
            << "b = " << b << " +/- " << sb1 << '\n'
            << '\t' << "Correlazione tra i parametri di interpolazione = " << sab << '\n'
            << '\t' << "Coefficiente di correlazione dei parametri = " << pearson << '\n' << '\n'
            << "Test errore a posteriori____________________________________" << '\n'
            << "Errore a posteriori = " << err << '\n'
            << "Errore ascisse (sy) = " << sy << '\n';
            if (err > sy) {
                output4 << '\t' << "Sottostima di sy, incertezze sperimentali piccole" << '\n' << '\n';
            }
            else if (err < sy) {
                output4 << '\t' << "Sovrastima di sy, incertezze sperimentali grandi (overfitting)" << '\n' <<'\n';
            }

            chi_quadro (dati_Fm, v[i], a, b, sy);
            output4 << '\n' << '\n';
        }
        
        output2 << a <<'\t'<< sa2 << '\n' //fit_gnuplot.txt, è come lo farebbe gnuplot
        << b <<'\t'<< sb2 << '\n'<<'\n';

        output3 << a <<'\t'<< sa1 << '\n' //fit_analitico.txt
        << b <<'\t'<< sb1 << '\n'<<'\n';
    }

    return 0;
}

// Funzione delta
double f_delta(const vector<double>& vx) {
    double sum1 = 0., sum2 = 0.;
    for (auto & x : vx) {
        sum1 += x * x;
        sum2 += x;
    }
    return vx.size() * sum1 - sum2 * sum2;
}

// Funzione parametro a
double f_a(const vector<double>& vx, const vector<double>& vy, double delta) {
    double sum1 = 0., sum2 = 0., sum3 = 0., sum4 = 0.;

    for (size_t i = 0; i < vx.size(); i++) {
        sum1 += vx[i] * vx[i];
        sum2 += vy[i];
        sum3 += vx[i];
        sum4 += vx[i] * vy[i];
    }

    return (sum1 * sum2 - sum3 * sum4) / delta;
}

// Funzione parametro b
double f_b(const vector<double>& vx, const vector<double>& vy, double delta) {
    double sum1 = 0., sum2 = 0., sum3 = 0.;

    for (size_t i = 0; i < vx.size(); i++) {
        sum1 += vx[i] * vy[i];
        sum2 += vx[i];
        sum3 += vy[i];
    }

    return (vx.size() * sum1 - sum2 * sum3) / delta;
}

// Funzione incertezza parametro a
double f_ia(const vector<double>& vx, double delta, double incertezza) {
    double sum = 0.;
    for (auto & x : vx) {
        sum += x * x;
    }
    return (sqrt(sum / delta)) * incertezza;
}

// Funzione incertezza parametro b
double f_ib(const vector<double>& v, double delta, double incertezza) {
    return (sqrt(v.size() / delta)) * incertezza;
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

//funzione deviazione standard residua
double f_devres (const vector <double> & vx, const vector <double> & vy, double a, double b) {
    double sum = 0.;
    for (int i = 0; i < vx.size(); i++) {
        sum += pow(vy[i]-a-b*vx[i],2);
    }
    return sqrt(sum/(vx.size()-2));
}

//funzione covarianza parametri
double f_covpar (double x, int N, double sy, double Sx) {
    return -(x*sy*sy)/(N*Sx*Sx);
}

//funzione indice correlazione
double f_pearson (double cov, double x, double y) {
    return cov/( pow(x,2) + pow(y,2));
}

//funzione errore a posteriori
double f_errpost (const vector <double> & vx,const vector <double> & vy, double a, double b) {
    double sum = 0.;
    for (int i = 0; i < vx.size(); i++) {
        sum += pow(vy[i] - (a + b * vx[i]), 2);
    }
    return sqrt(sum / (vx.size() - 2));
}

//funzione chi quadro
void chi_quadro (const vector <double> & x, const vector <double> & y, double a, double b, double sy) {
    double sum = 0.;

    output4 << "Test Chi Quadro_____________________________________________"<<'\n';
    output4 << setw(10) << "F (N)" << setw(10) << "x (m)" << setw(13) << "sy (m)" << setw(14) << "x* (m)" << setw(13) << "Chi-quadro" << '\n';

    for (int i = 0; i < x.size(); i++) {
        sum += pow((y[i] - (a + b * x[i])) / sy, 2);
        output4 << setw(10) << x[i] << setw(10) << y[i] << setw(13) << sy << setw(14) << a + b * x[i] << setw(13) << pow((y[i] - (a + b * x[i])) / sy, 2) << '\n';
    }

    int NDOF = x.size() - 2;
    output4 << '\n' << "Gradi di libertà = " << NDOF << '\n'
    << "Chi-quadro = " << sum << '\n';
    double critico1 = 16.919, critico2 = 19.023, critico3 = 21.666, critico4 = 23.589;
    
    if (sum > 24) {
        output4 << '\t' << "Test superato con una confidenza maggiore di 0.995" << '\n'
        << '\t' << "Attenzione! Probabile overfitting." << '\n';
    }
    else if (sum > critico4) {
        output4 << "Test superato con una confidenza di 0.995" << '\n';
    }
    else if (sum > critico3) {
        output4 << "Test superato con una confidenza di 0.99" << '\n';
    }
    else if (sum > critico2) {
        output4 << "Test superato con una confidenza di 0.975" << '\n';
    }
    else if (sum > critico1) {
        output4 << "Test superato con una confidenza di 0.95" << '\n';
    }
    else {
        output4 << "Test non superato per confidenza di 0.95" << '\n';
    }

    output4 << '\n';
}