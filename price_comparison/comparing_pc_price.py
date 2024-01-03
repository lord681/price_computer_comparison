import pandas as pd
from aliexpress import find_computers_aliexpress
from jumia import find_computers_jumia

def comparison():
  data_aliexpress=find_computers_aliexpress()
  data_aliexpress_copy=data_aliexpress[:]
  data_jumia=find_computers_jumia()
  data_jumia_copy=data_jumia[:]
  for items1 in data_jumia:
    for items2 in data_aliexpress:
      if items2['name']==items1['name'] and items2['total_price']>items1['total_price']:
        keys_to_remove=["name","price_without_transportion_fee","transport_fee","promo","total_price"]
        for item2 in data_aliexpress:
          for keys in keys_to_remove:
            del item2[keys]

      if items2['name']==items1['name'] and items2['total_price']<items1['total_price']:
        keys_to_remove=["name","price_without_transportion_fee","transport_fee","promo","total_price"]
        for item1 in data_jumia_copy:
          for keys in keys_to_remove:
            del item1[keys]

  new_data=pd.concat([pd.DataFrame(data_aliexpress_copy), pd.DataFrame(data_jumia_copy)], ignore_index=True)
  return new_data

if __name__=="__main__":

  new_data = comparison()
  with pd.ExcelWriter("final_output.xlsx") as writer:
    new_data.to_excel(writer, sheet_name="sheet1", index=False)
        
