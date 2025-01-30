import json

def remove_empty_objects(data):
    """
    Recursively removes empty dictionaries from a JSON structure.

    :param data: The JSON data as a Python dictionary
    :return: Cleaned JSON data with empty objects removed
    """
    if isinstance(data, dict):
        return {k: remove_empty_objects(v) for k, v in data.items() if v != {}}
    elif isinstance(data, list):
        return [remove_empty_objects(item) for item in data if item != {}]
    else:
        return data

def addQuestion(question, file_path, type_of_question="text", options=None):
    flag_valid = False
    with open(file_path, 'r+') as f:
        data = json.load(f)
        if type_of_question == "text":
            flag_valid = True
            a = {
                'id':  getUniqueIdForNewQuestion(file_path), 
                'question': question, 
                'type': type_of_question # multiple_choice or text
                }

        if type_of_question == "multiple_choice" and options != None: 
            flag_valid = True
            a = {
                'id': len(data['questionnaire']['questions'])+int(1), 
                'question': question, 
                'type': type_of_question, # multiple_choice or text
                'options': options
                }
        if flag_valid == False:
            print("something went wrong, bad arguments")
            return 0

        # length = len(data['questionnaire']['questions'])
        data['questionnaire']['questions'].append(a)
        # <--- add `id` value.
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part

def deleteQuestion(questionId,file_path):
    flag_valid = False
    with open(file_path, 'r+') as f:
        data = json.load(f)
        data = remove_empty_objects(data)
        for item in data['questionnaire']['questions']:
            # print(item)
            
            if(item['id']) == questionId:
                print(True)
                flag_valid = True    
                item.clear()
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(remove_empty_objects(data), f, indent=4)
        f.truncate()     # remove remaining part
    if flag_valid == True:
        return 1
    return 0

def getLargestId(file_path):
    flag_valid = False
    data=readJson(file_path)
    number = 0
    for item in data['questionnaire']['questions']:
        if(item['id'] > number):
            # print(item['id'] > number)
            number = item['id'] 
            flag_valid = True
    if flag_valid == True:
        return number
    return 0

def getUniqueIdForNewQuestion(file_path):
    return getLargestId(file_path) + 1

def changeTitle(newTitle,file_path):
    with open(file_path, 'r+') as f:
        data = json.load(f)
        data['questionnaire']['title']=newTitle
        # <--- add `id` value.
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part

def changeDescription(newDescription,file_path):
    with open(file_path, 'r+') as f:
        data = json.load(f)
        data['questionnaire']['description']=newDescription
        # <--- add `id` value.
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part
    
def readJson(file_path):
    with open(file_path, 'r+') as f:
        return json.load(f)

def validateAndReadJson(file_path):
    try:
        data = readJson(file_path)
    except:
        print("error reading the file")
        return -1
    try:
        if(data['questionnaire'] != None): # has main body
            pass
    except:
        print("error reading the file")
        return -1

    try:
        if(data['questionnaire']['title'] != None): # has in body the title
            pass
    except:
        print("error reading the file - title missing")
        return -1

    try:
        if(data['questionnaire']['description'] != None): # has in body the fr
            pass
    except:
        print("error reading the file - description missing")
        return -1
    try:
        if(data['questionnaire']['questions'] != None): # has in body the questions
            pass
    except:
        print("error reading the file")
        return -1
    try:
        for item in data['questionnaire']['questions']:
            temp = str(item['question']) 
            if(item['type']) == "multiple_choice":
                temp = str(item['type'] )
                for option in item['options']:
                    temp =str(option) 
    except:
        print("if something went wrong here check questions sintax")
        return -1
    return data

def getMetadataTitle(file_path):
    data = validateAndReadJson(file_path)
    return data['questionnaire']['title'] 
     
    
def getMetadataDescription(file_path):
    data = validateAndReadJson(file_path)
    return data['questionnaire']['description']

if __name__ == "__main__":
    print("Use this as an import or edit the script")
    

