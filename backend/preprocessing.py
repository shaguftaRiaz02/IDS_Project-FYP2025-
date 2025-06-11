import pandas as pd

def check_and_fix_features(df: pd.DataFrame, model_features: list) -> pd.DataFrame:
    input_cols = list(df.columns)
    missing_cols = [col for col in model_features if col not in input_cols]
    extra_cols = [col for col in input_cols if col not in model_features]

    if missing_cols:
        print(f"Adding missing columns with zeros: {missing_cols}")
        for col in missing_cols:
            df[col] = 0

    if extra_cols:
        print(f"Dropping extra columns: {extra_cols}")
        df = df.drop(columns=extra_cols, errors='ignore')

    # Reorder columns to match model expectations
    df = df[model_features]

    return df

def preprocess_uploaded_csv(df: pd.DataFrame) -> pd.DataFrame:
    # Step 1: Strip leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Step 2: Rename inconsistent columns to match model expectations
    rename_dict = {
        'Dst Port': 'Destination Port',
        'Total Fwd Packet': 'Total Fwd Packets',
        'Total Bwd packets': 'Total Backward Packets',
        'Fwd Segment Size Avg': 'Avg Fwd Segment Size',
        'Bwd Segment Size Avg': 'Avg Bwd Segment Size',
        'FWD Init Win Bytes': 'Init_Win_bytes_forward',
        'Bwd Init Win Bytes': 'Init_Win_bytes_backward',
        'Fwd Act Data Pkts': 'act_data_pkt_fwd',
        'Fwd Seg Size Min': 'min_seg_size_forward',
        'Label': 'Attack Type',
        # Aliases if present (optional, not used in features)
        'Source Port': 'Src Port',
        'Source IP': 'Src IP',
        'Destination IP': 'Dst IP'
    }
    df = df.rename(columns=rename_dict)

    # Step 3: Drop unwanted identifier columns
    drop_cols = ['Flow ID', 'Src IP', 'Src Port', 'Dst IP', 'Protocol', 'Timestamp']
    df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')

    # Step 4: Define required model feature columns (must match model exactly)
    model_features = [
        'Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
        'Total Length of Fwd Packets', 'Total Length of Bwd Packets', 'Fwd Packet Length Max',
        'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std',
        'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean',
        'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean',
        'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean',
        'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean',
        'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Fwd URG Flags',
        'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s',
        'Min Packet Length', 'Max Packet Length', 'Packet Length Mean', 'Packet Length Std',
        'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count',
        'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count',
        'Down/Up Ratio', 'Average Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size',
        'Fwd Header Length.1', 'Subflow Fwd Packets', 'Subflow Fwd Bytes',
        'Subflow Bwd Packets', 'Subflow Bwd Bytes', 'Init_Win_bytes_forward',
        'Init_Win_bytes_backward', 'act_data_pkt_fwd', 'min_seg_size_forward', 'Active Mean',
        'Active Std', 'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min'
    ]

    # Step 5: Ensure final DataFrame has all and only model features in correct order
    df = check_and_fix_features(df, model_features)

    return df
