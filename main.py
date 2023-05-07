import requests #pip install requests
from bs4 import BeautifulSoup #pip install bs4
import pygame 
import os
import time
import smtplib
import json
from colored import fg, attr

#Opening The Settings.json file
with open('settings.json','r') as file:
    settings = json.load(file)

# To play a ding if the product is in our budget 
pygame.mixer.init()
pygame.mixer.music.load(settings["remind-sound-path"])

# Set your budjet
my_price = settings['budget']

# initializing Currency Symbols to substract it from our string
currency_symbols = ['€', '	£', '$', "¥", "HK$", "₹", "¥", "," ] 

# the URL we are going to use
URL = settings['url']

# Google "My User Agent" And Replace It
headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'} 

#Checking the price
def checking_price():
    page = requests.get(URL, headers=headers)
    soup  = BeautifulSoup(page.text, 'html.parser')

    #Finding the elements
    product_title = soup.find('span', id='productTitle').getText()
    product_price = soup.find('span', class_ = "a-offscreen").getText()

    # using replace() to remove currency symbols
    for i in currency_symbols : 
        product_price = product_price.replace(i, '')

    #Converting the string to integer
    product_price = int(float(product_price))

    ProductTitleStrip = product_title.strip()
    print(f"{fg('green_1')}The Product Name is:{attr('reset')}{fg('dark_slate_gray_2')} {ProductTitleStrip}{attr('reset')}")
    print(f"{fg('green_1')}The Price is:{attr('reset')}{fg('orange_red_1')} {product_price}{attr('reset')}")



    # checking the price
    if(product_price<my_price):
        pygame.mixer.music.play()
        print(f"{fg('medium_orchid_1b')}You Can Buy This Now!{attr('reset')}")
        time.sleep(3) # audio will be played first then exit the program. This time for audio playing.
        #send_mail()
        exit()
    else:
        print(f"{fg('red_1')}The Price Is Too High!{attr('reset')}")
        
    
# function that sends an email if the prices fell down
def send_mail():
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()

  server.login('sakshiikohlii@gmail.com', 'two(7678)')

  subject = 'Price Fell Down'
  body = "Check the amazon link https://www.amazon.in/dp/B0B56C7NGS/ref=sspa_dk_detail_2?pd_rd_i=B0B56C7NGS&pd_rd_w=vpsMH&content-id=amzn1.sym.2575ab02-73ff-40ca-8d3a-4fbe87c5a28d&pf_rd_p=2575ab02-73ff-40ca-8d3a-4fbe87c5a28d&pf_rd_r=S3J8MH4163FEYBMX1VRC&pd_rd_wg=RB0RM&pd_rd_r=887cf1fc-d862-4e16-ad2c-3f05cc97d19e&s=computers&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw&th=1 "

  msg = f"Subject: {subject}\n\n{body}"
  
  server.sendmail(
    'sakshiikohlii@gmail.com',
    'nimishajoshi@gmail.com',
    msg
  )
  #print a message to check if the email has been sent
  print('Hey Email has been sent')
  # quit the server
  server.quit()

while True:
    checking_price()
    time.sleep(settings['remind-time']) #It is set to run the program once in an hour! You can change by changing the value in seconds!
