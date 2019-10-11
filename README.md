# webhook_bot
This dirty script listens websocket, receives submitted JSON messages, if JSON contains 'CommonLabes' field it formats them to  user-readable fromat and
sends them to telegram.

This script is configured  by OS environment variables:  
**BOT_TOKEN** - Telegram bot token, received from BotFather  
**PROXY_URL** - proxy server URL (eg.: socks5://proxy.tg.io)  
**PROXY_USER** - username  
**PROXY_PASSWORD** - password  
**USER_LIST** - comma-separated chat_id list. (only commas, no additional spaces allowed)  
