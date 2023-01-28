import pandas as pd


class TestQuery:
    def test_query(self, connect_to_db) -> None:
        connection = connect_to_db
        sql = "Select * from configurations"
        print(pd.read_sql_query(sql, connection))
