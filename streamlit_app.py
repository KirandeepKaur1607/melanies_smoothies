import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title("Customize your Smoothie!")
st.write("Choose the fruits you want in your custom smoothie!")

# Snowflake connection
conn = st.connection("snowflake")
session = conn.session()

name_on_order = st.text_input("Name on Smoothie")
st.write("The current smoothie name is", name_on_order)

# Fruit list from Snowflake
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Submit logic
if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    if st.button("Submit Order"):
        session.sql(f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """).collect()

        st.success(f"{name_on_order}, Your Smoothie is ordered! ✅")

# API data (always visible)
smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

st.dataframe(
    data=smoothiefroot_response.json(),
    use_container_width=True
)
