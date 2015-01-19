
# Server load monitor Application

Here is a small web application that monitors server load

## Main features :

*   Displays information based on 'uptime' command in shell
*   Displays server uptime, users and server load
*   Displays server load history over the ten last minutes
*   Auto-refreshes every ten seconds
*   Alerts : if load is above a defined threshold, it triggers an alert and displays it on screen
*   You can modify threshold


## Get Started : 

On very first launch, go to monitor_app directory:

    $ cd ./monitonitor_app/
    
Then add to crontab the function that updates server load history :

    $ python manage.py set_cron

You can verify that crontab has been updated :

    $ crontab -l 

You can now run django developpement server :

    $ python manage.py runserver
