import pyarrow.parquet as pq


class ParquetModel:
    def read_parquet_file(self, file_path):
        table = pq.read_table(file_path)
        return table.to_pandas()

    def query_data(self, data, query):
        try:
            return data.query(query)
        except Exception as e:
            raise ValueError(repr(e))

    def get_schema(self, data):
        return data.dtypes.to_string()

    def convert_to_json(self, data, save_path):
        json_data = data.to_json(orient='records', lines=True)
        try:
            with open(save_path, 'w') as f:
                f.write(json_data)
        except Exception as e:
            raise ValueError(f"Error occurred while saving JSON file: {e}")
