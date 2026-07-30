SetPrintFormattingStatus("*stdout*", false);;
lines := [];;
input := InputTextFile("search/probe/wac_v1/_live20.txt");;
line := ReadLine(input);;
while line <> fail do
  Add(lines, Chomp(line));
  line := ReadLine(input);
od;;
CloseStream(input);;
els := List(lines, s -> EvalString(s));;
Print("n elements: ", Length(els), "\n");
G := Group(els);;
Print("group generated: size = ", Size(G), "\n");
closed := ForAll(els, a -> ForAll(els, b -> (a*b) in els));;
Print("closed under product: ", closed, "\n");
Print("contains identity: ", () in els, "\n");
inv_closed := ForAll(els, a -> a^-1 in els);;
Print("closed under inverse: ", inv_closed, "\n");
QUIT;
