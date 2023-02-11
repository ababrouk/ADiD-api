from collections import Counter
import json

# =============================================#
#  This method will take json and return json
# =============================================#


def json_to_json(json_list, model, transformer, dialect="all"):
    # Create return var
    output = {
        'distribution': [],
        'result': []
    }
    distribution = []

    # Loop for every text given from the user
    for data in json_list['request']:

        multi_predicted, text = predict(data, model, transformer)
        predicted = list(multi_predicted.keys())[0]

        # if dialect == "all" means return all
        # if dialect == x means return only x dialect
        if dialect.capitalize == "all".capitalize:

            output['result'].append(
                {
                    'id': data['id'],
                    'text': text,
                    'label': predicted,
                    'probability': multi_predicted
                }
            )
            # add to distribution
            distribution.append(predicted)
        elif dialect.capitalize == predicted.capitalize:
            output['result'].append(
                {
                    'id': data['id'],
                    'text': text,
                    'label': predicted,
                    'probability': multi_predicted
                }
            )
            # add to info
            distribution.append(predicted)
    temp = {
        'distribution': []
    }

    # if info is empty then no dialects are returned
    if (not distribution):
        return 'No data found for this target', 400

    # transform info into key and value
    k = list(Counter(distribution).keys())
    v = list(Counter(distribution).values())

    # use the key and value to create dictionary of calculated values for each key
    temp = {k[i]: round((v[i]/len(distribution))*100, 3) for i in range(len(k))}

    # sort the dictionary by the value
    temp = dict(sorted(temp.items(), key=lambda x: x[1], reverse=True))

    # change output info to the dictionary created above
    output['distribution'] = temp

    return g_string_to_json(output)

# =============================================#
#  This method will take list and return json
# =============================================#


def list_to_json(data_list, model, transformer, dialect="all"):
    # Create return var
    output = {
        'distribution': [],
        'result': []
    }
    distribution = []

    # Loop for every text given from the user
    for data in data_list:

        multi_predicted, text = predict(data, model, transformer, True)
        predicted = list(multi_predicted.keys())[0]

        # if dialect == "all" means return all
        # if dialect == x means return only x dialect
        if dialect.capitalize() == "all".capitalize():
            output['result'].append(
                {
                    'id': data[0],
                    'text': data[1],
                    'label': predicted,
                    'probability': multi_predicted
                }
            )
            # add to info
            distribution.append(predicted)

        elif dialect.capitalize() == predicted.capitalize():
            output['result'].append(
                {
                    'id': data[0],
                    'text': data[1],
                    'label': predicted,
                    'probability': multi_predicted
                }
            )
            # add to info
            distribution.append(predicted)

    # if info is empty then no dialects are returned
    if (not distribution):
        return 'No data found for this target', 400

    # to calculate the result for each dialect
    dialect_info = dialect_calculator(distribution)
    output['distribution'] = dialect_info

    return g_string_to_json(output)

# ============================================GENERAL METHODS============================================


def g_string_to_json(string_to_json):
    return json.loads(json.dumps(string_to_json, ensure_ascii=True))


def data_prep(text):
    result = ''
    last_char = ''
    count = 0
    for c in text:
        # remove non-arabic characters and Hrakat
        if not (ord(c) >= ord('\u0621') and ord(c) <= ord('\u064A') or c.isspace()):
            result += ' '
            continue

        # remove repetition
        count += 1
        if (last_char == c and count > 1):
            continue
        elif last_char != c:
            last_char = c
            count = 0

        # remove newlines and add it to the result
        result += c.replace("\n", ' ')

    # remove extra spaces
    return ' '.join(result.split())


print(' * general_methods is loaded')


def dialect_calculator(distribution):
    # transform info into key and value
    k = list(Counter(distribution).keys())
    v = list(Counter(distribution).values())

    # use the key and value to create dictionary of calculated values for each key
    output = {k[i]: round((v[i]/len(distribution))*100, 3) for i in range(len(k))}

    # sort the dictionary by the value
    output = dict(sorted(output.items(), key=lambda x: x[1], reverse=True))

    # change output info to the dictionary created above
    return output


def predict(data, model, transformer, clean_input=False):

    text = data[1] if clean_input else data_prep(data['text'])
    to_predict = transformer.transform([text]).toarray()

    # to predict the dialect with probability
    predicted = model.predict_proba(to_predict)[0]

    v = predicted
    k = model.classes_
    
    return dict(sorted({k[i]: round(v[i],2) for i in range(len(k))}.items(), key=lambda x:x[1], reverse=True)), text