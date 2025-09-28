import discord
from discord.ext import commands
import asyncio


intents = discord.Intents.default()
intents.message_content = True

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
TOKEN = "KENDI_TOKENIN"

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Discord botun aktif! {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❌ Komut Bulunamadı",
            description="Böyle bir komut yok. `!komutlar` yazarak tüm komutları görebilirsin.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        raise error

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: str = None, *, reason="Sebep belirtilmedi."):
    if user is None:
        await ctx.send("❌ Kullanıcı bulunamadı. Etiket veya ID kullanın.")
        return

    try:
        # ID ile banlama
        if user.isdigit():  # Kullanıcı ID verdiyse
            user_obj = discord.Object(id=int(user))
            await ctx.guild.ban(user_obj, reason=reason)
            embed_desc = f"<@{user}> sunucudan banlandı."
        else:  # Kullanıcıyı etiket ile banlama
            member = await commands.MemberConverter().convert(ctx, user)
            await ctx.guild.ban(member, reason=reason)
            embed_desc = f"{member} sunucudan banlandı."

        embed = discord.Embed(
            title="🚫 Kullanıcı Banlandı",
            description=embed_desc,
            color=discord.Color.red()
        )
        embed.add_field(name="Sebep", value=reason, inline=False)
        embed.set_footer(text=f"Banlayan: {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("❌ Ban atılamadı.")
        print(f"Hata: {e}")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Sebep belirtilmedi."):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member} kicklendi. Sebep: {reason}")
    except:
        await ctx.send("❌ Kick atılamadı.")

bot.run(TOKEN)
