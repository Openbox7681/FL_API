FROM python:3

#設定環境變數,包括ES設定與排程等等
ENV LANG=C.UTF-8 \
  DEBIAN_FRONTEND=noninteractive\
  FLASK_APP=app.py\
  FLASK_RUN_HOST=0.0.0.0\
  FLASK_RUN_PORT=5001\
  NMAPSCAN_SCHED_PERIOD=1\
  FLOWSCAN_SCHED_PERIOD=1

  # runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
		ca-certificates \
		netbase \
    vim\
		apt-utils \
        nmap \
        wireshark\
        tshark

RUN apt-get -y install python3-pip \
	&& mkdir /usr/local/FL_API/

WORKDIR /usr/local/FL_API/


# Install the python packages
# requirement建議可以給版本號碼
# 將python套件掛載進去container
COPY requirements.txt /usr/local/FL_API/
RUN pip3 install -r requirements.txt

COPY . /usr/local/FL_API/
RUN chmod +x /usr/local/FL_API/manage.py

CMD ["python3", "manage.py"]


