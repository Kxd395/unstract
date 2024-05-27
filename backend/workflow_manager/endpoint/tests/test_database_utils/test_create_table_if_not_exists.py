import pytest  # type: ignore
from base_test_db import BaseTestDB
from workflow_manager.endpoint.database_utils import DatabaseUtils
from workflow_manager.endpoint.exceptions import (
    FeatureNotSupportedException,
    InvalidSchemaException,
    InvalidSyntaxException,
    SnowflakeProgrammingException,
)

from unstract.connectors.databases.unstract_db import UnstractDB


class TestCreateTableIfNotExists(BaseTestDB):
    def test_create_table_if_not_exists_valid(
        self, valid_dbs_instance: UnstractDB
    ) -> None:
        engine = valid_dbs_instance.get_engine()
        result = DatabaseUtils.create_table_if_not_exists(
            db_class=valid_dbs_instance,
            engine=engine,
            table_name=self.valid_table_name,
            database_entry=self.database_entry,
        )
        assert result is None

    def test_create_table_if_not_exists_bigquery_valid(
        self, valid_bigquery_db_instance: UnstractDB
    ) -> None:
        engine = valid_bigquery_db_instance.get_engine()
        result = DatabaseUtils.create_table_if_not_exists(
            db_class=valid_bigquery_db_instance,
            engine=engine,
            table_name=self.valid_bigquery_table_name,
            database_entry=self.database_entry,
        )
        assert result is None

    def test_create_table_if_not_exists_invalid_schema(
        self, invalid_dbs_instance: UnstractDB
    ) -> None:
        engine = invalid_dbs_instance.get_engine()
        with pytest.raises(InvalidSchemaException):
            DatabaseUtils.create_table_if_not_exists(
                db_class=invalid_dbs_instance,
                engine=engine,
                table_name=self.valid_table_name,
                database_entry=self.database_entry,
            )

    def test_create_table_if_not_exists_invalid_syntax(
        self, valid_dbs_instance: UnstractDB
    ) -> None:
        engine = valid_dbs_instance.get_engine()
        with pytest.raises((InvalidSyntaxException, SnowflakeProgrammingException)):
            DatabaseUtils.create_table_if_not_exists(
                db_class=valid_dbs_instance,
                engine=engine,
                table_name=self.invalid_syntax_table_name,
                database_entry=self.database_entry,
            )

    def test_create_table_if_not_exists_wrong_table_name(
        self, valid_dbs_instance: UnstractDB
    ) -> None:
        engine = valid_dbs_instance.get_engine()
        with pytest.raises(
            (
                FeatureNotSupportedException,
                SnowflakeProgrammingException,
                InvalidSyntaxException,
            )
        ):
            DatabaseUtils.create_table_if_not_exists(
                db_class=valid_dbs_instance,
                engine=engine,
                table_name=self.invalid_wrong_table_name,
                database_entry=self.database_entry,
            )

    def test_create_table_if_not_exists_feature_not_supported(
        self, invalid_dbs_instance: UnstractDB
    ) -> None:
        engine = invalid_dbs_instance.get_engine()
        with pytest.raises(FeatureNotSupportedException):
            DatabaseUtils.create_table_if_not_exists(
                db_class=invalid_dbs_instance,
                engine=engine,
                table_name=self.invalid_wrong_table_name,
                database_entry=self.database_entry,
            )

    def test_create_table_if_not_exists_invalid_snowflake_db(
        self, invalid_snowflake_db_instance: UnstractDB
    ) -> None:
        engine = invalid_snowflake_db_instance.get_engine()
        with pytest.raises(SnowflakeProgrammingException):
            DatabaseUtils.create_table_if_not_exists(
                db_class=invalid_snowflake_db_instance,
                engine=engine,
                table_name=self.invalid_wrong_table_name,
                database_entry=self.database_entry,
            )


if __name__ == "__main__":
    pytest.main()