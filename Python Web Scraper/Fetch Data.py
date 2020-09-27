import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
from datetime import date


def get_random_ua():
    import random
    l = ['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3) Gecko/20090305 Firefox/3.1b3 GTB5','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; ko; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2','Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.9b5) Gecko/2008032620 Firefox/3.0b5','Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.12) Gecko/20080214 Firefox/2.0.0.12','Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8,''Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.0.5) Gecko/20060819 Firefox/1.5.0.5','Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3','Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.9) Gecko/20050711 Firefox/1.0.5','Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) Gecko/20100720 Firefox/4.0b2','Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/20100818 Firefox/4.0b4','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre','Mozilla/5.0 (X11; Linux x86_64; rv:2.0b9pre) Gecko/20110111 Firefox/4.0b9pre','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre','Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2','Mozilla/5.0 (X11; Linux i686 on x86_64; rv:12.0) Gecko/20100101 Firefox/12.0','Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2','Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0','Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0','Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0','Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0','Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0','Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0']
    return random.choice(l)
user_agent = get_random_ua()


headers ={'user agent' : 'user_agent',}
url = 'https://www.mohfw.gov.in/index.html'
uClient = requests.get(url,headers = headers).text

page_soup = soup(uClient,'lxml')


table = page_soup.findAll('table' , {'class' : 'table table-striped table-dark'})
Covid19_table = table[-1]
#print(Covid19_table)

table_text = []
for row in Covid19_table('tr')[1:]:
    row_text = []
    td_cells = row.find_all('td')
    for td_cell in td_cells:
        row_text.append(td_cell.text)
    table_text.append(row_text)



data = pd.DataFrame(table_text, columns = ['SrNo' , 'States','Total Confirmed cases','Cured','Deaths'])
data = data.iloc[:27,1:]
data[["Total Confirmed cases","Cured","Deaths"]] = data[["Total Confirmed cases","Cured","Deaths"]].apply(pd.to_numeric)
data['Confirmed'] = data['Total Confirmed cases']
Data = data.copy()
Data = Data[['States','Confirmed','Deaths','Cured']]
print(Data.info())
print('Cases',Data['Confirmed'].sum())
print('Deaths',Data['Deaths'].sum())
print('Cured',Data['Cured'].sum())

Data.to_csv(r'/home/ubuntu/Covid19 Dataset/Live_Data.csv')

def Update_data():
    # India Data
    dataInd = pd.read_csv(r'/home/ubuntu/Covid19 Dataset/Covid19 India Data.csv', index_col='Date')
    from datetime import date
    today = date.today().isoformat()
    l = [Data['Confirmed'].sum(), Data['Deaths'].sum(), Data['Cured'].sum()]
    if dataInd.index[-1] == today and dataInd['Confirmed'][-1] != Data['Confirmed'].sum():
        dataInd = dataInd.iloc[:-2, :]
        dataInd = dataInd.append(pd.Series(l, index=dataInd.columns, name=today))
        print(dataInd.index[-1] == today)
    elif dataInd.index[-1] != today:
        # dataInd.loc[today] = l
        dataInd = dataInd.append(pd.Series(l, index=dataInd.columns, name=today))
    dataInd.to_csv(r'/home/ubuntu/Covid19 Dataset/Covid19 India Data.csv',index=True)

    # States Data
    Data1 = Data.copy()
    Data1.set_index('States')
    States = ['Andhra Pradesh', 'Andaman and Nicobar Islands', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Delhi', 'Goa',
              'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Ladakh',
              'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Mizoram', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
              'Tamil Nadu', 'Telengana', 'Uttarakhand', 'Uttar Pradesh','West Bengal']
    File_names = ['/home/ubuntu/Covid19 Dataset/Covid19 ' + i + ' Data.csv' for i
                  in States]

    for i in range(len(File_names)):
        dataSt = pd.read_csv(File_names[i], index_col='Date')
        l_st = [Data1.loc[Data1['States'] == States[i], 'Confirmed'].item(),
                Data1.loc[Data1['States'] == States[i], 'Deaths'].item(),
                Data1.loc[Data1['States'] == States[i], 'Cured'].item()]
        if dataInd.index[-1] == today and dataInd['Confirmed'][-1] != Data['Confirmed'].sum():
            dataSt = dataSt.iloc[:-2, :]
            dataSt = dataSt.append(pd.Series(l_st, index=dataSt.columns, name=today))

        elif dataSt.index[-1] != today:
            # dataInd.loc[today] = l
            dataSt = dataSt.append(pd.Series(l_st, index=dataSt.columns, name=today))
        #print(type(Data1.loc[Data1['States'] == States[i], 'Confirmed'].item()))
        dataSt.to_csv(File_names[i],index = True)
    print('\nData Updated')
Update_data()
