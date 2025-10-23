# Telegram Gas Reporter Bot

A simple Python Telegram bot that fetches Ethereum gas prices from the Etherscan API and reports them periodically.

## Features
- Fetches SafeGas and ProposeGas prices every 30 seconds.
- Sends updates to a Telegram chat when `/go` is triggered.
- Stops on `/stop`.
- Runs continuously via APScheduler.

## Setup

Before running, create a `.env` file in the project root and fill it with your own keys.

```
pip install -r requirements.txt
python app.py
```
