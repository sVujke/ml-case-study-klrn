
class Paths: 
    dataset = '/home/klarna-solution/data/dataset.csv'
    output_predictions = '/home/klarna-solution/data/output_predictions.csv'
    model_path = '/home/klarna-solution/data/model.pkl'
    encoder_path = '/home/klarna-solution/data/target_encoder.pkl'


NUMERICAL_FEATURES = [
    'time_hours',
    'age',
    'num_unpaid_bills',
    'max_paid_inv_0_24m',
    'sum_paid_inv_0_12m', 
    'max_paid_inv_0_12m',
    'num_active_inv',
    'sum_capital_paid_account_0_12m',
    'account_amount_added_12_24m',
    'num_active_div_by_paid_inv_0_12m',
    'sum_capital_paid_account_12_24m',
    'account_worst_status_0_3m',
    'account_worst_status_6_12m',
    'account_status',
    'account_worst_status_3_6m',
    'status_3rd_last_archived_0_24m',
    'num_arch_ok_0_12m', 
    'status_last_archived_0_24m',
    'num_arch_ok_12_24m', 
    'account_days_in_rem_12_24m',
    'status_2nd_last_archived_0_24m',
    'num_arch_dc_12_24m',
    'status_max_archived_0_6_months', 
    'account_worst_status_12_24m',
    'num_arch_rem_0_12m',
    'num_arch_dc_0_12m',
    'status_max_archived_0_24_months',
    'status_max_archived_0_12_months', 
    'worst_status_active_inv',
    'account_days_in_term_12_24m',
    ]

FEATURES_TO_ENCODE = [
    'merchant_group',
    'merchant_category',
    'name_in_email'
    ]

CATEGORICAL_FEATURES = [
    'merchant_category',
    'merchant_group',
    'name_in_email',
    ]

DROPPED_FEATURES = [
    'account_days_in_dc_12_24m',
    'account_days_in_rem_12_24m',
    'account_worst_status_12_24m',
    'avg_payment_span_0_12m',
    'avg_payment_span_0_3m',
    'has_paid',
    'num_arch_written_off_0_12m',
    'num_arch_written_off_12_24m',
    'recovery_debt',
    'status_3rd_last_archived_0_24m',
    'account_incoming_debt_vs_paid_0_24m',
    'default',
    'uuid'
]

MODEL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES 
FULL_FEATURE_SET = MODEL_FEATURES + DROPPED_FEATURES