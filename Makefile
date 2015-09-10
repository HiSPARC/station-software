.PHONY: gh-pages test

gh-pages:
ifeq ($(strip $(shell git status --porcelain | wc -l)), 0)
	git checkout gh-pages
	git rm -rf .
	git clean -dxf
	git checkout master doc doc-dev
	make -C doc/ html
	make -C doc/ latexpdf
	make -C doc-dev/ html
	make -C doc-dev/ latexpdf
	mkdir TO_DELETE
	mv -fv doc TO_DELETE
	mv -fv doc-dev TO_DELETE
	mkdir doc
	mkdir doc-dev
	mv -fv TO_DELETE/doc/_build/html/* doc/
	mv -fv TO_DELETE/doc/_build/latex/*.pdf doc/
	mv -fv TO_DELETE/doc-dev/_build/html/* doc-dev/
	mv -fv TO_DELETE/doc-dev/_build/latex/*.pdf doc-dev/
	rm -rf TO_DELETE
	git checkout HEAD .nojekyll index.html
	git add -A
	git commit -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`"
	git checkout master
else
	$(error Working tree is not clean, please commit all changes.)
endif

test:
	python -m unittest discover -s user/hsmonitor -p test_*.py
	flake8 --exit-zero --exclude=user/python,user/mysql,doc/,doc-dev/,portalocker.py,cloghandler.py .
	sphinx-build -anW doc doc/_build/html
	sphinx-build -anW doc-dev doc-dev/_build/html
