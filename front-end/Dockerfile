FROM nginx:alpine

# copy front end files
COPY . ./usr/share/nginx/html/

# cope the nginx conf
COPY ./nginx.conf ./etc/nginx/conf.d/default.conf

EXPOSE 80
