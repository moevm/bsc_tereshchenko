FROM python

RUN mkdir /vkr
WORKDIR /vkr

ADD ./requirements.txt /vkr

RUN pip install --no-cache-dir -r requirements.txt \
 && python -m spacy download xx_ent_wiki_sm \
 && python -m spacy download en \
 && python -m nltk.downloader stopwords \
 && pip install git+https://github.com/boudinfl/pke.git

ADD . /vkr

ENV FLASK_APP=main.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
