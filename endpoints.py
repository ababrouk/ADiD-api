from flask_restful import Resource, reqparse
from flask import send_file
# json methods
import json

# to load model and the transformer
import joblib

# load the methods
import twitter_methods as tw
import general_methods as gm


# ======================CONFIGURATIONS======================

# load the model and transformer into memory
model = joblib.load('models/completed_multinomialnb.joblib')
transformer = joblib.load('models/transformer_multinomialnb.joblib')

# configure reqparse
requst_args = reqparse.RequestParser()
requst_args.add_argument('request', action='append')


# ======================FUNCTIONS======================

class GeneralAPI(Resource):
    def post(self):
        args = requst_args.parse_args()

        try:
            # Try to parse our json file
            json_list = json.loads(
                str(args).replace('"', '').replace("'", '"'))
            # get predictions
            output = gm.json_to_json(json_list, model, transformer)
        except:
            return 'error: json file is not accepted',400

        # no errors return the labeled data
        return output


class twitterAPI(Resource):
    def get(self, target_type, twitter_user):

        # check if the database already have the result
        #lazy_data = gm.lazy_check(twitter_user, target_type == 'by_user')

        #

        # Try to parse our json file
        tw_list = tw.get_by_type(target_type, twitter_user)
        output = gm.list_to_json(tw_list, model, transformer)

        # return output
        # no errors return the labeled data
        return output


class twitterAPIv2(Resource):
    def get(self, target_type, twitter_user, target_dialect):

        # check if the database already have the result

            # return the lazy data from the database

        # Try to parse our json file
        tw_list = tw.get_by_type(target_type, twitter_user)
        output = gm.list_to_json(
            tw_list, model, transformer, dialect=target_dialect)
        # return output
        # no errors return the labeled data
        return output


class image(Resource):
    def get(self):
        return send_file('static/img/favicon-32x32.png', mimetype='image/gif')


print(' * endpoints is loaded')
