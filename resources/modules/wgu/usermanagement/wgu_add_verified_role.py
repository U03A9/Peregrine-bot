import discord


async def wgu_add_verified_role(self, VERIFIED_ROLE, UNVERIFIED_ROLE, member):
       
        try:

            await member.add_roles(
                discord.utils.get(payload.member.guild.roles, name=VERIFIED_ROLE)
            )

            await member.remove_roles(
               discord.utils.get(payload.member.guild.roles, name=UNVERIFIED_ROLE)
            )

    except Exception as e:
        print(e)
        errorMessage = "Failed to process verification role for new member: {}\nPlease hand verify this member or contact a bot developer".format(
            payload.member
        )
        await channel.send(content=errorMessage)

    return