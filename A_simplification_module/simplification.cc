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
#include <string>
#include <algorithm>



// https://spot.lre.epita.fr/compile.html
// https://spot.lre.epita.fr/tl.pdf
// https://spot.lre.epita.fr/ltlfilt.html
// https://spot.lre.epita.fr/tut01.html
// https://spot.lre.epita.fr/tut.html

// Run inside folder A_simplific_module
// g++ -std=c++17 simplification.cc -lspot -o simplification
// ./simplification

// Program that simplify the LTL formulas using spot library
// The program receives a file with LTL formulas and output a file with the simplified formulas
// The program receives the options to simplify the formulas
// The program also test all the options combination for a given formula
// The program output the simplified formula for each combination of options in the output/ folder

namespace fs = std::filesystem;

int simplify_formulas(std::string readFile, std::string outFile, bool basics, bool synt_impl, bool event_univ, bool containment_checks, bool containment_checks_stronger, bool nenoform_stop_on_boolean, bool reduce_size_strictly, bool boolean_to_isop, bool favor_event_univ) {

    // Open file
    std::ifstream file(readFile);
    if (!file.is_open()) { // Check if the file is open
        std::cerr << "Error: Unable to open file." << std::endl;
        return 1;
    }
    std::ofstream outputFile(outFile);
    if (!outputFile) { 
        std::cerr << "Error opening file for writing!" << std::endl;
        return 1; // Exit the program with an error status
    }

    // Read the file line by line
    std::string line;

  // Reading line
    // for (int i = 0; std::getline(file, line) && i < 50; ++i) {
    while (std::getline(file, line)) {
        // Process each line
        std::istringstream iss(line);
        std::vector<std::string> strings;
        std::string word;
        while (iss >> word) {
            strings.push_back(word);
        }

        for (const std::string& str : strings) {
          spot::tl_simplifier ss = spot::tl_simplifier_options(basics, synt_impl, event_univ, containment_checks, containment_checks_stronger, nenoform_stop_on_boolean, reduce_size_strictly, boolean_to_isop, favor_event_univ);
          spot::formula simplified_phi = ss.simplify(spot::parse_formula(str));

          // run abbreviator without <->, ->, M, R, W and Xor
          spot::unabbreviator unabbrev("eiMRW^");
          simplified_phi = unabbrev.run(simplified_phi);
          std::string simplified_phi_str = spot::str_psl(simplified_phi, true);
          // remove space in between the formula
          simplified_phi_str.erase(std::remove(simplified_phi_str.begin(), simplified_phi_str.end(), ' '), simplified_phi_str.end());
          // add space only before and after the U because the parser can't parse aU!a or aU a
          // however, it can read a|(aUXa), hence it doesn't work only when there is a not operator after U, or the spaces are not both sides of U
          // std::cout << simplified_phi_str << std::endl;
          // std::string::size_type pos = simplified_phi_str.find("U!");
          // if (pos != std::string::npos) {
          //   simplified_phi_str.replace(pos, 2, " U !");
          // }
          // std::cout << simplified_phi_str << std::endl;
          
          outputFile <<  "   " << simplified_phi_str;
          

        }
        outputFile <<  std::endl;
    }

    // Close the file
    outputFile.close();
    file.close();
    return 0;
}


void test_all_options_combination(std::string formula) {
  for (int i = 0; i < (1 << 9); ++i) {
        // Convert the number to a binary representation
        std::bitset<9> bits(i);
          bool basics;
          bool synt_impl;
          bool event_univ;
          bool containment_checks;
          bool containment_checks_stronger;
          bool nenoform_stop_on_boolean;
          bool reduce_size_strictly;
          bool boolean_to_isop;
          bool favor_event_univ;
        
        // Output the binary representation
        for (int j = 8; j >= 0; --j) {
            // std::cout << bits[j] << " ";
            if (j == 8) {
              basics = bits[j];
            } else if (j == 7) {
              synt_impl = bits[j];
            } else if (j == 6) {
              event_univ = bits[j];
            } else if (j == 5) {
              containment_checks = bits[j];
            } else if (j == 4) {
              containment_checks_stronger = bits[j];
            } else if (j == 3) {
              nenoform_stop_on_boolean = bits[j];
            } else if (j == 2) {
              reduce_size_strictly = bits[j];
            } else if (j == 1) {
              boolean_to_isop = bits[j];
            } else if (j == 0) {
              favor_event_univ = bits[j];
            }
        }
        // std::count 
        // std::cout << basics << synt_impl << event_univ << containment_checks << containment_checks_stronger << nenoform_stop_on_boolean << reduce_size_strictly << boolean_to_isop << favor_event_univ;
        // simplify_formulas("filtered_mutants_LTL.txt", "output/spot_containment_checks.txt", basics, synt_impl, event_univ, containment_checks, containment_checks_stronger, nenoform_stop_on_boolean, reduce_size_strictly, boolean_to_isop, favor_event_univ);
        spot::tl_simplifier ss = spot::tl_simplifier_options(basics, synt_impl, event_univ, containment_checks, containment_checks_stronger, nenoform_stop_on_boolean, reduce_size_strictly, boolean_to_isop, favor_event_univ);
        spot::formula simplified_phi = ss.simplify(spot::parse_formula(formula));

        // run abbreviator without <->, ->, M, R, W and Xor
        spot::unabbreviator unabbrev("eiMRW^");
        simplified_phi = unabbrev.run(simplified_phi);
        std::cout << simplified_phi;
        std::cout << std::endl;
    }
}

// Function to remove spaces within a formula
std::string remove_internal_spaces(const std::string& formula) {
    std::string result;
    // formula.erase(std::remove(formula.begin(), formula.end(), ' '), formula.end());
    // remove space
    for (char c : formula) {
        if (c != ' ') {
            result += c;
        }
    }
    return result;
}

int main() {
  // create array with "spot_event_univ.txt", "spot_boolean_to_isop.txt", "spot_reduce_basic.txt", "spot_no_options.txt"
  // std::string files[] = {"spot_event_univ.txt", "spot_boolean_to_isop.txt", "spot_reduce_basic.txt", "spot_no_options.txt"};


  std::string folder_name = "output";

  // Check if the folder exists
  if (fs::exists(folder_name)) {
      // Remove the existing folder and its contents
      fs::remove_all(folder_name);
      std::cout << "Existing folder '" << folder_name << "' deleted." << std::endl;
  }

  // Create a new empty folder
  fs::create_directory(folder_name);
  std::cout << "New folder '" << folder_name << "' created." << std::endl;


  //no options
  bool basics = false;
  bool synt_impl = false;
  bool event_univ = false;
  bool containment_checks = false;
  bool containment_checks_stronger = false;
  bool nenoform_stop_on_boolean = false;
  bool reduce_size_strictly = false;
  bool boolean_to_isop = false;
  bool favor_event_univ = false;
  // simplify_formulas("filtered_mutants_LTL.txt", "output/spot_no_options.txt", basics, synt_impl, event_univ, containment_checks, containment_checks_stronger, nenoform_stop_on_boolean, reduce_size_strictly, boolean_to_isop, favor_event_univ);
  

  // reduce basic
  basics = true;
  synt_impl = false;
  event_univ = false;
  containment_checks = false;
  containment_checks_stronger = false;
  nenoform_stop_on_boolean = false;
  reduce_size_strictly = false;
  boolean_to_isop = false;
  favor_event_univ = false;
  // simplify_formulas("filtered_mutants_LTL.txt", "output/spot_basics_2.txt", basics, synt_impl, event_univ, containment_checks, containment_checks_stronger, nenoform_stop_on_boolean, reduce_size_strictly, boolean_to_isop, favor_event_univ);
  
  // synactic implications (cheap way, sometimes it doesn't work)
  basics = false;
  synt_impl = true;
  event_univ = false;
  containment_checks = false;
  containment_checks_stronger = false;
  nenoform_stop_on_boolean = false;
  reduce_size_strictly = false;
  boolean_to_isop = false;
  favor_event_univ = false;
  // simplify_formulas("filtered_mutants_LTL.txt", "output/spot_synt_impl.txt", basics, synt_impl, event_univ, containment_checks, containment_checks_stronger, nenoform_stop_on_boolean, reduce_size_strictly, boolean_to_isop, favor_event_univ);
  
   // lift subformulas and lower subformulas
  basics = false;
  synt_impl = false;
  event_univ = false;
  containment_checks = false;
  containment_checks_stronger = false;
  nenoform_stop_on_boolean = false;
  reduce_size_strictly = false;
  boolean_to_isop = false;
  favor_event_univ = true;
  // simplify_formulas("filtered_mutants_LTL.txt", "output/spot_favor_event_univ.txt", basics, synt_impl, event_univ, containment_checks, containment_checks_stronger, nenoform_stop_on_boolean, reduce_size_strictly, boolean_to_isop, favor_event_univ);
  
   // language containment check and strict(reduction based on automata-based containements?)
  basics = false;
  synt_impl = false;
  event_univ = false;
  containment_checks = true;
  containment_checks_stronger = true;
  nenoform_stop_on_boolean = false;
  reduce_size_strictly = false;
  boolean_to_isop = false;
  favor_event_univ = false;
  // simplify_formulas("filtered_mutants_LTL.txt", "output/spot_containment_checks.txt", basics, synt_impl, event_univ, containment_checks, containment_checks_stronger, nenoform_stop_on_boolean, reduce_size_strictly, boolean_to_isop, favor_event_univ);
  

  // all the options
  basics = true;
  synt_impl = true;
  event_univ = true;
  containment_checks = true;
  containment_checks_stronger = true;
  nenoform_stop_on_boolean = true;
  reduce_size_strictly = true;
  boolean_to_isop = true;
  favor_event_univ = true;
  // No issue if the folder doesn't exists. It will be generated
  simplify_formulas("../generate/output/filtered_mutants_LTL.txt", "output/spot_all_options.txt", basics, synt_impl, event_univ, containment_checks, containment_checks_stronger, nenoform_stop_on_boolean, reduce_size_strictly, boolean_to_isop, favor_event_univ);
  

  // std::string formula = "(G(X(\"a\")))&(G(\"a\"))"; //GX(a)&G(a)
  // std::string formula2 = "G((X(\"a\"))&(\"a\"))"; //G(X(a)&a)
  // test_all_options_combination(formula2);


  return 0;
}