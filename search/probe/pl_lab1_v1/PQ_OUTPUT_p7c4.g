F := FreeGroup( 8 );
F := PcGroupFpGroupNC( F / [
 F.1^7,
 F.2^7,
 F.3^7,
 F.4^7,
 F.5^7,
 F.6^7,
 F.7^7,
 F.8^7,
 Comm( F.2, F.1 ) / F.3,
 Comm( F.3, F.1 ) / F.4,
 Comm( F.3, F.2 ) / F.5,
 Comm( F.4, F.1 ) / F.6,
 Comm( F.4, F.2 ) / F.7,
 Comm( F.5, F.1 ) / F.7,
 Comm( F.5, F.2 ) / F.8] );
MapImages := [];
MapImages[1] :=  F.1;
MapImages[2] :=  F.2;
