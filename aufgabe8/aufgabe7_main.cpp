//
//  aufgabe7_main.cpp
//  
//
//  Created by Sarah Okafor on 11.02.21.
//
#include <string>
#include "PDA.hpp"

int main(int argc, char*argv[]){
    std :: string sequenze = argv[1];
    int m = sequenze.size();
    sequenze.push_back('S');
    PDA pda;
    PDA :: State state;
    
    for (int i = 0; i < m; i++)
    { state = pda.next(sequenze[i]);
     if (state==PDA::State::FAIL) {
         return 1;
     }
     else if (state==PDA::State :: SUCCESS) {return 1;}
    }
    
    
}

