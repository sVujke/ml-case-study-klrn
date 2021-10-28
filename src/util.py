from category_encoders import TargetEncoder
import pandas as pd 

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # with zero to anotate missing category
    df['account_status']  = df['account_status'].fillna(0)

    # replacing with 1 because the split by target variable looks very similar to the one from cat=1 
    df['account_worst_status_0_3m']  = df['account_worst_status_0_3m'].fillna(1)
    df['account_worst_status_3_6m']  = df['account_worst_status_3_6m'].fillna(1)
    df['account_worst_status_6_12m']  = df['account_worst_status_6_12m'].fillna(1)
    df['account_worst_status_12_24m']  = df['account_worst_status_12_24m'].fillna(1)

    # replacing with 1 because the split by target variable looks very similar to the one from cat=1 
    df['worst_status_active_inv'] = df['worst_status_active_inv'].fillna(1)

    # with zero because the distribution has a long-tail (most values are close to 0)
    df['account_days_in_dc_12_24m']  = df['account_days_in_dc_12_24m'].fillna(0)
    df['account_days_in_rem_12_24m']  = df['account_days_in_rem_12_24m'].fillna(0)
    df['account_days_in_term_12_24m']  = df['account_days_in_term_12_24m'].fillna(0)

    # replacing with 0 because cat = 1 and 2 result in default=0 most of the time
    # unlike users with NaN values
    df['num_arch_written_off_0_12m']  = df['num_arch_written_off_0_12m'].fillna(0)
    df['num_arch_written_off_12_24m']  = df['num_arch_written_off_12_24m'].fillna(0)

    df['num_active_div_by_paid_inv_0_12m']  = df['num_active_div_by_paid_inv_0_12m'].fillna(0)

    # using median because the distribution is slightly skewed to the right
    df['avg_payment_span_0_3m'] = df['avg_payment_span_0_3m'].median()
    df['avg_payment_span_0_12m'] = df['avg_payment_span_0_12m'].median()

    # no particular signal and to many values to replace
    df = df.drop(['account_incoming_debt_vs_paid_0_24m'], axis=1)

    return df


def get_target_encoder(X_train: pd.DataFrame, target_feature: str, features_to_encode: list) -> object:
    encoder = TargetEncoder()
    encoder = encoder.fit(X_train[features_to_encode], X_train[target_feature])
    return encoder

def transform_features_with_encoder(df: pd.DataFrame, encoder: object, features_to_encode: list) -> pd.DataFrame:
    df[features_to_encode] = encoder.transform(df[features_to_encode])
    return df