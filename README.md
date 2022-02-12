# aiogram-template

### [![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/downloads/)  [![Aiogram](https://img.shields.io/badge/aiogram-3-blue)](https://pypi.org/project/aiogram/) 

### About
A template for creating bots as quickly as possible. Written on [aiogram](https://github.com/aiogram/aiogram). Contains a lot of tools right out of the box, such as broadcasting, simple statistics, new user notifications, etc.

### Setting up

#### Preparations
- Update package lists `sudo apt-get update`;
- Make sure Git and docker-compose are installed `apt-get install git docker-compose -y`;
- Clone this repo via `git clone https://github.com/rdfsx/aiogram-template`;
- Move to the directory `cd aiogram-template`.

#### Deployment
- Rename `.env.sample` to `.env` and replace a token placeholder and owner id with your own one;
- Start the bot: `sudo docker-compose up`.
