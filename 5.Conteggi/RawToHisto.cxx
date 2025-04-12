#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>

//to compile: g++ -Wall RawToHisto.cxx -o RawToHisto

using namespace std;

int GetPowerOfTen(unsigned int i){
	if(i==0) return 0;
	else return (int)log10(i);
}

int main(int argc, char* argv[]){

	//Variables containing general information are declared here
    string inputFileName;
    string outputFileName = "output.txt";
    int rebinFactor = 1;

    if(argc < 2){
        cout << "Error: not enough parameters!" << endl;
        cout << "For help type " << endl;
        cout << "./RawToHisto -h " << endl;
        return -1;
    }

	//User interface
    for(int i=1; i<argc; i++){
        string option = string(argv[i]);

		if( option == "-h" || option == "--help" ){
			cout << "Usage:\n";
			cout << "./RawToHisto [options, ...] \n";
			cout << "\t-in\tfilename\t\t\tSpecify input file name\n";
			cout << "\t-out\tfilename\t\t\tSpecify output file name (default is output.txt)\n";
			cout << "\t-rebin\t[#]\t\t\tSpecify rebin factor (default is 1)\n";
			cout << endl;
			return 0;
		}

		if ( option == "-in"){
			inputFileName = string(argv[++i]);
		    continue;
		}

		if ( option == "-out"){
			outputFileName = string(argv[++i]);
		    continue;
		}

		if ( option == "-rebin"){
			rebinFactor = stoi(argv[++i]);
		    continue;
		}

        cout << "Option " << option << " not implemented" << endl;
        return -1;
	}

	cout << "Converting raw data to histogram format with the following parameters:\n";
	cout << "Input file name: " << inputFileName << "\n";
	cout << "Output file name: " << outputFileName << "\n";
	cout << "Rebin factor: " << rebinFactor << "\n";
	cout << endl;

	//Here we open the input file
	ifstream fin (inputFileName.c_str());
	if(!fin.is_open()){
		cout << "Error: cannot open input file " << inputFileName << endl;
		return -1;
	} else cout << "Input file opened" << endl;

	//Here we open the output file
	ofstream fout (outputFileName.c_str());
	if(!fout.is_open()){
		cout << "Error: cannot open output file " << inputFileName << endl;
		return -1;
	} else cout << "Output file created" << endl;

	//first we load all the input data in a vector
	string temp;
	vector<int>data;
	while(getline(fin,temp,',')){
		if (temp == "Bins") continue;
		else if (temp == "Counts0")  data.push_back(stoi("0"));
		else data.push_back(stoi(temp));
	}
	cout << "Data loaded in memory" << endl;
	cout << "Size of vector is " << data.size() << endl;

	int powerOfTen;

	int binAdded = 0;
	double binCenter = 0;
	double binContent = 0;

//	for (auto i: data) fout << i<< endl; 

	for(unsigned int i=0; i<(data.size()-1); i++){

		powerOfTen = GetPowerOfTen(i);
		switch(powerOfTen){
			case 0: binCenter+=data.at(i) % 10 + 0.5; break;
			case 1: binCenter+=data.at(i) % 100 + 0.5; break;
			case 2: binCenter+=data.at(i) % 1000 + 0.5; break;
			case 3: binCenter+=data.at(i) % 10000 + 0.5; break;
			default: cout << "Error: powerOfTen is " << powerOfTen << endl; break;
		}
		
		//fout << __LINE__ <<endl;
		
		powerOfTen = GetPowerOfTen(i+1);
		switch(powerOfTen){
			case 0: binContent+=data.at(i+1) / 10; break;
			case 1: binContent+=data.at(i+1) / 100; break;
			case 2: binContent+=data.at(i+1) / 1000; break;
			case 3: binContent+=data.at(i+1) / 10000; break;
			default: cout << "Error: powerOfTen is " << powerOfTen << endl; break;
		}
		//fout << __LINE__ <<endl;
	
		binAdded++;
		
		//fout << binAdded << endl ;

		if(binAdded == rebinFactor){
			//we calculate the average as the binCenter
			
		//	fout << binCenter << "\t" << binContent << "\n";	
			
			binCenter = binCenter / (pow(binAdded,2));

			fout << binCenter << "\t" << binContent << "\n";

			binAdded = 0;
			binCenter = 0;
			binContent = 0;
		}
	}

	//check if we wrote the last bin
/*	if(binAdded != 0){
		//we calculate the average as the binCenter
		binCenter = binCenter / binAdded;

		fout << binCenter << "\t" << binContent << "\n";
	}*/

	cout << "\nRaw data successfully converted to histogram format" << endl;

    return 0;
}
