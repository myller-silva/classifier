# Use uma imagem base do Python
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask 

COPY . .

# Expõe a porta 5000
EXPOSE 5000

CMD [ "python", "app.py" ]

