import graphlab as gl
import argparse,codecs

types = {u'armed struggle' : 0,
             u'invasion' : 1,
             u'occupation': 2,
             u'protest' : 3,
             u'rebellion': 4,
             u'strike' :5}
# result_dataset = gl.load_sframe("graphlab/my_dataset_test") # "my_dataset
def save_positive_results_with_event_type_and_date(result_dataset):
    csvfile = "classification/data/extraction_fields.tsv"
    with codecs.open(csvfile,"r",encoding="utf8") as infile:
        lines = infile.readlines()
    #types = set()
    #for line in lines[5:]:
    #        types.add(line.split(",")[2].strip().lower())

    sf = gl.load_sframe("graphlab/my_training_dataset")

    # lines[-1].split("\t") = [u'620', u'E1', u'protest', u'', u'', u'T2', u'NGO' ...]
    size = int(lines[-1].split("\t")[0]) + 1 # latest news index 620 starts from 0 do 620+1
    labels = [0]*size

    for line in lines:
        fields = line.split("\t")
        key = fields[2].strip().lower()
        if key:
            ind = int(fields[0].strip())
            labels[ind] = types[key]

    #rel_folder="classification/data/v6/class_rel/"
    ef = sf.filter_by([1], "rel") # add_arguments(None,rel_folder,1,vec_model)

    ef['event_type'] = ef['filenames'].apply(lambda p: labels[int(p[1:5])])

    # evnt type classifier
    event_type_cls = gl.classifier.create(ef, target="event_type",features=['vectors','1gram features'])

    pos_results = result_dataset.filter_by([1], "class")

    pos_res_res = event_type_cls.classify(pos_results)

    pos_results.add_column(pos_res_res.select_column("class"),"event_type")
    pos_results.add_column(pos_res_res.select_column("probability"),"et_probability")

    pos_results.filter_by([5],"event_type")


    pos_results['date'] = pos_results['filenames'].apply(lambda x: x[:-5].split('_'))
    pos_results = pos_results.unpack('date')
    pos_results.rename({'date.0':'year', 'date.1':'month','date.2':'day', 'date.3':'index'})
    pos_results['year'] = pos_results['year'].apply(lambda year_str : int(year_str))
    pos_results['month'] = pos_results['month'].apply(lambda m_str : int(m_str))
    pos_results.save("graphlab/pos_results") ##_2005")
    #month_count = pos_results.groupby(['year','month'], gl.aggregate.COUNT)


# given an event_key counts the number of events per month
def by_year_month_event_type(pos_results,event_key):
    sframe = gl.SFrame()
    for year in pos_results['year'].unique():
        filtered = pos_results.filter_by([event_key],"event_type").filter_by([year], "year")
        #filtered_count = filtered.groupby(['year','month'], {"count" : gl.aggregate.COUNT})
        filtered_count = filtered.groupby( key_columns= ['year','month','event_type'], operations = {"count" : gl.aggregate.COUNT('month')})
        sframe = sframe.append(filtered_count.sort('month'))
    return sframe

def count_monthly(pos_results):
    """
    sframe = gl.SFrame()
    for event_type,event_key in types.items():
        sframe = sframe.append(by_year_month_event_type(pos_results,event_key))
    """
    sframe = pos_results.groupby( key_columns= ['year','month','event_type'], operations = {"count" : gl.aggregate.COUNT('month')}).sort('month')
    return sframe

def get_count_dict(pos_results):
    sframe = count_monthly(pos_results)
    out = sframe.pack_columns(columns=['year','month','event_type','count'],dtype=dict)
    my_dict = {}
    for year in pos_results['year'].unique():
        my_dict[int(year)] = {}
        for month in range(1,13):
            my_dict[int(year)][month] = [0]*6
    for line in out:
        year = line['X1']['year']
        month = line['X1']['month']
        event_type = line['X1']['event_type']
        count = line['X1']['count']
        my_dict[year][int(month)][int(event_type)] = count
    return my_dict

def get_norm_dict(pos_results,events = [0,1,2,3,4,5]):
    sframe = count_monthly(pos_results)
    count_dict = {}
    for event in events:
        count_dict[event] = {}
    for event_key in events:
        filtered = pos_results.filter_by([event_key],"event_type")
        sframe = filtered.groupby( key_columns= ['year','event_type'], operations = {"count" : gl.aggregate.COUNT('year')}).sort(['year'])
        out = sframe.pack_columns(columns=['year','count'],dtype=dict)
        for line in out:
            event = line['event_type']
            year = line['X2']['year']
            count = line['X2']['count']
            count_dict[event][year] = float(count)
        total = pos_results.groupby( key_columns= ['year'], operations = {"count" : gl.aggregate.COUNT('year')}).sort(['year'])
        count_dict['total'] = {}
        for line in total:
            count_dict['total'][line['year']] = float(line['count'])
    return count_dict


def main():
    parser = argparse.ArgumentParser(description = "Classifies given dataset and saves the results.")
    parser.add_argument("--classified_dir", required = False, default=None ,type=str,
                        help = "Directory for dataset after classification ex: result_dataset")
    parser.add_argument("--print", required = False ,action='store_true',dest="print_results",help = "")
    parser.add_argument("--pprint", required = False , type=int ,dest="print_pretty",help = "")

    args = parser.parse_args()
    if args.classified_dir:
        result_dataset = gl.load_sframe(args.classified_dir)
        save_positive_results_with_event_type_and_date(result_dataset)
    if args.print_results:
        pos_results = gl.load_sframe("graphlab/pos_results")
        sframe = count_monthly(pos_results)
        sframe.print_rows(sframe.shape[0])
    elif args.print_pretty == 0:
        pos_results = gl.load_sframe("graphlab/pos_results")
        my_dict = get_count_dict(pos_results)
        print("\n".join(["%d %d %s" %(year,month, " ".join([str(l) for l in my_dict[year][month]]) ) for month in range(1,13) for year in pos_results['year'].unique()]))
    elif args.print_pretty == 1:
        pos_results = gl.load_sframe("graphlab/pos_results")
        my_dict = get_count_dict(pos_results)
        count_dict = get_norm_dict(pos_results,events = [3,5])
        print("\n".join(["%d-%d %.4f %.4f %.4f" %(year,month,
                                                  my_dict[year][month][3]/count_dict[3][year],
                                                  my_dict[year][month][5]/count_dict[5][year],
                                                  sum(my_dict[year][month])/count_dict['total'][year])
                         for month in range(1,13) for year in pos_results['year'].unique()]))

if __name__=='__main__':
    main()

"""
result_dataset = gl.load_sframe("graphlab/result_dataset")

filtered = pos_results.filter_by([3],"event_type")
filtered.groupby( key_columns= ['year','event_type'], operations = {"count" : gl.aggregate.COUNT('year')}).sort(['year'])

pos_results.groupby( key_columns= ['year'], operations = {"count" : gl.aggregate.COUNT('year')}).sort(['year'])
"""
