#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>
#include <iomanip>

using namespace std;

double f_media(const vector<double>&);
double f_dev(const vector<double>&, double);

int main() {
    ifstream input("statici.txt");
    if (!input) {
        cerr << "Errore apertura file input" << endl;
        return 1;
    }
    
    vector<double> t;
    const double x = (70 - 40) * 1e-2; // Conversione cm -> m
    
    double ez;
    while (input >> ez) {
        t.push_back(ez);
    }
    
    if (t.empty()) {
        cerr << "Errore: file vuoto o dati non validi." << endl;
        return 1;
    }
    
    double media_t = f_media(t);
    if (media_t == 0) {
        cerr << "Errore: media del tempo nulla, divisione per zero." << endl;
        return 1;
    }
    
    double v = x / media_t;
    double a = 0.5 * (v * v) / (x / 2 + 0.20);
    
    cout << fixed << setprecision(6);
    cout << "a = " << a << " m/s^2" << endl;
    cout << "g = " << a / 0.005454 << " m/s^2" << endl;
    
    return 0;
}

// Funzione media
double f_media(const vector<double>& v) {
    double somma = 0.0;
    for (auto& c : v) {
        somma += c;
    }
    return somma / v.size();
}

// Funzione deviazione standard
double f_dev(const vector<double>& v, double m) {
    double somma = 0.0;
    for (auto& c : v) {
        somma += pow(c - m, 2);
    }
    return sqrt(somma / (v.size() - 1));
}
