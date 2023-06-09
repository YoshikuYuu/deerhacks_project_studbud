import discord
from reminder import *
from db import *
from datetime import datetime
from discord.ext import commands, tasks

def run_discord_bot():

    ###
    TOKEN = 'MTEwMTMyNDY0MDg5MjI0NDAzMA.GpOKLH.1-G0Gu-hs9wgUPHKTpxbcDJyeXn3kDW9CC2xI0'

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='$', intents=intents)

    # Initialize database and sets conn and cursor
    conn, cursor = initialize_db()
    ###

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running')
        check_time.start()

    @bot.command(name="hi")
    async def hi(ctx):
        await ctx.send(f'Hi, {ctx.author.mention}')


    @bot.command(name='task')
    async def record_task(ctx, task: str, time_str: str):
        user_id = str(ctx.author.id)
        if not user_in_db(cursor, user_id):
            add_user_to_db(cursor, conn, user_id)
        try:
            # remember to convert time_str into the appropriate format
            p_time_str = datetime.strptime(time_str, '%H:%M')
            task_time = datetime.now()
            task_time = task_time.replace(hour=p_time_str.hour,
                                          minute=p_time_str.minute)
            f_task_time = task_time.strftime('%d/%m/%y %H:%M')
            print(f_task_time)

            add_task(cursor, conn, user_id, task, f_task_time)

            await ctx.send(f'Recorded task: "{task}". Reminder set for {f_task_time}.')

        except ValueError as e:
            await ctx.send(f'Error {e}. Invalid time format. Please use the format "HH:MM".')

    @bot.command(name='done')
    async def done_task(ctx, finished_task: str):
        tasks_dict = get_user_tasks(cursor, ctx.author.id)
        for task in tasks_dict:
            if finished_task == task:
                add_points(cursor, 50, ctx.author.id)
                delete_task(cursor, conn, ctx.author.id, finished_task)
                await ctx.send(f"Good job on completing {finished_task}! You've earned 50 points!")

    @bot.command(name='todo')
    async def display_todo(ctx):
        user_id = str(ctx.author.id)
        values = display_values(cursor, user_id)
        await ctx.send(f"Tasks to do for {ctx.author.mention} :)")
        for value in values:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return
            for key in value:
                await ctx.send(f'- {str(key)}')

    @bot.command(name="points")
    async def points(ctx):
        p = get_points(cursor, ctx.author.id)
        await ctx.send(f'You have {p} points.')

    @tasks.loop(minutes=1)
    async def check_time():
        reminders = get_reminders(cursor)
        current_datetime = datetime.now().strftime('%d/%m/%y %H:%M')
        print(current_datetime)

        if current_datetime in reminders:
            task_tups = send_reminders(cursor, current_datetime, bot)

            for task in task_tups:
                user = await bot.fetch_user(int(task[0]))
                await user.send(f"Reminder to complete task: {task[1]}")

    @check_time.before_loop
    # Waits for the bot to start up before beginning the check_time loop
    async def before_check_time():
        await bot.wait_until_ready()
        print("Starting loop.")


    @bot.command(name="buy")
    async def buy(ctx, item: str, quantity: int):
        # Allows user to buy items
        pts = get_points(cursor, ctx.author.id)
        if item == 'colours':
            if pts >= 30 * quantity:
                for i in range(quantity):
                    await ctx.send('```fix\nHello```')
                    await ctx.send('```arm\nHello```')
                    await ctx.send('```elm\nHello```')
                    await ctx.send('```ini\n[Hello]```')
                add_points(cursor, quantity * -30, ctx.author.id)
                pts = get_points(cursor, ctx.author.id)
                await ctx.send(f'Thank you for your purchase. You have {pts} points left in your account.')
            else:
                await ctx.send("You don't have enough points!")
        elif item == 'pixelart':
            if pts >= 50 * quantity:
                for i in range(quantity):
                    await ctx.send('□□□□□□□□□□□□□□□□□□□□□□□□□□■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□□□□□□■□□□□□□□□□□■□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□□□□□■□■□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□□□□■□□□□□□□□□□□□□■■■■■■□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□□□■□□□■□□□□□□□■□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□□□■□□□□□■□□□■□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□□□■□□□□□□□■□□□□□□□□□□□□□□□■■■■■□□■□□□■□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□□□■□□□□□■□□□■□□□□□□□□□□□□□■□□□■□□□□■□□□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□□□■□□□■□□□□□□□■□□□□□□□□□□□■■■■■□□■□□□■□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□■□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□')
                    await ctx.send('□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□')
                add_points(cursor, quantity * -50, ctx.author.id)
                pts = get_points(cursor, ctx.author.id)
                await ctx.send(f'Thank you for your purchase. You have {pts} points left in your account.')
            else:
                await ctx.send("You don't have enough points!")
        elif item == 'beginner':
            if pts >= 2:
                add_points(cursor, -2, ctx.author.id)
                pts = get_points(cursor, ctx.author.id)
                user = ctx.author
                beginner = discord.utils.get(ctx.guild.roles, name="Beginner")
                await user.add_roles(beginner)
                await ctx.send(f'Thank you for your purchase. You have {pts} points left in your account.')
            else:
                await ctx.send("You don't have enough points!")
        elif item == 'apprentice':
            if pts >= 10:
                add_points(cursor, -10, ctx.author.id)
                pts = get_points(cursor, ctx.author.id)
                user = ctx.author
                apprentice = discord.utils.get(ctx.guild.roles, name="Apprentice")
                await user.add_roles(apprentice)
                await ctx.send(f'Thank you for your purchase. You have {pts} points left in your account.')
            else:
                await ctx.send("You don't have enough points!")
        elif item == 'practitioner':
            if pts >= 100:
                add_points(cursor, -100, ctx.author.id)
                pts = get_points(cursor, ctx.author.id)
                user = ctx.author
                practitioner = discord.utils.get(ctx.guild.roles, name="Practitioner")
                await user.add_roles(practitioner)
                await ctx.send(f'Thank you for your purchase. You have {pts} points left in your account.')
            else:
                await ctx.send("You don't have enough points!")
        elif item == 'master':
            if pts >= 500:
                add_points(cursor, -500, ctx.author.id)
                pts = get_points(cursor, ctx.author.id)
                user = ctx.author
                master = discord.utils.get(ctx.guild.roles, name="Master")
                await user.add_roles(master)
                await ctx.send(f'Thank you for your purchase. You have {pts} points left in your account.')
            else:
                await ctx.send("You don't have enough points!")
        elif item == 'legend':
            if pts >= 2500:
                add_points(cursor, -2500, ctx.author.id)
                pts = get_points(cursor, ctx.author.id)
                user = ctx.author
                legend = discord.utils.get(ctx.guild.roles, name="Legend")
                await user.add_roles(legend)
                await ctx.send(f'Thank you for your purchase. You have {pts} points left in your account.')
            else:
                await ctx.send("You don't have enough points!")
        else:
            await ctx.send('Invalid item. Please try again')

    @bot.command(name="items")
    async def list_of_items(ctx):
        # Shows the list of all available items
        await ctx.send('These items are available in the store: Roles: beginner, apprentice, practitioner, master, legend, Effects: colours, pixelart')


    bot.run(TOKEN)
