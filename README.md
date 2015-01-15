Here is a small load average monitoring application. 

Displays server load history over last ten minutes, based on 'uptime' command in shell. Auto-refreshes every ten seconds. 
If load is above a defined threshold, it triggers an alert and displays it on screen. You can modify threshold.

IMPORTANT : 

On very first launch, go to the directory where you cloned git repository and type :

cd ./monitonitor_app/
python manage.py set_cron

Verify that crontab has been updated ( crontab -l )

You can now  launch django developpement server :
python manage.py runserver
