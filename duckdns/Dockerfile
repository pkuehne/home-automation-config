FROM ubuntu:latest
MAINTAINER peter.kuehne@gmail.com

RUN apt-get update && apt-get -y install cron curl

# Add crontab file in the cron directory
ADD crontab-duckdns /etc/cron.d/crontab-duckdns

# Add duckdns.sh to /etc/
ADD duckdns.sh /etc/duckdns.sh
ADD token.txt /etc/token.txt

# Give execution rights on the cron job
RUN chmod a+rwx /etc/cron.d/crontab-duckdns
RUN chmod a+rwx /etc/duckdns.sh

# Create the log file to be able to run tail
RUN touch /var/log/duckdns.log

# Run the command on container startup
CMD /etc/duckdns.sh && tail -f /var/log/duckdns.log
