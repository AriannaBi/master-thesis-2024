// #ifndef test_emptiness_automata
// #define test_emptiness_automata

#include <iostream>
#include <spot/tl/parse.hh>
#include <spot/twaalgos/translate.hh>
#include <spot/twaalgos/hoa.hh>
#include <spot/twaalgos/dot.hh>
#include <spot/twaalgos/stats.hh>
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
#include <spot/twaalgos/product.hh>
#include <spot/twaalgos/emptiness.hh>
#include <spot/twaalgos/gtec/gtec.hh>

// write a program that check if two automata are equivalent
// g++ -std=c++17 emptiness/test_emptiness_automata.cc -lspot -o emptiness/test_emptiness_automata -lbddx


int check_emptiness_two_automaton(spot::formula formula, spot::formula formula2){
  // set the translator
  spot::translator trans;
  trans.set_type(spot::postprocessor::TGBA);
  trans.set_pref(spot::postprocessor::Deterministic);
  trans.set_level(spot::postprocessor::High);
  // negate formula_inv
  // spot::formula formula = spot::formula::Not(formula1);
  spot::formula formula_inv = spot::formula::Not(formula2);

  // std::cout << "Formula: " << formula << std::endl;
  // std::cout << "Formula inv: " << formula_inv << std::endl;


  // create the TGBA
  spot::twa_graph_ptr automata = trans.run(formula);
  spot::twa_graph_ptr automata_inv = trans.run(formula_inv);

  // create the intersection of the two automata (product automaton)
  spot::twa_graph_ptr intersection = spot::product(automata, automata_inv);

  // create the emptiness checker
  spot::option_map options; //empty options
  spot::emptiness_check_ptr emptiness_checker = spot::couvreur99(intersection, options);

  /// Perform the emptiness check
  spot::emptiness_check_result_ptr result = emptiness_checker->check();


  // Check if the automaton is empty
  if (!result) {
      // std::cout << "Automaton is empty." << std::endl;
      return 0;
  } else {
      // std::cout << "Automaton is not empty." << std::endl;
      // Optionally, retrieve an accepting run and print it
      spot::twa_run_ptr accepting_run = result->accepting_run();
      if (accepting_run) {
          std::cout << "Accepting run: " << *accepting_run << std::endl;
      }
      return 1;
  }

  return 1;
}

// #endif  test_emptiness_automata
