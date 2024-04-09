from kn_girls_day_24.pipelines import get_data

def test_get_data():
    get_data(limit=5, out_path="./tests/data/data.csv")