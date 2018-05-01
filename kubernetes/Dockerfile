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
ADD alcohol.npy /service/alcohol.npy
ADD beef.npy /service/beef.npy
ADD dairy.npy /service/dairy.npy
ADD egg.npy /service/egg.npy
ADD fish.npy /service/fish.npy
ADD flav_mat.npy /service/flav_mat.npy
ADD flav_norms.npy /service/flav_norms.npy
ADD gluten.npy /service/gluten.npy
ADD halal.npy /service/halal.npy
ADD ketogenic.npy /service/ketogenic.npy
ADD kosher.npy /service/kosher.npy
ADD lactoovo.npy /service/lactoovo.npy
ADD peanut.npy /service/peanut.npy
ADD pescatarian.npy /service/pescatarian.npy
ADD pork.npy /service/pork.npy
ADD sesame.npy /service/sesame.npy
ADD shellfish.npy /service/shellfish.npy
ADD soy.npy /service/soy.npy
ADD treenuts.npy /service/treenuts.npy
ADD vegan.npy /service/vegan.npy
ADD vegetarian.npy /service/vegetarian.npy
ADD wheat.npy /service/wheat.npy
WORKDIR /service/
RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords
CMD python -u app.py $APP_SETTINGS $DATABASE_URL
