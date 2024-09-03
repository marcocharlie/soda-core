from helpers.common_test_tables import customers_test_table
from helpers.data_source_fixture import DataSourceFixture

mock_schema = [
    {"type": "number", "name": "priority"},
    {"type": "singleSelect", "allowedValues": ["sales", "marketing"], "name": "department"},
    {"type": "multiSelect", "allowedValues": ["generated", "user-created"], "name": "tags"},
    {"type": "text", "name": "sales_owner"},
    {"type": "datetime", "name": "arrival_date"},
    {"type": "datetime", "name": "arrival_datetime"},
]
mock_variables = {"DEPT": "sales"}


def test_dataset_attributes_valid(data_source_fixture: DataSourceFixture):
    table_name = data_source_fixture.ensure_test_table(customers_test_table)

    scan = data_source_fixture.create_test_scan()
    scan.mock_check_attributes_schema(mock_schema)
    scan.add_variables(mock_variables)
    scan.add_sodacl_yaml_str(
        f"""
      configurations for {table_name}:
        attributes:
            priority: 1
            tags: ["user-created"]
      checks for {table_name}:
        - row_count > 0
    """
    )
    scan.execute()
    scan.assert_all_checks_pass()

    scan_result = scan.build_scan_results()
    assert scan_result["checks"][0]["resourceAttributes"] == [
        {"name": "priority", "value": "1"},
        {"name": "tags", "value": ["user-created"]},
    ]


def test_dataset_attributes_deprecation(data_source_fixture: DataSourceFixture):
    table_name = data_source_fixture.ensure_test_table(customers_test_table)

    scan = data_source_fixture.create_test_scan()
    scan.mock_check_attributes_schema(mock_schema)
    scan.add_variables(mock_variables)
    scan.add_sodacl_yaml_str(
        f"""
      configurations for {table_name}:
        attributes:
            priority: 1
            tags: ["user-created"]
      checks for {table_name}:
        - attributes:
            priority: 2
            tags: ["generated"]
        - row_count > 0
    """
    )
    scan.execute()
    scan.assert_all_checks_pass()

    scan_result = scan.build_scan_results()
    assert scan_result["checks"][0]["resourceAttributes"] == [
        {"name": "priority", "value": "1"},
        {"name": "tags", "value": ["user-created"]},
    ]


def test_dataset_attributes_overwriting(data_source_fixture: DataSourceFixture):
    table_name = data_source_fixture.ensure_test_table(customers_test_table)

    scan = data_source_fixture.create_test_scan()
    scan.mock_check_attributes_schema(mock_schema)
    scan.add_variables(mock_variables)
    scan.add_sodacl_yaml_str(
        f"""
      configurations for {table_name}:
        attributes:
            priority: 1
            tags: ["user-created"]
      checks for {table_name}:
        - row_count > 0:
            attributes:
                priority: 2
                tags: ["generated"]
    """
    )
    scan.execute()
    scan.assert_all_checks_pass()

    scan_result = scan.build_scan_results()
    assert scan_result["checks"][0]["resourceAttributes"] == [
        {"name": "priority", "value": "1"},
        {"name": "tags", "value": ["user-created"]},
    ]
