import datetime
import discord
from discord_components import *
import mysql.connector
from random import randrange
import time

intents = discord.Intents.default()
intents.members = True

try:
    db = mysql.connector.connect(host = "host", user = "user", password = "password", database = "database")
except:
    print("Database error")

class MyClient(discord.Client):

    client = discord.ext.commands.Bot("!")

    #Einloggen
    async def on_ready(self):
        await client.change_presence(activity = discord.Game(name="Last restart at " + str(datetime.datetime.utcnow().strftime('%d %B %Y - %H:%M:%S')) + " (UTC±0)"))
        support_channel = client.get_channel(960916801104007173)
        profile_channel = client.get_channel(960916801104007172)
        DiscordComponents(client)
        run = True
        while run:
            history = await support_channel.history(limit = 1).flatten()
            if history == []:
                run = False
            else:
                await support_channel.purge(limit = 100)
        run = True
        while run:
            history = await profile_channel.history(limit = 1).flatten()
            if history == []:
                run = False
            else:
                await profile_channel.purge(limit = 100)
        embed = discord.Embed(title="Create a ticket", description="React with 📨 to create a ticket!", color=0x3498db, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Ticket support", icon_url="https://cdn.discordapp.com/attachments/470926100550123520/961103773697196052/ticket.png")
        await support_channel.send(embed=embed, components=[[Button(style=2, emoji="📨", custom_id="support_ticket_create")]])

        embed = discord.Embed(title="Create a channel where you can view your own Profile", description="React with 👤 to create your channel!", color=0x3498db, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Profile Channel", icon_url="https://cdn.discordapp.com/attachments/470926100550123520/961254698822803496/profile-removebg-preview.png")
        await profile_channel.send(embed=embed, components=[[Button(style=2, emoji="👤", custom_id="profile_channel_create")]])

        print("Bot ist online :D")

    async def on_button_click(self, interaction):
        if interaction.custom_id == "profile_channel_create":
            try:
                db.commit()
                dbcursor = db.cursor()
                dbcursor.execute("SELECT coins FROM users WHERE id = %s", (interaction.user.id,))
                coins = dbcursor.fetchall()[0][0]
            except:
                dbcursor = db.cursor()
                dbcursor.execute("INSERT INTO users (id, name, coins, settings) VALUES (%s, %s, %s, %s)", (
                interaction.user.id, str(interaction.user), 0, "1"))
                db.commit()
                coins = 0
            name = "profile-" + str(interaction.user.id)
            test = True
            for i in interaction.guild.channels:
                if i.name == name:
                    profile_channel = i
                    test = False
            if test:
                category = client.get_channel(961850191886041119)
                overwrites = {interaction.guild.default_role:discord.PermissionOverwrite(view_channel = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, send_messages = False, embed_links = False, attach_files = False, add_reactions = False, external_emojis = False, mention_everyone = False, manage_messages = False, read_message_history = False, send_tts_messages = False, use_slash_commands = False), interaction.user:discord.PermissionOverwrite(view_channel = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, send_messages = True, embed_links = True, attach_files = True, add_reactions = True, external_emojis = True, mention_everyone = True, manage_messages = False, read_message_history = True, send_tts_messages = False, use_slash_commands = False)}
                profile_channel = await interaction.guild.create_text_channel(name, category = category, sync_permissions = True, overwrites = overwrites)
                embed = discord.Embed(title = str(coins) + " 🪙", description = "👷 -> Go to work\n🧰 -> Open your inventory\n🔄 -> Update your profile in this channel\n⚙ -> Manage your profile settings\n🔒 -> close your profile channel", color = 0x3498db, timestamp = datetime.datetime.utcnow())
                embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar_url)
                await profile_channel.send(embed = embed, components = [[Button(style = 3, emoji = "👷", custom_id = "profile_channel_work"), Button(style = 2, emoji = "🧰", custom_id = "profile_channel_inventory"), Button(style = 1, emoji = "🔄", custom_id = "profile_channel_update"), Button(style = 2, emoji = "⚙", custom_id = "profile_channel_settings"), Button(style = 4, emoji = "🔒", custom_id = "profile_channel_close")]])
                await interaction.send(content = "Your profile channel has been created:\n" + profile_channel.mention, ephemeral = True)
            else:
                await interaction.send(content = "You have already created a profile channel:\n" + profile_channel.mention, ephemeral = True)
        elif interaction.custom_id == "profile_channel_work":
            try:
                await interaction.respond()
            except:
                pass
            embed = discord.Embed(title = "Select a job", description = "💰 -> Moneysorter\n🚪 -> Leave", color = 0x3498db, timestamp = datetime.datetime.utcnow())
            embed.set_author(name = "Jobcenter", icon_url = "https://cdn.discordapp.com/attachments/470926100550123520/962725666330120232/worker.png")
            await interaction.channel.send(embed = embed, components = [[Button(style = 2, emoji = "💰", custom_id = "profile_channel_work_moneysorter"), Button(style = 4, emoji = "🚪", custom_id = "profile_channel_work_cancel")]])
        elif interaction.custom_id == "profile_channel_work_moneysorter":

            try:
                await interaction.respond()
            except:
                pass
            user = await client.fetch_user(int(interaction.channel.name.split("-")[1]))
            if self.check_member(interaction.channel, user):
                await interaction.channel.delete()
            else:
                await interaction.message.add_reaction("💵")
                await interaction.message.add_reaction("💴")
                await interaction.message.add_reaction("💶")
                await interaction.message.add_reaction("💷")
                random = randrange(1, 5)
                if random == 1:
                    emoji = "💵"
                elif random == 2:
                    emoji = "💴"
                elif random == 3:
                    emoji = "💶"
                elif random == 4:
                    emoji = "💷"
                await interaction.channel.send("Click on " + emoji + " to work.")
                time.sleep(1)
                message = await interaction.channel.fetch_message(interaction.message.id)
                test = self.check_reaction(message, random)
                if test:
                    time.sleep(1)
                    message = await interaction.channel.fetch_message(interaction.message.id)
                    test = self.check_reaction(message, random)
                    if test:
                        time.sleep(1)
                        message = await interaction.channel.fetch_message(interaction.message.id)
                        test = self.check_reaction(message, random)
                        if test:
                            time.sleep(1)
                            message = await interaction.channel.fetch_message(interaction.message.id)
                            test = self.check_reaction(message, random)
                            if test:
                                time.sleep(1)
                                message = await interaction.channel.fetch_message(interaction.message.id)
                                test = self.check_reaction(message, random)
                if not test:
                    try:
                        db.commit()
                        dbcursor = db.cursor()
                        dbcursor.execute("SELECT coins FROM users WHERE id = %s", (user.id,))
                        coins = dbcursor.fetchall()[0][0]
                        dbcursor = db.cursor()
                        dbcursor.execute("UPDATE users SET coins = %s WHERE id = %s", (
                        coins + randrange(1, 4), user.id))
                        db.commit()
                    except:
                        dbcursor = db.cursor()
                        dbcursor.execute("INSERT INTO users (id, name, coins, settings) VALUES (%s, %s, %s, %s)", (
                        user.id, str(user), 0, "1"))
                        db.commit()
                history = await interaction.channel.history(limit = 1).flatten()
                await history[0].delete()
                await interaction.message.clear_reactions()
        elif interaction.custom_id == "profile_channel_work_cancel":
            await interaction.message.delete()
        elif interaction.custom_id == "profile_channel_inventory":
            print("TEST")
        elif interaction.custom_id == "profile_channel_update":
            user = await client.fetch_user(int(interaction.channel.name.split("-")[1]))
            if self.check_member(interaction.channel, user):
                await interaction.channel.delete()
            else:
                try:
                    db.commit()
                    dbcursor = db.cursor()
                    dbcursor.execute("SELECT coins FROM users WHERE id = %s", (user.id,))
                    coins = dbcursor.fetchall()[0][0]
                except:
                    dbcursor = db.cursor()
                    dbcursor.execute("INSERT INTO users (id, name, coins, settings) VALUES (%s, %s, %s, %s)", (
                    user.id, str(user), 0, "1"))
                    db.commit()
                    coins = 0
                run = True
                while run:
                    history = await interaction.channel.history(limit = 1).flatten()
                    if history == []:
                        run = False
                    else:
                        await interaction.channel.purge(limit = 100)
                embed = discord.Embed(title = str(coins) + " 🪙", description = "👷 -> Go to work\n🧰 -> Open your inventory\n🔄 -> Update your profile\n⚙ -> Manage your profile settings\n🔒 -> close your profile channel", color = 0x3498db, timestamp = datetime.datetime.utcnow())
                embed.set_author(name = user.name, icon_url = user.avatar_url)
                await interaction.channel.send(embed = embed, components = [[Button(style = 3, emoji = "👷", custom_id = "profile_channel_work"), Button(style = 2, emoji = "🧰", custom_id = "profile_channel_inventory"), Button(style = 1, emoji = "🔄", custom_id = "profile_channel_update"), Button(style = 2, emoji = "⚙", custom_id = "profile_channel_settings"), Button(style = 4, emoji = "🔒", custom_id = "profile_channel_close")]])
        elif interaction.custom_id == "profile_channel_settings":
            try:
                await interaction.respond()
            except:
                pass
            user = await client.fetch_user(int(interaction.channel.name.split("-")[1]))
            if self.check_member(interaction.channel, user):
                await interaction.channel.delete()
            else:
                await interaction.channel.send(components = [Select(placeholder = "Select what you want to change", options = [SelectOption(label = "Show your coins to other", value = "profile_channel_settings_coins")])])
        elif interaction.custom_id == "profile_channel_settings_coins_on":
            user = await client.fetch_user(int(interaction.channel.name.split("-")[1]))
            if self.check_member(interaction.channel, user):
                await interaction.channel.delete()
            else:
                try:
                    dbcursor = db.cursor()
                    dbcursor.execute("UPDATE users SET settings = %s WHERE id = %s", ("1", user.id))
                    db.commit()
                except:
                    dbcursor = db.cursor()
                    dbcursor.execute("INSERT INTO users (id, name, coins, settings) VALUES (%s, %s, %s, %s)", (
                    user.id, str(user), 0, "1"))
                    db.commit()
                await interaction.message.delete()
        elif interaction.custom_id == "profile_channel_settings_coins_off":
            user = await client.fetch_user(int(interaction.channel.name.split("-")[1]))
            if self.check_member(interaction.channel, user):
                await interaction.channel.delete()
            else:
                try:
                    dbcursor = db.cursor()
                    dbcursor.execute("UPDATE users SET settings = %s WHERE id = %s", ("0", user.id))
                    db.commit()
                except:
                    dbcursor = db.cursor()
                    dbcursor.execute("INSERT INTO users (id, name, coins, settings) VALUES (%s, %s, %s, %s)", (
                    user.id, str(user), 0, "0"))
                    db.commit()
                await interaction.message.delete()
        elif interaction.custom_id == "profile_channel_close":
            await interaction.channel.delete()
        elif interaction.custom_id == "support_ticket_create":
            name = "ticket-" + str(interaction.user.id)
            test = True
            for i in interaction.guild.channels:
                if i.name == name:
                    ticket_channel = i
                    test = False
            if test:
                category = client.get_channel(961311914112196628)
                for i in interaction.guild.roles:
                    if i.name == "Moderator":
                        moderator_role = i
                overwrites = {interaction.guild.default_role:discord.PermissionOverwrite(view_channel = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, send_messages = False, embed_links = False, attach_files = False, add_reactions = False, external_emojis = False, mention_everyone = False, manage_messages = False, read_message_history = False, send_tts_messages = False, use_slash_commands = False), interaction.user:discord.PermissionOverwrite(view_channel = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, send_messages = True, embed_links = True, attach_files = True, add_reactions = True, external_emojis = True, mention_everyone = True, manage_messages = False, read_message_history = True, send_tts_messages = False, use_slash_commands = False), moderator_role:discord.PermissionOverwrite(view_channel = True, manage_channels = False, manage_permissions = True, manage_webhooks = False, create_instant_invite = False, send_messages = True, embed_links = True, attach_files = True, add_reactions = True, external_emojis = True, mention_everyone = True, manage_messages = False, read_message_history = True, send_tts_messages = False, use_slash_commands = False)}
                ticket_channel = await interaction.guild.create_text_channel(name, category = category, sync_permissions = True, overwrites = overwrites)
                embed = discord.Embed(title = "Manage the ticket", description = "React with 🔒 to close the ticket!", color = 0x3498db, timestamp = datetime.datetime.utcnow())
                embed.set_author(name = "Ticket support", icon_url = "https://cdn.discordapp.com/attachments/470926100550123520/961103773697196052/ticket.png")
                await ticket_channel.send(embed = embed, components = [
                    [Button(style = 4, emoji = "🔒", custom_id = "support_ticket_close")]])
                await interaction.send(content = "Your ticket has been created:\n" + ticket_channel.mention, ephemeral = True)
            else:
                await interaction.send(content = "You have already created a ticket:\n" + ticket_channel.mention, ephemeral = True)
        elif interaction.custom_id == "support_ticket_close":
            test = False
            for i in interaction.user.roles:
                if i.name == "Developer":
                    test = True
                elif i.name == "Admin":
                    test = True
                elif i.name == "Moderator":
                    test = True
            if test:
                category = client.get_channel(961829336153980948)
                overwrites = {interaction.guild.default_role:discord.PermissionOverwrite(view_channel = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, send_messages = False, embed_links = False, attach_files = False, add_reactions = False, external_emojis = False, mention_everyone = False, manage_messages = False, read_message_history = False, send_tts_messages = False, use_slash_commands = False)}
                history = await interaction.channel.history(limit = 1, oldest_first = True).flatten()
                for i in history:
                    await i.delete()
                await interaction.channel.edit(category = category, overwrites = overwrites)
                embed = discord.Embed(title = "React with 🗑️ to delete the ticket!", description = "Ticket was closed by " + interaction.user.mention, color = 0x3498db, timestamp = datetime.datetime.utcnow())
                embed.set_author(name = "Ticket support", icon_url = "https://cdn.discordapp.com/attachments/470926100550123520/961103773697196052/ticket.png")
                await interaction.channel.send(embed = embed, components = [[Button(style = 4, emoji = "🗑️", custom_id = "support_ticket_delete")]])
            else:
                await interaction.send(content = "You are not allowed to close the Ticket!", ephemeral = True)
        elif interaction.custom_id == "support_ticket_delete":
            await interaction.channel.delete()

    async def on_select_option(self, interaction):
        selected = interaction.values[0]
        if selected == "profile_channel_settings_coins":
            user = await client.fetch_user(int(interaction.channel.name.split("-")[1]))
            try:
                db.commit()
                dbcursor = db.cursor()
                dbcursor.execute("SELECT settings FROM users WHERE id = %s", (user.id,))
                settings = dbcursor.fetchall()[0][0]
            except:
                settings = "1"
            if settings == "1":
                msg = "✅"
            else:
                msg = "❌"
            embed = discord.Embed(title = "Show your coins to other is currently " + msg, description = "✅ -> Make your coins public\n❌ -> Hide your coins from the public", color = 0x3498db, timestamp = datetime.datetime.utcnow())
            embed.set_author(name = "Settings", icon_url = "https://cdn.discordapp.com/attachments/470926100550123520/962188370572877874/settings-removebg-preview.png")
            await interaction.channel.send(embed = embed, components = [
                [Button(style = 3, emoji = "✅", custom_id = "profile_channel_settings_coins_on"),
                    Button(style = 1, emoji = "❌", custom_id = "profile_channel_settings_coins_off")]])
        await interaction.message.delete()

    def check_member(self, channel, user):
        if channel.name.startswith("profile-"):
            test = True
            for i in channel.guild.members:
                if i.name == user.name:
                    test = False
            return test

    def check_reaction(self, message, random):
        test1 = True
        test2 = False
        for i in message.reactions:
            if i.emoji == "💵":
                if random == 1:
                    if i.count == 2:
                        test2 = True
                elif i.count == 2:
                    test1 = False
            elif i.emoji == "💴":
                if random == 2:
                    if i.count == 2:
                        test2 = True
                elif i.count == 2:
                    test1 = False
            elif i.emoji == "💶":
                if random == 3:
                    if i.count == 2:
                        test2 = True
                elif i.count == 2:
                    test1 = False
            elif i.emoji == "💷":
                if random == 4:
                    if i.count == 2:
                        test2 = True
                elif i.count == 2:
                    test1 = False
        if test1:
            if test2:
                return False
            else:
                return True
        else:
            return True

    #Wenn jemand eine Reaktion hinzufügt
    # async def on_raw_reaction_add(self, payload):
    #     guild = client.get_guild(payload.guild_id)
    #     channel = guild.get_channel(payload.channel_id)
    #     message = await channel.fetch_message(payload.message_id)
    #     if channel.name == "profile-" + str(payload.user_id):
    #         print(str(message.reactions))
    #         if not message.reactions == []:
    #             print("TEST")

    #Wenn jemand auf den Server joint
    async def on_member_join(self, member):
        welcome_channel = client.get_channel(960916801104007169)
        embed = discord.Embed(title = str(member) + " has entered the club.", description = "With an alcohol level of " + str(randrange(0, 5)) + "," + str(randrange(0, 10)) + "%", color = 0x3498db, timestamp = datetime.datetime.utcnow())
        embed.set_author(name = "The Bouncer", icon_url = "https://cdn.discordapp.com/attachments/470926100550123520/961905247587037216/tursteher.png")
        embed.set_image(url = member.avatar_url)
        await welcome_channel.send(embed = embed)

    #Wenn jemand den Server verlässt
    async def on_member_remove(self, member):
        welcome_channel = client.get_channel(960916801104007169)
        embed = discord.Embed(title = str(member) + " has exited the club.", description = "With an alcohol level of " + str(randrange(0, 5)) + "," + str(randrange(0, 10)) + "%", color = 0x3498db, timestamp = datetime.datetime.utcnow())
        embed.set_author(name = "The Bouncer", icon_url = "https://cdn.discordapp.com/attachments/470926100550123520/961905247587037216/tursteher.png")
        embed.set_image(url = member.avatar_url)
        await welcome_channel.send(embed = embed)

    #Wenn eine Nachricht gepostet wird
    async def on_message(self, message):
        if message.author == client.user:
            return
        if str(message.author) == "Melmacker#7448":
            if message.content.startswith("!"):
                if message.content == "!clear":
                    await message.channel.purge(limit = 100)

client = MyClient(intents = intents)
client.run("YOURTOKEN")
