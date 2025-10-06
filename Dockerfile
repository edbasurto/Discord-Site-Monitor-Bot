FROM python:3.11
WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y libcap2-bin iputils-ping iproute2 traceroute

RUN setcap cap_net_raw+ep /usr/local/bin/python3.11

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

CMD [ "python3", "-m", "src.main" ]
