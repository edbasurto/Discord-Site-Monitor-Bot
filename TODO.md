# Ideas
If site is down, have the bot send a message every so often that the site is down until 

Have separate list of sites that are down

# Commands
Completed:
-update [name] [new_ip] or [ip] [new_name] : updates a site's IP or renames a site (auto-detects by arg type)
-help : bot replies with all commands that can be used
-status : bot replies with the status of all site pings
-sites : bot replies with all monitored sites and their IPs
-unreachable : bot replies with all sites that are down
-add [site] [ip] : adds site with ip to json file, pings first and asks for confirmation if unreachable
-remove [site] or [ip] : removes site from monitoring by name or IP
