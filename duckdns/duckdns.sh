DOMAIN="quantumpete"
TOKEN=$(cat token.txt)
URL="https://www.duckdns.org/update?domains=$DOMAIN&token=$TOKEN&ip=" 
echo url="$URL" | curl -k -o - -K - >> /var/log/duckdns.log 
