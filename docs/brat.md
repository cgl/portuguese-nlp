### Play with it

    import extraction.extractannotationlists as ext
    path = "/Users/cagil/Downloads/brat-v1.3_Crunchy_Frog/data/Duru/full_main/"
    annotations = ext.extract_annotations(path,verbose=False)
    all_entities = ext.extract_entities(annotations)



    doc_name='4'
    ann = annotations[doc_name]
    entities = list(ann.get_entities())
    for entity in entities:
        print("%s\t%s\t%s\t%s\t%s" %(doc_name,entity.id, entity.text, entity.type, entity.attribute.value if entity.attribute else ""))
      
      4	T2	Metalúrgicos  	            Group	NOM
      4	T3	CUT	                       NonGov 	NAM
      4	T4	Sindicato dos Metalúrgicos	NonGov	NAM
      4	T5	São José dos Campos	     County-or-District	NAM
      4	T6	CUT (Central Única dos Trabalhadores	NonGov	NAM
      4	T7	hoje	                    Time
      4	T9	Sindicato dos Metalúrgicos de São José dos Campos e a CUT (Central Única dos Trabalhadores	Group	NOM
      4	T10	São José	                 County-or-District	NAM
      4	T11	em frente a GM	           Building-or-Grounds	NOM


    events = list(ann.get_events())
    for event in events:
       print("%s\t%s\t%s\t%s\t%s" %(doc_name,event.id,ann.get_ann_by_id(event.trigger).type,ann.get_ann_by_id(event.trigger).text,event))


    entity_dict = {entity.id: entity for entity in entities}
    for key in entity_dict.keys():
        print("%s\t%s" %(key,entity_dict[key].text))
     ....:
     T9	Sindicato dos Metalúrgicos de São José dos Campos e a CUT (Central Única dos Trabalhadores
     T6	CUT (Central Única dos Trabalhadores
     T7	hoje
     T4	Sindicato dos Metalúrgicos
     T5	São José dos Campos
     T2	Metalúrgicos
     T3	CUT
     T10	São José
     T11	em frente a GM


    relations = list(ann.get_relations())
    for relation in relations:
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s" %(doc_name,relation.id, relation.type,relation.arg1, entity_dict[relation.arg1].text, relation.arg2, entity_dict[relation.arg2].text))
     ....: 
        4	R1	Membership	T2	Metalúrgicos			    T3		CUT
        4	R2	Loc-Origin	T4	Sindicato dos Metalúrgicos	T5		São José dos Campos
        4	R3	Geographical	T11	em frente a GM			T10		São José



    triggers = list(ann.get_triggers())
    for trigger in triggers:
       print(trigger.id,trigger.get_text(),trigger.type)


    import extraction.event_search as search
    parsed_lines = search.extract_event("extraction/data/parsed/%s.txt" %doc_name,trigger.text)
  

    from nltk.tree import ParentedTree
    ptree = ParentedTree.fromstring(parsed_lines[0])
    leaf_values = ptree.leaves()
    if trigger.text in leaf_values:
    leaf_index = leaf_values.index(trigger.text)
    tree_location = ptree.leaf_treeposition(leaf_index)
    print tree_location
    print ptree[tree_location]

    doc_name='8'
    ann = annotations[doc_name]
    entities = list(ann.get_entities())
    events = list(ann.get_events())
    entity_dict = {entity.id: entity for entity in entities}
    relations = list(ann.get_relations())
    event=events[0]
    trigger = ann.get_ann_by_id(event.trigger)
    arg = ann.get_ann_by_id(event.args[1][1])
    parsed_lines = search.extract_event("extraction/data/parsed/%s.txt" %doc_name,trigger.text)
    ptree = ParentedTree.fromstring(parsed_lines[0])
    leaf_values = ptree.leaves()
    
