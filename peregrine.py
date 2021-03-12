#!/usr/bin/python3
'''Discord bot for WGU Discord Clubs'''

# Import required modules

import os
from dotenv import load_dotenv
import discord
import discord.utils
from discord.ext import commands

# Import core custom modules
from modules.core.peregrine_check_status import peregrine_check_status
from modules.core.peregrine_connect_database import peregrine_connect_database

# Import wgu custom database modules
from modules.wgu.database.database_check_existing_records import database_check_existing_records
from modules.wgu.database.database_create_new_entry import database_create_new_entry
from modules.wgu.database.database_check_verification_pin import database_check_verification_pin
from modules.wgu.database.database_push_to_verified import database_push_to_verified

# Import wgu custom email modules
from modules.wgu.email.email_send_verification_code import email_send_verification_code

# Import custom embed message modules
from modules.wgu.embeds.database_already_exists_embed import database_already_exists_embed
from modules.wgu.embeds.wgu_email_sent_embed import wgu_email_sent_embed
from modules.wgu.embeds.wgu_invalid_email_embed import wgu_invalid_email_embed
from modules.wgu.embeds.wgu_verification_invalid_code_embed import wgu_verification_invalid_code_embed
from modules.wgu.embeds.wgu_verification_successful_embed import wgu_verification_successful_embed
from modules.wgu.embeds.wgu_check_email_for_code_embed import wgu_check_email_for_code_embed
from modules.wgu.embeds.wgu_send_verification_start_embed import wgu_send_verification_start_embed

# Import environment variables

load_dotenv()

TOKEN = os.getenv('bot_token')
GUILD_ID = os.getenv('guild_id')
LOG_CHANNEL = os.getenv('log_channel_id')
VERIFICATION_CHANNEL = os.getenv('verification_channel_id')
VERIFICATION_MESSAGE = os.getenv('verification_message_id')
ENROLLMENT_MESSAGE = os.getenv('enrollment_self_role_message_id')
SUBSCRIPTION_MESSAGE = os.getenv('subscription_self_role_message_id')
VERIFIED_ROLE = os.getenv('verified_role_name')
UNVERIFIED_ROLE = os.getenv('unverified_role_name')
VERIFICATION_EMOJI = os.getenv('verification_emoji')
STUDENT_EMOJI = os.getenv('student_emoji')
ALUMNI_EMOJI = os.getenv('alumni_emoji')
CCDC_SUB_EMOJI = os.getenv('ccdc_sub_emoji')
NICE_SUB_EMOJI = os.getenv('nice_sub_emoji')
CTF_SUB_EMOJI = os.getenv('ctf_sub_emoji')
HTB_SUB_EMOJI = os.getenv('htb_sub_emoji')
THM_SUB_EMOJI = os.getenv('thm_sub_emoji')
OTW_SUB_EMOJI = os.getenv('otw_sub_emoji')
NCL_SUB_EMOJI = os.getenv('ncl_sub_emoji')
FOREIGN_SUB_EMOJI = os.getenv('foreign_sub_emoji')
DM_MESSAGE = os.getenv('dm_verification_message')
SRC_EMAIL = os.getenv('bot_email_address')
EMAIL_PASS = os.getenv('bot_email_password')
DB_USER = os.getenv('database_username')
DB_PASS = os.getenv('database_username_password')
DB_IPV4 = os.getenv('database_ipv4_address')
# DB_IPV6 = os.getenv('database_ipv6_address')
DB_NAME = os.getenv('database_name')

# Set up additional parameters for commands and intents

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.typing = True
intents.presences = True
intents.reactions = True

# Setup database connection

# Define bot under the commands framework

peregrine = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

# Jail all new members

@peregrine.event
async def on_member_join(member):
    '''Set users to Unverified when they join'''

    # Alert console of new member and push to log channel

    on_member_join_message = "Event triggered: Member joined\n   Member: {}".format(
        member
    )
    print(on_member_join_message)

    # Auto assign unverified role to new members and set nickname defaults

    await member.add_roles(discord.utils.get(member.guild.roles, name="Unverified"))

@peregrine.event
async def on_raw_reaction_add(payload):
    '''This function tells the bot to DM people who react to the verification message'''

    if str(payload.message_id) == str(VERIFICATION_MESSAGE):

        print("Triggering verification")

        # Set log channel

        channel = peregrine.get_channel(int(LOG_CHANNEL))
        print("Log channel set")

        # Alert console of member leaving and push to log channel

        on_reaction_add_verification_alert = (
            "Event triggered: Member verification reaction\n   Member: {}".format(payload.member)
        )

        print(on_reaction_add_verification_alert)
        await channel.send(content=on_reaction_add_verification_alert)

        # Initiate email verification process

        if str(payload.emoji.name) == str(VERIFICATION_EMOJI):
            await peregrine.get_user(payload.user_id).send(embed= await wgu_send_verification_start_embed(payload.member))

        return

# Main bot commands

@peregrine.command(name='status', description="Print connection status")
@commands.has_any_role("Administrator", "Moderator")
async def status(ctx):
    '''This function displays status information to the channel it is issued in'''

    # Get connection status of database
    database_status = await peregrine_connect_database(DB_IPV4, DB_USER, DB_PASS, DB_NAME)

    print("Verifying connection to database...\n")

    if bool(database_status.is_connected()) is True:

        try:
            print(f"\tCurrent database status is: {database_status.is_connected()}\n")

        except Exception as exception_message:
            print(exception_message)

    if bool(database_status.is_connected()) is False:

        try:
            message = "Unable to connect to database. Please verify credentials in\
             environment file are correct"
            print(message)
            print(f"\tCurrent database status is: {database_status.is_connected()}")
            return

        except Exception as exception_message:
            print(exception_message)
            return exception_message

    # Send message in triggered channel with bot status embed
    await ctx.send(embed= await peregrine_check_status(ctx.author.name, ctx.guild,
     ctx.guild.id, database_status.is_connected()))

# Verification process commands

@peregrine.command(name='email', description="Collect user email for verification")
async def email(ctx, user_email):
    '''This function collects the email from a wgu user for verification'''

    # Check if email is a valid wgu email address

    if user_email.split('@')[-1] != "wgu.edu":
        await ctx.send(embed= await wgu_invalid_email_embed(user_email))
        return

    # Check database for email entry

    email_check_result = await database_check_existing_records(
        await peregrine_connect_database(DB_IPV4, DB_USER, DB_PASS, DB_NAME), user_email)

    # Send message to alert member this email is already verified

    if email_check_result[0] is True and email_check_result[1] is False and str(email_check_result[2]) == str(ctx.author.id):

        # Set member to verified if Discord ID and email match verification entry

        guild = peregrine.get_guild(int(GUILD_ID))
        member = discord.utils.find(lambda m : m.id == ctx.message.channel.recipient.id, guild.members)
        await member.add_roles(discord.utils.get(guild.roles, name=VERIFIED_ROLE))
        await member.remove_roles(discord.utils.get(guild.roles, name=UNVERIFIED_ROLE))
        await member.edit(nick=email_check_result[0][3])

        # Send message to alert them that they have been verified

        await ctx.send(embed=await wgu_verification_successful_embed(ctx.author.name))

    if email_check_result[0] is False and email_check_result[1] is True and str(email_check_result[2]) != str(ctx.author.id):

        # Send message to alert them this email is already registered

        await ctx.send(embed=await database_already_exists_embed(user_email))

    if email_check_result[0] is False and email_check_result[1] is True and str(email_check_result[2]) == str(ctx.author.id):

        await ctx.send(embed= await wgu_check_email_for_code_embed(user_email))

    if email_check_result[0] is False and email_check_result[1] is False and email_check_result[2] is False:

        # Create new database entry for user

        await database_create_new_entry(await peregrine_connect_database(DB_IPV4, DB_USER,
         DB_PASS, DB_NAME), user_email, ctx.author.name, ctx.author.id)

        # Send message to user to alert them that the email and pincode has been sent

        await email_send_verification_code(await peregrine_connect_database(DB_IPV4, DB_USER,
        DB_PASS, DB_NAME), user_email, SRC_EMAIL, EMAIL_PASS)
        await ctx.send(embed= await wgu_email_sent_embed(user_email))

@peregrine.command(name='verify', description='Collects verification pin from user')
async def verify(ctx, submitted_auth_code):
    '''This function checks submitted auth code against database and validates Discord ID'''

    print(f"Submitted pin is: {submitted_auth_code}")

    auth_check_result = await database_check_verification_pin(await peregrine_connect_database(
        DB_IPV4, DB_USER, DB_PASS, DB_NAME), ctx.author.id, submitted_auth_code)

    if auth_check_result is True:

        # Push user information from auth table to verified table

        await database_push_to_verified(await peregrine_connect_database(
        DB_IPV4, DB_USER, DB_PASS, DB_NAME), ctx.author.id)

        # Set member to verified

        guild = peregrine.get_guild(int(GUILD_ID))
        member = discord.utils.find(lambda m : m.id == ctx.message.channel.recipient.id, guild.members)
        await member.add_roles(discord.utils.get(guild.roles, name=VERIFIED_ROLE))
        await member.remove_roles(discord.utils.get(guild.roles, name=UNVERIFIED_ROLE))
        await member.edit(nick=auth_check_result[0][3])

        # Send message to alert them that they have been verified

        await ctx.send(embed=await wgu_verification_successful_embed(ctx.author.name))

    if auth_check_result is False:
        await ctx.send(embed=await wgu_verification_invalid_code_embed(submitted_auth_code))

# Moderation management commands

# Administrator management commands

# Start the bot

peregrine.run(TOKEN)