import pandas as pd
import itertools

# Load your data into a Pandas DataFrame
df = pd.read_csv("./Participants/gun-violence-data_01-2013_03-2018(AutoRecovered).csv")

# Define a function to split the participant columns into separate rows
def split_columns(row):
    # Convert columns to strings to handle NaN values
    participant_age = str(row["participant_age"]).split("||")
    participant_age_group = str(row["participant_age_group"]).split("||")
    participant_gender = str(row["participant_gender"]).split("||")
    participant_status = str(row["participant_status"]).split("||")
    participant_type = str(row["participant_type"]).split("||")

    # Use zip_longest to handle uneven number of elements
    data = list(itertools.zip_longest(
        participant_age,
        participant_age_group,
        participant_gender,
        participant_status,
        participant_type,
        fillvalue=""
    ))

    # Create a new DataFrame with the split columns
    new_df = pd.DataFrame({
        "incident_id": [row["incident_id"]] * len(data),
        "participant_age": [x[0] for x in data],
        "participant_age_group": [x[1] for x in data],
        "participant_gender": [x[2] for x in data],
        "participant_status": [x[3] for x in data],
        "participant_type": [x[4] for x in data]
    })

    return new_df

# Apply the function to each row in the original DataFrame
new_df = pd.concat([split_columns(row) for index, row in df.iterrows()], ignore_index=True)

# Save the resulting DataFrame to a new CSV file
new_df.to_csv("./separated_data.csv", index=False)