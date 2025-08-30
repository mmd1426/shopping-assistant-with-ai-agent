FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple

COPY . .