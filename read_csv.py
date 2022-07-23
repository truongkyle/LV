
# Import pandas
import pandas as pd
 
# reading csv file
data = pd.read_csv("./g4g2.csv")
data["Established"] = pd.to
print(data.iloc[2]["Established"].to_list)