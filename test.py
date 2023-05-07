# import required files and modules

import requests
from bs4 import BeautifulSoup
import smtplib
import time

# set the headers and user string
headers = {
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}

# send a request to fetch HTML of the page
response = requests.get('https://www.amazon.in/dp/B0B56C7NGS/ref=sspa_dk_detail_2?pd_rd_i=B0B56C7NGS&pd_rd_w=vpsMH&content-id=amzn1.sym.2575ab02-73ff-40ca-8d3a-4fbe87c5a28d&pf_rd_p=2575ab02-73ff-40ca-8d3a-4fbe87c5a28d&pf_rd_r=S3J8MH4163FEYBMX1VRC&pd_rd_wg=RB0RM&pd_rd_r=887cf1fc-d862-4e16-ad2c-3f05cc97d19e&s=computers&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw&th=1', headers=headers)

# create the soup object
soup = BeautifulSoup(response.content, 'html.parser')

# change the encoding to utf-8
soup.encode('utf-8')

#print(soup.prettify())

# function to check if the price has dropped below 20,000
def check_price():
  title = soup.find(id= "productTitle").get_text()
  price = soup.find(id = "priceblock_ourprice").get_text().replace(',', '').replace('₹', '').replace(' ', '').strip()
  #print(price)

  #converting the string amount to float
  converted_price = float(price[0:5])
  print(converted_price)
  if(converted_price < 20000):
    send_mail()

  #using strip to remove extra spaces in the title
  print(title.strip())




# function that sends an email if the prices fell down
def send_mail():
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()

  server.login('email@gmail.com', 'password')

  subject = 'Price Fell Down'
  body = "Check the amazon link https://www.amazon.in/dp/B0B56C7NGS/ref=sspa_dk_detail_2?pd_rd_i=B0B56C7NGS&pd_rd_w=vpsMH&content-id=amzn1.sym.2575ab02-73ff-40ca-8d3a-4fbe87c5a28d&pf_rd_p=2575ab02-73ff-40ca-8d3a-4fbe87c5a28d&pf_rd_r=S3J8MH4163FEYBMX1VRC&pd_rd_wg=RB0RM&pd_rd_r=887cf1fc-d862-4e16-ad2c-3f05cc97d19e&s=computers&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw&th=1 "

  msg = f"Subject: {subject}\n\n{body}"
  
  server.sendmail(
    'sender@gmail.com',
    'receiver@gmail.com',
    msg
  )
  #print a message to check if the email has been sent
  print('Hey Email has been sent')
  # quit the server
  server.quit()

#loop that allows the program to regularly check for prices
while(True):
  check_price()
  time.sleep(60 * 60)