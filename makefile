# Need to export as ENV var
export TEMPLATE_DIR = templates

BOX_DIR = bigbox
BOX_DATA = $(BOX_DIR)/data
BOXPLOTS = $(shell ls $(BOX_DATA)/plot*.pdf)
DOCKER_DIR = docker
REQ_DIR = $(DOCKER_DIR)
REPO = indras_net
MODELS_DIR = models
NB_DIR = notebooks
WEB_DIR = webapp
WEB_PUBLIC = $(WEB_DIR)/public
WEB_SRC = $(WEB_DIR)/src
API_DIR = APIServer
PYLINT = flake8
PYLINTFLAGS = 
PYTHONFILES = $(shell ls $(MODELS_DIR)/*.py)
WEBFILES = $(shell ls $(WEB_SRC)/*.js)
WEBFILES += $(shell ls $(WEB_SRC)/components/*.js)
WEBFILES += $(shell ls $(WEB_SRC)/*.css)

UTILS_DIR = utils
PTML_DIR = html_src
INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/logo.txt $(TEMPLATE_DIR)/menu.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

FORCE:

notebooks: $(MODELFILES)
=======
notebooks: $(PYTHONFILES)
	cd $(NB_DIR); make

local: $(HTMLFILES) $(INCS)

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $< 
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

create_dev_env:
	pip3 install -r $(REQ_DIR)/requirements-dev.txt
	git submodule update https://github.com/gcallah/utils.git
	echo "Set PYTHONPATH and INDRA_HOME in your login script as follows:"
	echo "export INDRA_HOME=(You Indra location)"
	echo "export PYTHONPATH=$(INDRA_HOME):(old python path)"

setup_react:
	cd $(WEB_DIR); npm install

# Build react files to generate static assets (HTML, CSS, JS)
webapp: $(WEB_PUBLIC)/index.html

$(WEB_PUBLIC)/index.html: $(WEBFILES)
	- rm -r static || true
	- rm webapp.html || true
	- cd $(WEB_DIR) && \
	npm run build && \
	mv build/index.html build/webapp.html && \
	cp -r build/* .. && \
	cd ..

deploy_webapp: webapp
	echo "After completion you must run `make prod`"
	git add static/js/*js
	git add static/js/*map
	git add $(WEB_DIR)/build/static/js/*js
	git add $(WEB_DIR)/build/static/js/*map
	git add $(WEB_DIR)/build/webapp.html
	cd $(WEB_DIR); npm run deploy

# build tags file for vim:
tags: FORCE
	ctags --recurse .
	git add tags

submods:
	cd utils; git pull origin master

# run tests then commit all, then push
prod: tests
	- git commit -a
	- git pull origin master
	git push origin master

# run tests then push just what is already committed:
prod1: tests
	- git pull origin master
	git push origin master

tests: FORCE
	cd APIServer; make tests
	cd indra; make tests
	cd models; make tests

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

# dev container has dev tools
dev_container: $(DOCKER_DIR)/Dockerfile $(DOCKER_DIR)/requirements.txt $(DOCKER_DIR)/requirements-dev.txt
	docker build -t gcallah/$(REPO)-dev docker
	docker push gcallah/$(REPO)-dev:latest

# prod container has only what's needed to run
prod_container: $(DOCKER_DIR)/Deployable $(DOCKER_DIR)/requirements.txt
	docker system prune -f
	docker build -t gcallah/$(REPO) docker --no-cache --build-arg repo=$(REPO) -f $(DOCKER_DIR)/Deployable

deploy_container:
	docker push gcallah/$(REPO):latest

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm models/.coverage

# Build the webapp react docker image
webapp-image:
	docker build -f webapp/Dockerfile.dev -t gcallah/indras_webapp webapp
