# Run8LoggerEAST.py
Intended for use on the HRS Southeast maps (Fitzgerald, Waycross, A-Line)  
Tails a specified log file (typically Run8.log), apply noise filters, send relevant lines to a Discord bot/channel.  
To disable a particular log entry, add a # to the beginning of the line containing the string that is being caught and sent to Discord.  

# Run8LoggerWEST.py
Intended for use on the SoCal region maps (Seligman, Needles, Barstow, Mojave, Cajon, San Bernardino, Bakersfield)  
Tails a specified log file (typically Run8.log), apply noise filters, send relevant lines to a Discord bot/channel.  
To disable a particular log entry, add a # to the beginning of the line containing the string that is being caught and sent to Discord.  

# Launch from batch file
Replace the relevant details and save to a .bat file for easy launching of either script.  

python "X:\PATH\TO\Run8LoggerXXXX.py" -f "X:\PATH\TO\Run8.log" -t YOUR_DISCORD_BOT_KEY -c YOUR_CHANNEL_IDENTIFIER  
pause
