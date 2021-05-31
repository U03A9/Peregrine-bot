import discord

async def command_status_triggered_embed(issuer_name, guild_name, user_id):

    # Set initial message here

    status_log_message = discord.Embed(
        title="Command triggered!!",
        description=f"`!status`\nDiscord User: {issuer_name}\nUser ID: {user_id}\nIssued In: {guild_name}",
        colour=discord.Colour.dark_blue(),
    )
  
    # Standard footer and author

    status_log_message.set_footer(
        text="This is a club member run Discord officially sponsored by Western Governors University. All interactions on this server are logged. All users agree to the Discord Terms of Service"
    )
    status_log_message.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/758331935054889020/39da98d02a59e22606e230e7afe6841a.png"
    )
    status_log_message.set_author(
        name="Peregrine",
        icon_url="https://cdn.discordapp.com/avatars/716442510423228496/f293e738c3559906120db7e4d43da13e.png?size=256",
    )

    return status_log_message