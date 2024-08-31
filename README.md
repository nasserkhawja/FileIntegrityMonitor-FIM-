# FileIntegrityMonitor-FIM-
Create a FIM to monitor changes to directories and files and have it run on a cron.
Set the MONITOR_DIRECTORY variable to the directory you want to monitor.
Set BASELINE_FILE to where you want the baseline data saved (e.g., baseline.json).
Set LOG_FILE to where you want the log entries saved (e.g., fim.log).
To run the script, run: python fim.py
To further cronjob it, 0 * * * * /usr/bin/python3 /path/to/fim.py

Additional fewatures for future, add watchdog, centralized logging and alerting.
