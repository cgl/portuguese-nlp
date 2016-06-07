import graphlab as gl

def test_classifier(cls1,vec_model):
    test_folder = "/home/cagil/brazil/all_files_parsed/" # "/tmp/temp/"
    dataset = add_arguments(None,test_folder,None,vec_model)
    result171_dataset = cls1.classify(dataset)
    return dataset,result171_dataset

def print_url(dataset,result171_dataset,ind):
    print("http://mann.cmpe.boun.edu.tr/folha_data/%s %s" %(dataset['filenames'][ind].replace("_","/"),result171_dataset['probability'][ind]))

def print_positives_and_confidence(dataset,result171_dataset):
    for ind in range(0,result171_dataset.num_rows()):
        if result171_dataset['class'][ind]:
            print_url(dataset,result171_dataset,ind)

def count_positives_with_trigger(dataset,result171_dataset):
    triggers = add_trigger_feature()
    count = 0 ; positives=0
    for ind in range(0,result171_dataset.num_rows()):
        if result171_dataset["class"][ind]:
            positives+=1
            if check_trigger_exist(dataset['1gram features'][ind]):
                count+=1
                print("[%s] %s" %(ind,result171_dataset["probability"][ind]))
    print("%s/%s" %(count,positives))

def count_positives_with_mortes(result171_dataset): # dataset.shape[0]
    count = 0 ; positives=0
    for ind in range(0,dataset.num_rows()):
        if result171_dataset["class"][ind]:
            positives+=1
            if "mortes" in dataset['1gram features'][ind].keys():
                count+=1
                print("[%s] %s" %(ind,result171_dataset["probability"][ind]))
    print("%s/%s" %(count,positives))

def check_trigger_exist(grams):
    flag=False
    for token in grams.keys():
        if token.strip().decode('latin1') in triggers:
            print(token)
            flag=True
    return flag

def add_trigger_feature():
    filename = "classification/data/trigger_tokens.txt"
    with codecs.open(filename, "r", encoding="utf8") as infile:
        trigger_str = infile.read()
    triggers = list(set(trigger_str.split(",")))
    return triggers

def performance(sf):
    train_set, test_set = sf.random_split(0.8, seed=5)
    cls1 = gl.classifier.create(train_set, target="rel",features=['vectors','1gram features'])
    results = cls1.evaluate(test_set)
    print(results)
    """
    train_set = sf
    train_set, test_set = sf.random_split(0.8, seed=5)
    clsv = gl.classifier.create(train_set, target="rel",features=['vectors'])
    cls = gl.classifier.create(train_set, target="rel",features=['1gram features'])
    cls1 = gl.classifier.create(train_set, target="rel",features=['vectors','1gram features'])
    cls2 = gl.classifier.create(train_set, target="rel",features=['vectors','1gram features','2gram features'])

    linear_model = gl.linear_regression.create(train_set, target='rel',features=['vectors'])
    linear_model.evaluate(test_set)

    for mdl in [clsv,cls,cls1,cls2]:
        mdl.evaluate(test_set)
    """

def main():
    cls = gl.load_model("my_classifier")
    dataset,result171_dataset = test_classifier(cls,vec_model)
    print_positives_and_confidence(dataset,result171_dataset)

if __name__=='__main__':
    main()
