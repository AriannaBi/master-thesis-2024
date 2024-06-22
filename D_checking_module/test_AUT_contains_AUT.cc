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
#include <spot/parseaut/public.hh>
#include <spot/twaalgos/contains.hh>

// THIS IS THE TEST WITHOUT A MODEL, BUT WITH TWO AUTOMATAS OF THE SAME FORMULA, TRANSLATED WITH TWO DIFFERENT TRANSLATORS

// Test model checking with spot: if the first automata contains the second automata. 
// returns the result and compare if the model checking.


// Compare the two automatas, as one is the model and the other is the formula. 
// Since the two automatas are equivalent, the result should always be that the language is contained. 

// g++ -std=c++17 test_AUT_contains_AUT.cc -lspot -o test_AUT_contains_AUT -lbddx

// HOA_not_isomorph.txt contains all the automatas that are not isomorphic

int check_language_containment(std::string hoa_file) {
  // Open file
  std::string automata_name_spot;
  std::string automata_name_spin;

  std::ifstream read_file(hoa_file);
  if (!read_file.is_open()) { // Check if the file is open
    std::cerr << "Error: Unable to open file." << std::endl;
    throw std::runtime_error("Error parsing hoa file");
    return -1;
  }


  // read the file and split it by ~
  std::string line;
  bool spot = true;
  std::string HOA_spot;
  std::string HOA_spin;
  // read two by two automata, delimited with ~ and two automatas are separated by .
  int i = 0;
  std::string name_formula;
  int num_not_isomorphic = 0;
  int num_automatas = 0;
  int not_equivalent = 0;
  while (std::getline(read_file, line)) {
    if (line[0] == '~') {
      std::getline(read_file, line);
      HOA_spot.erase(HOA_spot.size() - 1);
      HOA_spin.erase(HOA_spin.size() - 1);
      // std::cout << HOA_spot << std::endl;
      // std::cout << HOA_spin << std::endl;

      // save hoa to file
      std::ofstream spot_file("spot.hoa");
      spot_file << HOA_spot;
      spot_file.close();

      std::ofstream spin_file("spin.hoa");
      spin_file << HOA_spin;
      spin_file.close();


      auto dict = spot::make_bdd_dict();
      spot::parsed_aut_ptr spot_aut = parse_aut("spot.hoa", dict);
      spot::parsed_aut_ptr spin_aut = parse_aut("spin.hoa", dict);

      if (!spot::contains(spot_aut->aut, spin_aut->aut)) {
        std::cout << "The first automata does not contain the second automata " <<  std::endl;
        std::cout << "Automatas for this formulas [" << name_formula << "] return F" << std::endl;
        not_equivalent++; 
        std::cout << '\n' << std::endl;
      } 
     


      HOA_spin = "";
      HOA_spot = "";
      spot = true;
      i = 0;
      num_automatas++;
    }
    if (line[0] == '.') {
      spot = false;
    }else if (spot){
      HOA_spot += line +'\n';
      if (i == 1){
        name_formula = line;
      }
      i++;

    } else {
      HOA_spin += line +'\n';
    }
  }
  
  // std::cout << "Number of automatas: " << num_automatas << std::endl;
  // std::cout << "Number of non isomorphic automatas: " << num_not_isomorphic << std::endl;
  // std::cout << "Number of non equivalent automatas: " << not_equivalent << std::endl;
  
  if (remove("files/spin.hoa") != 0) {
    perror("Error deleting file");
  }
  if (remove("files/spot.hoa") != 0) {
    perror("Error deleting file");
  }
  return 0;
}




int main()
{
  check_language_containment("../B_aut_translation_module/HOA_not_isomorph.txt");
  return 0;
}