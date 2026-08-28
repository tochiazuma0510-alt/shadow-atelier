## drophunt_sweep_clear_poison_lock_v1.g -- documented, machine-executed
## poison-lock clear procedure (裁定1776 item 5: "poison lockの解除手順も
## 整えて記録"). Intentionally requires a HUMAN to set DSDClearConfirm:=true
## before Read()-ing this file (no silent auto-clear) -- the poison lock's
## whole purpose is to force a human look at a DROP/ANOMALY/BUG halt before
## the sweep can continue, so the clear procedure must not be a one-liner
## `rm` that can be run on reflex.
##
## Usage (from a wrapper or interactively):
##   DSDClearConfirm := true;;
##   DSDClearLockPath := "search/certs/drophunt_sweep_droplock_v3_20260829.g";;   # or the scoped test path
##   Read("search/drophunt_sweep_clear_poison_lock_v1.g");;
##
## The procedure does NOT touch the checkpoint file (DSDCheckpointPath) --
## clearing the lock only re-enables resume from the checkpoint's own
## last_completed index; it does not retroactively "unhalt" or reprocess
## the window that triggered the lock (that window's halt-checkpoint JSON,
## e.g. drophunt_sweep_{drop,anomaly,bug}_<node16>_v3_20260829.json, remains
## on disk as a permanent record of the event -- clearing the lock allows
## the SWEEP TO CONTINUE PAST it, not to re-litigate it silently).
if not IsBound(DSDClearConfirm) or DSDClearConfirm <> true then
  Error("DSD: poison lock clear REFUSED -- set DSDClearConfirm:=true before Read()-ing this file (human confirmation required, see file header)");
fi;;
if not IsBound(DSDClearLockPath) then
  Error("DSD: poison lock clear REFUSED -- DSDClearLockPath not set (which lock file to clear?)");
fi;;
if not IsExistingFile(DSDClearLockPath) then
  Print("DSD_POISON_LOCK_CLEAR_NOOP path=", DSDClearLockPath, " (no lock file present -- nothing to clear)\n");;
else
  DSDPoisonLockReason := fail;; DSDPoisonLockIndex := fail;; DSDPoisonLockNodeId := fail;;
  Read(DSDClearLockPath);;
  Print("DSD_POISON_LOCK_CLEARING path=", DSDClearLockPath, " reason=", DSDPoisonLockReason,
    " index=", DSDPoisonLockIndex, " node_id=", DSDPoisonLockNodeId, "\n");;
  RemoveFile(DSDClearLockPath);;
  Print("DSD_POISON_LOCK_CLEARED path=", DSDClearLockPath, "\n");;
fi;;
Print("ALL_DONE\n");;
