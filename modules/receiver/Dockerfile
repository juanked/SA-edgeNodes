FROM sanoderegistry.azurecr.io/sa-python-linux.arm64:2

WORKDIR /usr/bin/app

COPY app app

WORKDIR /usr/bin/app/app/
CMD ["python", "receiver.py"]