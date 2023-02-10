from collections import Counter
import json

# =============================================#
#  This method will take json and return json
# =============================================#


def json_to_json(json_list, model, transformer, dialect="all"):
    # Create return var
    output = {
        'info': [],
        'result': []
    }
    info = []

    # Loop for every text given from the user
    for data in json_list['request']:

        text = data_prep(data['text'])
        to_predict = transformer.transform([text]).toarray()
        predicted = model.predict(to_predict)[0]

        # if dialect == "all" means return all
        # if dialect == x means return only x dialect
        if dialect.capitalize == "all".capitalize:

            output['result'].append(
                {
                    'id': data['id'],
                    'text': text,
                    'label': predicted
                }
            )
            # add to info
            info.append(predicted)
        elif dialect.capitalize == predicted.capitalize:
            output['result'].append(
                {
                    'id': data['id'],
                    'text': text,
                    'label': predicted
                }
            )
            # add to info
            info.append(predicted)
    temp = {
        'info': []
    }

    # if info is empty then no dialects are returned
    if (not info):
        return 'No data found for this target', 400

    # transform info into key and value
    k = list(Counter(info).keys())
    v = list(Counter(info).values())

    # use the key and value to create dictionary of calculated values for each key
    temp = {k[i]: round((v[i]/len(info))*100, 3) for i in range(len(k))}

    # sort the dictionary by the value
    temp = dict(sorted(temp.items(), key=lambda x: x[1], reverse=True))

    # change output info to the dictionary created above
    output['info'] = temp

    return g_string_to_json(output)

# =============================================#
#  This method will take list and return json
# =============================================#


def list_to_json(data_list, model, transformer, dialect="all"):
    # Create return var
    output = {
        'info': [],
        'result': []
    }
    info = []

    # Loop for every text given from the user
    for data in data_list:

        # print(data)
        to_predict = transformer.transform([data[1]]).toarray()

        # to predict the dialect
        predicted = model.predict(to_predict)[0]

        # if dialect == "all" means return all
        # if dialect == x means return only x dialect
        if dialect.capitalize() == "all".capitalize():
            output['result'].append(
                {
                    'id': data[0],
                    'text': data[1],
                    'label': predicted
                }
            )
            # add to info
            info.append(predicted)

        elif dialect.capitalize() == predicted.capitalize():
            output['result'].append(
                {
                    'id': data[0],
                    'text': data[1],
                    'label': predicted
                }
            )
            # add to info
            info.append(predicted)

    # if info is empty then no dialects are returned
    if (not info):
        return 'No data found for this target', 400

    # to calculate the result for each dialect
    dialect_info = dialect_calculator(info)
    output['info'] = dialect_info

    return g_string_to_json(output)

# ============================================GENERAL METHODS============================================


def g_string_to_json(string_to_json):
    return json.loads(str(string_to_json).replace("'", '"'))


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


def dialect_calculator(info):
    # transform info into key and value
    k = list(Counter(info).keys())
    v = list(Counter(info).values())

    # use the key and value to create dictionary of calculated values for each key
    output = {k[i]: round((v[i]/len(info))*100, 3) for i in range(len(k))}

    # sort the dictionary by the value
    output = dict(sorted(output.items(), key=lambda x: x[1], reverse=True))

    # change output info to the dictionary created above
    return output

