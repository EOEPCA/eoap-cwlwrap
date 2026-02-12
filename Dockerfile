# Stage 1: Build stage
FROM rockylinux/rockylinux:10.1-minimal AS builder

# Install necessary build tools
RUN microdnf -y update && \
    microdnf -y install curl tar python3 python3-pip python3-setuptools gcc wget && \
    microdnf clean all


# Download the hatch tar.gz file from GitHub
RUN curl -L https://github.com/pypa/hatch/releases/download/hatch-v1.14.0/hatch-x86_64-unknown-linux-gnu.tar.gz \
      -o /tmp/hatch.tar.gz && \
    tar -xzf /tmp/hatch.tar.gz -C /tmp && \
    install -m 0755 /tmp/hatch /usr/local/bin/hatch && \
    rm -rf /tmp/hatch* /tmp/hatch.tar.gz


# install yq
RUN VERSION="v4.45.4"                                                                               && \
    BINARY="yq_linux_amd64"                                                                         && \
    wget --quiet https://github.com/mikefarah/yq/releases/download/${VERSION}/${BINARY}.tar.gz -O - |\
    tar xz && mv ${BINARY} /usr/bin/yq   

#install oras
ARG ORAS_VERSION=0.12.0
RUN curl -LO "https://github.com/oras-project/oras/releases/download/v${ORAS_VERSION}/oras_${ORAS_VERSION}_linux_amd64.tar.gz" && \
    tar -xzf "oras_${ORAS_VERSION}_linux_amd64.tar.gz" && \
    mv oras /usr/local/bin/ && \
    chmod +x /usr/local/bin/oras && \
    oras version 

# Install runtime dependencies
RUN microdnf install -y --nodocs nodejs && \
    microdnf clean all && \
    curl -L https://github.com/jqlang/jq/releases/download/jq-1.8.1/jq-linux-amd64 -o /usr/bin/jq && \
    chmod +x /usr/bin/jq

WORKDIR /src
COPY . /src

# Build a wheel for your project (outputs into /src/dist)
RUN hatch build -t wheel


# Stage 2: Final stage
FROM rockylinux/rockylinux:10.1-minimal AS runtime


RUN microdnf -y update && \
    microdnf -y install python3 python3-pip git jq && \
    microdnf clean all

# Set up a default user and home directory
ENV HOME=/home/neo

# Create a user with UID 1001, group root, and a home directory
RUN useradd -u 1001 -r -g 0 -m -d ${HOME} -s /sbin/nologin \
        -c "Default neo User" neo && \
    mkdir -p /app && \
    mkdir -p /prod && \
    chown -R 1001:0 /app && \
    chmod g+rwx ${HOME} /app

# Copy the hatch binary from the build stage
COPY --from=builder /usr/bin/yq /usr/bin/yq
COPY --from=builder /usr/local/bin/oras /usr/bin/oras

# Switch to the non-root user
USER neo

# Copy the application files into the /app directory
COPY --chown=1001:0 . /app
WORKDIR /app

USER neo
WORKDIR /app

# Create a venv and install only wheel
ENV VIRTUAL_ENV=/app/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}:/usr/bin"
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir --upgrade pip


COPY --from=builder /src/dist/*.whl /app/dist/

RUN /app/venv/bin/pip install --no-cache-dir /app/dist/*.whl && \
    eoap-cwlwrap --help


WORKDIR /app

