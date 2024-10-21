import streamlit as st
import pickle
import numpy as np

## load the pre trained model
with open('models/lgbm_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)


#define the ordinal mapping
ordinal_mapping = {
    0: "very poor",
    1:"poor",
    2:"average",
    3:"good",
    4:"excellent",
    5:"outstanding"
}

## function to convert user friendly input back to numeric for prediction

def ordinal_to_numeric(ajay):
    reverse_mapping = {v:k for k ,v in ordinal_mapping.items()}
    return reverse_mapping[ajay]

    


satisfaction_mapping ={ 0:'neutral or dissatisfied' ,1:'satisfied'}

## function to predict satisdfication
def predict_satisfication(Online_boarding, Delay_Ratio, Inflight_wifi_service, Class,
       Type_of_Travel, Inflight_entertainment, Flight_Distance,
       Seat_comfort, Leg_room_service, On_board_service,
       Ease_of_Online_booking, Cleanliness):
    
    x_new = np.array([Online_boarding, Delay_Ratio, Inflight_wifi_service, Class,
       Type_of_Travel, Inflight_entertainment, Flight_Distance,
       Seat_comfort, Leg_room_service, On_board_service,
       Ease_of_Online_booking, Cleanliness]).reshape(1 ,-1)
    
    y_pred_new = loaded_model.predict(x_new)
    return y_pred_new



# streamlit app titile and layout
st.title("flight satisfiaction prediction")
st.markdown(""" get an instant prediction of flight satisfaction based  on variours factors""")

## create two columns for a better layout
col1 , col2 = st.columns(2)

#column1 collectin delay and distance info
with col1:
    st.header('flight information')

    arrival_delay = st.number_input('Arrival Delay (minutes)' ,min_value=0.0 ,step=1.0 ,help='total minute flight was delayed up to')
    departure_delay = st.number_input('Departure Delay (minutes)' ,min_value=0.0 ,step=1.0 ,help='total minute flight was delayed up to')
    flight_distance = st.number_input('Flight Distance (km)' ,min_value=0.0 , value =1000.0 ,step=1.0 ,help='distance between departure delay and arrival delay')
    
    ## calculate total delay and delay ratio
    total_delay =arrival_delay +departure_delay
    delay_ratio =total_delay/(flight_distance+1)

## column 2 collecting user preference for flight service
with col2:
    st.header('service rating')

    # Online boarding',
#  'Delay Ratio',
#  'Inflight wifi service',
#  'Class',
#  'Type of Travel',
#  'Inflight entertainment',
#  'Flight Distance',
#  'Seat comfort',
#  'Leg room service',
#  'On-board service',
#  'Ease of Online booking',
#  'Cleanliness'
    
    inflight_wifi =st.selectbox('Inflight wifi service' ,list(ordinal_mapping.values()) ,help = "rate the inflight wifi service.")
    online_borading =st.selectbox('Online boarding' ,list(ordinal_mapping.values()) ,help = "rate the online boarding processes.")
    ease_onlinebooking =st.selectbox('Ease of Online Booking' ,list(ordinal_mapping.values()) ,help = "rate the ease of booking.")
    seat_comfort =st.selectbox('Seat comfort' ,list(ordinal_mapping.values()) ,help = "rate the 'Seat comfort'.")
    Inflight_entertainment =st.selectbox('Inflight entertainment' ,list(ordinal_mapping.values()) ,help = "rate the 'Inflight entertainment'.")
    On_board_service =st.selectbox('On-board service' ,list(ordinal_mapping.values()) ,help = "rate the 'On-board service'.")
    Leg_room_service =st.selectbox('Leg room service' ,list(ordinal_mapping.values()) ,help = "rate the Leg room service.")
    Cleanliness =st.selectbox('Cleanliness' ,list(ordinal_mapping.values()) ,help = "rate the 'Cleanliness'.")
    

    ## convert ordinal values to numeric
    inflight_wifi_num = ordinal_to_numeric(inflight_wifi)
    online_borading_num = ordinal_to_numeric(online_borading)
    ease_onlinebooking_num = ordinal_to_numeric(ease_onlinebooking)
    seat_comfort_num = ordinal_to_numeric(seat_comfort)
    Inflight_entertainment_num = ordinal_to_numeric(Inflight_entertainment)
    On_board_service_num = ordinal_to_numeric(On_board_service)
    Leg_room_service_num = ordinal_to_numeric(Leg_room_service)
    Cleanliness_num = ordinal_to_numeric(Cleanliness)

    
## organization additonal options in a horzintal layout
st.header("additonal  travel information ")

col3 ,col4 = st.columns(2)

with col3:
    passenger_class = st.selectbox('Class' ,['Business' ,'Eco' ,'Eco plus'] , help = "select the class of yours trvavel")

with col4:
    travel_type = st.selectbox('Type of Travel' ,['Business travel' ,'Personal Travel'] , help="specify the purpose of your travel")


## convert type and travel type to numeric values

class_mapping = {'Business':0 ,'Eco':1 ,'Eco Plus':2}
tarvel_type_mapping = {'Business travel':0 ,'Personal Travel' :1}
passenger_class_num = class_mapping[passenger_class]
travel_type_num = tarvel_type_mapping[travel_type]

# make  the  button to predict

if st.button('predict satisfication'):
    # make prediction
    prediction = predict_satisfication(online_borading_num, delay_ratio ,inflight_wifi_num ,passenger_class_num ,travel_type_num ,Inflight_entertainment_num ,flight_distance,seat_comfort_num ,Leg_room_service_num ,On_board_service_num ,ease_onlinebooking_num ,Cleanliness_num)
    print(prediction)
# map the numeric prediciton with intersafaction label

    satisfaction_label = satisfaction_mapping[int(prediction[0])]
    print(satisfaction_label)
## display the predciton with interactivity

    if satisfaction_label == "satisfied":
        st.success(f'** prediction:{satisfaction_label.capitalize()}**')

    else:
        st.warning(f'**predcition :{satisfaction_label}')