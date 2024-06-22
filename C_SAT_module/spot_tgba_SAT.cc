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
#include <spot/twaalgos/contains.hh>
#include <spot/twaalgos/emptiness.hh>
#include <spot/twaalgos/gtec/gtec.hh>


// write a program that from a ltl formula it generates a tgba automaton and then check if two automata are equivalent
// g++ -std=c++17 spot_tgba_SAT.cc -lspot -o spot_tgba_SAT

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



spot::twa_graph_ptr ltl_2_tgba(std::string readFile, std::string delimiter) {
  // Open file
    std::ifstream file(readFile);
    if (!file.is_open()) { // Check if the file is open
        std::cerr << "Error: Unable to open file." << std::endl;
        throw std::runtime_error("Error parsing formula");
    }

    // Read the file line by line
    std::string line;
    bool has_different_SAT = false;

    std::set<std::string> setFormulas;
    std::set<std::string> setUNSAT;
    int countUNSAT = 0;
    bool hasDifferentAutomata = false;
    // std::string delimiter = " . ";

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
      // std::string delimiter = "/";
      strings = split (line, delimiter);
      strings.erase(std::remove_if(strings.begin(), strings.end(), [](const std::string& str) { return str.empty(); }),strings.end());
      
      std::string original_formula = strings[0];
      spot::formula original_pf = spot::parse_formula(original_formula);



      // create the TGBA
      spot::twa_graph_ptr original_automata = trans.run(original_pf);
      print_hoa(original_stream, original_automata);
      original_string = original_stream.str();
      // std::vector<std::string> original_body = parseBody(original_string);


      // create the emptiness checker
      spot::option_map options; //empty options
      spot::emptiness_check_ptr original_emptiness_checker = spot::couvreur99(original_automata, options);

      /// Perform the emptiness check
      spot::emptiness_check_result_ptr original_SAT = original_emptiness_checker->check();

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
          // std::vector<std::string> mutation_body = parseBody(mutation_string);


          // put all the UNSAT into a set and keep count of how many unsat are there
          // if ((original_body.size() == 1) & (original_body[0].compare("State: 0") == 0)) {
          //   setUNSAT.insert(original_formula);
          //   countUNSAT++;
          // }
          // if ((mutation_body.size() == 1) & (mutation_body[0].compare("State: 0") == 0)) {
          //   setUNSAT.insert(str);
          //   countUNSAT++;
          // }
          // test if two automatas are equivalent using emptiness checking.
          // if (check_emptiness_two_automaton(original_pf, mutation_formula) == 1) {
          //   std::cout << "The two automata are not equivalent " << '\n' << original_string << '\n' << mutation_string << std::endl;
          //   std::cout << "Original formula: [" << original_formula << "] mutant formula [" << str <<"]" <<  std::endl;
          //   std::cout << '\n' << std::endl;
          // }

          // create the emptiness checker
          spot::emptiness_check_ptr mutation_emptiness_checker = spot::couvreur99(mutation_aut, options);

          /// Perform the emptiness check
          spot::emptiness_check_result_ptr mutation_SAT = mutation_emptiness_checker->check();

          // std::cout << original_pf << mutation_formula << original_SAT << mutation_SAT << std::endl;
          
          if (!original_SAT && mutation_SAT) {
            has_different_SAT = true;
            std::cout << "The formula [" << original_pf << "] is UNSAT and [" << mutation_formula << "] is SAT" << std::endl;
          } else if (original_SAT && !mutation_SAT) {
            has_different_SAT = true;
            std::cout << "The formula [" << original_pf << "] is SAT and [" << mutation_formula << "] is UNSAT" << std::endl;
          }

          
          // Check if the automaton is empty
          // if (!result) {
          //     // std::cout << "Automaton is empty." << std::endl;
          //     return 0;
          // } else {
          //     // std::cout << "Automaton is not empty." << std::endl;
          //     // Optionally, retrieve an accepting run and print it
          //     spot::twa_run_ptr accepting_run = result->accepting_run();
          //     if (accepting_run) {
          //         std::cout << "Accepting run: " << *accepting_run << std::endl;
          //     }
          //     return 1;
          // }
                }

      }
    }
    if (!has_different_SAT) {
      std::cout << "All the formulas/automatas maintain the relation of SAT and UNSAT!" << std::endl;
    }

    return 0;
}
int main()
{
  spot::twa_graph_ptr a1 = ltl_2_tgba("../generate/output/filtered_mutants_LTL.txt", " ");

  
  return 0;
}