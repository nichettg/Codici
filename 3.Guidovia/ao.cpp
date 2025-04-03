#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <string>
#include <sstream>
#include <iomanip>

using namespace std;

string iname, oname;

ofstream output_chi("elaborato.txt", ios::trunc);
bool first_append = true;
ofstream output_g("g_costanti.txt", ios::trunc);

double f_media(const vector<double>&);
double f_dev(const vector<double>&, double);
double f_sv(double, double, double, double);

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

    const double sx = (0.5 * 1e-3) / sqrt(24);
    double a1, b1, b2, b3, b4, b5;
    vector<double> vt, vv, vst, vsv, vx;

    for (int i = 0; i < 4; i++) {
        if (first_append == false) {
            output_chi << '\n' << '\n' << '\n';
        }
        first_append = false;
        
        if (i == 0) {
            iname = "progressivo1.txt";
            oname = "plot1.txt";
            output_chi << "SERIE 1" << '\n'
            << "Potenza 3, Inclinazione 18.75', Carrellino vuoto" << '\n' << '\n';
        }
        if (i == 1) {
            iname = "progressivo2.txt";
            oname = "plot2.txt";
            output_chi << "SERIE 2" << '\n'
            << "Potenza 3, Inclinazione 18.75', Carrellino un ottone" << '\n' << '\n';
        }
        if (i == 2) {
            iname = "progressivo3.txt";
            oname = "plot3.txt";
            output_chi << "SERIE 3" << '\n'
            << "Potenza 3, Inclinazione 18.75', Carrellino un ottone e due alluminio" << '\n' << '\n';
        }
        if (i == 3) {
            iname = "progressivo4.txt";
            oname = "plot4.txt";
            output_chi << "SERIE 4" << '\n'
            << "Potenza 4, Inclinazione 18.75', Carrellino vuoto" << '\n' << '\n';
        }

        ifstream input(iname);
        ofstream output(oname);

        if(!input) {
            cerr << "Errore apertura file " << iname << '\n';
            return 1;
        }
        if(!output) {
            cerr << "Errore apertura file " << oname << '\n';
            return 1;
        }
        if(!output_chi) {
            cerr << "Errore apertura file elaborato.txt" << '\n';
            return 1;
        }

        vt.clear();
        vv.clear();
        vst.clear();
        vsv.clear();
        vx.clear();

        while (input >> a1 >> b1 >> b2 >> b3 >> b4 >> b5) {
            vector<double> dati_t = { b1, b2, b3, b4, b5 };

            double x = (a1 - 40) * 1e-2;  // m
            double media_t = f_media(dati_t);  // s
            double dev_t = f_dev(dati_t, media_t);
            
            double v = x / media_t;  // m/s
            double sv = f_sv(x, media_t, sx, dev_t);

            output << setw(10) << media_t / 2 << setw(10) << v << setw(15) << dev_t / sqrt(dati_t.size())
                   << setw(15) << sv << '\n';
            
            vt.push_back(media_t / 2);
            vv.push_back(v);
            vst.push_back(dev_t / sqrt(dati_t.size()));
            vsv.push_back(sv);
            vx.push_back(x);
        }

        double delta = f_delta(vt, vsv);
        double a = f_a(vt, vv, vsv, delta);
        double b = f_b(vt, vv, vsv, delta);
        double sa = f_sa(vt, vsv, delta);
        double sb = f_sb(vt, vsv, delta);

        output_chi << "v(t) = v0 + at" << '\n'
        << "v0 = " << a << " +/- " << sa << '\n'
        << "a = " << b << " +/- " << sb << '\n' << '\n';

        // calcolo di g
        double alpha = 18.75 / 60.0 * M_PI / 180.0; //alpha in rad
        double salpha = sqrt( pow( (5./(12.*60.0)*M_PI/180.0)/sqrt(24.), 2 ) + pow( (0.5/60.*M_PI/180.)/sqrt(12.), 2 ) ); //incertezza alpha in rad
        double salphaBRUTTO = (5./(6.*60.0)*M_PI/180.0)/sqrt(24.); //incertezza senza errore orizzontalizzazione
        double g = b / sin(18.75 / 60.0 * M_PI / 180.0);
        double sg = sqrt ( pow(sb/ sin(alpha), 2) + pow(b * cos(alpha) * salpha / (sin (alpha) * sin (alpha)), 2 ));
        double sgBRUTTO = sqrt ( pow(sb/ sin(alpha), 2) + pow(b * cos(alpha) * salphaBRUTTO / (sin (alpha) * sin (alpha)), 2 ));

        output_chi << "Incertezza alpha senza errore orizzontalizzazione = " << salphaBRUTTO << '\n'
        << "Incertezza alpha con errore orizzontalizzazione = " << salpha << '\n'
        << "Stima di g senza errore orizzontalizzazione= " << g << " +/- " << sgBRUTTO << '\n'
        << "Stima di g con errore orizzontalizzazione= " << g << " +/- " << sg << '\n' << '\n';
        output_g << i+1 << '\t' << g << '\t' << sg << '\n';

        // correlazione campioni t e v
        double tm = f_media(vt);
        double vm = f_media(vv);
        double cov_tv = f_cov(vt, vv, tm, vm);
        double tdev = f_dev(vt, tm);
        double vdev = f_dev(vv, vm);
        double pearson_tv = f_pearson(cov_tv, tdev, vdev);

        /*output_chi << '\n'
                   << "Covarianza tra t e v = " << cov_tv << '\n'
                   << "Indice di correlazione lineare (Pearson) = " << pearson_tv << '\n';*/

        // correlazione parametri a e b
        double svm = f_media(vsv);  // media delle incertezze delle v, usata per la cov_ab
        double cov_ab = f_covpar(tm, vt.size(), svm, tdev);
        double pearson_ab = f_pearson(cov_ab, sa, sb);

        /*output_chi << '\n'
                   << "Covarianza tra v0 e a = " << cov_ab << '\n'
                   << "Indice di correlazione lineare (Pearson) = " << pearson_ab << '\n';*/        

        // chi quadro
        chi_quadro(vt, vv, a, b, vsv);

        // errore a posteriori interpolazione
        double err = f_errpost(vt, vv, a, b);
        int magg = 0, min = 0;

        output_chi << '\n' << "Test Errore a Posteriori____________________________________" << '\n'
        << setw(20) << "Deviazione Residua" << setw(30) << "Incertezza Ordinate" << '\n';
        for (auto & c: vsv) {
            output_chi << setw(20) << err << setw(10);
            if(err > c) {
                output_chi << ">";
                magg++;
            }
            if(err < c) {
                output_chi << "<";
                min++;
            }
            output_chi << setw(20) << c << '\n';
        }
        output_chi << '\n' << "Deviazioni Residue maggiori delle Incertezze: " << magg << '\n'
        << "Deviazioni Redisue minori delle Incertezze: " << min << '\n';
    }

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
    return (x / t) * sqrt(pow(sx / x, 2) + pow(st / t, 2));
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
        sum1 += (vx[i] * vx[i]) / (vsy[i] * vsy[i]);
        sum2 += vy[i] / (vsy[i] * vsy[i]);
        sum3 += vx[i] / (vsy[i] * vsy[i]);
        sum4 += (vx[i] * vy[i]) / (vsy[i] * vsy[i]);
    }

    return (sum1 * sum2 - sum3 * sum4) / delta;
}

// Funzione parametro b
double f_b(const vector<double>& vx, const vector<double>& vy, const vector<double>& vsy, double delta) {
    double sum1 = 0., sum2 = 0., sum3 = 0., sum4 = 0.;

    for (int i = 0; i < vx.size(); i++) {
        sum1 += 1 / (vsy[i] * vsy[i]);
        sum2 += (vx[i] * vy[i]) / (vsy[i] * vsy[i]);
        sum3 += vx[i] / (vsy[i] * vsy[i]);
        sum4 += vy[i] / (vsy[i] * vsy[i]);
    }

    return (sum1 * sum2 - sum3 * sum4) / delta;
}

// Funzione incertezza parametro a
double f_sa(const vector<double>& vx, const vector<double>& vsy, double delta) {
    double sum = 0.;

    for (int i = 0; i < vx.size(); i++) {
        sum += (vx[i] * vx[i]) / (vsy[i] * vsy[i]);
    }

    return sqrt(sum / delta);
}

// Funzione incertezza parametro b
double f_sb(const vector<double>& vx, const vector<double>& vsy, double delta) {
    double sum = 0.;

    for (int i = 0; i < vx.size(); i++) {
        sum += 1 / (vsy[i] * vsy[i]);
    }

    return sqrt(sum / delta);
}

// Funzione covarianza
double f_cov(const vector<double>& v1, const vector<double>& v2, double m1, double m2) {
    double somma = 0.;

    for (int i = 0; i < v1.size(); i++) {
        somma += (v1.at(i) - m1) * (v2.at(i) - m2);
    }

    return somma / (v1.size() - 1);
}

// Funzione covarianza parametri
double f_covpar(double x, int N, double sy, double Sx) {
    return -(x * sy * sy) / (N * Sx * Sx);
}

// Funzione indice correlazione pearson
double f_pearson(double cov, double devx, double devy) {
    return cov / (devx * devy);
}

// Funzione errore a posteriori
double f_errpost(const vector<double>& vx, const vector<double>& vy, double a, double b) {
    double sum = 0.;
    for (int i = 0; i < vx.size(); i++) {
        sum += pow(vy[i] - (a + b * vx[i]), 2);
    }
    return sqrt(sum / (vx.size() - 2));
}

// funzione chi quadro
void chi_quadro(const vector<double>& x, const vector<double>& y, double a, double b, const vector<double>& sy) {
    double sum = 0.;

    output_chi << "Test Chi Quadro_____________________________________________" << '\n';
    output_chi << setw(10) << "t (s)" << setw(10) << "v (m/s)" << setw(13) << "sv (m/s)" << setw(14) << "v* (m/s)" << setw(13) << "Chi-quadro" << '\n';

    for (int i = 0; i < x.size(); i++) {
        sum += pow((y[i] - (a + b * x[i])) / sy[i], 2);
        output_chi << setw(10) << x[i] << setw(10) << y[i] << setw(13) << sy[i] << setw(14) << a + b * x[i]
                   << setw(13) << pow((y[i] - (a + b * x[i])) / sy[i], 2) << '\n';
    }

    int NDOF = x.size() - 2;
    output_chi << '\n'
               << "Gradi di libertà = " << NDOF << '\n'
               << "Chi-quadro = " << sum << '\n';
}
