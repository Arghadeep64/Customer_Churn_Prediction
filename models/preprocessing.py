import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("dataset/customer_churn.csv")

# Cleaning
df['TotalCharges'] = pd.to_numeric(
    df['TotalCharges'],
    errors='coerce'
)

df['TotalCharges'] = df['TotalCharges'].fillna(
    df['TotalCharges'].median()
)

# Remove customerID
df = df.drop('customerID', axis=1)

encoder = LabelEncoder()

categorical_columns = df.select_dtypes(include=['object','string']).columns

for col in categorical_columns:
    df[col] = encoder.fit_transform(df[col].astype(str))

print(df.head())

print()

print("\nShape :", df.shape)