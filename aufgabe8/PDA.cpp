//  PDA.cpp
#include <vector>
#include <tuple>
#include <stack>
#include <string>
#include "PDA.hpp"


PDA::PDA(const Language l){
    transitionfunction = {
        {'a',PDA::State::IN_PROGRESS,'$',PDA::State::IN_PROGRESS,"$uW"},
        {'c',PDA::State::IN_PROGRESS,'$',PDA::State::IN_PROGRESS,"$gW"},
        {'g',PDA::State::IN_PROGRESS,'$',PDA::State::IN_PROGRESS,"$cW"},
        {'u',PDA::State::IN_PROGRESS,'$',PDA::State::IN_PROGRESS,"$aW"},
        {'a',PDA::State::IN_PROGRESS,'W',PDA::State::IN_PROGRESS,"uT"},
        {'c',PDA::State::IN_PROGRESS,'W',PDA::State::IN_PROGRESS,"gT"},
        {'g',PDA::State::IN_PROGRESS,'W',PDA::State::IN_PROGRESS,"cT"},
        {'u',PDA:: State::IN_PROGRESS,'W',PDA::State::IN_PROGRESS,"aT"},
        {'a',PDA::State::IN_PROGRESS,'T',PDA::State::IN_PROGRESS,"uM"},
        {'c',PDA::State::IN_PROGRESS,'T',PDA::State::IN_PROGRESS,"gM"},
        {'g',PDA::State::IN_PROGRESS,'T',PDA::State::IN_PROGRESS,"cM"},
        {'u',PDA::State::IN_PROGRESS,'T',PDA::State::IN_PROGRESS,"aM"},
        {'g',PDA::State::IN_PROGRESS,'M',PDA::State::IN_PROGRESS,"aL"},
        {'a',PDA::State::IN_PROGRESS,'L',PDA:: State::IN_PROGRESS,"a"},
        {'c',PDA::State::IN_PROGRESS,'L',PDA::State::IN_PROGRESS,"a"},
    };
    
}

PDA::State PDA::  next(const char a) {
    if (called == false){
		basement.push('$');
		called = true;
		}
    int sizetransition = transitionfunction.size();
    bool transitionnotfound = true;
    int m = 0;
    bool found = false;
    if(a == basement.top()){
		found = true;
		}
    if(found==true){
        basement.pop();
        if(basement.size()==0){
			state= PDA::State::SUCCESS;
            return PDA::State :: SUCCESS;
            }
        else{
			state=PDA::State::IN_PROGRESS;
            return PDA::State::IN_PROGRESS;
            }
		}
    else {
		while (transitionnotfound && m < sizetransition){
			if (std::get<0>(transitionfunction[m]) == a && std::get<2>(transitionfunction[m]) == (basement.top()) && std::get<1>(transitionfunction[m]) == state){
				basement.pop();
				for (int i = 0; i < std::get<4>(transitionfunction[m]).size();i++){
					basement.push(std::get<4>(transitionfunction[m])[i]);
					}
				state = PDA::State::IN_PROGRESS;
				transitionnotfound = false;
				return PDA::State::IN_PROGRESS;
				}
			else {m++;}
			}
		}
	state = PDA::State::FAIL;
	return PDA::State::FAIL;

 
    
}


void  PDA :: reset(){
    while(!basement.empty()){
		basement.pop();
		}
    state = PDA::State::IN_PROGRESS;
    basement.push('$');
    
}
