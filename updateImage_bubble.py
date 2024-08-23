import pandas as pd

# Load the CSV files
all_offers_df = pd.read_csv(r'D:\malej\Downloads\AllOffers.csv', usecols=['PUBLICATION'])
to_order_df = pd.read_csv(r'D:\malej\Downloads\toOrder.csv')

# Add a helper column to 'all_offers_df' to keep track of the original order
all_offers_df['Order'] = range(len(all_offers_df))

# Merge 'to_order_df' with 'all_offers_df' based on the publication names
# 'how='right'' ensures all entries in 'all_offers_df' dictate the order and are included
merged_df = pd.merge(all_offers_df, to_order_df, left_on='PUBLICATION', right_on='Publications', how='right')

# Sort by the new 'Order' column
merged_df.sort_values('Order', inplace=True)

# Drop the 'Order' and any other unnecessary columns
merged_df.drop(columns=['Order'], inplace=True)

# Reset the index
merged_df.reset_index(drop=True, inplace=True)

# Save the reordered DataFrame to a new CSV file
merged_df.to_csv(r'D:\malej\Downloads\ReorderedToOrder.csv', index=False)