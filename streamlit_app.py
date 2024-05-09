# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# Get the current credentials
cnx=st.connection('snowflake')
session = cnx.session()



my_dataframe=session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe,use_container_width=True)

name_on_order=st.text_input("Name on Smoothie :")
st.write("The name on your smoothie will be :",name_on_order)

ingredients_list=st.multiselect(
    "Choose upto  five ingredients : ", my_dataframe,max_selections=5
)

if ingredients_list:
	
    

    ingredients_string=' '

    for i in ingredients_list:
	    ingredients_string=ingredients_string+i+' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    st.write(my_insert_stmt)

    #st.write(my_insert_stmt)

    time_to_insert=st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)





