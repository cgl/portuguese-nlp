import graphlab as gl
import argparse,codecs

# result_dataset = gl.load_sframe("graphlab/my_dataset_test") # "my_dataset
def save_positive_results_with_event_type_and_date(result_dataset):
        csvfile = "classification/data/extraction_fields.csv"
        with codecs.open(csvfile,"r",encoding="utf8") as infile:
            lines = infile.readlines()
        #types = set()
        #for line in lines[5:]:
        #        types.add(line.split(",")[2].strip().lower())

        types = {u'armed struggle' : 0,
                 u'invasion' : 1,
                 u'occupation': 2,
                 u'protest' : 3,
                 u'rebellion': 4,
                 u'strike' :5}

        sf = gl.load_sframe("graphlab/my_training_dataset")
        #for ind in range(0,521):
        #    sf['filenames'][ind]

        labels = [0]*521

        for line in lines[5:]:
            fields = line.split(",")
            labels[int(fields[0].strip())] = types[fields[2].strip().lower()]

        #for ind in range(0,521):
        #    labels[int(sf['filenames'][ind][1:-4]))]

        #rel_folder="classification/data/v5/class_rel/"
        ef = sf.filter_by([1], "rel") # add_arguments(None,rel_folder,1,vec_model)

        ef['event_type'] = ef['filenames'].apply(lambda p: labels[int(p[1:-4])])

        # evnt type classifier
        event_type_cls = gl.classifier.create(ef, target="event_type",features=['vectors','1gram features'])

        pos_results = result_dataset.filter_by([1], "rel")

        pos_res_res = event_type_cls.classify(pos_results)

        pos_results.add_column(pos_res_res.select_column("class"),"event_type")
        pos_results.add_column(pos_res_res.select_column("probability"),"et_probability")

        pos_results.filter_by([5],"event_type")


        pos_results['date'] = pos_results['filenames'].apply(lambda x: x[:-5].split('_'))
        pos_results = pos_results.unpack('date')
        pos_results.rename({'date.0':'year', 'date.1':'month','date.2':'day', 'date.3':'index'})

        pos_results.save("graphlab/pos_results") ##_2005")

        #month_count = pos_results.groupby(['year','month'], gl.aggregate.COUNT)

def by_year_month(pos_results):
    sframe = gl.SFrame()
    for year in pos_results['year'].unique():
        filtered = pos_results.filter_by([year], "year")
        filtered_count = filtered.groupby(['year','month'], gl.aggregate.COUNT)
        sframe = sframe.append(filtered_count)

def by_year_month_event_type(event_key):
    sframe = gl.SFrame()
    for year in pos_results['year'].unique():
        filtered = pos_results.filter_by([event_key],"event_type").filter_by([year], "year")
        filtered_count = filtered.groupby(['year','month'], {"count" : gl.aggregate.COUNT})
        sframe = sframe.append(filtered_count)
    return sframe

def bu_ne():
    year_month_all = by_year_month()

    sframe = gl.SFrame()
    for event_type,event_key in types.items():
        sframe = sframe.append(by_year_month_event_type(event_key))

def main():
    parser = argparse.ArgumentParser(description = "Classifies given dataset and saves the results.")
    parser.add_argument("--classified_dir", required = True, default=None ,type=str,
                        help = "Directory for dataset after classification ex: result_dataset")
    #parser.add_argument("--print", required = False ,action='store_true', dest='print_results',help = "")

    args = parser.parse_args()
    if args.classified_dir:
        result_dataset = gl.load_sframe(args.classified_dir)
        save_positive_results_with_event_type_and_date(result_dataset)



if __name__=='__main__':
    main()
