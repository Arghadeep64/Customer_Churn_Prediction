import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("dataset/customer_churn.csv")


# ==========================
# Data Cleaning
# ==========================

df['TotalCharges'] = pd.to_numeric(
    df['TotalCharges'],
    errors='coerce'
)

df['TotalCharges'] = df['TotalCharges'].fillna(
    df['TotalCharges'].median()
)


# Remove unnecessary column
df = df.drop('customerID', axis=1)


# ==========================
# Encoding
# ==========================

encoders = {}

categorical_columns = df.select_dtypes(
    include=['object', 'string']
).columns


for col in categorical_columns:

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(
        df[col].astype(str)
    )

    encoders[col] = encoder


# ==========================
# Features and Target
# ==========================

X = df.drop('Churn', axis=1)

y = df['Churn']


# ==========================
# Train Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)


# ==========================
# Random Forest Model
# ==========================

model = RandomForestClassifier(

    n_estimators=500,

    max_depth=10,

    min_samples_split=5,

    random_state=42

)


# ==========================
# Train Model
# ==========================

model.fit(

    X_train,

    y_train

)


# ==========================
# Prediction
# ==========================

pred = model.predict(

    X_test

)


accuracy = accuracy_score(

    y_test,

    pred

)


# ==========================
# Save Model
# ==========================

joblib.dump(

    model,

    "models/churn_model.pkl"

)


joblib.dump(

    encoders,

    "models/encoders.pkl"

)


# ==========================
# Results
# ==========================

print()

print(

    "Accuracy :",

    round(

        accuracy*100,

        2

    ),

    "%"

)

print()

print(

    "Model Saved Successfully!"

)

print(

    "Encoders Saved Successfully!"

)

importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

print()
print(importance)