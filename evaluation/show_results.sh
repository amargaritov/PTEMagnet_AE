for i in $(ls ./results); do pushd ./results/$i > /dev/null; avg_time=$(grep -R Test_time | awk '{ sum += $2; n++ } END { if (n > 0) print sum / n; }'); echo "$i $avg_time"; popd > /dev/null ; done
