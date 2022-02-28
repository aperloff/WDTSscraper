
# Make the base image configurable:
ARG BASEIMAGE=python:3.10.2

# Set up the CMSSW base:
FROM ${BASEIMAGE}

ARG BUILD_DATE
ARG VCS_REF
ARG VCS_URL
ARG VERSION
LABEL   org.label-schema.build-date=$BUILD_DATE \
        org.label-schema.name="WDTSscraper Docker image" \
        org.label-schema.description="Provide a completely offline-runnable image with the WDTSscraper dependencies pre-installed." \
        org.label-schema.url="https://github.com/aperloff/WDTSscraper/" \
        org.label-schema.vcs-ref=$VCS_REF \
        org.label-schema.vcs-url=$VCS_URL \
        org.label-schema.vendor="A. Perloff" \
        org.label-schema.version=$VERSION \
        org.label-schema.schema-version="1.0"

# minimal software stack
# libspatialindex-dev needed by rtree
RUN echo "\n\nInstalling system packages using apt-get ..." && \
    apt-get update  && \
    apt-get install -y vim emacs git imagemagick ghostscript libspatialindex-dev && \
    apt-get clean

# update pip and the python software stack
RUN echo "\n\nInstalling packages from pip ..." && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pytest six magiconfig pdfplumber numpy pandas shapely fiona pyproj rtree geoalchemy2 geopy mapclassify matplotlib geopandas

# fetch the repository and change the workdir
RUN echo "\n\nCloning the WDTSscraper repo ..." && \
    git clone https://github.com/aperloff/WDTSscraper.git
WORKDIR /WDTSscraper

# if requested, download the input files so that this doesn't need to be done later
ARG DOWNLOAD_DATA=false
RUN if ${DOWNLOAD_DATA}; then echo "\n\nDownload and extract the needed input files ..." && data/download.sh; fi

# default command
CMD ["/bin/bash"]