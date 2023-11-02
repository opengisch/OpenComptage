FROM qgis/qgis:final-3_28_4

RUN apt update -y && DEBIAN_FRONTEND=noninteractive apt install -y \
    python3-pip \
    xvfb \
    iputils-ping \
    glibc-tools \
    && apt clean && apt autoremove --purge

WORKDIR /usr/src/app

# crashes to STDERR
ENV LD_PRELOAD="/lib/x86_64-linux-gnu/libSegFault.so"
ENV SEGFAULT_SIGNALS="abrt segv"
ENV LIBC_FATAL_STDERR_=1

COPY ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt
