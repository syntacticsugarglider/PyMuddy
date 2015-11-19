def searchForItemInHashTable(itemName,dictionary):
	names=itemName.split(' ')
	if itemName=='' or itemName==' ':
		return None
	for name in names:
		name=name.lower()
		log('LOGGINGITEMS %s ALSO %s ' % (str([i.split(' ') for i in dictionary.keys()][0]),str(names)))
		if name in [i.split(' ') for i in dictionary.keys()][0]:
			items=[value for key, value in dictionary.items() if names[0] in key.lower()]
			if len(items)==1:
				item=items[0]
				if len(item)==1:
					final_item=item[0]
					return ('single',final_item)
				else:
					return ('multi',item)
			else:
				concat_list=[item for sublist in items for item in sublist]
				return('multi',concat_list)
	return None
