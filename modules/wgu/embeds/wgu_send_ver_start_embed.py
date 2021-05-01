import discord

async def wgu_send_ver_start_embed(discord_member):

    # Set initial message here

    verification_start_message = discord.Embed(
        title="Verification Process!",
        description=f"Hello {discord_member},\nWelcome to the WGU Cyber Club. Before you continue, we'd like to make you aware of a few things you are agreeing to before you complete the verification process.\n\nReady for verification? Simply reply to me with\n\n`!email <your student email>` (e.x: !email jdoe@wgu.edu)\n\nto begin the process. If you need assistance, please contact a moderator in [#verification-support](https://discordapp.com/channels/688822375327989875/768993144380981248)",
        colour=discord.Colour.dark_blue(),
    )

    verification_start_message.set_image(
        url='https://cdn.discordapp.com/attachments/819072570266877992/823683896414699561/submit_your_email.gif'
    )

    # Standard footer and author

    verification_start_message.set_footer(
        text="This is a club member run Discord officially sponsored by Western Governors University. All interactions on this server are logged. All users agree to the Discord Terms of Service"
    )
    verification_start_message.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/758331935054889020/39da98d02a59e22606e230e7afe6841a.png"
    )
    verification_start_message.set_author(
        name="Peregrine",
        icon_url="https://cdn.discordapp.com/avatars/716442510423228496/f293e738c3559906120db7e4d43da13e.png?size=256",
    )

    return verification_start_message