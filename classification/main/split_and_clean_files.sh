#!/bin/bash

mydir=/tmp/brazil
raw_dirs=${mydir}/raw/files
log_dir=${mydir}/logs/clean
out_dir=$mydir/results

function run_all_pipeline {
    for year in `seq 2004 2015`; # year=2004
    do
	raw_dir=${raw_dirs}/$year
	mkdir -p $raw_dir/irr
	cp $mydir/files/${year}* ${raw_dir}/irr/

	printf "raw_dir:%s \n" $raw_dir;
	eval x_$year=$(find $raw_dir -maxdepth 2 -type f -size +1024c | wc -l); # echo $[x_$year] = 7876
	for i in `seq 1 $[(x_$year/4000)+1]`;
	do
	    divided_dir=${mydir}/raw/divided/${year}/${i}
	    clean_dir=${mydir}/clean/divided/${year}/${i}
	    log_file=${log_dir}/clean_err_${year}_${i}.txt
	    mkdir -pv ${divided_dir}/irr
	    find $raw_dir -maxdepth 2 -type f -size +1024c | head -n 4000 | xargs -i mv "{}" "$divided_dir/irr"
	    python /home/users/guest7/brazil/clean.py --raw_dir $divided_dir --parsed_dir $clean_dir 2> $log_file &
	    calculate_results
	done
    done
}

function mymain {
    for year in `seq 2004 2015`; # year=2004
    do
	raw_dir=${raw_dirs}/$year
	printf "raw_dir:%s \n" $raw_dir;
	for i in `ls ${mydir}/clean/divided/${year}`;
	do
	    clean_dir=${mydir}/clean/divided/${year}/${i}
	    calculate_results
	done
    done
}

function calculate_results {
    textdir=$clean_dir
    java_output_file=$out_dir/classification_${year}_$i.output
    java -Xmx6g -ea -Djava.awt.headless=true -Dfile.encoding=UTF-8 -server -classpath $mydir/factorie_2.11-1.2-SNAPSHOT-nlp-jar-with-dependencies.jar cc.factorie.app.classify.Classify --read-text-dirs $textdir --read-text-encoding ISO-8859-1 --training-portion 0.0 --read-vocabulary $mydir/vocab.txt --read-classifier $mydir/mymodel.factorie > $java_output_file
    printf "Results written to:%s \n" $java_output_file
}

function show_classification_results {
    find $out_dir -type f -print0 | xargs -0 grep "rel" | wc -l
}

function check_if_divided {
    for year in `ls $raw_dirs`;
    do
	eval x_$year=$(find $raw_dirs/$year -maxdepth 2 -type f | wc -l);
	printf "%s: %d\n" $year $[x_${year}];
    done
}

function how_many_cleaned_html {
    search_dir=${mydir}/clean/divided
    for year in `ls $search_dir`;
    do
	eval x_$year=$(find $search_dir/$year -maxdepth 3 -type f | wc -l);
	printf "%s: %d\n" $year $[x_${year}];
    done
}

function news_per_month {
    search_dir=/ai/home/acelebi/folca/data
    for year in `ls $search_dir`;
    do
	for month in `ls $search_dir/${year}`;
	do
	    eval x_${year}_$month=$(find $search_dir/$year/$month -maxdepth 3 -type f | wc -l);
	    #printf "%s,%s : %d\n" $year $month $[x_${year}_${month}];
	    printf "norm[%s][%s] = %d\n" $year $month $[x_${year}_${month}];
	done
    done
}


#for year in `seq 2004 2015`;
#do
#    mkdir -p $mydir/raw/files/$year/irr
#    cp $mydir/files/irr/${year}* $mydir/raw/files/$year/irr/
#done

#to roll back
# rm -rf /tmp/brazil/clean/divided
# rm -rf /tmp/brazil/raw
# mkdir -p ${mydir}/clean/divided/
# mkdir -p $out_dir

# to get the original files to files/
# cp -r /ai/home/acelebi/folca/data /tmp/brazil/
# cd ${mydir}/data/
# mkdir ${mydir}/files/
# find . -name '*.html' -size +1024c -printf '%P\0' | pax -0rws ':/:_:g' ${mydir}/files/
