FROM nginx:alpine

# Copy Nginx config
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy SSL certificates for local dev
COPY cert.pem /etc/nginx/cert.pem
COPY key.pem /etc/nginx/key.pem

EXPOSE 80
EXPOSE 443
