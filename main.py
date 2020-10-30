import discord
import config
from botCommand import dbStatement, removeBracketsFrom
import mysql.connector

client = discord.Client()

db = mysql.connector.connect(
    host='HOSTNAME_HERE',
    user='USERNAME_HERE',
    passwd='PASSWORD_HERE',
    database='DB_NAME_HERE'
)


@client.event
async def on_ready():
    print(f'Logged on as {client.connection.user}!')


@client.event
async def on_raw_reaction_add(payload):  # give role to a user
    message_id = payload.message_id
    if message_id == config.POST_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        string_role = removeBracketsFrom(dbStatement(db, payload.emoji.name))
        role = discord.utils.get(guild.roles, name=string_role)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print(f'[SUCCESS] User: {member.display_name} has been granted with role: {role.name}')
            else:
                print('[ERROR] Member not found')
        else:
            print('[ERROR] Role not found')


@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == config.POST_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        string_role = removeBracketsFrom(dbStatement(db, payload.emoji.name))
        role = discord.utils.get(guild.roles, name=string_role)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print(f'[SUCCESS] User: {member.display_name} has removed the role: {role.name}')
            else:
                print('[ERROR] Member not found')
        else:
            print('[ERROR] Role not found')


@client.event
async def on_message(message):  # выдача лога сообщений. работает пока бот онлайн
    if message.author != client.user:  # Проверка на пользователя (чтобы бот сам от себя не циклился)
        print(f'{message.created_at}: {message.channel}: {message.author}: {message.content}')

    if (message.content.find('Майя') != -1 or  # основные функции
        message.content.find('M.A.I.A.') != -1 or
        message.content.find('майя') != -1) and (message.content.find('привет') != -1 or
                                                 message.content.find('поздоровайся') != -1 or
                                                 message.content.find('помощь') != -1 or
                                                 message.content.find('хелп') != -1):
        await message.channel.send(config.HELP_INFO)


def read_token():
    return config.TOKEN


client.run(read_token())
