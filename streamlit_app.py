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

# Fruit list from Snowflake (include SEARCH_ON)
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)

# Show dataframe for testing
st.dataframe(data=my_dataframe, use_container_width=True)

# Create fruit name list for multiselect
fruit_rows = my_dataframe.collect()
fruit_list = [row["FRUIT_NAME"] for row in fruit_rows]

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    fruit_list,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Find SEARCH_ON value for selected fruit
        search_on = fruit_chosen
        for row in fruit_rows:
            if row["FRUIT_NAME"] == fruit_chosen:
                search_on = row["SEARCH_ON"]
                break

        st.subheader(fruit_chosen + " Nutrition Information")

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )

        st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

    if st.button("Submit Order"):
        session.sql(f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """).collect()

        st.success(f"{name_on_order}, Your Smoothie is ordered! ✅")
