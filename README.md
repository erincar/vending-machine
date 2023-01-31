# `vending-machine`
Vending Machine API implementation for the MVP Match backend assignment.

# Command Log

```sh
mkdir vending-machine && cd vending-machine
git init
git remote add origin git@github.com:erincar/vending-machine.git
touch README.md
touch .gitignore
poetry init
poetry add django djangorestframework
poetry add -G dev mypy black isort autoflake flake8 ipython
poetry run django-admin startproject api .
{cd api && poetry run django-admin startapp vending_machine}
poetry run python manage.py runserver migrate
poetry run python manage.py runserver 0.0.0.0:8000
python manage.py createsuperuser --username=admin --email=admin@example.com
```

# TODO

## Functionality
- [x] Add app
- [x] Add models: VendingMachineUser, Product
- [ ] Add views: VendingMachineUserView, ProductView
- [ ] Add urls: admin, auth, users, products
- [ ] Base model for timestamping
- [ ] UUID primary keys
- [ ] Run translations
- [ ] Add tests

## Developer
- [x] Add `check-all` script running all linter/formatters
- [ ] Add check-all as a poetry command
- [ ] Fix errors & Enable mypy check
- [ ] Project high-level documentation
- [ ] Git workflows, Git <--> CI/CD Integration
- [ ] Handle secret keys, Application security

## Deployment
- [ ] Proper database
- [ ] Multiple environment settings
- [ ] Containerization

# Setup

## Requirements

* `python3.11` and `poetry` should be installed and visible on the path.

```sh
git clone git@github.com:erincar/vending-machine.git
cd vending-machine
poetry install
```

## Deployment

### Local

```sh
poetry run python manage.py runserver 0.0.0.0:8000
```

### Test

### Production


## Testing

### Unit tests


## Development

```sh
python manage.py createsuperuser --username=admin --email=admin@example.com
# You will be prompted to set a password
```