import joblib
import pandas as pd


model = joblib.load("models/churn_model.pkl")
encoders = joblib.load("models/encoders.pkl")


def encode(column, value):
    return encoders[column].transform([str(value)])[0]


def yn(value):

    return "Yes" if int(value) == 1 else "No"


def predict_customer(

    gender,
    senior,
    partner,
    dependents,
    tenure,
    phone,
    multiple,
    internet,
    security,
    backup,
    device,
    support,
    tv,
    movies,
    contract,
    paper,
    payment,
    monthly

):


    total = tenure * monthly


    internet_map = {

        0: "DSL",
        1: "Fiber optic",
        2: "No"

    }


    contract_map = {

        0: "Month-to-month",
        1: "One year",
        2: "Two year"

    }


    payment_map = {

        0: "Bank transfer (automatic)",
        1: "Credit card (automatic)",
        2: "Electronic check",
        3: "Mailed check"

    }



    data = pd.DataFrame({


        "gender":[

            encode(

                "gender",

                gender

            )

        ],


        "SeniorCitizen":[

            int(senior)

        ],



        "Partner":[

            encode(

                "Partner",

                yn(partner)

            )

        ],


        "Dependents":[

            encode(

                "Dependents",

                yn(dependents)

            )

        ],



        "tenure":[

            tenure

        ],



        "PhoneService":[

            encode(

                "PhoneService",

                yn(phone)

            )

        ],



        "MultipleLines":[

            encode(

                "MultipleLines",

                yn(multiple)

            )

        ],



        "InternetService":[

            encode(

                "InternetService",

                internet_map[int(internet)]

            )

        ],



        "OnlineSecurity":[

            encode(

                "OnlineSecurity",

                yn(security)

            )

        ],



        "OnlineBackup":[

            encode(

                "OnlineBackup",

                yn(backup)

            )

        ],



        "DeviceProtection":[

            encode(

                "DeviceProtection",

                yn(device)

            )

        ],



        "TechSupport":[

            encode(

                "TechSupport",

                yn(support)

            )

        ],



        "StreamingTV":[

            encode(

                "StreamingTV",

                yn(tv)

            )

        ],



        "StreamingMovies":[

            encode(

                "StreamingMovies",

                yn(movies)

            )

        ],



        "Contract":[

            encode(

                "Contract",

                contract_map[int(contract)]

            )

        ],



        "PaperlessBilling":[

            encode(

                "PaperlessBilling",

                yn(paper)

            )

        ],



        "PaymentMethod":[

            encode(

                "PaymentMethod",

                payment_map[int(payment)]

            )

        ],



        "MonthlyCharges":[

            monthly

        ],



        "TotalCharges":[

            total

        ]

    })



    print()
    print(data)
    print()


    prediction = model.predict(data)[0]

    probability = model.predict_proba(data)[0]



    if prediction == 1:

        result = "Customer Will Churn"

        confidence = probability[1] * 100


    else:

        result = "Customer Will Stay"

        confidence = probability[0] * 100



    return result, confidence