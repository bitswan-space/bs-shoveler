FROM teskalabs/bspump:nightly AS builder

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

RUN apt-get update
RUN pip3 install --no-cache-dir cython

# Install fastkafka
RUN apt-get -y install \
	curl \
	make \
	gcc \
	g++ \
	libc-dev \
	libz-dev \
	libzstd-dev \
	wget

RUN apt-get -y install git
RUN curl -O -L https://github.com/edenhill/librdkafka/archive/v1.5.2.tar.gz --silent --fail \
	&& tar xzf v1.5.2.tar.gz \
	&& cd librdkafka-1.5.2 \
	&& ./configure \
	&& cd src \
	&& make \
	&& make install
RUN ldconfig
RUN pip3 install --no-cache-dir git+https://lmiodeploy:bR88sBTwX6ys5b2d47cG@gitlab.com/TeskaLabs/fastkafka@f5dc0a932928f296b1a585a4b9cf2ac23101daf0
RUN pip3 install xxhash

COPY ./bs_shoveler /app/bs_shoveler/bs_shoveler
COPY ./bs_shoveler.py /app/bs_shoveler/bs_shoveler.py
COPY ./CHANGELOG.md /app/

# Create manifest
RUN apt-get update && apt-get install --assume-yes git
COPY .git /app/bs_shoveler/.git
RUN wget 'https://github.com/TeskaLabs/asab/blob/master/asab-manifest.py?raw=true' -O /app/bs_shoveler/asab-manifest.py
RUN chmod +x /app/bs_shoveler/asab-manifest.py
WORKDIR /app/bs_shoveler
RUN ./asab-manifest.py /app/MANIFEST.json

CMD ["python3", "/app/bs_shoveler/bs_shoveler.py", "-c", "/conf/bs_shoveler.conf"]
