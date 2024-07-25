# Webpage(s) monitoring + email notification

This project combines a simple Python script (`web_monitor.py`), a `.env` file with variable specifications (for "secrets" like emails and passwords), and a cron job (a local time-based task for the computer) that runs a shell script (`run_web_monitor.sh`) to monitor a webpage or multiple webpages in one go, at regular time intervals. If a change in  content is noted, the script sends an email to (and from) the specified email addresses. (Note: We could adapt this code to send a text instead of - or in addition to - an email!) 

Currently, the script monitors the UC Berkeley Philosophy department webpage for Fall 2024 courses, in addition to one specific Graduate Seminar course listing webpage, in order to track when information on these pages is updated (notably with the topics for the Graduate Seminars). It runs once a day - every 24 hours - this can be adapted as per the needs.

## Requirements
- Python install. Download here: https://www.python.org/downloads.
- git install. Download here: https://git-scm.com/downloads. 
- Package manager. e.g. pip, mamba, conda.
    - pip install. If a recent version of Python is downloaded, pip comes with it. Otherwise: https://pip.pypa.io/en/stable/installation. 
- Terminal access. Learn more: https://www.freecodecamp.org/news/command-line-for-beginners.
- See requirements.txt for library dependencies (see below for more info).

## How to get this to run on your computer
1. Make sure you've got all the requirements above checked off. 
2. Clone this project locally using git. https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository.
3. Install relevant dependencies (libraries) / create a virtual environment from the requirements.txt file. 
    - To do so, you can run in your terminal: `pip install -r requirements.txt`. If you don't want to clutter your base environment (i.e. if you don't want to install a bunch of code packages/libraries directly in your global Python install – highly recommended), create a virtual environment first via venv (comes with recent Python versions), mamba, or conda. For venv, type into the terminal `python -m venv web-monitor` to create your new environment (called 'web-monitor' here); then type `source web-monitor/bin/activate` to enter the virtual environment; and finally the `pip install -r requirements.txt.` This will install all the packages / code libraries the code (`web_monitor.py`) needs to run.
4. Create an app-specific password to access email* via this script. https://myaccount.google.com/apppasswords.
5. Update the example.env file with the appropriate information (email addresses and the above password). 
    - Once updated, change the name of the file to `.env` (this file is set to not be tracked via the `.gitignore` – if you're using GitHub).

To run this script as a cron job (a task your machine does at regular intervals e.g. every 24 hours):

6. Open up your terminal, and make sure the shell script can be executed, by adapting and typing: `chmod +x path/to/your/run_web_monitor.sh`. For example, on my machine (since `run_web_monitor.sh` is located in my web-change-notif folder, which is located in my GitHub folder, which is located in my root directory) that would be: `chmod +x ./GitHub/web-change-notif/run_web_monitor.sh`. Press enter. The script is now executable.
7. Still in the terminal, type: `crontab -e`. This opens up the crontab file.
8. Add a line (and a new job) to the crontab file with the shell script path: `0 12 * * 1-6 /usr/bin/python3 ./path/to/your/run_web_monitor.sh` (update this with your info! e.g. `0 12 * * 1-6 ./GitHub/web-change-notif/run_web_monitor.sh`).
    - `0 12 * * 1-6 means` the script will run at the 0th minute, the 12th hour (noon), every month, Monday through Saturday.
    - `/path/to/your/run_web_monitor.sh` is the path to the shell script to run the code with the virtual environment you created (above). Update this path!
    - (Optional) note: I appreciate saving the log output and errors produced by the cron job to an accessible local logfile (instead of it being sent to the system mail). To do so, instead of the above crontab line, adapt and add ` >> /path/to/cron.log 2>&1` to the crontab file line so that it becomes: `0 12 * * 1-6 /path/to/your/web_monitor.sh >> /path/to/cron.log 2>&1` e.g. `0 12 * * 1-6 ./GitHub/web-change-notif/run_web_monitor.sh >> ./GitHub/web-change-notif/cron.log 2>&1`.
9. To save & exit (using the default text editor - vim - likely used to open up your crontab file in the terminal): press the `esc` key, then type `:x`, and that should save the file (at least on a Mac). Based on your computer's operating system and your (default) terminal text editor, you might have to use different commands; if the aforementioned doesn't work try `Ctrl + X` to exit, then `Y` to confirm changes, and `Enter` to save. If that still doesn't work: good ol' Google.
10. Verify that the cron job has been added correctly by typing into the terminal: `crontab -l`. If it shows the line we just wrote: yay - the script is up and running! Now we just gotta wait for that email.  

## Adapt this code
Check out the `web_monitor.py` file to change the URL(s) being monitored, the email subject, the text in the body, etc.

## Notes

The very first time this script is run, it'll send out an email. You can ignore it - it doesn't mean the content has changed - but is a good confirmation that the script is running successfully.

Contributions very welcome!   
CC0 (Creative Commons Zero: use this code as you wish)

\*  App-specific passwords (temporarily) work around new safety requirements for Google accounts. For dev rabbit-holing, see: https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp.