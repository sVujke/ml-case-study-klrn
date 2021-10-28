import os
import time
import pickle

import pandas as pd
from waitress import serve
from flask import request, Flask

from config import Paths, FEATURES_TO_ENCODE, CATEGORICAL_FEATURES, NUMERICAL_FEATURES, MODEL_FEATURES, FULL_FEATURE_SET 
from util import handle_missing_values, transform_features_with_encoder

app = Flask(__name__)
RUN_PROD = os.environ.get('RUN_PROD')

with open(Paths.model_path, "rb") as input_file:
    MODEL = pickle.load(input_file)
with open(Paths.encoder_path, "rb") as input_file:
    ENCODER = pickle.load(input_file)

@app.route('/predict-default-probability', methods=['POST'])
def predict_default_probability():
    data = request.json
    passed_features = list(data.keys())

    if not set(MODEL_FEATURES).issubset(passed_features):
        missing_features = set(MODEL_FEATURES) - set(passed_features)
        return {'status': 'error', 'message': f"Missing feature(s): {','.join(missing_features)}"}

    if not set(passed_features).issubset(FULL_FEATURE_SET):
        unknown_features = set(passed_features) - set(FULL_FEATURE_SET)
        return {'status': 'error', 'message': f"Unknown feature(s): {', '.join(unknown_features)}"}

    features_with_incorrect_type = [feature for feature in CATEGORICAL_FEATURES if not isinstance(data[feature], str)]
    if features_with_incorrect_type:
        return {
            'status': 'error',
            'message': (f"""The following features should be passed as STRING:
                {', '.join(features_with_incorrect_type)}"""
            ),
        }

    features_with_incorrect_type = [
        feature for feature in NUMERICAL_FEATURES
        if not isinstance(data[feature], (int, float, type(None)))
    ]
    if features_with_incorrect_type:
        return {
            'status': 'error',
            'message': (f"""The following features should be specified as INT, FLOAT, NaN
                {', '.join(features_with_incorrect_type)}"""
            ),
        }

    input_data = pd.DataFrame([data])

    input_data = handle_missing_values(input_data)
    input_data = transform_features_with_encoder(input_data, ENCODER, FEATURES_TO_ENCODE)
    probabilities = MODEL.predict_proba(input_data[MODEL_FEATURES])
    probability_of_default = float(probabilities[0,1])


    return {'probability_of_default': probability_of_default, 'status': 'success'}


if __name__ == '__main__':
    if RUN_PROD:
        print('Running production server')
        serve(app, host='0.0.0.0', port=80)
    else:
        print('Running development server')
        app.run(host='0.0.0.0', port=5000, debug=True)