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
ADD topic_profs.npy /service/topic_profs.npy
ADD model_components.npy /service/model_components.npy
ADD cv_vocabulary.npy /service/cv_vocabulary.npy
WORKDIR /service/
RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords
CMD python -u app.py $APP_SETTINGS $DATABASE_URL
