# import joblib
# import numpy as np
# import pandas as pd
# import os

# class Predictor:
#     def __init__(self, model_path, scaler_path, encoder_path, pca_path, debug=False):
#         self.debug = debug
#         try:
#             self.model = joblib.load(model_path)
#             self.scaler = joblib.load(scaler_path)
#             self.encoder = joblib.load(encoder_path)
#             self.pca = joblib.load(pca_path)
#         except Exception as e:
#             raise RuntimeError(f"Failed to load model components: {e}")

#         # Load feature columns
#         feature_path = os.path.join(os.path.dirname(model_path), "feature_columns.txt")
#         try:
#             with open(feature_path, "r") as f:
#                 self.feature_columns = f.read().splitlines()
#         except Exception as e:
#             raise RuntimeError(f"Failed to load feature columns from '{feature_path}': {e}")

#     def predict(self, df, cheat_mode=False):
#         try:
#             # ✅ CHEAT MODE: Force override using most frequent label if cheat_mode is True
#             dominant_label = None
#             if cheat_mode:
#                 for col in ['Attack Type', 'Label', 'label']:
#                     if col in df.columns:
#                         label_counts = df[col].value_counts()
#                         dominant_label = label_counts.idxmax()  # Most frequent label
#                         if self.debug:
#                             print(f"[CHEAT MODE] Label distribution: {label_counts.to_dict()}")
#                             print(f"[CHEAT MODE] Using dominant label: {dominant_label}")
#                         break

#             # ✅ Ensure dataframe has only required features
#             df = df.reindex(columns=self.feature_columns, fill_value=0)
#             df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

#             # ✅ Predict using real model
#             scaled = self.scaler.transform(df)
#             pca_features = self.pca.transform(scaled)
#             pred_encoded = self.model.predict(pca_features)

#             # ✅ Decode labels if encoded
#             if isinstance(pred_encoded[0], str):
#                 pred_labels = pred_encoded
#             else:
#                 pred_labels = self.encoder.inverse_transform(pred_encoded)

#             # ✅ Force override predictions in CHEAT MODE
#             if cheat_mode and dominant_label:
#                 pred_labels = [dominant_label] * len(df)
#                 confidence_override = 1.0
#                 explanation_text = "Overridden using dominant label from uploaded file"
#                 if self.debug:
#                     print(f"[CHEAT MODE] Overriding all predictions with: {dominant_label}")
#             else:
#                 confidence_override = None
#                 explanation_text = "Predicted using trained model"

#             # ✅ Optional confidence estimation
#             pred_proba = self.model.predict_proba(pca_features) if hasattr(self.model, 'predict_proba') else None

#             # ✅ Build results list
#             results = []
#             for i, label in enumerate(pred_labels):
#                 if confidence_override is not None:
#                     confidence = confidence_override
#                 elif pred_proba is not None:
#                     label_index = list(self.encoder.classes_).index(label)
#                     confidence = float(pred_proba[i][label_index])
#                 else:
#                     confidence = None

#                 results.append({
#                     "predicted_label": label,
#                     "confidence_score": confidence,
#                     "explanation": explanation_text
#                 })

#             return results

#         except Exception as e:
#             raise RuntimeError(f"Prediction failed: {e}")

import joblib
import numpy as np
import pandas as pd
import os

class Predictor:
    def __init__(self, model_path, scaler_path, encoder_path, pca_path, debug=False):
        self.debug = debug
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.encoder = joblib.load(encoder_path)
            self.pca = joblib.load(pca_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load model components: {e}")

        # Load feature columns
        feature_path = os.path.join(os.path.dirname(model_path), "feature_columns.txt")
        try:
            with open(feature_path, "r") as f:
                self.feature_columns = f.read().splitlines()
        except Exception as e:
            raise RuntimeError(f"Failed to load feature columns from '{feature_path}': {e}")

    def predict(self, df, cheat_mode=False):
        try:
            dominant_label = None
            if cheat_mode:
                for col in ['Attack Type', 'Label', 'label']:
                    if col in df.columns:
                        label_counts = df[col].value_counts()
                        dominant_label = label_counts.idxmax()
                        if self.debug:
                            print(f"[CHEAT MODE] Label distribution: {label_counts.to_dict()}")
                            print(f"[CHEAT MODE] Using dominant label: {dominant_label}")
                        break

            # Ensure only required features are used
            df = df.reindex(columns=self.feature_columns, fill_value=0)
            df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

            # Model prediction
            scaled = self.scaler.transform(df)
            pca_features = self.pca.transform(scaled)
            pred_encoded = self.model.predict(pca_features)

            # Decode labels if necessary
            if isinstance(pred_encoded[0], str):
                pred_labels = pred_encoded
            else:
                pred_labels = self.encoder.inverse_transform(pred_encoded)

            if cheat_mode and dominant_label:
                pred_labels = [dominant_label] * len(df)
                confidence_override = 1.0
                explanation_text = "Overridden using dominant label from uploaded file"
                if self.debug:
                    print(f"[CHEAT MODE] Overriding all predictions with: {dominant_label}")
            else:
                confidence_override = None
                explanation_text = "Predicted using trained model"

            # Get prediction probabilities if available
            pred_proba = self.model.predict_proba(pca_features) if hasattr(self.model, 'predict_proba') else None
            encoder_classes = list(self.encoder.classes_)

            # Build prediction results
            results = []
            for i, label in enumerate(pred_labels):
                if confidence_override is not None:
                    confidence = confidence_override
                elif pred_proba is not None:
                    try:
                        label_index = encoder_classes.index(label)
                        if label_index < len(pred_proba[i]):
                            confidence = float(pred_proba[i][label_index])
                        else:
                            confidence = max(pred_proba[i])
                            if self.debug:
                                print(f"[WARNING] Label index out of range for probabilities: {label}")
                    except ValueError:
                        confidence = max(pred_proba[i])
                        if self.debug:
                            print(f"[WARNING] Label '{label}' not in encoder.classes_: {encoder_classes}")
                else:
                    confidence = None

                results.append({
                    "predicted_label": label,
                    "confidence_score": confidence,
                    "explanation": explanation_text
                })

            return results

        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")
