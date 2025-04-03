#include <string>
#include <cctype>
#include <vector>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

using namespace std;

bool f_spazio (string);

double f_media(const vector<double>&);
double f_dev(const vector<double>&, double);

//minimi quadrati 1
double f_delta1(const vector<double>&);
double f_a1(const vector<double>&, const vector<double>&, double);
double f_b1(const vector<double>&, const vector<double>&, double);
double f_sa1(const vector<double>&, double, double);
double f_sb1(const vector<double>&, double, double);

//minimi quadrati 2
double f_delta2(const vector<double>&, const vector<double>&);
double f_a2(const vector<double>&, const vector<double>&, const vector<double>&, double);
double f_b2(const vector<double>&, const vector<double>&, const vector<double>&, double);
double f_sa2(const vector<double>&, const vector<double>&, double);
double f_sb2(const vector<double>&, const vector<double>&, double);

double f_errpost(const vector<double>&, const vector<double>&, double, double);
double f_chi_quadro(const vector<double>&, const vector<double>&, double, double, const vector<double>&);

void elaborato(const vector<double>&, const vector<double>&, const vector<double>&, double, double, double, double);

ifstream input("dati.txt");
ofstream output("plot.txt");
ofstream output_elab("elaborato.txt");
ofstream output_stokes("stokes.txt");
ofstream output_eta_intervalli("eta_intervalli.txt");
ofstream output_eta_tempi("eta_tempi.txt");
string test;
int serie = 0, indice = 0;

double x0, t1, t2, t3, t4;
double delta, a, b, sa, sb;
double d, sd, v, sv, eta, seta; //diametro (m), velocita (m/s), viscosità (N * (s/m^2))
vector <double> v_eta, v_seta; //stokes.txt
vector <double> v_eta_intervalli, v_seta_intervalli; //eta_intervalli.txt
vector<double> x, t, t_medi, st_medi;
vector <double> tempi1, tempi2, tempi3, tempi4;  //eta_tempi.txt
double delta_tempi, v_tempi, sv_tempi, eta_tempi, seta_tempi;
vector <vector <double>> container_tempi;

int main() {

    const char daghene = 'g';

    double rho_0, srho_0;

    if (daghene == 'g') {
        cout << "Glicerolo" << '\n';
        rho_0 = 1260.; //densità fluido
        srho_0 = 10.;
    } 

    if (daghene == 's') {
        cout << "Sapone" << '\n';
        rho_0 = 1032.; //densità fluido
        srho_0 = 1.;
    } 

    const double sd = 1e-5;
    const double rho = 7870.; //densità sferette in kg/m^3
    const double srho = 1.;
    const double srho_TOT = sqrt( srho*srho + srho_0*srho_0);
    const double g = 9.8065855;
    const double sg = 0.001;

    const double sx = (0.5e-3)/sqrt(24); //errore distribuzione triangolare con risoluzione 5mm
    const double st = (0.001)/sqrt(12); //errore distribuzione uniforme con risoluzione 0.001s

    output  << left << setw(7) << "x (m)" << left << setw(15) << "sx" << left << setw(15) << "sx/x" 
    << left << setw(15) << "t (s)" << left << setw(15) << "st" << left << setw(15) << "st/t" << '\n' << '\n';
    
    output_stokes << left << setw(15) << "d" << left << setw(15) << "sd" << left << setw(15) << "v" << left << setw(15) << "sv" << left << setw(15) << "eta" << left << setw(15) << "s eta" << left << setw(15) << "d^2" << left << setw(15) << "s d^2" <<'\n' << '\n';

    output_eta_intervalli << left << setw(15) << "d" << left << setw(15) << "sd" << left << setw(15) << "t" << left << setw(15) << "st" << left << setw(15) << "v" << left << setw(15) << "sv" << left << setw(15) << "eta" << left << setw(15) << "s eta" << left << setw(15) << "x" << left << setw(15) << "sx" << '\n' << '\n';

    output_eta_tempi << left << setw(15) << "d" << left << setw(15) << "sd" << left << setw(15) << "indice" << left << setw(15) << "v" << left << setw(15) << "sv" << left << setw(15) << "eta" << left << setw(15) << "s eta" << '\n' << '\n';

    if (!input) {
        cerr << "Errore nell'apertura del file!" << endl;
        return 1;
    }
    if (!output) {
        cerr << "Errore nell'apertura del file!" << endl;
        return 1;
    }
    if (!output_elab) {
        cerr << "Errore nell'apertura del file!" << endl;
        return 1;
    }
    if (!output_eta_intervalli) {
        cerr << "Errore nell'apertura del file!" << endl;
        return 1;
    }
    if (!output_eta_tempi) {
        cerr << "Errore nell'apertura del file!" << endl;
        return 1;
    }

    while (getline(input, test)) {

        istringstream input_string(test);
        while (input_string >> x0 >> t1 >> t2 >> t3 >> t4) {
           
            x.push_back(x0);
            t = {t1, t2, t3, t4};

            tempi1.push_back(t1);
            tempi2.push_back(t2);
            tempi3.push_back(t3);
            tempi4.push_back(t4);
            container_tempi = {tempi1, tempi2, tempi3, tempi4};
            
            double t_medio = f_media(t);
            double t_dev = f_dev(t, t_medio);
            double t_dev_media = t_dev/sqrt(t.size());
            double err_rel_x = sx/x0;
            double err_rel_t = t_dev_media/t_medio;

            //plot.txt
            output  << left << setw(7) << x0 << left << setw(15) << sx << left << setw(15) << err_rel_x 
                    << left << setw(15) << t_medio << left << setw(15) << t_dev_media << left << setw(15) << err_rel_t << '\n';
            
            t_medi.push_back(t_medio);
            st_medi.push_back(t_dev_media);
        }

        if (f_spazio(test)) {
            
            //interpolazione, minimi quadrati 2
            double delta = f_delta2(x, st_medi);
            double a = f_a2(x, t_medi, st_medi, delta);
            double b = f_b2(x, t_medi, st_medi, delta);
            double sa = f_sa2(x, st_medi, delta);
            double sb = f_sb2(x, st_medi, delta);

            //diametri in base alla serie
            if (serie == 0) {
                d = 0.00150;
                output_elab << "SERIE 1" << '\n' << "0.150cm" << '\n';
            }
            if (serie == 1) {
                d = 0.00200;
                output_elab << "SERIE 2" << '\n' << "0.200cm" << '\n';
            }
            if (serie == 2) {
                d = 0.00318;
                output_elab << "SERIE 3" << '\n' << "0.318cm" << '\n';
            }
            if (serie == 3) {
                d = 0.00476;
                output_elab << "SERIE 4" << '\n' << "0.476cm" << '\n';
            }
            if (serie == 4) {
                d = 0.00635;
                output_elab << "SERIE 5" << '\n' << "0.635cm" << '\n';
            }

            //stokes.txt 
            v = 1/b;
            sv = sb/(b*b); //propagazione incertezze per v
            eta = d*d * (rho - rho_0)/(18 * v) * g;
            seta = sqrt( pow(2*(sd/d), 2) + pow(srho_TOT/(rho-rho_0), 2) + pow(sv/v, 2) + pow(sg/g, 2) ); //propagazione incertezze per eta
            v_eta.push_back(eta);
            v_seta.push_back(seta);

            output_stokes << left << setw(15) << d << left << setw(15) << sd << left << setw(15) << v << left << setw(15) << sv << left << setw(15) << eta << left << setw(15) << seta << left << setw(15) << d*d << left << setw(15) << 2*d*sd << '\n';

            //eta_intervalli.txt
            for (int i = 0; i < t_medi.size(); i++) {
                double delta_t = t_medi[i] - t_medi[i-1];
                double sdelta_t = sqrt( pow(st_medi[i], 2) + pow(st_medi[i], 2) );
                double v_intervalli = (x[1]-x[0]) / delta_t;
                double sv_intervalli = v_intervalli * sqrt( pow( sx / (x[1]-x[0]),2) + pow( sdelta_t / delta_t, 2) );
                double eta_intervalli = d*d * (rho - rho_0)/(18 * v_intervalli) * g;
                double seta_intervalli = sqrt( pow(2*(sd/d), 2) + pow(srho_TOT/(rho-rho_0), 2) + pow(sv_intervalli/v_intervalli, 2) + pow(sg/g, 2) );

                v_eta_intervalli.push_back(eta_intervalli);
                v_seta_intervalli.push_back(seta_intervalli);

                output_eta_intervalli << left << setw(15) << d << left << setw(15) << sd << left << setw(15) << delta_t << left << setw(15) << sdelta_t << left << setw(15) << v_intervalli << left << setw(15) << sv_intervalli << left << setw(15) << eta_intervalli << left << setw(15) << seta_intervalli << left << setw(15) << x[i]/2 << left << setw(15) << sx << '\n';
            }
            output_eta_intervalli << '\n' << '\n';

            //elaborato.txt
            elaborato(x, t_medi, st_medi, a, b, sa, sb);
            output_elab << '\n' << '\n';

            output << '\n' << '\n';

            //eta_tempi.txt
            for(int i = 0; i < container_tempi.size(); i++) {

                //minimi quadrati 1
                delta_tempi = f_delta1 (container_tempi[i]);

                if (delta_tempi <= 0) {
                    cerr << "Delta non positivo" << '\n';
                    return 1;
                }

                v_tempi = f_b1 (container_tempi[i], x, delta_tempi);
                sv_tempi = f_sb1 (container_tempi[i], sx, delta_tempi);

                eta_tempi = d*d * (rho - rho_0)/(18 * v_tempi) * g;
                seta_tempi = sqrt( pow(2*(sd/d), 2) + pow(srho_TOT/(rho-rho_0), 2) + pow(sv_tempi/v_tempi, 2) + pow(sg/g, 2) );

                output_eta_tempi << left << setw(15) << d << left << setw(15) << sd << left << setw(15) << indice << left << setw(15) << v_tempi << left << setw(15) << sv_tempi << left << setw(15) << eta_tempi << left << setw(15) << seta_tempi << '\n';
                indice ++;
            }

            output_eta_tempi << '\n' << '\n';

            //reset vettori
            x.clear();
            t.clear();
            t_medi.clear();
            st_medi.clear();
            container_tempi.clear();
            tempi1.clear();
            tempi2.clear();
            tempi3.clear();
            tempi4.clear();
            serie ++;
            continue;
        }
    }

    //stokes.txt
    double media_eta = f_media(v_eta);
    double dev_eta = f_dev(v_eta, media_eta);
    output_stokes   << '\n' << "Miglior stima di eta = " << media_eta << " +/- " << dev_eta/sqrt(v_eta.size()) << '\n'
                    << "Deviazione standard campionaria = " << dev_eta;

    //eta_intervalli.txt
    double media_eta_intervalli = f_media(v_eta_intervalli);
    double dev_eta_intervalli = f_dev(v_eta_intervalli, media_eta_intervalli);
    output_eta_intervalli   << '\n' << "Miglior stima di eta = " << media_eta_intervalli << " +/- " << dev_eta_intervalli/sqrt(v_eta_intervalli.size()) << '\n'
                            << "Deviazione standard campionaria = " << dev_eta_intervalli;
    return 0;
}

// Test per spaziare nel file output
bool f_spazio (string s) {
    istringstream verifica(s); //legge la stringa
    char c;
    while (verifica >> c) { //legge ogni singolo carattere della stringa
        if (!isspace(c)) //se non sono tutti vuoti (spazi, tablature etc) ritorna un valore false
        return 0;
    }
    return 1;
}

// Funzione media
double f_media(const vector<double>& v) {
    double somma = 0.;
    for (auto &c : v) {
        somma += c;
    }
    return somma / v.size();
}

// Funzione deviazione standard
double f_dev(const vector<double>& v, double m) {
    double somma = 0.;
    for (auto& c : v) {
        somma += pow(c - m, 2);
    }
    return sqrt(somma / (v.size() - 1));
}


// Funzione delta
double f_delta1(const vector<double>& vx) {
    double sum1 = 0., sum2 = 0.;
    for (auto & x : vx) {
        sum1 += x * x;
        sum2 += x;
    }
    return vx.size() * sum1 - sum2 * sum2;
}

// Funzione parametro a
double f_a1(const vector<double>& vx, const vector<double>& vy, double delta) {
    double sum1 = 0., sum2 = 0., sum3 = 0., sum4 = 0.;
    for (int i = 0; i < vx.size(); i++) {
        sum1 += vx[i] * vx[i];
        sum2 += vy[i];
        sum3 += vx[i];
        sum4 += vx[i] * vy[i];
    }
    return (sum1 * sum2 - sum3 * sum4) / delta;
}

// Funzione parametro b
double f_b1(const vector<double>& vx, const vector<double>& vy, double delta) {
    double sum1 = 0., sum2 = 0., sum3 = 0.;
    for (int i = 0; i < vx.size(); i++) {
        sum1 += vx[i] * vy[i];
        sum2 += vx[i];
        sum3 += vy[i];
    }
    return (vx.size() * sum1 - sum2 * sum3) / delta;
}

// Funzione incertezza parametro a
double f_sa1(const vector<double>& vx, double sy, double delta) {
    double sum = 0.;
    for (auto & x : vx) {
        sum += x * x;
    }
    return (sqrt(sum / delta)) * sy;
}

// Funzione incertezza parametro b
double f_sb1(const vector<double>& vx, double sy, double delta) {
    return (sqrt(v.size() / delta)) * sy;
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

// Funzione errore a posteriori
double f_errpost(const vector<double>& vx, const vector<double>& vy, double a, double b) {
    double sum = 0.;
    for (int i = 0; i < vx.size(); i++) {
        sum += pow(vy[i] - (a + b * vx[i]), 2);
    }
    return sqrt(sum / (vx.size() - 2));
}

// Funzione chi quadro
double f_chi_quadro(const vector<double>& vx, const vector<double>& vy, double a, double b, const vector<double>& vsy) {
    double sum = 0.;
    for (int i = 0; i < vx.size(); i++) {
        double y = vy[i];
        double y_star = a + b * vx[i];
        double sy = vsy[i];
        double chi_quadro_i = pow((y - y_star) / sy, 2);
        sum += chi_quadro_i;
    }
    return sum;
}

// Elaborato
void elaborato(const vector<double>& vx, const vector<double>& vy, const vector<double>& vsy, double a, double b, double sa, double sb) {

    //parametri
    output_elab << "Parametri___________________________________________________" << '\n'
                << "y = a + bx" << '\n'
                << "a = " << a << " +/- " << sa << '\n'
                << "b = " << b << " +/- " << sb << '\n' << '\n';
    //chi quadro
    output_elab << "Test Chi Quadro_____________________________________________" << '\n'
                << setw(10) << "x" << setw(10) << "y" << setw(13) << "sy" << setw(14) << "y*" << setw(13) << "Chi-quadro" << '\n';

    double sum1 = 0.;
    for (int i = 0; i < vx.size(); i++) {
        double y = vy[i];
        double y_star = a + b * vx[i];
        double sy = vsy[i];
        double chi_quadro_i = pow((y - y_star) / sy, 2);
        sum1 += chi_quadro_i;
        output_elab << setw(10) << vx[i] << setw(10) << y << setw(13) << sy << setw(14) << y_star
                   << setw(13) << chi_quadro_i << '\n';
    }
    double chi_quadro = sum1;

    int NDOF = vx.size() - 2;
    output_elab << '\n'
                << "Gradi di libertà = " << NDOF << '\n'
                << "Chi-quadro = " << chi_quadro << '\n'
                << "Chi-quadro ridotto = " << chi_quadro/NDOF << '\n';
    if (chi_quadro > NDOF) {
        output_elab << "Incertezze Sottostimate" << '\n' << '\n';
    }
    if (chi_quadro < NDOF) {
        output_elab << "Incertezze Sovrastimate" << '\n' << '\n';
    }



    //errore a posteriori
    output_elab << "Test Errore a Posteriori____________________________________" << '\n';

    double sum2 = 0.;
    for (int i = 0; i < vx.size(); i++) {
        sum2 += pow(vy[i] - (a + b * vx[i]), 2);
    }
    double err = sqrt(sum2 / (vx.size() - 2));

    output_elab << setw(20) << "Deviazione Residua" << setw(30) << "Incertezza Ordinate" << '\n';
    int magg = 0, min = 0;
    for (auto & c: vsy) {
        output_elab << setw(20) << err << setw(10);
        if(err > c) {
            output_elab << ">";
            magg++;
        }
        if(err < c) {
            output_elab << "<";
            min++;
        }
        output_elab << setw(20) << c << '\n';
    }
    output_elab << '\n' << "Deviazioni Residue maggiori delle Incertezze: " << magg << '\n'
                << "Deviazioni Redisue minori delle Incertezze: " << min << '\n';
}
