#include <iostream>
#include <cmath>
#include <vector>
#include <sstream>
#include <fstream>
#include <string>

using namespace std;

double moli (const vector<double>&);
double smoli(const vector<double>&);
double mmoli(const vector<double>&, const vector<double>&);
double smmoli(const vector<double>&);
double errore3(const vector<double>&);

int main(){
   ofstream molitempo("moli_temp.txt");
   ofstream clearFile("../Elaborati/Errore3.txt");
   clearFile.close();
   string celestino= "3";
   string antonietta= "15";
   string beppi= "25";
   string efisio= "35";
   string luigina= "45";
   string gianfranco= "55";

   vector<double> totale;
   vector<double> stotale;

   for(int p=0; p<=5; p++){
      ifstream corretto;
      ofstream elaborato;
      ifstream compressione;
      ifstream espansione;
      if(p==0){
         corretto.open("../Raw/GR03_primo_corretto.txt");
         elaborato.open("../Elaborati/moli_primo.txt");
      }
      
      else if(p==1){
         corretto.open("../Raw/15_gradi.txt");
         elaborato.open("../Elaborati/moli_15.txt");
         compressione.open("../Raw/15_compressione.txt");
         espansione.open("../Raw/15_espansione.txt");
      }

      else if(p==2){
         corretto.open("../Raw/25_gradi.txt");
         elaborato.open("../Elaborati/moli_25.txt");
         compressione.open("../Raw/25_compressione.txt");
         espansione.open("../Raw/25_espansione.txt");
      }

      else if(p==3){
         corretto.open("../Raw/35_gradi.txt");
         elaborato.open("../Elaborati/moli_35.txt");
         compressione.open("../Raw/35_compressione.txt");
         espansione.open("../Raw/35_espansione.txt");
      }

      else if(p==4){
         corretto.open("../Raw/45_gradi.txt");
         elaborato.open("../Elaborati/moli_45.txt");
         compressione.open("../Raw/45_compressione.txt");
         espansione.open("../Raw/45_espansione.txt");
      }

      else if(p==5){
         corretto.open("../Raw/55_gradi.txt");
         elaborato.open("../Elaborati/moli_55.txt");
         compressione.open("../Raw/55_compressione.txt");
         espansione.open("../Raw/55_espansione.txt");
      }

      if (!elaborato) {
         cout<< "Errore nell'apertura del file di output!"<< endl;
         return 1;
      }

      if (!corretto) {
         cout<< "Errore nell'apertura del file corretto (input)!"<< endl;
         return 1;
      }

      if (!espansione) {
         cout<< "Errore nell'apertura del file espansione!"<< endl;
         return 1;
      }

      if (!compressione) {
         cout<< "Errore nell'apertura del file compressione!"<< endl;
         return 1;
      }
      
      vector<double> mediamoli;
      vector<double> mediasmoli;

      double i= 0;

      string line;
      while (getline(corretto, line)){
         istringstream ss(line);
         vector<double> dati;
         double num;
         i+= 0.1;
         while(ss>>num){
            dati.push_back(num);
         }
         double errpos= moli(dati) + smoli(dati);
         double errneg= moli(dati) - smoli(dati);
         elaborato<< i<< " "<< moli(dati)<< " "<< smoli(dati)<< " "<< errpos<< " "<< errneg<< endl;
         mediamoli.push_back(moli(dati));
         mediasmoli.push_back(smoli(dati));
         totale.push_back(moli(dati));
         stotale.push_back(smoli(dati));
      }
      
      if(p>=1){
         ofstream erroretre("../Elaborati/Errore3.txt", ios::app);
         vector<double> comp;
         vector<double> scomp;
         vector<double> esp;
         vector<double> sesp;
         vector<double> calcolo;

         string riga;
         while (getline(compressione, riga)){
            istringstream ss(riga);
            vector<double> dati;
            double num;
            while(ss>>num){
               dati.push_back(num);
            }
            comp.push_back(moli(dati));
            scomp.push_back(smoli(dati));
         }

         string striscia;
         while (getline(espansione, striscia)){
            istringstream ss(striscia);
            vector<double> dati;
            double num;
            while(ss>>num){
               dati.push_back(num);
            }
            esp.push_back(moli(dati));
            sesp.push_back(smoli(dati));
         }
         calcolo.push_back(mmoli(esp, sesp));
         calcolo.push_back(mmoli(comp, scomp));
         calcolo.push_back(mmoli(mediamoli, mediasmoli));
         erroretre<< errore3(calcolo)<< endl;
         erroretre.close();
      }

      switch (p){
         case 0: molitempo<< celestino; break;
         case 1: molitempo<< antonietta; break;
         case 2: molitempo<< beppi; break;
         case 3: molitempo<< efisio; break;
         case 4: molitempo<< luigina; break;
         case 5: molitempo<< gianfranco; break;
         default: break;
      }
      
      double mps= mmoli(mediamoli, mediasmoli) + smmoli(mediasmoli);
      double mms= mmoli(mediamoli, mediasmoli) - smmoli(mediasmoli);

      molitempo<< " "<< mmoli(mediamoli, mediasmoli)<< " "<< smmoli(mediasmoli)<< " "<< mps<< " "<< mms<< endl;

      corretto.close();
      elaborato.close();
      compressione.close();
      espansione.close();
   }
   cout<< endl<< mmoli(totale, stotale)<< " "<< smmoli(stotale)<< endl;
   molitempo.close();
   return 0;
}

double moli(const vector<double>& mandolino){
   double R= 8.314;
   double P= mandolino.at(0) * 98066.5;
   double V= mandolino.at(1) * (1 * pow(10, -6));
   double T= mandolino.at(2) + 273.15;
   double n= (P * V) / (R * T);

   return n;
}

double smoli(const vector<double>& pizza){
   double R= 8.314;
   double P= pizza.at(0) * 98066.5;
   double V= pizza.at(1) * (1 * pow(10, -6));
   double T= pizza.at(2) + 273.15;
   
   double sR= 0;
   double sP= 0.01 / sqrt(12);
   double sV= (1 * pow(10, -6)) / (sqrt(12));
   double sT= 0.01 / (sqrt(12));
   
   double term1= (V*sP)/(R*T);
   double term2= (P*sV)/(R*T);
   double term3= (-P*V*sR)/(R*R*T);
   double term4= (-P*V*sT)/(R*T*T);
   
   double sigma= sqrt((term1*term1) + (term2*term2) + (term3*term3) + (term4*term4));

   return sigma;
}

double mmoli(const vector<double>& carbonara, const vector<double>& amatriciana){
   double numeratore= 0;
   double denominatore1= 0;
   for(int l=0; l<carbonara.size(); l++){
      numeratore+= carbonara.at(l) / (amatriciana.at(l) * amatriciana.at(l));
      denominatore1+= 1 / (amatriciana.at(l) * amatriciana.at(l));
   }
   double mediapesata= numeratore / denominatore1;
   return mediapesata;
}

double smmoli(const vector<double>& gricia){
   double denominatore2= 0;
   for(int n=0; n<gricia.size(); n++){
      denominatore2+= 1 / (gricia.at(n) * gricia.at(n));
   }
   double smediapesata= sqrt(1 / denominatore2);
   return smediapesata;
}

double errore3(const vector<double>& risotto){
   double numeratore3= risotto.at(0) - risotto.at(1);
   double denominatore3= 2 * sqrt(3) * risotto.at(2);
   double incertezza= abs(numeratore3) / denominatore3;
   return incertezza;
}