# Metabolitics

[![Build Status](https://travis-ci.org/MuhammedHasan/metabolitics.svg?branch=master)](https://travis-ci.org/MuhammedHasan/metabolitics)

A research project on biologic networks for [detail](http://biodb.sehir.edu.tr/Home/Project/2).

## Install
~~~
pip install -r requirements.txt
cd src
python main.py --help
~~~

## Run celery
~~~
celery -A api.celery worker
flower -A api.celery --port=5555
~~~

## Related Projects

[metabol](https://github.com/MuhammedHasan/metabol)
