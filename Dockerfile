FROM python
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
#Running your APP and doing some PORT Forwarding
CMD gunicorn -b 0.0.0.0:80 app:server