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
#include <spot/twaalgos/are_isomorphic.hh>
#include <spot/twaalgos/contains.hh>

// SPOT IMPLEMENTATION: first configuration in the thesis.

// USED TO COMPARE TWO AUTOMATAS GENERATED FROM TWO DIFFERENT FORMULAS AND WITH SPOT TRANSALTOR
// Test equivalences and isomorphism of two automata.
// Write a program that from a ltl formula it generates a tgba automaton. So it does that with a formula and a mutant and
// then check if the two automata are equivalent.


// Formulas are original and mutant, and the translator is the spot translator same for both formulas. 
// This means that we test whether the translator produced equivalent automatas when input two different but equivalent formulas.


// g++ -std=c++17 test_check_equiv_isomorph.cc -lspot -o test_check_equiv_isomorph


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

    bool exist_not_equivalent = false;
    bool exist_not_isomorphic = false;
    // Read the file line by line
    std::string line;
    int num_isomorphic = 0;
    int num_equal = 0;

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
      // std::string delimiter = "   ";
      strings = split (line, delimiter);
      strings.erase(std::remove_if(strings.begin(), strings.end(), [](const std::string& str) { return str.empty(); }),strings.end());
      
      std::string original_formula = strings[0];
      spot::formula original_pf = spot::parse_formula(original_formula);
      


      // create the TGBA
      spot::twa_graph_ptr original_automata = trans.run(original_pf);
      print_hoa(original_stream, original_automata); // print the automata to the stream
      original_string = original_stream.str();
      



      for (const std::string& str : strings) {
        if (!str.empty()) {
          // std::cout << str << std::endl;
          std::string mutation_string = "";
          std::stringstream mutatio_stream;
          spot::formula mutation_formula = spot::parse_formula(str);
          // std::cout << original_pf << " and " << str << std::endl;

          // create the TGBA
          spot::twa_graph_ptr mutation_automata = trans.run(mutation_formula);
          print_hoa(mutatio_stream, mutation_automata);
          mutation_string = mutatio_stream.str();
          
          // Test if the two automatas are structurally equal
          if (original_string != mutation_string) {
            std::cout << original_string << mutation_string<< std::endl;
            hasDifferentAutomata = true;
          }
          // print_hoa(std::cout, original_automata);
          // print_hoa(std::cout, mutation_automata);

          // Test if two automatas are isomorphic with the spot function spot::are_isomorphic
          if (!spot::isomorphism_checker::are_isomorphic(original_automata,mutation_automata)){
            std::cout << "The two automata are not isomorphic " << '\n' << original_string << '\n' << mutation_string << std::endl;
            std::cout << "Original formula: [" << original_formula << "] mutant formula [" << str <<"]" <<  std::endl;
            std::cout << '\n' << std::endl;
            exist_not_isomorphic = true;
          } else {
            num_isomorphic++;
          }
          
          // Test if two automatas are equivalent with the spot function spot::are_equivalent
          if (!spot::are_equivalent(original_automata,mutation_automata)){
            std::cout << "The two automata are not equivalent " << '\n' << original_string << '\n' << mutation_string << std::endl;
            std::cout << "Original formula: [" << original_formula << "] mutant formula [" << str <<"]" <<  std::endl;
            std::cout << '\n' << std::endl;
            exist_not_equivalent = true;
          } else {
            num_equal++;
          }

        }

      }
    }
    if (!hasDifferentAutomata) {
      std::cout << "All automata are equal" << std::endl;
    }
    if (!exist_not_equivalent) {
      std::cout << "All automata are equivalent" << std::endl;
    }
    if (!exist_not_isomorphic) {
      std::cout << "All automata are isomorphic" << std::endl;
    }
    std::cout << "Number of isomorphic automata: " << num_isomorphic << std::endl;
    std::cout << "Number of equivalent automata: " << num_equal << std::endl;
    return nullptr;
}




int main()
{
  spot::twa_graph_ptr a1 = ltl_2_tgba("../A_simplification_module/output/not_equal_simplif_all_options.txt", " ");
  // ltl_2_tgba("../A_simplification_module/output/spot_all_options.txt", "   ");
              // XGaUGa XGa isomorphic 0


//   spot::translator trans;
//   trans.set_type(spot::postprocessor::TGBA);
//   trans.set_pref(spot::postprocessor::Deterministic);
//   trans.set_level(spot::postprocessor::High);


//   std::string original_formula = "(c U a) & (a U (b U c))";
//   std::string mutant_formula = "((a) U ((b) U (c))) & ((c) U (a))";
  
//   spot::formula original_pf = spot::parse_formula(original_formula);
//   spot::formula mutant_pf = spot::parse_formula(mutant_formula);

//   spot::twa_graph_ptr original_automata = trans.run(original_pf);
//   spot::twa_graph_ptr mutant_automata = trans.run(mutant_pf);

// // 1 are isomorphic, meaning they have the same structure
//   std::cout << spot::isomorphism_checker::are_isomorphic(original_automata, mutant_automata) << std::endl;

  return 0;
}