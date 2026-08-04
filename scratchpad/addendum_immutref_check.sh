#!/bin/bash
# Machine check for hsp7_cond4_summary_v2_addendum_immutref_20260805.json
# Confirms: git commit exists, blob exists inside that commit at the stated path,
# extracted blob bytes sha256 equals the pinned value, and records the current
# live-path divergence as a fact (not an assertion of consistency).
set -e

COMMIT=468287e1c3f12b124da94b2e925936d4854ebfb0
BLOB=eca5dc71854123acfaf333bcb3e2d7afc089e041
EXPECT_SHA256=2ebf7c5e63a41b8989719823527a6f18bb2c5614435bf25a08340080060fa8e7
LIVE_PATH=sol/sol_reply_102_math29.md

echo "commit_type=$(git cat-file -t $COMMIT)"
echo "blob_type=$(git cat-file -t $BLOB)"
echo "path_in_commit=$(git ls-tree -r $COMMIT | grep $BLOB | awk '{print $4}')"

git cat-file blob $BLOB > scratchpad/.addendum_blob_extract.bin
ACTUAL_SHA256=$(sha256sum scratchpad/.addendum_blob_extract.bin | awk '{print $1}')
echo "blob_bytes_sha256_actual=$ACTUAL_SHA256"
echo "blob_bytes_sha256_expected=$EXPECT_SHA256"
if [ "$ACTUAL_SHA256" = "$EXPECT_SHA256" ]; then
  echo "MATCH=true"
else
  echo "MATCH=false"
fi

echo "live_path_sha256_current=$(sha256sum $LIVE_PATH | awk '{print $1}')"
echo "live_path_git_hash_object_current=$(git hash-object $LIVE_PATH)"
echo "blob_byte_count=$(wc -c < scratchpad/.addendum_blob_extract.bin)"
echo "live_byte_count=$(wc -c < $LIVE_PATH)"
