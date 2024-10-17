# Setting up an AWS EC2 instance with the Chatbot

Once the EC2 instance has been setup, SSH into the EC2 instance, e.g

```bash
ssh -i ~/.ssh/customer-feedback-chatbot.pem ubuntu@51.112.52.47
```

## Setting up SSH Keys on the EC2 instance

Run the following in the home directory to generate the public/private SSH key pair.
Then add it to the SSH agent

```bash
ssh-keygen -t rsa -b 4096 -C "ubuntu@51.112.52.47"
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub
```
Now paste the key as a new SSH key inside the Github Account

https://github.com/settings/keys

Inside the EC2 instance, create a directory for the project, and clone the repository

```bash
mkdir ~/chat_bot
cd ~/chat_bot
git clone git@github.com:smaameri/customer-feedback-chatbot.git
```

Now move into the project directory, and setup the .env file

```bash
cd ~/chat_bot/customer-feedback-chatbot
vi .env
```

Update the server, and install pip and venv
```bash
sudo apt-get update
sudo apt install python3-pip
sudo apt install python3.12-venv
```

Install and start MySQL (should be done before installing PIP packages)
```bash
sudo apt install mysql-server
sudo apt install libmysqlclient-dev
sudo systemctl start mysql.service
```

Or if using Postgres
```bash
sudo apt-get install libpq-dev
```

Setup a user in MySql

mysql -u root -p
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'admin'@'localhost' WITH GRANT OPTION;

(setting up the postgres database with sufficient privelages for a user admin)
```bash
```python
GRANT ALL PRIVILEGES ON DATABASE "kanari_insights" to admin;
grant usage on schema public to admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON DATABASE "kanari_insights" to admin;
ALTER USER admin WITH SUPERUSER;
```


Now setup the virtual environment, and install the required python packages for the project
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Or if using Poetry
sudo apt install python3-poetry




