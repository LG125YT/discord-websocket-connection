# discord-websocket-connection
Basic websocket connections specifically built for Discord and similar sites, can be used in old discord revivals like Hummus and Oldground.

## Notice:
If you are working with a website like Fosscord/Spacebar, please use [Fossbotpy](https://gitlab.com/arandomnewaccount/fossbotpy) instead.

## About:
This project is made for Hummus, it provides a working bot to function on it. Hummus is a Discord 2016 revival.

This project is very basic, its made for the people who are too lazy to go figure out websocket connections themselves.

In the project's `check` function, all messages are checked and this is where you add new commands. The only command in this example is a simple response to a test command. Having your bot perform actions has to be done so through raw POST, GET, and PATCH requests to the API, since no wrapper is involved in this project. For information on Discord/Hummus's v6 API, read through [the documentation.](https://oldground.haydar.dev/developers/docs/intro)
