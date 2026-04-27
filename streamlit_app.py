# Import python packages.
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Write directly to the app.
st.title("Customize your Smoothie!")
st.write("Choose the fruits you want in your custom smoothie!")

session = Session.builder.configs(connection_parameters).create()


name_on_order = st.text_input("Name on Smoothie")
st.write("The current smoothie name is", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]


ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',
    fruit_list,
    max_selections=5
)

if ingredients_list:
    st.write(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """','""" + name_on_order + """')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        if name_on_order == "":
            st.warning("Please enter your name")
        else:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
            st.success(f'{name_on_order}, Your Smoothie is ordered!', icon="✅")
