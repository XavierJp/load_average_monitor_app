
# Server load monitor Application

Here is a small web application that monitor server load

## Main features :

*   Displays informations based on 'uptime' command in shell
*   Displays IP, server uptime, nb of user and server load
*   Displays server load history over last ten minutes
*   Auto-refreshes every ten seconds
*   Alerts : if load is above a defined threshold, it triggers an alert and displays it on screen
*   You can modify threshold


## Get Started : 

On very first launch, go to the directory where you cloned git repository and go to /monitor_app directory :

    $ cd ./monitonitor_app/
    
Then add server load update history to crontab by typing :

    $ python manage.py set_cron

You can verify that crontab has been updated :

    $ crontab -l 

You can now  launch django developpement server :

    $ python manage.py runserver
