from flask_restful import Resource, reqparse
from flask import send_file, request, jsonify
# json methods
import json

# to load model and the transformer
import joblib

# load the methods
import twitter_methods as tw
import general_methods as gm


# ======================CONFIGURATIONS======================

# load the model and transformer into memory
model = joblib.load('models/MultinomialNB(CountVectorizer).joblib')
transformer = joblib.load('models/transformerMultinomialNB(CountVectorizer).joblib')

# configure reqparse
requst_args = reqparse.RequestParser()
requst_args.add_argument('request', action='append')


# ======================FUNCTIONS======================

class GeneralAPI(Resource):
    def post(self):
        try:
            # try to parse request body
            json_data = request.get_json(force=True)
            json_list = jsonify(json_data).get_json()

            # get predictions
            output = gm.json_to_json(json_list, model, transformer)
        except NameError:
            print(NameError)
            return 'error: json file is not accepted',400
        # no errors return the labeled data
        return output


class twitterAPI(Resource):
    def get(self, target_type, twitter_user):

        # Try to parse our json file
        tw_list = tw.get_by_type(target_type, twitter_user)
        output = gm.list_to_json(tw_list, model, transformer)

        # return output
        # no errors return the labeled data
        return output


class twitterAPIv2(Resource):
    def get(self, target_type, twitter_user, target_dialect):

        # Try to parse our json file
        tw_list = tw.get_by_type(target_type, twitter_user)
        output = gm.list_to_json(
            tw_list, model, transformer, dialect=target_dialect)
        # return output
        # no errors return the labeled data
        return output


class image32(Resource):
    def get(self):
        return send_file('static/img/32x32_ADC_icon.png', mimetype='image/gif')

class image16(Resource):
    def get(self):
        return send_file('static/img/16x16_ADC_icon.png', mimetype='image/gif')


print(' * endpoints is loaded')
