FROM jupyter/datascience-notebook
#設定環境變數,包括ES設定與排程等等
ENV LANG=C.UTF-8 \
  DEBIAN_FRONTEND=noninteractive\
  FLASK_APP=app.py\
  FLASK_RUN_HOST=0.0.0.0\
  FLASK_RUN_PORT=5001\
  NMAPSCAN_SCHED_PERIOD=1\
  FLOWSCAN_SCHED_PERIOD=1

  # runtime dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     python3-scipy\
#     ca-certificates \
#     netbase \
#     vim\
#     apt-utils \
#     python3-sklearn python3-sklearn-lib python3-sklearn-doc

RUN mkdir /home/jovyan/FL_API/

WORKDIR /home/jovyan/FL_API/


# Install the python packages
# requirement建議可以給版本號碼
# 將python套件掛載進去container
COPY requirements.txt /home/jovyan/FL_API/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /home/jovyan/FL_API/
RUN /bin/bash -c 'ls -la; chmod -R 777 /home/jovyan/FL_API/;  ls -la'

CMD ["python3", "manage.py"]


