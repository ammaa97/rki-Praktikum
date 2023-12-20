
#include <utility> // for pair
#include <string>  // for string
#include <iostream>	
#include <fstream>	

char complement(char const x) 
{
	switch (x)
	{
		case 'A' :										// Die verschiedenen Buchstaben A,C,G,T werden jeweils ersetzt durch Komplementaerbase ersetzt
			return 'T';									
			break;
		case 'T' :
			return 'A';
			break;
		case 'C' :
			return 'G';
			break;
		case 'G' :
			return 'C';
			break;
		default:										// falls ein Zeichen nicht aus dem Alphabet {A,C,G,T} ist, wird 0 wiedergegeben
			return '0';
			}

}

std::string reverseComplement(std::string const& input)
{   
													
	std::string reverse=std::string(input.rbegin(), input.rend());     //String umdrehen
	char* c = &reverse[0];											   // String umwandeln in Char Array, damit Funktion complement(char const x) angewandt werden kann
	for (unsigned int i=0; i < reverse.length();i++)                   // Char Array durchgehen und Funktion complement anwenden
	{ 
	c[i]= complement(c[i]);
	}
	std::string s = c;													// char Array in std:: string umwandeln
	return s;                                                           // reverseComplement wird widergegeben
	
}


std::pair<std::string, std::string> readFasta(std::string const& in_file)
{
	std::ifstream f;
	f.open(in_file.c_str()); 										//öffnet Datei durch pointer auf c-string
	std::string line;
	std::string metadata;				
	std::string sequence;
	while (std::getline(f, line)){              					//speichert character in String bis Zeilenende ('\n')
        if (line[0] == '>') {										//metadata (1.Zeile) wird erkannt durch '>' und später als ersten String zum Stringpaar hinzugefügt
            metadata += line;
		}
		else 
		{															// beginnt die Zeile nicht mit '>' handelt es sich um die sequence , die den 2.String im Stringpaar darstellt
			sequence += line;
		}
	}
    std::pair<std::string, std::string> paar = {"",""};
    paar.first = metadata;
    paar.second = sequence;
    return paar;
}

bool writeFasta(std::string const& out_file, std::string const& meta,std::string const& seq){
	std:: ofstream write;
	write.open(out_file);
	if(!write) 																	// prüft, ob Datei geöffnet werden kann und gibt Fehlermeldung aus wenn nicht
    {  
     std::cerr<< "Fehler, Datei kann nicht geoeffnett werden."  << std::endl;
     return 0;
    } 
    write << meta << "\n";                                               // schreibt metadata in Datei
	int seqlaenge = seq.size();
	write << seq[0];                                                     //schreibt sequence in Datei ; nach jeden 80 zeichen wird ein Zeilenumbruch eingefügt
	for( int i =1 ; i< seqlaenge;i++){ 
		if (i % 80 == 0){
			write << "\n"<< seq[i];
		}
		else{
		write << seq[i] ;
		}
	}
	write.close();
	return 1;
}

bool reverseComplementFASTA(std::string const& input_file,std::string const& output_file) {
	std::pair<std::string, std::string> Fasta = readFasta(input_file);          // Stringpaar definieren, mit meta und seq Aufteilung durch readFasta Funktion
	std::string s = reverseComplement(Fasta.second);							//reverses Complement von seq
	bool sucess = writeFasta(output_file, Fasta.first , s);                     // gibt true , wenn reverse complement in output_file gespeichert werden kann
	return sucess;																// wenn in_file not readable or out_file not writable wird false ausgegeben
	
}
        
int main()
{
	
}
