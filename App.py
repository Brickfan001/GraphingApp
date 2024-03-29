import streamlit as st
import json
from datetime import datetime, date
import calendar
import time


def date_to_day(date):
    date_object = datetime.strptime(date, '%Y-%m-%d').date()
    x = calendar.day_name[date_object.weekday()]
    return x


st.title('Decode Your Chats: Telegram Insights at Your Fingertips!')
data = st.file_uploader('Upload Your Chat File', type='json')

hel = '''To Get Your Chat File:-\n
Open Telegram on your PC -> 
Go To Your Chat ->
Click on Three Dots on To Right->
Click on export Chat and Export Chat in json format
'''

x = st.write(hel)
if data is not None:
    data = json.load(data)

    participants = {}  # to count messages per person
    words_dict = {}  # count of word used per person
    totalmsgs = len(data['messages'])

    min_word_length = 3  # minimum length for most used mostUsedWords

    # total count of per persons
    char_count_dict = {}
    word_count_dict = {}

    # word count per person per word
    person_word_Dict = {}
    mostUsedWords = {}

    # count of hour,date per person
    date_dict = {}
    time_dict = {}

    # count of day per person
    day_dict = {}

    # main loop
    for i in data['messages']:

        if i['type'] == 'message':
            if i['from'] not in participants:
                mostUsedWords[i['from']] = {}
                participants[i['from']] = 0
                char_count_dict[i['from']] = 0
                word_count_dict[i['from']] = 0
                person_word_Dict[i['from']] = {}
                day_dict[i['from']] = {"Monday": 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0,
                                       'Saturday': 0, 'Sunday': 0}
                time_dict[i['from']] = {}
                date_dict[i['from']] = {}

            if i['date'][0:10] not in date_dict[i['from']]:
                date_dict[i['from']][i['date'][0:10]] = 0

            if i['date'][11:13] not in time_dict[i['from']]:
                time_dict[i['from']][i['date'][11:13]] = 0

            participants[i['from']] += 1
            date_dict[i['from']][i['date'][0:10]] += 1
            time_dict[i['from']][i['date'][11:13]] += 1
            day_dict[i['from']][date_to_day(i['date'][0:10])] += 1

            if type(i['text']) != list:
                for j in i['text'].lower().split():
                    if j.lower() not in words_dict and len(j) > min_word_length:
                        words_dict[j.lower()] = 0

                    if j.lower() not in person_word_Dict[i['from']] and len(j) > min_word_length:
                        person_word_Dict[i['from']][j.lower()] = 1

                    if len(j.lower()) > min_word_length:
                        words_dict[j.lower()] += 1
                        person_word_Dict[i['from']][j.lower()] += 1

                # averages
                char_count_dict[i['from']] += len(i['text'].replace(" ", ""))
                word_count_dict[i['from']] += len(i['text'].split())

    # sorting dictionaries
    words_dict = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)
    words_dict = dict(words_dict[0:11])

    mostdays = 0
    for i in date_dict:
        if len(date_dict[i]) > mostdays:
            mostdays = len(date_dict[i])

    for i in participants:
        temp = sorted(person_word_Dict[i].items(), key=lambda x: x[1], reverse=True)
        temp = dict(temp)
        person_word_Dict[i] = temp

    person_day_dict = {}
    for i in day_dict:
        person_day_dict[i] = sum(day_dict[i].values())

    for i in words_dict:
        for j in mostUsedWords:
            mostUsedWords[j][i] = 0
            if i in person_word_Dict[j]:
                mostUsedWords[j][i] += person_word_Dict[j][i]

    st.header(f'''General Stats\n
   Total Messages - {totalmsgs}\n
   Total Days Talked - {mostdays}\n
   '''
              )

    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        st.subheader('Total Messages')
        st.bar_chart(participants)

    st.header('Averages')

    st.subheader(f'''Averages Per Day
   Messages - {str(totalmsgs / mostdays).split('.')[0]}\n
             ''')

    col1, col2, col3 = st.columns([1, 4, 1])

    mdm = {}
    for i in participants:
        mdm[i] = participants[i] / mostdays
    with col2:
        st.subheader('Messages')
        st.bar_chart(mdm)

    wdm = {}
    for i in word_count_dict:
        wdm[i] = word_count_dict[i] / mostdays

    st.header('Date-Wise Stats')
    st.bar_chart(data=date_dict)

    st.header('Weekly Stats')
    st.bar_chart(data=day_dict)

    st.header('Hourly Stats')
    st.bar_chart(data=time_dict)
