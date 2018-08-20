FROM python:3-alpine

WORKDIR /usr/src/app

RUN apk add no-cache git bash nano

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./related_posts.py" ]
