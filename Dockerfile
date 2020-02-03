FROM python:3
LABEL maintainer="joshua phartogi <joshuaphartogi@qlue.id>"

USER root

# Install all OS dependencies
# ENV DEBIAN_FRONTEND noninteractive
# RUN apt-get update && \
#         apt-get install -yq --no-install-recommends \
#         build-essential \
#         python3-opencv \
#         libopencv-dev \
#         cmake \
#         git \
#         wget

COPY script /app/script

COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . . 

CMD ["python3","/app/script/main.py"]