dtmc

module sender

	s : [0..1] init 0;
	[] s=0 -> 1/2 : (s'=0) + 1/2 : (s'=1);
	[] s=1 -> 1 : (s'=1);
	
	
endmodule

label "a" = (s=0);
label "b" = (s=1);

