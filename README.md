# recipes-telegram-bot
> I am your cooking bot if you are a lazy human!


## Goal

This project creates a telegram bot that is able to recommend you recipes based on the ingredients you already have. It might propose you recipes with item you don't have and its his goal! It is here to help you make your shopping list for your next trip to the grocery store.

## Presentation of the bot

I have writen a Medium post about the details of this bot! if you are interested I encourage you the read the following [post!](https://romain-gratier.medium.com/create-a-simple-bot-with-telegram-that-notifies-you-about-the-progress-of-your-code-69bab685b9db) on  [<img src="https://github.com/RomainGratier/telegram-coffee-break/blob/main/documents/medium.png" width="100"/>](https://romain-gratier.medium.com/create-a-simple-bot-with-telegram-that-notifies-you-about-the-progress-of-your-code-69bab685b9db)

## Installation & setup

**If you don't have Docker**, please follow those steps! This should take 30 minutes.

```sh
pip3 install -r requirements.txt
```
```sh
bash setup.sh
```
```sh
python3.7 train_and_populate_recommendation_db.py
```

**If you do have Docker**, you can simply pull the following image:
```sh
docker pull tylerdurden1291/telegram-bot-recipes:mainimage
```

## Preparation

You need to first generate a telegram bot by following this [post](https://romain-gratier.medium.com/create-a-simple-bot-with-telegram-that-notifies-you-about-the-progress-of-your-code-69bab685b9db) on  [<img src="https://github.com/RomainGratier/telegram-coffee-break/blob/main/documents/medium.png" width="100"/>](https://romain-gratier.medium.com/create-a-simple-bot-with-telegram-that-notifies-you-about-the-progress-of-your-code-69bab685b9db). Or by following the steps below. Beware to keep the bot token for you and not share it for security reasons. 

**First: You will need to create a new telegram bot as follows:**

Go to the BotFather (if you open it in desktop, make sure you have the Telegram app), then create new bot by sending the /newbot command. Follow the steps until you get the username and token for your bot. You can go to your bot by accessing this URL: https://telegram.me/YOUR_BOT_USERNAME and your token should looks like this.

```sh
7044NNNNN:AAEtcZ*************
```

Keep the token safe in a file and set your bot.


## How to run the bot

**If you don't have docker**

```sh
python3.7 app.py <your_token>
```

**If you do have docker**

```sh
docker run -e token=Your_token_gen_by_Fatherbot tylerdurden1291/telegram-bot-recipes:mainimage
```
