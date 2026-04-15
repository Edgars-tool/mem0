# Discord 機器人

這是一個 Docker 範本，可讓您使用 embedchain 套件建立自己的 Discord 機器人。若要進一步了解機器人及其使用方法，請前往[這裡](https://docs.embedchain.ai/examples/discord_bot)。

若要執行此操作，請使用以下命令，

```bash
docker run --name discord-bot -e OPENAI_API_KEY=sk-xxx -e DISCORD_BOT_TOKEN=xxx -p 8080:8080 embedchain/discord-bot:latest
```