import discord
import asyncio
import subprocess
from discord.ext import commands
from command import *
from _token import get_token


class Un_bot_mal_code(discord.Client):

    def __init__(self):
        super().__init__()
        self.admin = admin = [200227803189215232,  # p0slx
                              205434999888019456,  # Andrew
                              194852069004410880]  # Nathan

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def call_script(self):        # func to call a bash script
        subprocess.call("./script.sh")  # call the bash script in a subprocess

    async def read_file(self, file, line_min):
        with open(file, 'r') as f:
            final = ""                              # init final string
            line_number = 0                         # init line number as int
            line_max = line_min + 35                # print max 35 lines
            for line in f:                          # for each line in file
                if line_number < line_min:          # if not reached minumum line to read
                    pass                            # continue to read line
                elif line_number == line_max:       # if reach line max
                    return final                    # return final string
                else:                               # if reached minimum line to read
                    if line.startswith("Script") or line.startswith("<?xml"):  # Filter
                        pass                        # keep reading
                    else:
                        final += line               # append line to final string
                line_number += 1                    # increase line number
            return final                            # return final string

    async def get_command_name(self, command: str):  # all is in the name
        return command.split()[0]                    # return only the command

    async def is_supported(self, command: str):
        return True if command not in non_supported_command else False

    async def write_command(self, ctx, command: str):
        try:
            with open("script.sh", 'w') as f:
                f.write(find_command(await self.get_command_name(command), command))
        except PermissionError:
            await ctx.channel.send("Error : Permission Denied")

    async def send_message(self, ctx, line_min):
        await self.call_script()                                # exec script.sh
        output = await self.read_file("output.txt", line_min)   # read output.txt
        if len(output) > 2:                                     # if message not empty
            await ctx.channel.send(("```" + output + "```"))    # print output in code format
        else:                                                   # if message empty
            await ctx.channel.send("Done.")                     # Send "Done."

    async def on_message(self, ctx):
        if ctx.author.id == self.user.id:                       # return if new message is self
            return

        if ctx.content.startswith('$') and ctx.author.id in self.admin:  # Set your id here, so only you can use it
            command = ctx.content[1:]                                    # trim $ char
            if command != "":                                            # check is command empty
                if await self.get_command_name(command) == "cpu":        # command for CPU usage
                    await self.write_command(ctx, "mpstat -P ALL")       # write "mpstat -P ALL" to bash script
                    await self.send_message(ctx, 0)                      # send message

                elif await self.get_command_name(command) == "man":      # if man command issued
                    try:                                                 # try the following line
                        int(command[-1])                                 # check if last letter is a number
                        nb_page = ""                                     # init page number as str
                        for letter in command[::-1]:                     # reverse order str
                            if letter != " ":                            # if space is current letter
                                nb_page = letter + nb_page               # add page number tu final string
                            else:                                        # end of parsing page number
                                await self.write_command(ctx, command[:-len(nb_page)]) # write only command and argument in file
                                await self.send_message(ctx, int(nb_page)) # send message at line nb_page
                                return                                   # exit loop
                    except ValueError:                                   # if last letter NaN
                        await self.write_command(ctx, command)           # write usual
                        await self.send_message(ctx, 0)                  # send message
                else:                                                    # all other command goes here
                    await self.write_command(ctx, command)               # write usual
                    await self.send_message(ctx, 0)                      # send message
            else:                                                        # if command empty
                await ctx.channel.send("Please enter a command")         # send message


client = Un_bot_mal_code()
client.run(get_token())

# TODO
# Implement page system for man
# optimize code for man
# finish to implement non_supported command
# fix echo ""
# try other command that might bug the hell out of it ?
