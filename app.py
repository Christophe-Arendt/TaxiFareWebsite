import streamlit as st
import datetime
import requests
from streamlit_folium import folium_static
import folium

'''
# TaxiFareModel front

This front queries the Le Wagon [taxi fare model API](http://taxifare.lewagon.ai/predict_fare/?key=2012-10-06%2012:10:20.0000001&pickup_datetime=2012-10-06%2012:10:20%20UTC&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2)
'''

def geocode(address):
    params = {'q' : address, 'format' : 'json'}
    places = requests.get(f'https://nominatim.openstreetmap.org/search?', params = params).json()
    return places[0]['lat'], places[0]['lon']

location = st.sidebar.text_input('Where are you ?','178 7th Ave S, New York, NY 10014, United States')
destination = st.sidebar.text_input('What is your destination ?', 'Queens, NY 11430, United States')


key = '2012-10-06 12:10:20.0000001'
pickup_date = st.sidebar.date_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
pickup_time = st.sidebar.time_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
pickup_datetime = f'{pickup_date} {pickup_time}UTC'


#pickup_longitude = st.number_input('pickup longitude', value=40.7614327)
#pickup_latitude = st.number_input('pickup latitude', value=-73.9798156)
#dropoff_longitude = st.number_input('dropoff longitude', value=40.6413111)
#dropoff_latitude = st.number_input('dropoff latitude', value=-73.7803331)
passenger_count = st.sidebar.number_input('passenger_count', min_value=1, max_value=8, step=1, value=1)



pickup_longitude = float(geocode(location)[1])
pickup_latitude = float(geocode(location)[0])
dropoff_longitude = float(geocode(destination)[1])
dropoff_latitude =float(geocode(destination)[0])


# center on Liberty Bell
m = folium.Map(location=[40.7831, -73.9712], zoom_start=11)

# add marker for Liberty Bell
folium.Marker(
    [pickup_latitude, pickup_longitude], popup=location,
    tooltip= f"Current Location : {location}"
).add_to(m)

folium.Marker(
    [dropoff_latitude, dropoff_longitude], popup=location,
    tooltip= f"Destionation Location : {destination}"
).add_to(m)


# call to render Folium map in Streamlit
folium_static(m)
# enter here the address of your flask api
#url = 'https://wagon-exo-z7fyqqvx3a-ew.a.run.app/predict_fare'
url = 'https://taxifareapi-lrbsb3mzwa-ew.a.run.app/predict_fare'
params = dict(
    key=key,
    pickup_datetime=pickup_datetime,
    pickup_longitude=pickup_longitude,
    pickup_latitude=pickup_latitude,
    dropoff_longitude=dropoff_longitude,
    dropoff_latitude=dropoff_latitude,
    passenger_count=passenger_count)

st.markdown('The taxi fare for this journey is : ')

response = requests.get(url, params=params)
prediction = response.json()
pred = prediction['prediction']
st.write(round(pred,2),'💲')
