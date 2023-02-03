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
- [x] Add views: VendingMachineUserView, ProductView
- [x] Add authentication & authorization
- [x] Add urls: admin, auth, users, products, deposit, reset, buy
- [ ] Add views: deposit, reset, buy
- [ ] Add tests
  - [ ] `UserView`
  - [ ] `ProductView`
  - [ ] `DepositView`
  - [ ] `ResetView`
  - [ ] `BuyView`
- [ ] Postman

## Developer
- [x] Add `check-all` script running all linter/formatters
  - [ ] Add check-all as a poetry command
  - [ ] Fix errors & Enable mypy check

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

# Improvement Notes

## Scalability
- Multiple environment settings (`base`, `test`, `local`, `staging`, `production`)
- Git workflows, Git <--> CI/CD Integration
- Containerization
- i18n, l10n

## Security
- UUID pk
- Application secret key, Secrets management
- Allowed hosts, Debug
- Default auth classes
- Edge case: User not having a corresponding VendingMachineUser -- can't

## Maintainability
- API Documentation
### Separation of Concerns
- Separate apps
- `Wallet` model

## Utility (PAGNIs)
- Timestamped base model
- Soft delete base model
- Better Database (PostgreSQL)


## RESTful URI design
- `/deposit`, `/reset`, `/buy`


## Final Note
There are so many things to improve in this implementation, as well as in the way our web frameworks are designed and used. Although some amount of customization is inevitable due to a vast range of varying requirements, I also think some of the aspects of Web development, specifically under heavy compliance with a standard such as the RESTful design, we can generalize more and customize less.

This possibility, as well as exploration of various Python project development practices and their comparison, stole my attention and made me wander off to paths in my mental map, that are usually dark and uncharted. In addition to this, I have been working and trying to conclude class projects and studying for an exam. Therefore, I could only note some improvements rather than implementing them.

I will be happy to discuss all this and more in an interview session.