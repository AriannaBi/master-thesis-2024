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
#include <spot/twaalgos/product.hh>
#include <spot/twaalgos/emptiness.hh>
#include <spot/twaalgos/gtec/gtec.hh>
#include <stdio.h> 
#include "test_emptiness_automata.hh"

// write a program that check if two automata are equivalent
// g++ -std=c++17 emptiness/test_emptiness_automata.cc -lspot -o emptiness/test_emptiness_automata -lbddx


int main()
{
  // 0 means equivalent because empty 
  // 1 means not equivalent because not empty

  spot::formula formula = spot::parse_formula("F G ! (a U X a)");
  spot::formula formula_inv = spot::parse_formula("F G ! (a U X (!b U c))");
  assert(check_emptiness_two_automaton(formula,formula_inv) == 1); 

  // formula = spot::parse_formula("Ga U Fb | Xa");
  // formula_inv = spot::parse_formula("!(Ga U Fb | Xa)");
  // assert(merge_two_automaton(formula,formula_inv) == 0); //empty - equivalent

  // formula = spot::parse_formula("Ga U Fb | Xa");
  // formula_inv = spot::parse_formula("!(FFa U Gb | Xa)");
  // assert(merge_two_automaton(formula,formula_inv) == 1); //not empty - not equivalent

  // They are supposed to be equivalent
  // formula = spot::parse_formula("(a U X(a | Xa)) U Xa");
  // formula_inv = spot::parse_formula("a  U  X(a  |  Xa) ");
  // assert(check_emptiness_two_automaton(formula,formula_inv) == 0); //empty - equivalent
  // check_emptiness_two_automaton(formula,formula_inv);
  return 0;
}