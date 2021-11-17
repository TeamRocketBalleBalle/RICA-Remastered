FROM nginx:alpine

# copy front end files
ARG nginx_path=./usr/share/nginx/html
COPY chemist ${nginx_path}/chemist
COPY ["doctor select", "${nginx_path}/doctor-select"]
COPY god_code ${nginx_path}/god-code
COPY heart_rate ${nginx_path}/heart-rate
COPY login ${nginx_path}/login
COPY patient ${nginx_path}/patient
COPY ["resource(images)", "${nginx_path}/resource"]
COPY ["welcome page", "${nginx_path}/welcome-page"]

# cope the nginx conf
COPY ./nginx.conf ./etc/nginx/conf.d/default.conf

EXPOSE 80
