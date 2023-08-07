FROM public.ecr.aws/h9w9d7v3/bspump:2023-39-git-8444683

LABEL src=https://gitlab.com/LibertyAces/Product/bs-shoveler

RUN set -ex \
&& apt-get -y update \
&& apt-get -y upgrade

COPY . /app/bs_shoveler/
COPY ./CHANGELOG.md /app/

# Create manifest
RUN apt-get update && apt-get install --assume-yes git
COPY .git /app/bs_shoveler/.git
COPY .gitignore /app/bs_shoveler/.gitignore
WORKDIR /app/bs_shoveler

CMD ["python3", "/app/bs_shoveler/bs_shoveler.py", "-c", "/conf/bs_shoveler.conf"]
