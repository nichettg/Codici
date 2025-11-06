#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <string>
#include <sstream>
#include <iomanip>

using namespace std;

string iname;

ofstream output("plot.txt");
ofstream output_chi("elaborato.txt");

double f_media(const vector<double>&);
double f_dev(const vector<double>&, double);
double f_sv(double, double, double, double);

// Interpolazione lineare: caso 2
double f_delta(const vector<double>&, const vector<double>&);
double f_a(const vector<double>&, const vector<double>&, const vector<double>&, double);
double f_b(const vector<double>&, const vector<double>&, const vector<double>&, double);
double f_sa(const vector<double>&, const vector<double>&, double);
double f_sb(const vector<double>&, const vector<double>&, double);

double f_cov(const vector<double>&, const vector<double>&, double, double);
double f_covpar(double, int, double, double);
double f_pearson(double, double, double);

double f_errpost(const vector<double>&, const vector<double>&, double, double);
void chi_quadro(const vector<double>&, const vector<double>&, double, double, const vector<double>&);

int main() {
    
    cout << "Digita il nome del file di input: ";
    cin >> iname;
    ifstream input(iname);

        const double sx = (0.5 * 1e-3) / sqrt(24);

        double a1, b1, b2, b3, b4, b5;
        vector<double> vt, vv, vst, vsv, vx;

        while (input >> a1 >> b1 >> b2 >> b3 >> b4 >> b5) {
            vector<double> dati_t = { b1, b2, b3, b4, b5 };

            double x = (a1 - 40) * 1e-2;  // m
            double media_t = f_media(dati_t);  // s
            double dev_t = f_dev(dati_t, media_t);

            double v = x / (media_t);  // m/s
            double sv = f_sv(x, media_t, sx, dev_t);

            output << setw(10) << media_t / 2 << setw(10) << v << setw(15) << dev_t / sqrt(dati_t.size())
                   << setw(15) << sv << '\n';
            // formato t(s), v(m/s), st, sv

            // vettori con i dati del file plot.txt
            vt.push_back(media_t / 2);        // campione delle medie dei campioni di t
            vv.push_back(v);                  // campione delle velocità dei campioni
            vst.push_back(dev_t / sqrt(dati_t.size()));  // incertezze t
            vsv.push_back(sv);                // incertezze v
            vx.push_back(x);                  // vettore con i x
        }

        // calcolo parametri a e b
        double delta = f_delta(vt, vsv);
        double a = f_a(vt, vv, vsv, delta);
        double b = f_b(vt, vv, vsv, delta);
        double sa = f_sa(vt, vsv, delta);
        double sb = f_sb(vt, vsv, delta);

        output_chi << "v0 = " << a << " +/- " << sa << '\n'
                   << "a = " << b << " +/- " << sb << '\n';

        // correlazione campioni t e v
        double tm = f_media(vt);
        double vm = f_media(vv);
        double cov_tv = f_cov(vt, vv, tm, vm);
        double tdev = f_dev(vt, tm);
        double vdev = f_dev(vv, vm);
        double pearson_tv = f_pearson(cov_tv, tdev, vdev);

        output_chi << '\n'
                   << "Covarianza tra t e v = " << cov_tv << '\n'
                   << "Indice di correlazione lineare (Pearson) = " << pearson_tv << '\n';

        // correlazione parametri a e b
        double svm = f_media(vsv);  // media delle incertezze delle v, usata per la cov_ab
        double cov_ab = f_covpar(tm, vt.size(), svm, tdev);
        double pearson_ab = f_pearson(cov_ab, sa, sb);

        output_chi << '\n'
                   << "Covarianza tra v0 e a = " << cov_ab << '\n'
                   << "Indice di correlazione lineare (Pearson) = " << pearson_ab << '\n';

        // errore a posteriori interpolazione
        double err = f_errpost(vt, vv, a, b);
        output_chi << '\n'
                   << "Errore a posteriori = " << err << '\n'
                   << "Media delle incertezze delle v = " << svm << '\n' << '\n';

        // chi quadro
        chi_quadro(vt, vv, a, b, vsv);

        // calcolo di g
        double g = b / sin(18.75 / 60.0 * M_PI / 180.0);
        double sg = sb / sin(18.75 / 60.0 * M_PI / 180.0);

        output_chi << "Stima di g = " << g << " +/- " << sg << '\n';

        return 0;
    }

// funzione media
double f_media(const vector<double>& v) {
    double somma = 0.;
    for (auto& c : v) {
        somma += c;
    }
    return somma / v.size();
}

// funzione deviazione standard
double f_dev(const vector<double>& v, double m) {
    double somma = 0.;
    for (auto& c : v) {
        somma += pow(c - m, 2);
    }
    return sqrt(somma / (v.size() - 1));
}

// Funzione propagazione errori sv
double f_sv(double x, double t, double sx, double st) {
    return (x / t) * sqrt(pow(sx / x, 2) + pow(st / t, 2) + 2*(sx/x)*(st/t));
}

// Funzione delta
double f_delta(const vector<double>& vx, const vector<double>& vsy) {
    double sum1 = 0., sum2 = 0., sum3 = 0.;

    for (int i = 0; i < vx.size(); i++) {
        sum1 += 1 / (vsy[i] * vsy[i]);
        sum2 += (vx[i] * vx[i]) / (vsy[i] * vsy[i]);
        sum3 += vx[i] / (vsy[i] * vsy[i]);
    }

    return sum1 * sum2 - sum3 * sum3;
}

// Funzione parametro a
double f_a(const vector<double>& vx, const vector<double>& vy, const vector<double>& vsy, double delta) {
    double sum1 = 0., sum2 = 0., sum3 = 0., sum4 = 0.;

    for (int i = 0; i < vx.size(); i++) {
        sum1 += (vx[i]*vx[i]) / (vsy[i]*vsy[i]);
        sum2 += vy[i] / (vsy[i]*vsy[i]);
        sum3 += vx[i] / (vsy[i]*vsy[i]);
        sum4 += (vx[i]*vy[i]) / (vsy[i]*vsy[i]);
    }

    return (sum1 * sum2 - sum3 * sum4) / delta;
}

// Funzione parametro b
double f_b(const vector<double>& vx, const vector<double>& vy, const vector<double>& vsy, double delta) {
    double sum1 = 0., sum2 = 0., sum3 = 0., sum4 = 0.;

    for (int i = 0; i < vx.size(); i++) {
        sum1 += 1/ (vsy[i]*vsy[i]);
        sum2 += (vx[i]*vy[i]) / (vsy[i]*vsy[i]);
        sum3 += vx[i] / (vsy[i]*vsy[i]);
        sum4 += vy[i] / (vsy[i]*vsy[i]);
    }

    return (sum1 * sum2 - sum3 * sum4) / delta;
}

// Funzione incertezza parametro a
double f_sa(const vector<double>& vx, const vector<double>& vsy, double delta) {
    double sum = 0.;
   
    for (int i = 0; i < vx.size(); i++) {
        sum += (vx[i]*vx[i]) / (vsy[i]*vsy[i]);
    }

    return sqrt(sum / delta);
}

// Funzione incertezza parametro b
double f_sb(const vector<double>& vx, const vector<double>& vsy, double delta) {
    double sum = 0.;
   
    for (int i = 0; i < vx.size(); i++) {
        sum += 1 / (vsy[i]*vsy[i]);
    }

    return sqrt(sum / delta);
}


// Funzione covarianza
double f_cov (const vector<double>& v1, const vector<double>& v2, double m1, double m2) {
    double somma = 0.;

    for (int i = 0; i < v1.size(); i++) {
        somma += (v1.at(i) - m1)*(v2.at(i) - m2);
    }

    return somma/(v1.size()-1);
}

// Funzione covarianza parametri
double f_covpar (double x, int N, double sy, double Sx) {
    return -(x*sy*sy)/(N*Sx*Sx);
}

// Funzione indice correlazione pearson
double f_pearson (double cov, double devx, double devy) {
    return cov/ (devx*devy);
}

// Funzione errore a posteriori
double f_errpost (const vector <double> & vx,const vector <double> & vy, double a, double b) {
    double sum = 0.;
    for (int i = 0; i < vx.size(); i++) {
        sum += pow(vy[i] - (a + b * vx[i]), 2);
    }
    return sqrt(sum / (vx.size() - 2));
}

//funzione chi quadro
void chi_quadro (const vector <double> & x, const vector <double> & y, double a, double b, const vector <double>& sy) {
    double sum = 0.;

    output_chi << "Test Chi Quadro_____________________________________________"<<'\n';
    output_chi << setw(10) << "t (s)" << setw(10) << "v (m/s)" << setw(13) << "sv (m/s)" << setw(14) << "v* (s)" << setw(13) << "Chi-quadro" << '\n';

    for (int i = 0; i < x.size(); i++) {
        sum += pow((y[i] - (a + b * x[i])) / sy[i], 2);
        output_chi << setw(10) << x[i] << setw(10) << y[i] << setw(13) << sy[i] << setw(14) << a + b * x[i] << setw(13) << pow((y[i] - (a + b * x[i])) / sy[i], 2) << '\n';
    }

    int NDOF = x.size() - 2;
    output_chi << '\n' << "Gradi di libertà = " << NDOF << '\n'
    << "Chi-quadro = " << sum << '\n';
}