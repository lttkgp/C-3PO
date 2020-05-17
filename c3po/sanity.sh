dodgy --ignore paths env, venc
isort -rc --atomic ./
pydocstyle --config=./.pydocstylerc
pycodestyle ./ --config=./.pycodestylerc
