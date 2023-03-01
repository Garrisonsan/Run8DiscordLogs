#! python3

"""LICENSE INFORMATION (Run8DiscordLogs.py)
This program performs the equivalent of tail -f on the specified file
and sends it to a specified Discord channel.

Copyright (C) 2023 Garrisonsan

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

"""LICENSE INFORMATION (discord.py)
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

"""LICENSE INFORMATION (Pygtail)
Pygtail is licensed under the GNU Public License v2
https://opensource.org/license/gpl-2-0/
"""

"""
Tail implementation from https://pypi.org/project/pygtail/
Discord.py library from https://github.com/Rapptz/discord.py
Basis for Discord communication from https://github.com/Rapptz/discord.py/blob/v2.1.1/examples/background_task_asyncio.py
"""

import argparse
import os
import discord
import asyncio
#import re
import sys
from pygtail import Pygtail

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())
        
    async def on_ready(self):
        channel = client.get_channel(args.channel)
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        await channel.send("**Bot is online.**")

    async def my_background_task(self):
        await self.wait_until_ready()
        file = args.file
        channel = client.get_channel(args.channel)
        waittime = args.wait
        while not self.is_closed():
            await file_tail(channel,file)

            await asyncio.sleep(waittime)


client = MyClient(intents=discord.Intents.default())

def LogFilter(line):
    # Join
    if ("has joined the session" in line):
        return ":green_circle: " + line
    
    # Join 2
    elif ("Name:" in line):
        return ":passport_control: " + line
        
    # Leave
    elif ("has exited the session" in line):
        return ":yellow_circle: " + line
        
    # Player attempt spawn train
    elif ("has attempted to spawn a train into the world" in line):
        return ":new: :bust_in_silhouette: :steam_locomotive: " + line
        
    # Player delete train
    elif ("has just deleted a train" in line):
        return ":put_litter_in_its_place: :steam_locomotive: " + line
        
    # DTMF
    elif ("used DTMF" in line):
        return ":hash: " + line
    
    # Player spawn AI train
    elif ("has spawned a random AI train" in line):
        return ":new: :desktop: :steam_locomotive: " + line
    
    # Place/remove MOW Object
    elif ("an MOW Flag or Object" in line):
        return ":stop_sign: " + line
    
    # Current Player List
    elif ("Current Player List" in line):
        return ":white_check_mark: " + line
    
    # Current Player List 2
    elif ("ClientID:" in line):
        return ":white_check_mark: " + line
    
    # Kick/Ban
    elif ("kicked and added to the Banned List" in line):
        return ":no_entry: " + line
    
    # Bad Password
    elif ("This guy tried to join with a Bad Password" in line):
        return ":lock: " + line
    
    # Loco Failure
    elif ("LocoFailure Message Sent" in line):
        return ":poo: :steam_locomotive: " + line
    
    # Otto Toggle
    elif ("AIDS Toggled by" in line):
        return ":man_technologist: " + line
    
    # Integri-tah Problem
    elif ("Train has an integrity problem" in line):
        return ":face_with_symbols_over_mouth: :steam_locomotive: " + line
        
    # Say
    elif ("0: " in line and "Track 210" not in line and "Track 10" not in line and "New EOT" not in line):
        return "\N{SPEECH BALLOON} " + line
        
    # No match found
    else:
        return False


async def file_tail(channelID, filename):
    channel = client.get_channel(args.channel)
    for line in Pygtail(filename, full_lines=True, copytruncate=True, paranoid=True):
        if LogFilter(line) != False:
            await channel.send(LogFilter(line))
            #sys.stdout.write(line)


parser = argparse.ArgumentParser(description="Tail a file and output as a Discord bot to a Discord channel.")

parser.add_argument('--token','-t',help="The bot token that will connect to Discord.")
parser.add_argument('--channel','-c',type=int,help="Discord channel to output to.")
parser.add_argument('--file','-f',help="The file to tail.",required=True)
parser.add_argument('--wait','-W',metavar='SEC',type=int,help="Try to read new lines every SEC seconds. (default: 10)",default=10)

args = parser.parse_args()

try:
    client.run(args.token)
except discord.LoginFailure:
    sys.exit("FATAL ERROR: Couldn't login with token \"{}\".".format(args.token))