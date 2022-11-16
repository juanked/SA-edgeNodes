FROM sanoderegistry.azurecr.io/sa-python-linux.arm64:1

WORKDIR /usr/bin/app

COPY app/ .

WORKDIR /usr/bin/app/app/
CMD ["python", "receiver.py"]