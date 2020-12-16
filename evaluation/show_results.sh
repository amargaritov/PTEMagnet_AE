RESULTS_DIR="$1"
if [ -z "$1" ]
  then
    RESULTS_DIR=$REPO_ROOT/evaluation/results
fi


echo "Using results from $RESULTS_DIR"
if [ ! -d $RESULTS_DIR ]; then 
   echo "can't find directory with the results. Are you sure it exists?"
else
   for i in $(ls $RESULTS_DIR); do pushd $RESULTS_DIR/$i > /dev/null; avg_time=$(grep -R Full_time | awk '{ sum += $2; n++ } END { if (n > 0) print sum / n; }'); echo "$i $avg_time"; popd > /dev/null ; done | sed 's/-on-/,/g' | sed 's/-kernel\ */,/g' | $REPO_ROOT/evaluation/calc_impr.py
  fi
