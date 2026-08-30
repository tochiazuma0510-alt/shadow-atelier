#############################################################################
## Generic gap-run.yml adapter for the raw-row repaired batch-64 v29 driver.
## The filename intentionally matches gap-run.yml's authenticated A0 prefix.
#############################################################################
D411BatchDriver:="search/d972_r07_history_free_positive_fast_resume_batch64_gha_driver_v29.g";;
if not IsExistingFile(D411BatchDriver) then
  Error("task408 missing batch driver");
fi;
Read(D411BatchDriver);;
