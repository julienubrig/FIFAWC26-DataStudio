import pandas as pd
import kagglehub
import gspread
from google.oauth2.service_account import Credentials


# 1. Télécharger dataset Kaggle
path = kagglehub.dataset_download("swaptr/fifa-wc-2026-teams")
csv_path = f"{path}/teams.csv"
df = pd.read_csv(csv_path)


# 2. Connexion Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "fifa-wc2026-500516-8d45ce2c746b.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)


# 3. Ouvrir la Sheet
sheet_title = "FIFAWC26"
try:
    sheet = client.open(sheet_title).sheet1
except gspread.SpreadsheetNotFound:
    sh = client.create(sheet_title)
    sh.share("my-email@gmail.com", perm_type="user", role="writer")
    sheet = sh.sheet1


# 4. Envoyer les données
sheet.clear()
df = df.where(pd.notnull(df), "")
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print("Données envoyées dans Google Sheets !")