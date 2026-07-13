from database.db_connection import get_connection
import pandas as pd


def save_prediction(
    
    username,

    user_id,

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
    monthly,

    prediction,
    confidence

):

    connection = get_connection()

    cursor = connection.cursor()

    query = """

    INSERT INTO prediction_history(
        username,
        user_id,
        gender,
        senior_citizen,
        partner,
        dependents,
        tenure,
        phone_service,
        multiple_lines,
        internet_service,
        online_security,
        online_backup,
        device_protection,
        tech_support,
        streaming_tv,
        streaming_movies,
        contract,
        paperless_billing,
        payment_method,
        monthly_charges,
        prediction,
        confidence

    )

    VALUES(

        %s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,
        %s,%s

)

    """

    values = (
        username,
         
        user_id,

        gender,

        "Yes" if int(senior) else "No",

        "Yes" if int(partner) else "No",

        "Yes" if int(dependents) else "No",

        tenure,

        "Yes" if int(phone) else "No",

        "Yes" if int(multiple) else "No",

        ["DSL", "Fiber optic", "No"][int(internet)],

        "Yes" if int(security) else "No",

        "Yes" if int(backup) else "No",

        "Yes" if int(device) else "No",

        "Yes" if int(support) else "No",

        "Yes" if int(tv) else "No",

        "Yes" if int(movies) else "No",

        [
            "Month-to-month",
            "One year",
            "Two year"
        ][int(contract)],

        "Yes" if int(paper) else "No",

        [
            "Bank transfer (automatic)",
            "Credit card (automatic)",
            "Electronic check",
            "Mailed check"
        ][int(payment)],

        monthly,

        prediction,

        confidence

    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()

    connection.close()


def get_prediction_history():

    connection = get_connection()

    query = """

    SELECT *

    FROM prediction_history

    ORDER BY prediction_time DESC

    """

    df = pd.read_sql(

        query,

        connection,


)

    connection.close()

    return df


def get_prediction_analytics_history():

    connection = None

    try:

        connection = get_connection()

        query = """

        SELECT
            prediction,
            confidence,
            prediction_time

        FROM prediction_history

        """

        return pd.read_sql(

            query,

            connection

        )


    except Exception as error:

        print("Unable to load prediction analytics:", type(error).__name__)

        return pd.DataFrame(

            columns=[
                "prediction",
                "confidence",
                "prediction_time"
            ]

        )


    finally:

        if connection is not None:

            connection.close()

def register_user(

    username,

    email,

    password

):

    connection = get_connection()

    cursor = connection.cursor()

    query = """

    INSERT INTO users(

        username,

        email,

        password

    )

    VALUES(

        %s,

        %s,

        %s

    )

    """
    try:

        cursor.execute(

            query,

            (

                username,

                email,

                password

            )

        )

        connection.commit()

        return True


    except:

        return False


    finally:

        cursor.close()

        connection.close()

def delete_user(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        "DELETE FROM prediction_history WHERE user_id=%s",

        (user_id,)

    )

    cursor.execute(

        "DELETE FROM users WHERE id=%s",

        (user_id,)

    )

    connection.commit()

    cursor.close()

    connection.close()

    
def check_login(

    username,

    password

):

    connection = get_connection()

    cursor = connection.cursor()

    query = """

SELECT id, username

FROM users

WHERE username=%s

AND password=%s

"""

    cursor.execute(

        query,

        (

            username,

            password

        )

    )

    user = cursor.fetchone()

    cursor.close()

    connection.close()

    return user

def delete_selected_predictions(ids):

    connection = get_connection()

    cursor = connection.cursor()


    query = """

    DELETE FROM prediction_history

    WHERE id = %s

    """


    for i in ids:

        cursor.execute(

            query,

            (i,)

        )


    connection.commit()

    cursor.close()

    connection.close()



def delete_all_predictions():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        DELETE FROM prediction_history

        """

    )


    connection.commit()

    cursor.close()

    connection.close()
