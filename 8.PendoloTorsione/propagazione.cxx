#include <iostream>
#include <cmath>

using namespace std;

double propagazione(double A, double sA, double B, double sB, double C, double sC);

int main(){
    double A1= 1285e-03;
    double sA1= 7.6e-03;
    double B1= 60606.4e-04;
    double sB1= 9.1e-04;
    double C1= 662.7e-04;
    double sC1= 2.1e-04;

    double A2= 1145.6e-03;
    double sA2= 1e-03;
    double B2= 603836.4e-05;
    double sB2= 3.7e-05;
    double C2= 4472.3e-05;
    double sC2= 4.9e-05;

    cout<< endl<< "Incertezza giornata 1: "<< propagazione(A1, sA1, B1, sB1, C1, sC1)<< endl<< "Incertezza giornata 2: "<< propagazione(A2, sA2, B2, sB2, C2, sC2)<< endl<< endl;

return 0;
}
double propagazione (double A, double sA, double B, double sB, double C, double sC){
    double x= B;
    double sx= sB;

    double ricorrente1= (B*B) + 2*(C*C) - (x*x);
    double ricorrente2= 4*(C*C)*(x*x) + (ricorrente1*ricorrente1);

    double numeratore1= A*(-8*(C*C)*x + 4*x*ricorrente1);
    double denominatore1= 2*((ricorrente2)*(ricorrente2));
    double addendo1= pow(((numeratore1 * sx)/denominatore1), 2);

    double denominatore2= 2*(ricorrente2);
    double addendo2= pow((sA/denominatore2), 2);

    double numeratore3= -2*A*B*(ricorrente1);
    double denominatore3= (ricorrente2)*(ricorrente2);
    double addendo3= pow(((numeratore3*sB)/denominatore3), 2);

    double numeratore4= A*(-8*C*(x*x) - 8*C*ricorrente1);
    double denominatore4= denominatore1;
    double addendo4= pow(((numeratore4*sC)/denominatore4), 2);

    double incertezza= sqrt(addendo1 + addendo2 + addendo3 + addendo4);

return incertezza;
}