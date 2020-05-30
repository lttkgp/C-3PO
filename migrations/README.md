## Alembic migration setup
This project uses [Alembic](https://pypi.org/project/alembic/) for DB migrations. For most incremental changes, the below instructions should be sufficient. In special cases, please refer to the [complete documentation](https://alembic.sqlalchemy.org/en/latest/).

### General instructions
The Alembic configuration is present in the project root at [`alembic.ini`](alembic.ini). Since this folder is already setup, it is no longer required to run `alembic init`.

When there is a schema change being made, run the below command to auto-generate the migration script for the change:
```sh
alembic revision --autogenerate -m "Change description"
```
This will generate a new script within the [`versions`](migrations/versions) folder. Open the script and verify that the changes look correct. Once verified, you can apply the changes to the database using:
```sh
alembic upgrade head
```