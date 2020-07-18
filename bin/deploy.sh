cd /home/ubuntu/C-3PO

git pull origin master

export PATH="/home/ubuntu/.pyenv/bin:$PATH"
eval "$( command pyenv init - )"
eval "$(pyenv virtualenv-init -)"

pyenv local C-3PO

pip install -r requirements/common.txt
pip install -r requirements/dev.txt
pip install -e .
alembic upgrade head

sudo systemctl restart c3po.service
