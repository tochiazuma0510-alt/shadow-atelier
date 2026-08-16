## One-shot local driver for the canonical KBMAG v2 audit.
## This file is versioned source; the receipt is written to GAP's temp dir.
if not IsBound(D972_B4_KBMAG_V2_OUTPUT) then
  D972_B4_KBMAG_V2_OUTPUT := Filename(DirectoryTemporary(),
    "d972_b4_kbmag_v2_receipt.json");
fi;
if not IsBound(D972_B4_KBMAG_V2_MAXEQNS) then
  D972_B4_KBMAG_V2_MAXEQNS := 50000;
fi;
if not IsBound(D972_B4_KBMAG_V2_MAXSTATES) then
  D972_B4_KBMAG_V2_MAXSTATES := 50000;
fi;
if not IsBound(D972_B4_KBMAG_V2_MAXWDIFFS) then
  D972_B4_KBMAG_V2_MAXWDIFFS := 50000;
fi;
if not IsBound(D972_B4_KBMAG_V2_MAXSTORED) then
  ## The canonical presentation contains relators of length 150.  The
  ## historical [100,100] cap rejects the input before KB starts.
  D972_B4_KBMAG_V2_MAXSTORED := [1000,1000];
fi;
Read("search/d972_b4_kbmag_v2.g");;
