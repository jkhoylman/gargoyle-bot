# gargoyle-bot
Simple Discord bot for the server my friends and I use.

# Commands
- !help: Lists all commands available to all users
- !wisdon: Sends a message with a random "wise" quote one of us has said in the past.  I plan on adding an optional argument at some point to request a quote from a specific person
- !kill: Logs out the bot and kills this script. Available only to server admins

# Features
Every 15 minutes, the bot counts the number of messages sent in a specified channel since the last count. If any have been sent, it sends a direct message with this information to specified users.  I added this because I was having trouble receiving notifications on mobile.

I'v been having issues where occasionally the number of times this was called would increase, causing the number of times I would be notified for a given 15 minute interval to balloon over time.  Currently looking into a fix for this.
