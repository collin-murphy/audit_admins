import sys
import json
import csv
import re
import os

##
# Convert to string keeping encoding in mind...
##
def to_string(s):
    try:
        return str(s)
    except:
        #Change the encoding type if needed
        return s.encode('utf-8')


##
# This function converts an item like 
# {
#   "item_1":"value_11",
#   "item_2":"value_12",
#   "item_3":"value_13",
#   "item_4":["sub_value_14", "sub_value_15"],
#   "item_5":{
#       "sub_item_1":"sub_item_value_11",
#       "sub_item_2":["sub_item_value_12", "sub_item_value_13"]
#   }
# }
# To
# {
#   "node_item_1":"value_11",
#   "node_item_2":"value_12",
#   "node_item_3":"value_13",
#   "node_item_4_0":"sub_value_14", 
#   "node_item_4_1":"sub_value_15",
#   "node_item_5_sub_item_1":"sub_item_value_11",
#   "node_item_5_sub_item_2_0":"sub_item_value_12",
#   "node_item_5_sub_item_2_0":"sub_item_value_13"
# }
##
def reduce_item(key, value):
    global reduced_item
    
    #Reduction Condition 1
    if type(value) is list:
        i=0
        for sub_item in value:
            reduce_item(key+'_'+to_string(i), sub_item)
            i=i+1

    #Reduction Condition 2
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key+'_'+to_string(sub_key), value[sub_key])
    
    #Base Condition
    else:
        reduced_item[to_string(key)] = to_string(value)

def sorted_nicely(l):
    """
    Sort the given iterable in the way that humans expect.
    https://stackoverflow.com/a/2669120
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(l, key=alphanum_key)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print ("\nUsage: python json_to_csv.py <json_in_file_path> <csv_out_file_path>\n")
    else:
        #Reading arguments
        node = sys.argv[1]
        directory = sys.argv[2]
        csv_file_path = sys.argv[3]
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        reps = 0
        for filename in os.listdir(directory):
            json_path = os.path.join(directory, filename)
            fp = open(json_path, 'r')
            json_value = fp.read()
            raw_data = json.loads(json_value)
            fp.close()
            
            try:
                data_to_be_processed = raw_data[node]
            except:
                data_to_be_processed = raw_data

            processed_data = []
            header = []
            j = 0
            for item in data_to_be_processed:
                reduced_item = {}
                reduce_item(node, item)

                header += reduced_item.keys()
                if j == 0:
                    pass
                else:
                    processed_data.append(reduced_item)
                j+=1
            processed_data = processed_data[:-1]
            header = list(set(header))
            header = sorted_nicely(header)
            
            
            with open(csv_file_path, 'a+') as f:
                writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for row in processed_data:
                    writer.writerow(row)
                reps += 1
        output = "Finished writing files from " + directory + " to \"" + csv_file_path + "\""
        print(output)
        #print ("Just completed writing to  file with %d columns" % len(header))
