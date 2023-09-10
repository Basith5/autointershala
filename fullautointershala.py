import requests
from bs4 import BeautifulSoup
import pandas as pd
import telebot
from datetime import datetime
import pytz
import time

bot_token = '6581789747:AAGzQCDbY-6RvH0H968m5oJCx0Yb4w7YauI'
channel_chat_id = '-1001979941409'
bot = telebot.TeleBot(token=bot_token)

url = 'https://internshala.com/jobs/'

def create_message(row):
    view_details_link = f"https://internshala.com/{row[5]}"  # Construct the complete link
    message = f"{row[0]}\n" \
              "\n" \
              f"Company: {row[1]}\n" \
              "\n" \
              f"Location: {row[2]}\n" \
              "\n" \
              f"CTC: {row[3]}\n" \
              "\n" \
              f"Experience: {row[4]}\n" \
              "\n" \
              f"View Details: {view_details_link}\n" \
              "\n" \
              f"Connect With Us : Click Here (https://t.me/indiacareerss)\n"
    return message

def send_to_telegram(job_data):
    for job in job_data:
        message = create_message(job)
        bot.send_message(chat_id=channel_chat_id, text=message)

def scrape_and_send():
    try:
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            job_listings = soup.find_all('div', class_='container-fluid individual_internship visibilityTrackerItem')

            job_data = []
            for job in job_listings:
                job_title = job.find('h3', class_='heading_4_5 profile').text.strip()
                company_name = job.find('h4', class_='heading_6 company_name').text.strip()
                
                location_elem = job.find('p', id='location_names')
                location = location_elem.find('a', class_='location_link').text.strip() if location_elem else "Location not specified"
                
                ctc_elem = job.find('div', class_='item_body salary')
                ctc = ctc_elem.find_all('span')[0].text.strip()
                
                experience_elem = job.find('div', class_='item_body desktop-text', string='0-5 years')
                experience = experience_elem.text.strip() if experience_elem else "Experience not specified"
                
                view_details_elem = job.find('a', class_='view_detail_button_outline')
                view_details_link = view_details_elem['href'] if view_details_elem else "Link not specified"
                
                job_data.append([job_title, company_name, location, ctc, experience, view_details_link])

            send_to_telegram(job_data)
    except Exception as e:
        print(str(e))

while True:
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    if now.hour == 12 and now.minute == 30:
        scrape_and_send()
        time.sleep(60)  # wait for 60 seconds before checking the time again to avoid multiple messages
