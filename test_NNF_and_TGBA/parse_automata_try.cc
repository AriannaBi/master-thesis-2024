#include <iostream>
#include <spot/tl/parse.hh>
#include <spot/twaalgos/translate.hh>
#include <spot/twaalgos/hoa.hh>
#include <spot/twaalgos/dot.hh>
#include <spot/twaalgos/stats.hh>
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
#include <spot/parseaut/public.hh>
#include <spot/twaalgos/postproc.hh>
#include <spot/twa/bddprint.hh>
#include <string>
#include <iostream>
#include <spot/parseaut/public.hh>
#include <spot/twaalgos/hoa.hh>
#include <spot/twa/bddprint.hh>

// Test equivalences of two automata by creating one single automaton (from two automaton supposed equivalent) and then compute 
// the minimization of the automaton. After that map the states of the two automaton to the states of the minimized automaton.
// If the mapping is the same, then the two automaton are equivalent, otherwise they are not.
// This is more efficient than the previous method because it is based on the minimization of the automaton.
// The previous method is based on the syntactic comparison of the body of the automaton.
// The two automaton are isomorphic hence equivalent but syntactically different.


// Generate test.hoa file with an LTL formula
// ltl2tgba -U 'G(b & c) & a' | tee tut21.hoa



// write a program that from a ltl formula it generates a tgba automaton and then check if two automata are equivalent
// g++ -std=c++17 spot_2_tgba_equivalent.cc -lspot -o spot_2_tgba_equivalent -lbddx


int read_start_state(std::string filename) {
    // Open the file
    std::ifstream file(filename);
    std::string line;

    // Move to line number 3
    for (int i = 0; i < 4; ++i) {
        std::getline(file, line);
    }
    std::cout << "Line 3: " << line << std::endl;

    // Read the number from line number 3
    std::istringstream iss(line);
    std::string start;
    int number;
    iss >> start >> number; // Read the "Start:" string and the number

    // Output the number
    // std::cout << "Number from line number 3: " << number << std::endl;

    // Close the file
    file.close();

    return number;
}


int merge_two_automaton(spot::parsed_aut_ptr& pa1, spot::parsed_aut_ptr& pa2) {

    // set the translator
    spot::translator trans;
    trans.set_type(spot::postprocessor::TGBA);
    trans.set_pref(spot::postprocessor::Deterministic);
    trans.set_level(spot::postprocessor::High);


  // Reading line
    // while (std::getline(file, line)) {
    // for (int i = 0; std::getline(file, line) && i < 1; ++i) {
    //   std::string original_string = "";
    //   std::stringstream original_stream;

    //   // Process each line
    //   std::vector<std::string> strings;
    //   std::string delimiter = "/";
    //   strings = split (line, delimiter);
    //   strings.erase(std::remove_if(strings.begin(), strings.end(), [](const std::string& str) { return str.empty(); }),strings.end());
      
    //   // take first string
    //   std::string original_formula = strings[0];
    //   spot::formula original_pf = spot::parse_formula(original_formula);


    //   // create the TGBA
    //   spot::twa_graph_ptr original_automata = trans.run(original_pf);
    //   print_hoa(original_stream, original_automata);
    //   original_string = original_stream.str();




    // }



    return 1;
}
int main()
{
  // spot::twa_graph_ptr a1 = ltl_2_tgba("output/filtered_spot_all_options.txt");
  // ltl_2_tgba("output/filtered_spot_all_options.txt");

  spot::parsed_aut_ptr pa = parse_aut("HOA1.hoa", spot::make_bdd_dict());
  if (pa->format_errors(std::cerr)){
    std::cout << "Format error\n";
    return 1;
  }
  if (pa->aborted)
  {
    std::cout << "--ABORT-- read\n";
    return 1;
  }

  spot::parsed_aut_ptr pa2 = parse_aut("HOA1.hoa", spot::make_bdd_dict());
  if (pa2->format_errors(std::cerr)){
    std::cout << "Format error\n";
    return 1;
  }
  if (pa2->aborted)
  {
    std::cout << "--ABORT-- read\n";
    return 1;
  }
  // print_hoa(std::cout, pa->aut);
  // merge_two_automaton(pa, pa2);


  int n = read_start_state("HOA1.hoa");
  std::cout << "Start state: " << n << std::endl;

  return 0;
}