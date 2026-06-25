import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dataset/customer_churn.csv")

df["Churn"].value_counts().plot(
    kind="bar"
)

plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Count")

plt.show()