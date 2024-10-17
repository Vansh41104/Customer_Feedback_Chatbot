# Customer Feedback Chatbot

## Installation

We are using Python 3.12.1 for this project, you can create seperate conda/virtual environment with same python verson

For install requires packages 

```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

create .env file in folder home directory and copy paste below key-value
add your openai key below

```
OPENAI_API_KEY=
```

## For SQL bot to run

```
cd sql_bot
chainlit run app.py -w
```

## For CSV bot to run

```
cd csv_bot
chainlit run bot.py -w
```

# Deployment steps

Push code to master.

Next, SSH into the server and navigate to the project directory, and pull the latest code

```
ssh -i ~/.ssh/customer-feedback-chatbot.pem ubuntu@35.180.17.113
cd ~/chat_bot/customer-feedback-chatbot
git reset --hard
git pull
```

Now, attach to the terminal sessions that the bot is running in

```
tmux attach -t 3
```

Once inside th terminal session where the bot is running, press `Ctrl + C` to kill the bot script. Then
once again start the bot script

```
chainlit run app.py --headless
```

Then, to detach from the terminal session, press Ctrl+b, then d.

Feel free to now exit the server

You can then find your app running on

http://35.180.17.113:8000