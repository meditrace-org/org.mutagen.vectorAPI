FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /home

RUN apt-get update &&  apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./ .

RUN pip3 install --no-cache-dir -r requirements.txt


CMD ["fastapi", "run", "app/main.py"]