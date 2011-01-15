all: host-repos

update-repos:
	./mk-repos.sh

host-repos: update-repos
	./reposd.sh
