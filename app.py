from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Load boycott data
try:
    # Use 'latin-1' for Tunisian accents and 'sep=None' to let pandas guess the separator
    data = pd.read_csv("boycott_list.csv", encoding="latin-1", sep=",", quotechar='"')
    
    #  pandas still fails to split columns (length of columns is 1) ==> fix it manually
    if len(data.columns) == 1:
        col_name = data.columns[0] # This is "product,status,alternative"
        new_cols = col_name.replace('"', '').split(',')
        # Split the single column into three
        data[new_cols] = data[col_name].str.split(',', expand=True)
        # Drop the original messy column
        data = data.drop(columns=[col_name])

    # Standardize column names
    data.columns = [c.strip().replace('"', '').lower() for c in data.columns]
    
    # Clean the data cells
    for col in data.columns:
        data[col] = data[col].astype(str).str.strip().str.replace('"', '')

    print("SUCCESS: Loaded columns:", data.columns.tolist())
    print("Verification - First Product:", data.iloc[0]['product'])
    
except Exception as e:
    print(f"Error reading CSV: {e}")


@app.get("/")
def home():
    return {"message": "ConsumeSafe API is running"}

@app.get("/check/{product}")
def check_product(product: str):
    try:
        row = data[data["product"].str.lower() == product.lower()]
        if row.empty:
            return {
                "product": product,
                "status": "Not Found",
                "message": "Product not in database"
            }
        status = row.iloc[0]["status"]
        alternative = row.iloc[0]["alternative"]
        if status == "Boycott":
            return {
                "product": product,
                "status": "Boycott",
                "alternative": alternative,
                "message": "This product is boycotted. Try a Tunisian alternative."
            }
        return {
            "product": product,
            "status": "OK",
            "message": "This product is safe to buy"
        }
    except Exception as e:
        return {"error": str(e)}

