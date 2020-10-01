FROM centos:latest
RUN yum install -y epel-release
RUN yum -y update
RUN yum install -y python3-pip
COPY . /WABot
WORKDIR /WABot
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python3", "app.py"]