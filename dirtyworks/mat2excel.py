import pandas as pd


output_py_file = "combined_tables.py"


output_content = "# tabledata \n\n"

# turn into python dictionary
for i in range(7):
    file_path = rf"D:\mfile\output_table{i}.xlsx"
    df = pd.read_excel(file_path)
    
    # DataFrame transform into dictionary
    data = df.to_dict(orient='records')
    
    output_content += f"table_{i} = {data}\n\n"

with open(output_py_file, "w", encoding="utf-8") as f:
    f.write(output_content)

print(f"load data {output_py_file}")