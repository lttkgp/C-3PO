dodgy --ignore paths env venv migrations
isort -rc --atomic ./ --skip  env
pydocstyle --config=./.pydocstylerc
pycodestyle ./ --config=./.pycodestylerc
black . --exclude '/migrations/'
