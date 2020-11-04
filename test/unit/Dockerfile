FROM centos AS centosbase
WORKDIR /home/bwijayaw
RUN yum update -y
RUN yum install -y glibc-langpack-en epel-release python3 python3-pip

FROM centosbase AS unittest
COPY unittest.py /home/bwijayaw
RUN pip3 install requests
RUN python3 /home/bwijayaw/unittest.py
