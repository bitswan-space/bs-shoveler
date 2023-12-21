FROM bitswan/pipeline-runtime-environment:latest@sha256:be221ad4f2f17b803924651a5cef33f1493f147daafbf3e064f4a7a9eefe1cbb

LABEL src=https://gitlab.com/LibertyAces/Product/bs-shoveler

RUN set -ex \
&& apt-get -y update \
&& apt-get -y upgrade

COPY . /app/bs_shoveler/
COPY requirements.txt /app/bs_shoveler/requirements.txt

# Create manifest
RUN apt-get update && apt-get install --assume-yes git
RUN pip install -r /app/bs_shoveler/requirements.txt
COPY .git /app/bs_shoveler/.git
COPY .gitignore /app/bs_shoveler/.gitignore
WORKDIR /app/bs_shoveler

CMD ["python3", "/app/bs_shoveler/bs_shoveler.py", "-c", "/conf/bs_shoveler.conf"]
