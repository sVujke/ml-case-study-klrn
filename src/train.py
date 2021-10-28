import pandas as pd
from config import Paths
import pickle
from config import FEATURES_TO_ENCODE, MODEL_FEATURES
from util import handle_missing_values, get_target_encoder, transform_features_with_encoder
from sklearn.model_selection import train_test_split 
from sklearn.metrics import roc_auc_score, recall_score, confusion_matrix, precision_score
from xgboost import XGBClassifier

XGB_PARAMS = {
    'max_depth': 2,
    'scale_pos_weight': 100
}


if __name__ == "__main__":

    df = pd.read_csv(Paths.dataset, sep=';')

    df_final_output = df[df['default'].isna()].reset_index()
    df = df[~df['uuid'].isin(df_final_output['uuid'])]

    df = handle_missing_values(df)

    X_train, X_test, y_train, y_test = train_test_split(df, df['default'], test_size=0.2, random_state=1)
    X_train_eval, X_val, y_train_eval, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1)


    encoder = get_target_encoder(X_train, 'default', FEATURES_TO_ENCODE)
    pickle.dump(encoder, open(Paths.encoder_path,'wb'))
    X_train = transform_features_with_encoder(X_train, encoder, FEATURES_TO_ENCODE)
    X_test = transform_features_with_encoder(X_test, encoder, FEATURES_TO_ENCODE)
    X_val = transform_features_with_encoder(X_val, encoder, FEATURES_TO_ENCODE)
    X_train_eval = transform_features_with_encoder(X_train_eval, encoder, FEATURES_TO_ENCODE)
    df_final_output = transform_features_with_encoder(df_final_output, encoder, FEATURES_TO_ENCODE)

    X_train, X_train_eval, X_val, X_test = X_train[MODEL_FEATURES], X_train_eval[MODEL_FEATURES], X_val[MODEL_FEATURES], X_test[MODEL_FEATURES]

    # we want to get some evaluation metrics
    model = XGBClassifier()
    model.set_params(**XGB_PARAMS)
    eval_set = [(X_val, y_val)]
    model.fit(X_train_eval, y_train_eval, eval_metric='auc', eval_set=eval_set, verbose=False)

    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)

    print('Confusion Matrix: ')
    print(confusion_matrix(y_test, y_pred))
    print('Recall:', recall_score(y_test, y_pred))
    print('Precision:', precision_score(y_test, y_pred))
    print('ROC-AUC: ', roc_auc_score(y_test, y_pred))

    # there should be some alerting in case of metric drop compared to historical values,
    # but that is more for the real world than for a home assignment

    # Now training with more data (using X_TRAIN not X_TRAIN_EVAL)
    model = XGBClassifier()
    model.set_params(**XGB_PARAMS)
    eval_set = [(X_test, y_test)]
    model.fit(X_train, y_train, eval_metric="auc", eval_set=eval_set, verbose=False)

    final_prob = model.predict_proba(df_final_output[MODEL_FEATURES])
    df_probabilities = pd.DataFrame(final_prob, columns=['npd', 'pd'])
    df_final_output = df_final_output.join(df_probabilities[['pd']])
    df_final_output[['uuid', 'pd']].to_csv(Paths.output_predictions, index=False)

    confident_default_pred = len(df_final_output[df_final_output['pd']>0.7]) / len(df_final_output) * 100
    # also useful for alerts (in case of dramatic changes)
    print(f'{confident_default_pred}% of predicted default (with high confidence)')


    pickle.dump(model, open(Paths.model_path,'wb'))