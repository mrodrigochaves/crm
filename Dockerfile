FROM fedora
LABEL maintainer="Márcio Rodrigo"

RUN dnf -y install nginx

EXPOSE 80
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]