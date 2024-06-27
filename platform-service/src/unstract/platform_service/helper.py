from typing import Any, Optional

import peewee
from unstract.platform_service.constants import DBTableV2, FeatureFlag
from unstract.platform_service.exceptions import CustomException
from unstract.flags.feature_flag import check_feature_flag_status


class AdapterInstanceRequestHelper:
    @staticmethod
    def get_adapter_instance_from_db(
        db_instance: peewee.PostgresqlDatabase,
        organization_id: str,
        adapter_instance_id: str,
        organization_uid: Optional[int] = None,
    ) -> dict[str, Any]:
        """Get adapter instance from Backend Database.

        Args:
            db_instance (peewee.PostgresqlDatabase): Backend DB
            organization_id (str): organization schema id
            adapter_instance_id (str): adapter instance id

        Returns:
            _type_: _description_
        """
        if check_feature_flag_status(FeatureFlag.MULTI_TENANCY_V2):
            query = (
                "SELECT id, adapter_id, adapter_metadata_b FROM "
                f"{DBTableV2.ADAPTER_INSTANCE} x "
                f"WHERE id='{adapter_instance_id}' and "
                f"organization_id='{organization_uid}'"
            )
        else:
            query = (
                f"SELECT id, adapter_id, adapter_metadata_b FROM "
                f'"{organization_id}".adapter_adapterinstance x '
                f"WHERE id='{adapter_instance_id}'"
            )
        cursor = db_instance.execute_sql(query)
        result_row = cursor.fetchone()
        if not result_row:
            raise CustomException(message="Adapter not found", code=404)
        columns = [desc[0] for desc in cursor.description]
        data_dict: dict[str, Any] = dict(zip(columns, result_row))
        cursor.close()
        db_instance.close()
        return data_dict


class PromptStudioRequestHelper:
    @staticmethod
    def get_prompt_instance_from_db(
        db_instance: peewee.PostgresqlDatabase,
        organization_id: str,
        prompt_registry_id: str,
    ) -> dict[str, Any]:
        """Get prompt studio registry from Backend Database.

        Args:
            db_instance (peewee.PostgresqlDatabase): Backend DB
            organization_id (str): organization schema id
            prompt_registry_id (str): prompt_registry_id

        Returns:
            _type_: _description_
        """
        if check_feature_flag_status(FeatureFlag.MULTI_TENANCY_V2):
            query = (
                "SELECT prompt_registry_id, tool_spec, "
                "tool_metadata, tool_property FROM "
                f"{DBTableV2.PROMPT_STUDIO_REGISTRY} x "
                f"WHERE prompt_registry_id='{prompt_registry_id}'"
            )
        else:
            query = (
                f"SELECT prompt_registry_id, tool_spec, "
                f"tool_metadata, tool_property FROM "
                f'"{organization_id}".prompt_studio_registry_promptstudioregistry x'
                f" WHERE prompt_registry_id='{prompt_registry_id}'"
            )
        cursor = db_instance.execute_sql(query)
        result_row = cursor.fetchone()
        if not result_row:
            raise CustomException(message="Custom Tool not found", code=404)
        columns = [desc[0] for desc in cursor.description]
        data_dict: dict[str, Any] = dict(zip(columns, result_row))
        cursor.close()
        db_instance.close()
        return data_dict
