FROM python:3.8 AS build
WORKDIR /
COPY requirements.txt .
# Install app dependencies
RUN pip install --user -r requirements.txt


FROM python:3.8 AS release
WORKDIR /
COPY --from=build /root/.local /root/.local
COPY run.py entrypoint.sh manage.py sensitive.conf ./
