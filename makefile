BOX_DIR = bigbox
BOX_DATA = $(BOX_DIR)/data
BOXPLOTS = $(shell ls $(BOX_DATA)/plot*.pdf)
DOCKER_DIR = docker

dist: setup.py
	-git commit -a -m "Building new distribution"
	git push origin master
	python3 setup.py sdist upload	

boxdata:
	./all_box_plots.sh
	-git commit -a -m "Building new Big Box data sets."
	git push origin master

prod: $(SRCS) $(OBJ)
	./test/all_tests.sh
	-git commit -a -m "Building production."
	git push origin master
	ssh indrasnet@ssh.pythonanywhere.com 'cd /home/indrasnet/indras_net; /home/indrasnet/indras_net/rebuild.sh'

db:
	./db.sh

container: $(DOCKER_DIR)/Dockerfile  $(DOCKER_DIR)/requirements.txt
	docker build -t indra docker

repo:
	-git commit -a
	git push origin master
