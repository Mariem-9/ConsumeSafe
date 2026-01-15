from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# --- 🛠 SETUP FOR FRONTEND ---
# Mount static files (CSS/JS) and templates (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 1️⃣ Load boycott CSV
try:
    data = pd.read_csv("boycott_list.csv", encoding="latin-1", sep=",", quotechar='"')
    
    # Fix if CSV is read as a single column
    if len(data.columns) == 1:
        col_name = data.columns[0]
        new_cols = col_name.replace('"','').split(',')
        data[new_cols] = data[col_name].str.split(',', expand=True)
        data = data.drop(columns=[col_name])

    # Clean columns
    data.columns = [c.strip().replace('"','').lower() for c in data.columns]
    
    # Clean cell values
    for col in data.columns:
        data[col] = data[col].astype(str).str.strip().str.replace('"','')

    # Make a product list for AI
    products = data["product"].tolist()
    print("Loaded products:", products[:5])

except Exception as e:
    print("Error loading CSV:", e)
    products = []  # fallback if CSV fails

# Train AI ONCE
vectorizer = TfidfVectorizer()
product_vectors = vectorizer.fit_transform(products)

def recommend_alternatives(user_product):
    user_vec = vectorizer.transform([user_product])
    scores = cosine_similarity(user_vec, product_vectors)[0]

    # Rank products by similarity
    ranked = sorted(zip(products, scores), key=lambda x: -x[1])

    # Filter out the original product and any boycotted ones
    safe_recs = [
        p for p, s in ranked
        if p.lower() != user_product.lower() and 
           data[data["product"].str.lower() == p.lower()].iloc[0]["status"] != "Boycott"
    ]

    return safe_recs[:3]  # top 3 safe alternatives

# @app.get("/")
# def home():
#     return {"message": "ConsumeSafe API is running"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # This renders the index.html file from the /templates folder
    return templates.TemplateResponse("index.html", {"request": request})

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

@app.get("/recommend")
def recommend(product_name: str):
    alternatives = recommend_alternatives(product_name)
    return {"product": product_name, "recommendations": alternatives}

