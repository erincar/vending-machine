# Command Log

```sh
mkdir vending-machine && cd vending-machine
git init
touch README.md
touch .gitignore
poetry init
poetry add django djangorestframework
poetry add -G dev mypy black isort autoflake flake8 ipython
poetry run django-admin startproject api .
{cd api && poetry run django-admin startapp vending_machine}
poetry run python manage.py runserver 0.0.0.0:8000
```
# TODO

- [ ] Add app
- [ ] Add urls: admin, auth, users, products
- [ ] Add views: VendingMachineUserView, ProductView