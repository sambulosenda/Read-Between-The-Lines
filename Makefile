all: help

help:
	@echo 'Makefile Options'
	@echo "make blue"
	@echo "make commit message='things' "

blue:
	cf push ReadBTL

commit:
ifdef message
	@echo "Committing with message $(message)"
	git add -A
	git commit -m"$(message)"
	git push
else
	@echo "please specify message"
endif


