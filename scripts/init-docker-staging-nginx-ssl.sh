#!/bin/bash

# check if docker-compose is installed
if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  exit 1
fi

# init configuration
domains=(testing.ajaidanial.wtf)
rsa_key_size=4096
data_path="./compose/certbot"
email="ajaidanial@gmail.com"
staging=1 # Set to 1 if you're testing your setup to avoid hitting request limits

# download TLS parameters
if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "Downloading recommended TLS parameters..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf >"$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem >"$data_path/conf/ssl-dhparams.pem"
  echo
fi

# create dummy cretificates for verification
echo "Creating dummy certificate for $domains..."
path="/etc/letsencrypt/live/$domains"
mkdir -p "$data_path/conf/live/$domains"
docker-compose -f staging-nginx-ssl.yml run --rm --entrypoint " \
  openssl req -x509 -nodes -newkey rsa:1024 -days 1 \
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot
echo

# start nginx to verify certificates
echo "Starting nginx..."
docker-compose -f staging-nginx-ssl.yml up --force-recreate -d nginx
echo

# delete dummy certificates
echo "Deleting dummy certificate for $domains..."
docker-compose -f staging-nginx-ssl.yml run --rm --entrypoint " \
  rm -Rf /etc/letsencrypt/live/$domains && \
  rm -Rf /etc/letsencrypt/archive/$domains && \
  rm -Rf /etc/letsencrypt/renewal/$domains.conf" certbot
echo

echo "Requesting Let's Encrypt certificate for $domains..."
# Join $domains to -d args
domain_args=""
for domain in "${domains[@]}"; do
  domain_args="$domain_args -d $domain"
done

# Select appropriate email arguments
case "$email" in
"") email_arg="--register-unsafely-without-email" ;;
*) email_arg="--email $email" ;;
esac

# Enable staging mode if needed
if [ $staging != "0" ]; then staging_arg="--staging"; fi

# creating the main certificates for domains
docker-compose -f staging-nginx-ssl.yml run --rm --entrypoint " \
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot
echo

echo "Reloading nginx..."
docker-compose -f staging-nginx-ssl.yml exec nginx nginx -s reload