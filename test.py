
import pandas as pd
import datetime

data=open('/home/cappittall/Downloads/data (1).txt').read().splitlines()
excl=pd.read_excel('/home/cappittall/Downloads/RotaAktiviteAsıl (1).xls')
## Burada eval kullanımı sadece dosyadan data.txt yiokuduğumda text formatında okuyor satırları
# senin kullanmana gerek olmayabilir. 

# WONDER_OP_D_ID ilk datanın ilk bilgisi : 6237 ve değişmeyecek kabul ediyoruz. 
WORDER_OP_D_ID = eval(data[0])[0]   #6237
for inx in range(7):
    WORDER_M_ID = eval(data[inx])[7] 
    print(inx, excl.loc[inx, 'WORDER_M_ID'], excl.loc[inx, 'WORDER_OP_D_ID'])
    excl.loc[inx, 'WORDER_M_ID']=WORDER_M_ID
    excl.loc[inx, 'WORDER_OP_D_ID']=WORDER_OP_D_ID
    print(inx, excl.loc[inx, 'WORDER_M_ID'], excl.loc[inx, 'WORDER_OP_D_ID'])


