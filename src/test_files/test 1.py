fp = "PrecursorGrams.csv"

split = fp.split('.')
new_str = f'{split[0]}1.{split[1]}'
print(new_str)