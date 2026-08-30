#############################################################################
## Generic gap-run.yml adapter for the exact-pinned batch-64 v28 driver.
## The filename intentionally matches gap-run.yml's authenticated A0 prefix.
#############################################################################
D409BatchDriver:="search/d972_r07_history_free_positive_fast_resume_batch64_gha_driver_v28.g";;
if not IsExistingFile(D409BatchDriver) then
  Error("task409 missing batch driver");
fi;
Read(D409BatchDriver);;
