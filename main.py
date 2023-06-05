import requests
import selectorlib
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3

URL="https://programmer100.pythonanywhere.com/"
HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

connection = sqlite3.connect("data.db")
def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value= extractor.extract(source)["temperature"]
    return value

def store(temperature):
    now = datetime.now()
    new_now = now.strftime("%Y-%m-%d-%H-%M-%S")
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO events VALUES({new_now},{temperature})")
    connection.commit()
    # with open("data.txt", "a") as file:
    #     file.write(f'{date},{temperature} \n')

if __name__=="__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    # now = datetime.now()
    # new_now=now.strftime("%Y-%m-%d-%H-%M-%S")
    # print(new_now)
    store(extracted)
    # with open("data.txt") as file:
    #     list= file.read()
    cursor = connection.cursor()
    cursor.execute("Select data from events ")
    x = list(cursor.fetchall())
    y=cursor.execute("Select temperature from events")
    y = list(cursor.fetchall())
    x_list = [list((item)) for item in x]
    y_list = [list(item) for item in y]
    x_L = [item[0] for item in x_list]
    y_L = [item[0] for item in y_list]
    x_ruyxat = list(map(int, x_L))
    y_ruyxat = list(map(int, y_L))
    print(x_ruyxat)
    print(y_ruyxat)


    # df = pd.read_csv("data.txt")
    #
    # # dict = df.to_dict()
    #
    # x= df['date_time']
    #
    # y= df['temp']

    # for key, value in dict.split():

    figure = px.line(x=x_ruyxat, y=y_ruyxat, labels={"x": "date", "y": "temperature"})
    st.plotly_chart(figure)


    # for key, value in dict:
    #     print(key)

    # for index, row in df.iterrows():
    #     print(row[)



