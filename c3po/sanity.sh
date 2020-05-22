dodgy
isort -rc --atomic ./
pydocstyle --config=./.pydocstylerc
pycodestyle ./ --config=./.pycodestylerc
