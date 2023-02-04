# `vending-machine`
Vending Machine API implementation for the MVP Match backend assignment.


# TODO

## Functionality
- [x] Add app
- [x] Add models: VendingMachineUser, Product
- [x] Add views: VendingMachineUserView, ProductView
- [x] Add authentication & authorization
- [x] Add urls: admin, auth, users, products, deposit, reset, buy
- [x] Add views: deposit, reset, buy
- [x] Add tests
  - [x] `UserView`
  - [x] `DepositView`
  - [x] `BuyView`
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
*This runs a development server on the developer machine, using the host environment. This could be improved by providing a local docker compose setup that deploys the set of services required for local development.*

### Production
*If there was a production environment, this would probably make use of the Docker files of individual services to create instances on the cloud.*

## Testing

### Unit tests
```sh
poetry run python manage.py test
```

## Development

```sh
# You will be prompted to set a password
python manage.py createsuperuser --username=admin --email=admin@example.com

# This runs all the developer tools for linting, formatting, type checking.
scripts/check-all.sh
```

# Improvement Notes

## Scalability
This project currently assumes that the project will only be run locally, and will need to change before being developed by a team with a shared repository. If this assumption changes, a proper Git workflow with feature and sub branches, pull requests with code reviews, protected `main` and `development` branches should be used. In addition, Pull requests could include checks for code quality and run tests before allowing the branches to be merged.

Moreover, as opposed to having a single source of settings, a shared settings file and separate setting files for different environments such as `local`, `test`, `staging`, `production` would be implemented.

On the usage scalability side, since there is no production environment, this requirement is skipped. However, the use of this API in production would require additional infrastructure such as containerization, a proper database such as PostgreSQL with a replica structure, a reverse proxy etc. would have to be implemented. In addition, i18n and l10n would need to be set as part of the pipeline.

## Security
There are several changes to be made to ensure the security of the application. This includes several changes for cloud environments such as `staging` and `production`, where we need to set the `ALLOWED_HOSTS`, `DEBUG` and other settings properly. In addition, any secret information should be moved to a secret provider instead of residing in the repository.

Obviously, HTTPS should be used on the cloud environments.

The data constraints enforced by the API are also assumed in the application logic, however the data can also be manipulated on different layers, e.g. through the Django shell, which could break the data integrity. These cases should also be handled in the application logic. One example is creating a `User` instance manually, and not creating the related `VendingMachineUser` object. This user would be allowed to make requests, but any Vending Machine User operation would fail.

Last but not least, I implemented a `Basic Authentication` scheme that authenticates users with a `username, password` pair sent on each request. This is not the most secure scheme, and could be improved. Moreover, especially in the case we use this scheme, the HTTPS protocol must be used when transporting the requests.

## Maintainability
As the API scales to more features and more endpoints, it becomes more difficult to be on top of the codebase. Therefore, an automatically generated API specification would be handy.

### Separation of Concerns
For sake of simplicity, I implemented all the functionality in a single Django app. However, in an ideal case, there could be multiple apps with distinct responsibilities. One example is a `users` app for managing user operations and data, and a `vending-machine` app for the implementation and operation of the Vending Machine.

## Utility (PAGNIs)
A longer-term Django project would most likely make use of a few generalized functionalities on multiple layers. For example, on the data layer, the use of base models such as a `TimestampedModel` that implements instance timestamping and a `SoftDeletedModel` that implements marking of instances as deleted without deleting them from the database could be useful.

## RESTful URI design

For sake of simplicity, I implemented the `/deposit`, `/reset`, `/buy` endpoints at their generic URLs. However, in a purely RESTful approach, all endpoints should be designed as *resources*, that may or may not persist in a storage. *Action* endpoints should be avoided.

In our case, a `deposit` operation is the creation of a  `Deposit Request` resource on a related `User` resource. Based on RESTful method properties, the most relevant implementation would be `POST /api/users/<pk>/deposit-requests`, as these requests would not be idempotent.

Similarly, `reset` operation would be a `Reset Request` resource, however subsequent resets would have the same effect, and there be idempotent. Therefore, I would enable the `PUT` method for this operation.

Finally, the `buy` endpoint could be `POST`ed on a `Product`'s related `Purchase Request` resource.

## Final Note
There are so many things to improve in this implementation, as well as in the way our web frameworks are designed and used. Although some amount of customization is inevitable due to a vast range of varying requirements, I also think some of the aspects of Web development, specifically under heavy compliance with a standard such as the RESTful design, we can generalize more and customize less.

This possibility, as well as exploration of various Python project development practices and their comparison, stole my attention and made me wander off to paths in my mental map, that are usually dark and uncharted.

In addition to this, I have been working and trying to conclude class projects and studying for an exam. Therefore, I could only note some improvements rather than implementing them. This hopefully also explains the delay in my submission.

I will be happy to discuss all this and more in an interview session.