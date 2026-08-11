F := FreeGroup( 10 );
F := PcGroupFpGroupNC( F / [
 F.1^5,
 F.2^5,
 F.3^5,
 F.4^5,
 F.5^5,
 F.6^5,
 F.7^5,
 F.8^5,
 F.9^5,
 F.10^5,
 Comm( F.2, F.1 ) / F.3,
 Comm( F.3, F.1 ) / F.4,
 Comm( F.3, F.2 ) / F.5,
 Comm( F.4, F.1 ) / F.6,
 Comm( F.4, F.2 ) / F.7,
 Comm( F.4, F.3 ) / F.9,
 Comm( F.5, F.1 ) / (F.7*F.9*F.10^2),
 Comm( F.5, F.2 ) / F.8,
 Comm( F.5, F.3 ) / F.10^2,
 Comm( F.6, F.2 ) / F.9,
 Comm( F.7, F.1 ) / F.9^2,
 Comm( F.7, F.2 ) / F.10,
 Comm( F.8, F.1 ) / F.10^3] );
MapImages := [];
MapImages[1] :=  F.1;
MapImages[2] :=  F.2;
