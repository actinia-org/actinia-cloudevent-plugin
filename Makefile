# Makefile to run setup.py

clean:
	python3 setup.py clean

docs:
	python3 setup.py docs

build:
	python3 setup.py build

install:
	python3 setup.py install

bdist:
	python3 setup.py bdist

dist:
	python3 setup.py dist

test:
	./tests_with_cloudevent_receiver.sh

unittest:
	./tests_with_cloudevent_receiver.sh unittest

devtest:
	./tests_with_cloudevent_receiver.sh dev

integrationtest:
	./tests_with_cloudevent_receiver.sh integrationtest
