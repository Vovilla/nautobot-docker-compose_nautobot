ARG PYTHON_VER=3.9
ARG NAUTOBOT_VERSION=1.2.8
FROM networktocode/nautobot:${NAUTOBOT_VERSION}-py${PYTHON_VER} as base

USER 0

RUN echo "Acquire::http:Proxy \"http://192.168.104.66:3129/\";" > /etc/apt/apt.conf
RUN echo "Acquire::https:Proxy \"http://192.168.104.66:3129/\";" >> /etc/apt/apt.conf
RUN echo "Acquire::ftp:Proxy \"http://192.168.104.66:3129/\";" >> /etc/apt/apt.conf

RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99fixbadproxy
RUN echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99fixbadproxy
RUN echo "Acquire::BrokenProxy true;" >> /etc/apt/apt.conf.d/99fixbadproxy

RUN http_proxy=http://192.168.104.66:3129/  apt-get update -y

# RUN apt-get update -y && apt-get install -y libldap2-dev libsasl2-dev libssl-dev





# ---------------------------------
# Stage: Builder
# ---------------------------------
FROM base as builder

# RUN http_proxy=http://192.168.104.66:3129/ apt-get update

RUN http_proxy=http://192.168.104.66:3129/ apt-get install -y gcc && \
    apt-get autoremove -y && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/*

# RUN pip3 install --upgrade pip wheel && pip3 install django-auth-ldap && pip3 install nautobot-device-lifecycle-mgmt
RUN pip3 install --upgrade pip wheel && pip3 install nautobot-device-lifecycle-mgmt

# ---------------------------------
# Stage: Final
# ---------------------------------
FROM base as final
ARG PYTHON_VER
USER 0

COPY --from=builder /usr/local/lib/python${PYTHON_VER}/site-packages /usr/local/lib/python${PYTHON_VER}/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
USER nautobot

WORKDIR /opt/nautobot
