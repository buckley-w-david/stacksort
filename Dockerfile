from archlinux:latest

WORKDIR /src

RUN pacman -Sy
RUN yes | pacman -S python python-setuptools vim python-pip
