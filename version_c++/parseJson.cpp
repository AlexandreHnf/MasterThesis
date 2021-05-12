// reading a text file
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

void parse(const char string[14]) {
  string line;
  ifstream myfile ("example.txt");
  if (myfile.is_open())
  {
    while ( getline (myfile,line) )
    {
      cout << line << '\n';
    }
    myfile.close();
  }

  else cout << "Unable to open file";

}

