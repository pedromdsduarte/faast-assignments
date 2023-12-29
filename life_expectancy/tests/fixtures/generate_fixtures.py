from life_expectancy.data_io import load_data

if __name__ == "__main__":
    INPUT_DATA_PATH = "life_expectancy/data/eu_life_expectancy_raw.tsv"
    OUTPUT_DATA_PATH = "life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv"

    raw_data = load_data(INPUT_DATA_PATH)
    sample_data = raw_data.sample(n=300, random_state=42)
    sample_data.to_csv(OUTPUT_DATA_PATH, sep="\t", index=False)
