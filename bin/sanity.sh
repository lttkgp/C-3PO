dodgy
isort --atomic ./ --skip migrations
pydocstyle --config=./config.ini
pycodestyle ./ --config=./config.ini
