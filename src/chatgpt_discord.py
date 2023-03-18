import discord
import openai
import os

# ここにDiscord Botのトークンをお張りください。
DISCORD_TOKEN = ""
def question_chatgpt(content_question, token, model):
    openai.api_key = token
    response = openai.ChatCompletion.create(
        model=str(model),
        messages=[
            {"role": "user", "content": str(content_question)}
        ]
    )
    content_answer = response.choices[0]["message"]["content"].strip()
    return content_answer

def chatgpt_discord():
    client = discord.Client(intents=discord.Intents.all())
    @client.event
    async def on_ready():
        chat_gpt_token = [False, ""]
        print('初めまして Chatgpt-Discordでございます！\nまず、/set-chat (ChatgptのAPIトークン) と入力して、ChatgptのAPIトークンを入力してください。\n/chatをつけて質問を投稿したら\n回答が返ってきます。\nぜひ使ってみてください。')
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content.startswith('/token-chatgpt'):
            file = open("chat-gpt-token.txt", mode='w')
            file.write(str(message.content).replace('/set-chat ', ''))
            file.close()
            await message.channel.send("設定しました！")
        if message.content.startswith('/chatgpt'):
            try:
                if os.path.isfile("chat-gpt-token.txt"):
                    file = open("chat-gpt-token.txt")
                    token_chatgpt = file.read()
                    content_question = message.content.replace('/chat ', '')
                    content_answer = question_chatgpt(content_question, token_chatgpt, "gpt-3.5-turbo")
                    await message.channel.send(content_answer)
                else:
                    await message.channel.send("申し訳ございません。\nChatGptのApiトークンが設定されていないので、質問することができません。")
            except Exception as excep:
                    await message.channel.send("エラーが発生しました。\n"+str(excep))
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    chatgpt_discord()