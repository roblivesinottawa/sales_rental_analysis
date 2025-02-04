FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -y update
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -y build-essential python3.9 python3-pip python3-dev
RUN pip3 -q install pip --upgrade

RUN mkdir src
WORKDIR src/
COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install jupyter
RUN pip3 install mysql-connector-python
# RUN python3 employees_db/employees.py
# RUN rm /src/data/data.csv

WORKDIR /src/employees_db

ENV TINI_VERSION 0.6.0
ADD https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]