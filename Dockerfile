# test

FROM openjdk:slim as build

COPY --from=python:3.9 / /

WORKDIR /tool-build

RUN pip install tox

ADD . .


RUN tox .


# runtime

FROM openjdk:slim

COPY --from=python:3.9 / /

WORKDIR /tool-run

ADD ./requirements.txt ./

RUN pip install -r requirements.txt

ADD . .




ENTRYPOINT [ "python", "src/main.py" ]