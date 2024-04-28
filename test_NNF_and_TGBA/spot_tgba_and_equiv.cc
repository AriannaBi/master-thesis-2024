#include <iostream>
#include <spot/tl/parse.hh>
#include <spot/twaalgos/translate.hh>
#include <spot/twaalgos/hoa.hh>
#include <spot/twaalgos/dot.hh>
#include <spot/twaalgos/stats.hh>
#include <iostream>
#include <spot/tl/parse.hh>
#include <spot/tl/print.hh>
#include <spot/tl/simplify.hh>
#include <spot/tl/formula.hh>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <spot/tl/unabbrev.hh>
#include <bitset>
#include <set>


// write a program that from a ltl formula it generates a tgba automaton and then check if two automata are equivalent
// g++ -std=c++17 spot_tgba_and_equiv.cc -lspot -o spot_tgba_and_equiv


// Helper function to parse the BODY section of the HOA string and return it
// example
// --BODY--
// State: 0
// [0 & 1] 2
// [0 & !1] 1
// --END--
// Return : ["State: 0", "[0 & 1] 2", "[0 & !1] 1"]
std::vector<std::string> parseBody(const std::string& hoa) {
    std::istringstream iss(hoa);
    std::string line;
    std::vector<std::string> bodyLines;
    bool inBody = false;
    while (std::getline(iss, line)) {
        if (inBody) {
            if (line == "--END--") {
                break;
            }
            bodyLines.push_back(line);
        } else if (line == "--BODY--") {
            inBody = true;
        }
    }
    return bodyLines;
}

// helper function to split the line by a delimiter into a vector of strings (all the mutation formulas)
std::vector<std::string> split(std::string s, std::string delimiter) {
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    std::string token;
    std::vector<std::string> res;

    while ((pos_end = s.find(delimiter, pos_start)) != std::string::npos) {
        token = s.substr (pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back (token);
    }

    res.push_back (s.substr (pos_start));
    return res;
}



spot::twa_graph_ptr ltl_2_tgba(std::string readFile) {
  // Open file
    std::ifstream file(readFile);
    if (!file.is_open()) { // Check if the file is open
        std::cerr << "Error: Unable to open file." << std::endl;
        throw std::runtime_error("Error parsing formula");
    }

    // Read the file line by line
    std::string line;


    std::set<std::string> setFormulas;
    std::set<std::string> setUNSAT;
    int countUNSAT = 0;
    bool hasDifferentAutomata = false;
    std::string delimiter = " . ";

    // set the translator
    spot::translator trans;
    trans.set_type(spot::postprocessor::TGBA);
    trans.set_pref(spot::postprocessor::Deterministic);
    trans.set_level(spot::postprocessor::High);


  // Reading line
    while (std::getline(file, line)) {
    // for (int i = 0; std::getline(file, line) && i < 1; ++i) {
      std::string original_string = "";
      std::stringstream original_stream;

      // Process each line
      std::vector<std::string> strings;
      std::string delimiter = "/";
      strings = split (line, delimiter);
      strings.erase(std::remove_if(strings.begin(), strings.end(), [](const std::string& str) { return str.empty(); }),strings.end());
      
      std::string original_formula = strings[0];
      spot::formula original_pf = spot::parse_formula(original_formula);



      // create the TGBA
      spot::twa_graph_ptr original_automata = trans.run(original_pf);
      print_hoa(original_stream, original_automata);
      original_string = original_stream.str();
      std::vector<std::string> original_body = parseBody(original_string);



      for (const std::string& str : strings) {
        if (!str.empty()) {
          // std::cout << str << std::endl;
          std::string mutation_string = "";
          std::stringstream mutatio_stream;
          spot::formula mutation_formula = spot::parse_formula(str);


          // create the TGBA
          spot::twa_graph_ptr mutation_aut = trans.run(mutation_formula);
          print_hoa(mutatio_stream, mutation_aut);
          mutation_string = mutatio_stream.str();
          std::vector<std::string> mutation_body = parseBody(mutation_string);


          if (original_body == mutation_body) {
          } else {
            // hasDifferentAutomata = true;
            std::string union_original_mutant = original_formula + delimiter + str;
            setFormulas.insert(union_original_mutant);
            std::cout << "The two automata are not equivalent " << '\n' << original_string << '\n' << mutation_string << std::endl;
            std::cout << "Original formula: [" << original_formula << "] mutant formula [" << mutation_formula <<"]" <<  std::endl;
            std::cout << '\n' << std::endl;
          }

          // put all the UNSAT into a set and keep count of how many unsat are there
          // if ((original_body.size() == 1) & (original_body[0].compare("State: 0") == 0)) {
          //   setUNSAT.insert(original_formula);
          //   countUNSAT++;
          // }
          // if ((mutation_body.size() == 1) & (mutation_body[0].compare("State: 0") == 0)) {
          //   setUNSAT.insert(str);
          //   countUNSAT++;
          // }
        }

      }
    }

    // print the set of UNSAT formulas
    // for (const std::string& str : setUNSAT) {
    //   std::cout << "The LTL formula [" << str << "] is UNSAT" << std::endl;
    // }
    // std::cout << "The number of UNSAT formulas is " << countUNSAT << std::endl;

    return nullptr;
}
int main()
{
  spot::twa_graph_ptr a1 = ltl_2_tgba("output/filtered_spot_all_options.txt");

  
  return 0;
}