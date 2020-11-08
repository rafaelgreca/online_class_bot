# Online Class Bot

We all know that online classes are boring, so let the bot attend them for you!

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

## Installation

Repo and readme still under construction!

## Installation

Clone the repository using the following code:

```bash
git clone https://github.com/rafaelgreca/online_class_bot.git
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

or

```bash
pip3 install -r requirements.txt
```

## How to use

First of all you need to configure the "classes.csv". You **have to** add classes using the same format and the week day **must be** wrote in English.

After doing that and cloning the repository, you need to create a **.env** file inside the folder and add the following lines:

```bash
EMAIL=YOUR_EMAIL_LOGIN
PASSWORD=YOUR_EMAIL_PASSWORD
BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
```

All your notifications about attending the classes will be received in the Discord. So you **must have** a text channel called "online-classes" and a bot token to send the messages. (Still improving this part to make it easier to use)

## How it works

The bot will schedule all your classes using the csv file with the information. Then, when the time comes, it will attend to the class. It will leave automatically when the majority of the people leaves and send a notification on your Discord chat.

## Works on

- [x] Google Meet
- [ ] Microsoft Team (Coming soon)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)