% paper11.ly

\include "table11.ly";

paper_eleven = \paper {
	staffheight = 11.0\pt;
	% a4 paper
	linewidth = 15.0 \cm;
	textheight = 15.0 \cm;

        % ugh see table11 for sizes
	quartwidth = 3.63\pt;
	wholewidth = 5.45\pt;

	arithmetic_basicspace = 2.;
        arithmetic_multiplier = 4.8\pt;
	
	0=\symboltables { \table_eleven }
	\include "params.ly";
}

