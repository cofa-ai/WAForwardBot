FROM centos:latest
ENV PYTHONUNBUFFERED=1
RUN yum install -y epel-release
RUN yum -y update
RUN yum install -y python3-pip
COPY . /WABot
WORKDIR /WABot
RUN pip3 install -r requirements.txt
RUN python3 WebhookConfigure.py
EXPOSE 5000
CMD ["python3", "app.py"]