import requests

from bs4 import BeautifulSoup

year = 2021
month = 4
day = 27
hour = 0 # utc

year = str(year)
month = str(month).zfill(2)
day = str(day).zfill(2)
hour = str(hour).zfill(2)
link_head= "http://www.meteomanz.com/sy1?cou=2&l=1&ty=br&ind=00000&d1" \
      "=%s&m1=%s&y1=%s&ext=0&rt=0&h1=%sZ&h2=%sZ&d2=%s&m2=%s&y2=%s&so=102&np="%(day,month,year,hour,hour,day,month,year)
link_phi = "http://www.meteomanz.com/sy1?ty=br&l=1&cou=" \
      "5420&ind=00000&d1=%s&m1=%s&y1=%s&h1=%sZ&d2=%s&m2=%s&y2=%s&h2=%sZ"%(day,month,year,hour,day,month,year,hour)
country_list = []
station_list = []
date_list = []
time_list = []
data_list = []
Unnamed = []
for n in range(1,9):
    link = link_head + str(n)
    result = requests.get(link)
    print("Open : ", link)
    html = result.text

    BS = BeautifulSoup(html, "html.parser")

    A = BS.table.text
    B = A.split("\n")
    if n == 1:
        country = B[1]
        station = B[2]
        date = B[3][:-2]
        time = B[4]
        data = B[5]
    # country_list = [B[8],B[8+7],B[8+7+7],B[8+7+7+7],B[8 + 7 * 299]]
    # station_list = [B[9],B[9+7],B[9+7+7],B[9+7+7+7],B[9 + 7 * 299]]
    # date_list = [B[10],B[10+7],B[10+7+7],B[10+7+7+7],B[10 + 7 * 299]]
    # time_list = [B[11],B[11+7],B[11+7+7],B[11+7+7+7],B[11 + 7 * 299]]
    # data_list = [B[12],B[12+7],B[12+7+7],B[12+7+7+7],B[12 + 7 * 299]]
    for i in range(0,300):
        try:
            if B[12+i*7][0:4] == "AAXX":
                country_list.append(B[8+i*7])
                station_list.append(B[9+i*7])
                date_list.append(B[10+i*7])
                time_list.append(B[11+i*7])
                data_list.append(B[12+i*7])
                Unnamed.append(0)
            else:
                pass
        except:
            pass
    print("Data crawling")

result = requests.get(link_phi)
print("Open : ", link_phi)
html = result.text

BS = BeautifulSoup(html, "html.parser")

A = BS.table.text
B = A.split("\n")
for i in range(0,300):
    try:
        if B[12+i*7][0:4] == "AAXX":
            country_list.append(B[8+i*7])
            station_list.append(B[9+i*7])
            date_list.append(B[10+i*7])
            time_list.append(B[11+i*7])
            data_list.append(B[12+i*7])
            Unnamed.append(0)
        else:
            pass
    except:
        pass
print("SYNOP code crawling Finish!")

from pandas import DataFrame as df
df1 = df(data={country : country_list, station : station_list, date : date_list,
               time : time_list, data : data_list,"Unnamed: 5":Unnamed  })

df1.to_excel(excel_writer='D:\\sample.xlsx',index=False,header=True)