#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
using namespace std;

string nome;
ifstream input("muoni.txt");
ofstream output(nome);

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

    //raccolta dati input 
    float a,v1,v2,v3,v4;
    while(input>>a>>v1>>v2>>v3>>v4) {
        float media=(v1+v2+v3+v4)/4;
        output << a << " " << media << " " << sqrt(media) << endl; //dev standard approssimata
       
    }

    return 0;
}