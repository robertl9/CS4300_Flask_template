# Read from Ubuntu Base Image
FROM python:2.7
RUN mkdir -p /service
# Copy over all the files of interest
ADD app /service/app
ADD app.py /service/app.py
ADD config.py /service/config.py
ADD manage.py /service/manage.py
ADD requirements.txt /service/requirements.txt
ADD aggreg.json /service/aggreg.json
ADD all_ingrs.json /service/all_ingrs.json
WORKDIR /service/
RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords
CMD python -u app.py $APP_SETTINGS $DATABASE_URL
