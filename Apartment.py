import requests
import mysql.connector
from bs4 import BeautifulSoup

for page in range(1, 101):
    page = str(page)
    r = requests.get("https://shabesh.com/search/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4/%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86/%D8%AA%D9%87%D8%B1%D8%A7%D9%86?page=" + page)
    soup = BeautifulSoup(r.text, 'html.parser')

    property_types_list = []
    territories_list = []
    meterages_list = []
    number_of_rooms_list = []
    years_of_construct_list = []
    prices_per_squaremeter_list = []
    prices_list = []

    types = soup.find_all('span', attrs = {'class':'list_infoItem__8EH57 ellipsis d-block font-14'})
    for type in types:
        property_types_list.append(type.text)
    
    territories = soup.find_all('span', attrs = {'class':'list_infoItem__8EH57 ellipsis d-block'})
    for territory in territories:
        territories_list.append(territory.text)

    meterage_and_room_and_year = []
    for i in soup.find_all('span', attrs = {'class':'px-1 font-12'}):
        meterage_and_room_and_year.append(i.text)
    while(1):
        if len(meterage_and_room_and_year) == 0:
            break
        meterages_list.append(meterage_and_room_and_year[0])
        number_of_rooms_list.append(meterage_and_room_and_year[1])
        years_of_construct_list.append(meterage_and_room_and_year[2])
        del meterage_and_room_and_year[:3]

        prices_per_squaremeter = soup.find_all('span', attrs = {'class':'list_infoItem__8EH57 font-14 global_colorGray1__i1u0y d-block'})
        for price in prices_per_squaremeter:
            prices_per_squaremeter_list.append(price.text)

        prices = soup.find_all('span', attrs = {'class':'list_infoItem__8EH57 list_infoPrice___aJXK d-block'})
        for price in prices:
            prices_list.append(price.text)    

        result = list(zip(property_types_list, territories_list, meterages_list, number_of_rooms_list, years_of_construct_list, prices_per_squaremeter_list, prices_list))

        cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='house')
        for i in result:
            cursor = cnx.cursor()
            cursor.execute('INSERT IGNORE INTO information(type, territory, meterage, room, year, pps, price) VALUES (%s, %s, %s, %s, %s, %s, %s)',(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            cnx.commit()
        cnx.close()




