FROM    ubuntu
# Make sure the package repository is up to date
#RUN     echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN     apt-get update && apt-get install -y x11vnc xvfb firefox
RUN     mkdir ~/.vnc && x11vnc -storepasswd 1234 ~/.vnc/passwd
RUN     bash -c 'echo "firefox" >> /.bashrc'
