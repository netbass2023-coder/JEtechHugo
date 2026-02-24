import pandas as pd
import datetime
import os

def process_parish_data(input_file='target_20260214.ods', output_file='parish_summary.xlsx'):
    file_ext = os.path.splitext(input_file)[1].lower()
    engine = 'odf' if file_ext == '.ods' else 'openpyxl'
    
    print(f"Loading data from {input_file} (engine={engine})...")
    
    try:
        # Load the file
        df = pd.read_excel(input_file, engine=engine)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return

    # Normalize column names (strip whitespace)
    df.columns = df.columns.str.strip()
    
    # Required columns check
    required_columns = ['Name', 'BOD', 'Group', 'address']
    # Check if 'BOD' exists, sometimes it might be 'Birth' or similar, strict check for now based on request
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns: {missing_cols}")
        print(f"Found columns: {df.columns.tolist()}")
        return

    # 1. Filter by BOD (1976-01-01 to 1996-12-31)
    print("Filtering data by BOD (1976-1996)...")
    
    # Convert BOD to datetime, handling errors
    df['BOD'] = pd.to_datetime(df['BOD'], errors='coerce')
    
    start_date = pd.Timestamp('1976-01-01')
    end_date = pd.Timestamp('1996-12-31')
    
    # Filter valid dates within range
    filtered_df = df[
        (df['BOD'] >= start_date) & 
        (df['BOD'] <= end_date)
    ].copy()
    
    print(f"Original record count: {len(df)}")
    print(f"Filtered record count: {len(filtered_df)}")

    # 2. Create 'Group_Prefix' field (first character of Group)
    # Ensure Group is string
    filtered_df['Group'] = filtered_df['Group'].astype(str)
    filtered_df['Group_Prefix'] = filtered_df['Group'].str[0]
    
    # Filter where Group_Prefix is 1, 2, or 3
    # The request said: "Create new field... make a file up to here". 
    # But later it asks to count specific groups like '1교구'.
    # If we filter only 1,2,3 output file will only have those.
    # The requirement "Group의 첫 글자가 1,2,3으로 새로운 필드를 만들어줘" implies we create the field first.
    # It seems implied we want to focus on these, but let's keep all valid BODs in the main filtered file
    # or should we filter the dataset to ONLY 1,2,3?
    # "이중... Group의 첫 글자가 1,2,3으로 ... 여기까지로 하나의 파일을 만들어줘"
    # This suggests the output file should only contain these.
    
    target_prefixes = ['1', '2', '3']
    filtered_df = filtered_df[filtered_df['Group_Prefix'].isin(target_prefixes)]
    print(f"Records after filtering Group Prefix (1,2,3): {len(filtered_df)}")

    # Save Step 1 Output
    step1_output = 'filtered_parish_data.xlsx'
    filtered_df.to_excel(step1_output, index=False)
    print(f"Step 1 output saved to {step1_output}")

    # 3. Count Individuals by specific groups
    print("Calculating individual counts...")
    target_groups = [
        '1교구', '1교구/무소속',
        '2교구', '2교구/무소속',
        '3교구', '3교구/무소속'
    ]
    
    # We can group by the exact 'Group' string
    # Filter to only the target groups for counting? Or just count them if they exist?
    # The request says "For the above content... count for each group".
    
    # Let's do a value_counts on the whole filtered dataset and then extract what we need, 
    # or just filter for these specific values.
    # If the filtered data contains other variations (e.g. "1교구/구역장"), they won't be counted here 
    # unless we map them. Assuming exact match for now based on "1교구 또는 1교구/무소속...".
    
    individual_counts = filtered_df[filtered_df['Group'].isin(target_groups)]['Group'].value_counts().reindex(target_groups, fill_value=0)
    
    # 4. Count Households (by Address) for specific groups
    print("Calculating household counts...")
    household_counts = {}
    
    for group in target_groups:
        # Get subset for this group
        group_df = filtered_df[filtered_df['Group'] == group]
        # Count unique addresses
        # Drop duplicates based on address
        unique_households = group_df.drop_duplicates(subset=['address'])
        household_counts[group] = len(unique_households)
    
    household_series = pd.Series(household_counts, name='Households')
    individual_series = pd.Series(individual_counts, name='Individuals')
    
    summary_df = pd.DataFrame({
        'Individuals': individual_series,
        'Households': household_series
    })
    
    # Add a Total row
    summary_df.loc['Total'] = summary_df.sum()
    
    print("\nSummary Counts:")
    print(summary_df)

    # 5. Generate Final Summary Output
    with pd.ExcelWriter(output_file) as writer:
        summary_df.to_excel(writer, sheet_name='Summary')
        filtered_df.to_excel(writer, sheet_name='Filtered_Data', index=False)
    
    print(f"Final summary saved to {output_file}")

if __name__ == "__main__":
    process_parish_data()
