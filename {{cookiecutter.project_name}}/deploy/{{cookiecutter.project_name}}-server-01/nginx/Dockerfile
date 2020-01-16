FROM nginx:1.16.0-alpine
ARG USER_ID
RUN echo $USER_ID

RUN rm -rf /usr/share/nginx/html/*

ADD  {{cookiecutter.app_name}}-fe.tar.gz /usr/share/nginx/html


CMD ["nginx", "-g", "daemon off;"]