FROM python:3.12-slim-bookworm
COPY . /user/src/app
WORKDIR /user/src/app
RUN apt update -y && apt install zip curl -y
RUN python3 -m ensurepip --upgrade
RUN pip3 install -r ./requirements.txt
RUN python3 setup.py install
RUN reflex init
RUN reflex export --frontend-only --no-zip
STOPSIGNAL SIGKILL
ENTRYPOINT ["reflex", "run", "--frontend-port=8080", "--env", "prod"]