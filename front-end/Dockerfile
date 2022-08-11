FROM nginx:1.23.1-alpine

# copy front end files
ARG nginx_path=./usr/share/nginx/html
COPY chemist ${nginx_path}/chemist
COPY ["doctor select", "${nginx_path}/doctor-select"]
COPY heart_rate ${nginx_path}/heart-rate
COPY login ${nginx_path}/login
COPY patient ${nginx_path}/patient
COPY ["resource(images)", "${nginx_path}/resource"]
COPY ["welcome page", "${nginx_path}/welcome-page"]
COPY signup ${nginx_path}/signup
COPY successlogout.html .
COPY successlogout.html ${nginx_path}/

# cope the nginx conf
COPY ./nginx.conf ./etc/nginx/conf.d/default.conf

# test if nginx config is valid
RUN nginx -t

EXPOSE 80
