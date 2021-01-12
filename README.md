# recipes-telegram-bot
> Hi, I am your cooking bot! Why don't you give me a try?


## Goal

This project creates a telegram bot that can recommend recipes based on the ingredients you already have. It might propose you recipes with items you don't have, and it is its goal! It is here to help you make your shopping list for your next trip to the grocery store.

## Presentation of the bot

I have written a Medium post about the details of this bot! if you are interested I encourage you the read the following [post!](https://romain-gratier.medium.com/de2d314f565d?source=friends_link&sk=c5280f8c50aa5551d1b36619891e9b4f) on  [<img src="https://github.com/RomainGratier/telegram-coffee-break/blob/main/documents/medium.png" width="100"/>](https://romain-gratier.medium.com/de2d314f565d?source=friends_link&sk=c5280f8c50aa5551d1b36619891e9b4f)

## Installation & setup

**If you don't have Docker**, please follow those steps! It should take 30 minutes.

```sh
pip3 install -r requirements.txt
```
```sh
bash setup.sh
```
```sh
python3.7 train_and_populate_recommendation_db.py
```

**If you do have Docker**, you can easily pull the following image:
```sh
docker pull tylerdurden1291/telegram-bot-recipes:mainimage
```

## Preparation

You need to first generate a telegram bot by following this [post](https://romain-gratier.medium.com/create-a-simple-bot-with-telegram-that-notifies-you-about-the-progress-of-your-code-69bab685b9db) on  [<img src="https://github.com/RomainGratier/telegram-coffee-break/blob/main/documents/medium.png" width="100"/>](https://romain-gratier.medium.com/create-a-simple-bot-with-telegram-that-notifies-you-about-the-progress-of-your-code-69bab685b9db). Or by following the steps below. Beware of keeping the bot token for you and not share it for security reasons. 

**First: You will need to create a new telegram bot as follows:**

Go to the BotFather (if you open it on desktop, make sure you have the Telegram app), then create a new bot by sending the /newbot command. Follow the steps until you get the username and token for your bot. You can go to your bot by accessing this URL: https://telegram.me/YOUR_BOT_USERNAME, and your token should look like this.

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
docker run -e token=<your_token> tylerdurden1291/telegram-bot-recipes:mainimage
```
