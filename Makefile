all: clean install

clean:
	rm -rf *.spec *.gz build htmlcov

install:
	pyinstaller --clean --onefile --distpath ~/Desktop/ --name Maze.app main.py

uninstall:
	rm -rf ~/Desktop/Maze.app

dvi:
	open html_docs/_build/html/index.html

dist: install
	[ -d archiv ] || mkdir archiv
	cp -r *.py Makefile ~/Desktop/Maze.app archiv
	tar -cvzf Maze.tar.gz archiv
	rm -rf archiv

tests:
	python -m coverage run -m test
	python -m coverage html