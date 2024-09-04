#! python3

"""
Tail implementation from https://pypi.org/project/pygtail/
Discord.py library from https://github.com/Rapptz/discord.py
Basis for Discord communication from https://github.com/Rapptz/discord.py/blob/v2.1.1/examples/background_task_asyncio.py
"""

import argparse
import datetime
import discord
import os
import sys
from pygtail import Pygtail
from discord.ext import commands, tasks


def LogFilter(line):
    # Join
    if ("has joined the session" in line):
        return ":green_circle: " + line

    # Join 2
    if ("PW:" in line):
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
    # elif ("Current Player List" in line):
    #    return ":white_check_mark: " + line

    # Current Player List 2
    # elif ("ClientID:" in line and not "PendingRespawnRequest" in line):
    #    return ":white_check_mark: " + line

    # Kick/Ban
    elif ("kicked and added to the Banned List" in line):
        return ":no_entry: " + line

    # Bad Password
    elif ("This guy tried to join with a Bad Password" in line):
        frags = line.split('Password: ')
        cr = '\n'   # Carriage return for strip call below
        ret_line = f'{frags[0]}Password: {frags[1]}Password: `{frags[2].strip(cr)}`'
        return f':lock: ' + ret_line

    # Loco Failure
    elif ("LocoFailure Message Sent" in line):
        return ":poo: :steam_locomotive: " + line

    # Otto Toggle
    elif ("AIDS Toggled by" in line):
        return ":man_technologist: " + line

    # Integri-tah Problem
    elif ("Train has an integrity problem" in line):
        return ":face_with_symbols_over_mouth: :steam_locomotive: " + line

    # Manual Switch
    elif ("Manual Switch" in line):
        return ":bust_in_silhouette: :beginner: " + line

    # CTC Switch
    elif ("CTC switch" in line or "CTC Switch" in line):
        return ":desktop: :beginner: " + line

    # Interlocking Error
    elif ("Interlocking Error" in line):
        return ":lock: :beginner: :bangbang: " + line

    # Corrupt Train Detected
    elif ("Corrupt train detected" in line or "In the vicinity of Tile" in line):
        return ":face_with_symbols_over_mouth: :steam_locomotive: " + line

    # Split Track Condition
    elif ("Possible Split" and "Track Condition" in line):
        return ":twisted_rightwards_arrows: :steam_locomotive: " + line

    # Client Takes Ownership of Train
    elif ("Client Requested Train" in line):
        return ":pilot: :steam_locomotive: " + line

    # Client Relinquishes Train
    elif ("Client Train Relinquished" in line):
        return ":person_walking: :steam_locomotive: " + line

    # Say
    elif (
            "0: " in line and "Track 210" not in line and "Track 10" not in line and "Track 20" not in line and "New EOT" not in line):
        return "\N{SPEECH BALLOON} " + line

    # No match found
    else:
        # return line
        return ''


def file_tail(channel, filename):
    rval = ''
    for line in Pygtail(filename, full_lines=True, copytruncate=True, paranoid=True):
        rval += LogFilter(line)
    return rval


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Tail a file and output as a Discord bot to a Discord channel.")
    parser.add_argument('--token', '-t', help="The bot token that will connect to Discord.")
    parser.add_argument('--channel', '-c', type=int, help="Discord channel to output to.")
    parser.add_argument('--file', '-f', help="The file to tail.", required=True)
    parser.add_argument('--wait', '-W', metavar='SEC', type=int,
                        help="Try to read new lines every SEC seconds. (default: 10)", default=10)
    parser.add_argument('--hb_timer', '-b', type=int,
                        help="Time (minutes) between sending heartbeat messages (0 for no message, default = 30).",
                        default=30)
    parser.add_argument('--spawn', '-s', type=int,
                        help="Discord channel to send train spawn messages to. Default: send to main channel")
    args = parser.parse_args()
    #
    # Define discord bot command structure and register
    #

    # Instantiate client
    # client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
    # Above call only needed if the bot needs to respond to commands (which opens up permission issues)
    # Below call is for a bot that only sends messages to channels
    client = discord.Client(intents=discord.Intents.default())


    @client.event
    async def on_ready():
        tdstr = datetime.datetime.now().strftime("%H:%M:%S %m-%d-%Y")
        print(f'Discord bot [{client.user}] is starting {tdstr}')
        channel = client.get_channel(args.channel)
        await channel.send(f'LOGBOT starting {tdstr}')
        scan_log.start()
        if args.hb_timer != 0:
            report_size.start()

    @tasks.loop(seconds=args.wait)
    async def scan_log():
        file = args.file
        channel = client.get_channel(args.channel)
        if args.spawn:
            spawn_channel = client.get_channel(args.spawn)
        else:
            spawn_channel = client.get_channel(args.channel)
        rstr = file_tail(channel, file)
        if len(rstr) > 0:
            try:
                for line in rstr.splitlines():
                    if 'random AI' in line and args.spawn:
                        await spawn_channel.send(line.strip())
                    await channel.send(line.strip())
            except discord.HTTPException as e:
                print(f'Error sending message to discord channel {channel} : {e}')

    @tasks.loop(minutes=args.hb_timer)
    async def report_size():
        file = args.file
        channel = client.get_channel(args.channel)
        fstat = os.stat(file)
        tdstr = datetime.datetime.now().strftime("%H:%M:%S %m-%d-%Y")
        #sz_str = f'```ansi\n\u001b[1;32m[{tdstr}] **Logbot heartbeat** Log file size = {fstat.st_size / 1024:.1f} KB```'
        sz_str = f'`[{tdstr}] LOGBOT heartbeat : Log file size = {fstat.st_size / 1024:.1f} KB`'

        try:
            await channel.send(sz_str)
        except discord.HTTPException as e:
            print(f'Error sending message to discord channel {channel} : {e}')

    try:
        client.run(args.token)
    except discord.LoginFailure:
        sys.exit("FATAL ERROR: Couldn't login with token \"{}\".".format(args.token))

