# -*- coding: utf-8 -*-
from tradingview_ta import TA_Handler, Interval, Exchange
from twilio.rest import Client 
from datetime  import datetime
import pytz,time
import requests
import json
import smtplib
import pandas as pd



def get_data(base_symbol,interval = Interval.INTERVAL_5_MINUTES):
  IN_tmzn = pytz.timezone('Asia/Kolkata')
  exchange = ["Binance",'HUOBI',"KUCOIN",'OKEX',"POLONIEX"]
  last_symbol = ['USDT','USD','BTC','BUSD']
  # if crypto_symbol =="EZUSDT":
  #   crypto_symbol = "EZUSD"
  found = False
  num1 = 0
  while not found:
    for ex in exchange:
      # print(ex)
      crypto_name = base_symbol+last_symbol[num1]
      # print(crypto_name)
      try:

        crypto = TA_Handler(
        symbol=crypto_name,
        screener="Crypto",
        exchange=ex,
        interval=Interval.INTERVAL_1_MINUTE)
        open_price = crypto.get_indicators()['open']
      
      except:
        pass
      else:
        found = True
        break
    num1+=1
    if num1>=len(last_symbol):
      found = True
    # found=True
    # print(open_price

      
  
    

  print(f'{crypto_name} price')
  print(f"Current price {open_price} at {datetime.now(IN_tmzn).strftime('%I:%M  %d-%m-%y')}")
  return open_price,crypto_name

def read_file():
    
    crypto_df = pd.read_csv('/content/drive/MyDrive/Projects/crypto_list.csv',index_col="Unnamed: 0")
    # crypto_df
    
    # crypto_df.to_csv('/content/drive/MyDrive/Projects/crypto_list.csv')
    
    crypto_list = crypto_df.to_dict()['crypto_name']

    len(crypto_list)
    return crypto_list

def make_storage(dict_values):
  storage = {}
  for k,v in dict_values.items():
    storage[k] =[]
  return storage
# storage = make_storage(crypto_list)

def analysis(l,v):
  desc = None
  change = None
  Time_taken =None
  l.append(v)
  if len(l) >=2 :
    print("Inside analysis")
    print(f'+-change {round((l[-1]-l[-2])/l[-2]*100,2)}%')

    if (abs((l[-2]-l[-1])/l[-2]) >=0.05):
      print('--'*60)
      print("Price Increased by 5% within 2 mins")
      desc = f"{round(l[-2],3)}-->{round(l[-1],3)}"
      change = round((l[-1]-l[-2])/l[-2]*100,2) 
      Time_taken = 2
  if len(l) >=3:
      if abs((l[-3]-l[-1])/l[-3]) >=0.05:
        print('--'*60)
        print("Price Increased by 5% in 5 mins")
        desc = f"{round(l[-3],3)}-->{round(l[-1],3)}" 
        change = round((l[-1]-l[-3])/l[-3]*100,2) 
        Time_taken = 5
  if len(l) >=4:
    if abs((l[-4]-l[-1])/l[-4]) >=0.05:
      print('--'*60)
      print("Price Increased by 5% in 7 mins")
      desc = f"{round(l[-4],3)}-->{round(l[-1],3)}" 
      change = round((l[-1]-l[-4])/l[-4]*100,2)
      Time_taken = 7
  if len(l) >=5:
    if abs((l[-5]-l[-1])/l[-5]) >=0.05:
      print('--'*60)
      print("Price Increased by 5% in 9 mins")
      desc = f"{round(l[-5],3)}-->{round(l[-1],3)}" 
      change = round((l[-1]-l[-5])/l[-5]*100,2)
      Time_taken = 9
  if len(l) >=6:
    if abs((l[-6]-l[-1])/l[-6]) >=0.05:
      print('--'*60)
      print("Price Increased by 5% in 12 mins")
      desc = f"{round(l[-6],3)}-->{round(l[-1],3)}" 
      change = round((l[-1]-l[-6])/l[-6]*100,2)
      Time_taken = 12
  if len(l) ==7:
    if abs((l[-7]-l[-1])/l[-7]) >=0.05:
      print('--'*60)
      print("Price Increased by 5% in 15 mins")
      desc = f"{round(l[-7],3)}-->{round(l[-1],3)}" 
      change = round((l[-1]-l[-7])/l[-7]*100,2)
      Time_taken = 15

  if len(l) >7:
    l.pop(0)

  print(l)
  return desc,change,Time_taken

def print_result(row_num,df_,crypto_name,desc,change,Time_taken):
  IN_tmzn = pytz.timezone('Asia/Kolkata')
  df = df_.append({'Timestamp': pd.to_datetime(datetime.now(IN_tmzn),format='%d/%m/%y %I:%M'),'crypto_name':crypto_name,'Desc':desc,'change%':change,"Time_taken(In Mins)":Time_taken},ignore_index=True)
  # df.insert(row_num, 'TimeStamp', pd.to_datetime(datetime.now(IN_tmzn),format='%Y/%m/%d %H:%M:%S').replace(microsecond=0))
  print("*"*60)
  print("*"*60)
  print(desc)
  print("*"*60)
  return df


## sending sms
def send_sms(body):
 
  account_sid = '********************************' 
  auth_token = '**************************' 
  # client = Client(account_sid, auth_token) 
  
  client = Client(account_sid, auth_token)

  client.api.account.messages.create(
      to="**********************",
      from_="",
      body=body)



# !rm '/content/drive/MyDrive/Projects/status.csv'

def run():
    
    wazrix_app = "https://wazirx.com/exchange/HIVE-USDT"
    crypto_list = readfile()
    storage = make_storage(crypto_list)
    df = pd.DataFrame(columns=['Timestamp','crypto_name','Desc','change%',"Time_taken(In Mins)"])
    num = 1
    row_num =0
    while True:
      print('--'*50)
      for k,v in crypto_list.items():
        print(num)
        # print(v)
    
        price,crypto_name = get_data(v)
        desc,change,Time_taken = analysis(storage[k],price)
        if desc:
          df = print_result(row_num,df,crypto_name,desc,change,Time_taken)
          df.to_csv('/content/drive/MyDrive/Projects/status.csv',index=False)
          body = f"""{crypt_name} changed from {desc} {change} in {Time_taken} Mins
          applink: {wazrix_app}"""
          send_sms(body)
          row_num +=1
    
        time.sleep(0.3)
        num+=1

if __name__ =="__main__":
    run()
