// do NOT change this file!

#include <utility> // for pair
#include <string>  // for string

/// compute the complement for input @p x from alphabet {ACGT}
char complement(char const x);

/// reverse a DNA string and complement all bases
std::string reverseComplement(std::string const& input);

/// read a FASTA entry from a file, returning a pair containing meta data and sequence (without linebreaks or whitespace)
/// Returns a pair with empty strings if @p in_file is not readable 
std::pair<std::string, std::string> readFasta(std::string const& in_file);

/// write a FASTA entry to file
/// Upon writing, sequence is split such that each line is 80 characters long (the last line can be shorter of course)
/// Return true on success, false otherwise (e.g. @p out_file not writable)
bool writeFasta(std::string const& out_file,
                std::string const& meta,
                std::string const& seq);

/// read a FASTA file with a single sequence, and store the sequence's reverse complement in @p output_file
/// Uses @p readFasta() and @p writeFasta() internally.
/// Returns true on success, false otherwise (in_file not readable, or out_file not writable)
bool reverseComplementFASTA(std::string const& input_file,
                            std::string const& output_file);
