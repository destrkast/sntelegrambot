# sntelegrambot v2.0.0
This is a simple example on how to create a telegram bot and connect it to a ServiceNow instance.
## Step 1
- Create a telegram bot via https://t.me/BotFather in telegram app.
- There you can set name and logo of the bot. Most important  - you'll get a token for telegram bot.
## Step 2
- Copy script
- Install all the required(imported) libraries
- Replace Token and ServiceNow instance url with yours.
- To build requests to ServiceNow use REST API Explorer for the desired table.
- To send messages to the chat just create REST message in ServiceNow and use this url template: https://api.telegram.org/bot{token}/sendMessage (you can use this for incident state updates and so on).
  Example payload:
  {
        "chat_id": "1850673",
        "text": "TEST",
        "parse_mode": "Markdown"

}
You should store chat_id on user table on a dedicated field or as a JSON attachment for each user.
## Step 3
- Modify it to you needs. Telegram API is huge, Chat-GPT will help you ;)
