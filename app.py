# ==========================IMPORTS=========================
# flask rest api
from flask import Flask, render_template
from flask_restful import Api

# import Database not sure***


# swagger to document the api
from flask_swagger_ui import get_swaggerui_blueprint

# import endpoints
import endpoints


# ======================CONFIGURATIONS======================

# configure flask
app = Flask(__name__)
api = Api(app)

# configure swagger
SWAGGER_URL = '/api/doc'
API_URL = '/static/swagger.yml'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Arabic Dialect Identification API Documentation',
        'layout': 'BaseLayout'
    }
)

# add swagger to the app
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

# General API functions:
api.add_resource(endpoints.GeneralAPI, '/api/general')

# Twitter API functions:
api.add_resource(endpoints.twitterAPI,
                 '/api/twitter/<string:target_type>/<string:twitter_user>')

api.add_resource(endpoints.twitterAPIv2,
                 '/api/twitter/<string:target_type>/<string:twitter_user>/<string:target_dialect>')

# Overrides swagger img
api.add_resource(endpoints.image32, '/api/doc/favicon-32x32.png')

# Overrides swagger img
api.add_resource(endpoints.image16, '/api/doc/favicon-16x16.png')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':

    print(' * app is starting...')
    # Start the server
    app.run(debug=True)
    
