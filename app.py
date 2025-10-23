#!/bin/python3
import requests
import telepot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from telepot.loop import MessageLoop
import time
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

bot = telepot.Bot(BOT_TOKEN)
send_messages = False

URL = f"https://api.etherscan.io/v2/api?chainid=1&module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"

def handle(msg):
    global send_messages
    content_type, chat_type, chat_id = telepot.glance(msg)
    text = msg.get('text', '')

    if content_type == 'text':
        if text.lower() == '/go':
            send_messages = True
            bot.sendMessage(chat_id, "[+] Gas price reporting started")
        elif text.lower() == '/stop':
            send_messages = False
            bot.sendMessage(chat_id, "[-] Gas price reporting stopped")
        else:
            bot.sendMessage(chat_id, "Unknown command. Use /go or /stop")

MessageLoop(bot, handle).run_as_thread()

def fetch_gas_and_send():
    global send_messages
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            safe_gas = float(data['result']['SafeGasPrice'])
            propose_gas = float(data['result']['ProposeGasPrice'])
            diff = propose_gas - safe_gas
            message = f"SafeGasPrice: {safe_gas:.2f}, ProposeGasPrice: {propose_gas:.2f}, Diff: {diff:+.2f}"
            if send_messages:
                bot.sendMessage(CHAT_ID, message)
            now = datetime.now().strftime('%H:%M:%S')
            print(f"[{now}] {message}")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred: {e}")

def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_gas_and_send, 'interval', seconds=30)
    scheduler.start()
    print("Telegram Gas Reporter Bot started")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped manually.")
        scheduler.shutdown()

if __name__ == "__main__":
    main()
