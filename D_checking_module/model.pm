mdp

module automaton

    s : [0..1] init 0;

    // State transitions
    [] s=0 -> (s'=1);


endmodule

// Define acceptance conditions (Buchi)
label "acc" = (s=1) | (s=0);
