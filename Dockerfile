FROM rockylinux:9.3-minimal

# Any python libraries that require system libraries to be installed will likely
# need the following packages in order to build
RUN microdnf update -y && \
    microdnf install -y libpq python3.11 python3.11-pip curl git wget tar jq

ENV VERSION=v4.44.3 \
    BINARY=yq_linux_amd64

RUN wget https://github.com/mikefarah/yq/releases/download/${VERSION}/${BINARY}.tar.gz -O - |\
    tar xz && mv ${BINARY} /usr/bin/yq
WORKDIR /code

ENV HOME=/home/neo

RUN useradd -u 1001 -r -g 100 -m -d ${HOME} -s /sbin/nologin \
      -c "Default Neo User" neo && \
  chown -R 1001:100 /code && \
  chmod g+rwx ${HOME} 

COPY . /code

RUN cd /code && pip3.11 install . 

USER neo

RUN eoap-cwlwrap --help
