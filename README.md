# Run8LoggerEAST.py
Intended for use on the HRS Southeast maps (Fitzgerald, Waycross, A-Line, Baldwin). 
Tails a specified log file (typically Run8.log), applies noise filters, & sends relevant lines to a Discord bot/channel.  
To disable a particular log entry, add a # to the beginning of the line containing the string that is being caught and sent to Discord.  

# Run8LoggerWEST.py
Intended for use on the SoCal region maps (Seligman, Needles, Barstow, Mojave, Cajon, San Bernardino, Bakersfield)  
Tails a specified log file (typically Run8.log), applies noise filters, & sends relevant lines to a Discord bot/channel.  
To disable a particular log entry, add a # to the beginning of the line containing the string that is being caught and sent to Discord.  

# Launch from batch file
Copy the lines below into a blank notepad window and replace the relevant details with your information, then save to a .bat file (e.g.
Launch_LogBot_WEST.bat) for easy launching of either script. Do this for each instance of the log bot you wish to run. 
```
TITLE Log Bot XXXX
python "X:\PATH\TO\Run8LoggerXXXX.py" -f "X:\PATH\TO\Run8.log" -t YOUR_DISCORD_BOT_KEY -c YOUR_CHANNEL_IDENTIFIER
pause
```
# Switches:
--file / -f `<location and file name of Run8 log file>`

--token / -t `<the unique bot token>` 

--wait / -W `<the number of seconds between scanning of log file>`

--channel / -c `<the discord channel ID to write log messages to>`

--spawn / -s `<the discord channel ID to write player spawn AI messages to (optional)>`

--hb_timer / -b `<How often (in minutes) to send logbot status message (default: 30) - enter 0 to disable>`


# Troubleshooting
The library used to follow the log files does attempt to detect when Run-8 rotates its logs and starts a new file, but sometimes it misses.
If the logger stops sending messages to Discord even after restarting the script, go into the directory where the python file lives and
find a file matching the log file name but with an extension of .offset (e.g. Run8.log.offset) and delete that file, then restart the script
again.  The log will then be piped into Discord from the top and should run like normal.
