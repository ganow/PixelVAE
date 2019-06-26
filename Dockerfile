FROM nvcr.io/nvidia/cuda:10.0-cudnn7-devel

RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update -qq -y && \
  apt-get install -qq -y \
    curl wget nodejs npm software-properties-common git && \
  add-apt-repository -y ppa:deadsnakes/ppa && \
  apt-get update -qq -y && \
  apt-get install -qq -y python3.6 python3-pip && \
  python3.6 -m pip install pip && \
  ln -sf /usr/bin/python3.6 /usr/bin/python3 && \
  apt purge -y software-properties-common && \
  rm -rf /var/lib/apt/lists/*

RUN npm install --global n && \
  n stable && \
  apt purge -y curl nodejs npm

COPY Pipfile .
COPY Pipfile.lock .

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN pip3 install --no-cache-dir -q pipenv && \
  pipenv install --system --skip-lock --pre && \
  jt -t grade3 -T -N && \
  jupyter contrib nbextension install > /dev/null 2>&1 && \
  jupyter nbextension enable hinterland/hinterland && \
  jupyter nbextension enable --py widgetsnbextension && \
  jupyter labextension install @jupyter-widgets/jupyterlab-manager

CMD ["bash"]
