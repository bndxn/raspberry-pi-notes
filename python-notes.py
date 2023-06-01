# Aside on comprehending list comprehensions 

[item for sublist in train_df['completion'] for item in sublist]

# think about this as:

[item # each item
 for sublist in train_df['completion'] # for each sublist in the main list (the outer loop)
 for item in sublist] # for each item in the sublist (the inner loop)