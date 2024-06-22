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

// INPUT: hoa_file & hoa_model
// OUTPUT: equality satisfiability of the model with the automata

// Test model checking with spot: test the model automata with the first automata, and then with the equivalent second automata. 
// compare if they are both satisfiable.

// g++ -std=c++17 test_contain_checking_spot.cc -lspot -o test_contain_checking_spot -lbddx


// HOA_not_isomorph.txt contains all the automatas that are not isomorphic

int check_module_spot(std::string hoa_file, std::string hoa_model) {
  // Open file
  std::string automata_name_spot;
  std::string automata_name_spin;

  std::ifstream read_file(hoa_file);
  if (!read_file.is_open()) { // Check if the file is open
    std::cerr << "Error: Unable to open file." << std::endl;
    throw std::runtime_error("Error parsing hoa file");
    return -1;
  }
  std::ifstream read_model(hoa_model);
  if (!read_model.is_open()) { // Check if the file is open
    std::cerr << "Error: Unable to open file." << std::endl;
    throw std::runtime_error("Error parsing hoa model");
    return -1;
  }
  // https://spot.lre.epita.fr/hoa.html
  // autfil uses the state based acceptance. If i want to use another option I can use ltl2tgba -Hm
  // HOA_spot = "ltl2tgba "G (a -> Xb) & F (b -> Xa) | F(a -> c)"";

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
    auto dict = spot::make_bdd_dict();
    if (line[0] == '~') {
      std::getline(read_file, line);
      HOA_spot.erase(HOA_spot.size() - 1);
      HOA_spin.erase(HOA_spin.size() - 1);

      // save hoa to file
      std::ofstream spot_file("files/spot.hoa");
      spot_file << HOA_spot;
      spot_file.close();

      std::ofstream spin_file("files/spin.hoa");
      spin_file << HOA_spin;
      spin_file.close();


      spot::parsed_aut_ptr spot_model_aut = parse_aut(hoa_model, dict);
      spot::parsed_aut_ptr spot_aut = parse_aut("files/spot.hoa", dict);
      spot::parsed_aut_ptr spin_aut = parse_aut("files/spin.hoa", dict);

      bool contains_model_spot = spot::contains(spot_model_aut->aut, spot_aut->aut);
      bool contains_model_spin = spot::contains(spot_model_aut->aut, spin_aut->aut);

      if (contains_model_spot && !contains_model_spin) {
        std::cout << "The model contains the spot model, but the model doesn't contain the spin model" <<  std::endl;
        std::cout << "Automatas for this formulas [" << name_formula << "]" << std::endl;
        std::cout << '\n' << std::endl;
        not_equivalent++;
      } else if (!contains_model_spin && contains_model_spot){
        std::cout << "The model doesn't contains the spot model, but the model contains the spin model" <<  std::endl;
        std::cout << "Automatas for this formulas [" << name_formula << "]" << std::endl;
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
  if (not_equivalent == 0) {
    std::cout << "All automatas are satisfied by the model M" << std::endl;
  } else {
    std::cout << "Some automatas are NOT satisfied by the model M" << std::endl;
  }

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
  // HOA_not_isomorph.txt is created by the B_aut_translation_module in the file test_spot_spni_compare.cc
  check_module_spot("../B_aut_translation_module/files/HOA_not_isomorph.txt", "files/spot_model.hoa");
  return 0;
}