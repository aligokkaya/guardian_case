import jwt
from fastapi import FastAPI, Depends, UploadFile, File, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
import requests
from jose import jwt
import io
import pandas as pd
from fastapi.responses import StreamingResponse
from app.model import SessionLocal,UserCreate,User,Data,DataCreate,DataUpdate
# import sys
# sys.path.insert(0, ".")
app = FastAPI()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

class AuthHandler:
    def __init__(self, secret_key, algorithm):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Token süresi doldu."
        except jwt.InvalidTokenError:
            return "Geçersiz token."

auth_handler = AuthHandler(SECRET_KEY, ALGORITHM)
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_token(user: UserCreate, db) -> str:
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        return existing_user.token

    payload = {
        'sub': user.username,
        'exp': datetime.utcnow() + timedelta(days=365)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    new_user = User(username=user.username, surname=user.surname, token=token)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return token

@app.post("/create_user")
async def create_user(user: UserCreate, db=Depends(get_db)):
    token = get_token(user, db)
    return {"message": "Kullanıcı başarıyla oluşturuldu", "token": token}

@app.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    username = auth_handler.decode_token(credentials.credentials)
    # print(isinstance(username, str))
    # print(username)
    if isinstance(username, str):
        return {"message": username}

@app.post("/upload")
async def save_from_excel(token: str, file: UploadFile = File(...), db=Depends(get_db)):
    if not token:
        return {"message": "Token eksik."}
    
    # result = auth_handler.decode_token(token)
    user = db.query(User).filter(User.token == token).first()
    # print(result)
    print(user)

    if user:
        try:
            contents = await file.read()
            df = pd.read_excel(BytesIO(contents))

            for idx, row in df.iterrows():
                try:
                    if pd.isna(row['Segment']) or pd.isna(row['Country']) or pd.isna(row['Product']):
                        continue

                    units_sold = int(row['Units Sold']) if pd.notna(row['Units Sold']) else ''
                    manufacturing_price = int(row['Manufacturing Price']) if pd.notna(row['Manufacturing Price']) else ''
                    sale_price = int(row['Sale Price']) if pd.notna(row['Sale Price']) else ''
                    gross_sales = int(row['Gross Sales']) if pd.notna(row['Gross Sales']) else ''
                    discounts = int(row['Discounts']) if pd.notna(row['Discounts']) else ''

                    data = Data(
                        user_id=user.id,
                        segment=row['Segment'],
                        country=row['Country'],
                        product=row['Product'],
                        discount_band=row['Discount Band'],
                        units_sold=units_sold,
                        manufacturing_price=manufacturing_price,
                        sale_price=sale_price,
                        gross_sales=gross_sales,
                        discounts=discounts,
                        sales=int(row[' Sales']) if pd.notna(row[' Sales']) else '',
                        cogs=int(row['COGS']) if pd.notna(row['COGS']) else '',
                        profit=int(row['Profit']) if pd.notna(row['Profit']) else '',
                        date=row['Date'],
                        month_number=int(row['Month Number']) if pd.notna(row['Month Number']) else '',
                        month_name=row['Month Name'],
                        year=int(row['Year']) if pd.notna(row['Year']) else ''
                    )
                    db.add(data)
                except Exception as e:
                    return {"message": f"Hata oluştu satır kaydedilemedi: {str(e)}, Satır: {idx + 2}, Değerler: {row}"}

            db.commit()
            return {"message": "Veriler başarıyla kaydedildi."}
        except Exception as e:
            return {"message": f"Hata oluştu: {str(e)}"}
    else:
        return {"message": 'Geçersiz Token'}


def get_user(token: str = Header(...), db=Depends(get_db)):
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    return user

@app.get("/brut_satis/{segment}")
async def get_brut_satis(segment: str, para_birimi: str = "USD", user: User = Depends(get_user), db=Depends(get_db)):
    brutsatis_query = db.query(Data).join(User).filter(User.id == user.id, Data.segment == segment)
    
    brutsatis = brutsatis_query.with_entities(Data.gross_sales).all()
    toplam_brut_satis = sum([float(satis[0]) for satis in brutsatis])

    exchangerate_api_url = f"https://api.exchangerate-api.com/v4/latest/{para_birimi}"
    response = requests.get(exchangerate_api_url)
    exchange_rates = response.json().get("rates")

    if para_birimi != "USD" and para_birimi in exchange_rates:
        usd_rate = exchange_rates["USD"]
        brut_satis_para_birimi = toplam_brut_satis / usd_rate
    else:
        brut_satis_para_birimi = toplam_brut_satis

    return {"segment": segment, "brut_satis": brut_satis_para_birimi, "para_birimi": para_birimi}




@app.post("/create_data")
async def create_data(data: DataCreate, user: User = Depends(get_user), db=Depends(get_db)):
    new_data = Data(
        user_id=user.id,
        segment=data.segment,
        country=data.country,
        product=data.product,
        discount_band=data.discount_band,
        units_sold=data.units_sold,
        manufacturing_price=data.manufacturing_price,
        sale_price=data.sale_price,
        gross_sales=data.gross_sales,
        discounts=data.discounts,
        sales=data.sales,
        cogs=data.cogs,
        profit=data.profit,
        date=data.date,
        month_number=data.month_number,
        month_name=data.month_name,
        year=data.year
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"message": "Kayıt başarıyla oluşturuldu", "data": new_data}

@app.put("/update_data/{data_id}")
async def update_data(data_id: int, data: DataUpdate, user: User = Depends(get_user), db=Depends(get_db)):
    existing_data = db.query(Data).filter(Data.id == data_id, Data.user_id == user.id).first()
    if not existing_data:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")

    existing_data.segment = data.segment
    existing_data.country = data.country
    existing_data.product = data.product
    existing_data.discount_band = data.discount_band
    existing_data.units_sold = data.units_sold
    existing_data.manufacturing_price = data.manufacturing_price
    existing_data.sale_price = data.sale_price
    existing_data.gross_sales = data.gross_sales
    existing_data.discounts = data.discounts
    existing_data.sales = data.sales
    existing_data.cogs = data.cogs
    existing_data.profit = data.profit
    existing_data.date = data.date
    existing_data.month_number = data.month_number
    existing_data.month_name = data.month_name
    existing_data.year = data.year

    db.commit()
    return {"message": "Kayıt başarıyla güncellendi", "data": existing_data}

@app.delete("/delete_data/{data_id}")
async def delete_data(data_id: int, user: User = Depends(get_user), db=Depends(get_db)):
    existing_data = db.query(Data).filter(Data.id == data_id, Data.user_id == user.id).first()
    if not existing_data:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")

    db.delete(existing_data)
    db.commit()
    return {"message": "Kayıt başarıyla silindi"}

@app.get("/list_data")
async def list_data(page: int = 1, user: User = Depends(get_user), db=Depends(get_db)):
    per_page = 20
    offset = (page - 1) * per_page

    total_count = db.query(Data).filter(Data.user_id == user.id).count()
    total_pages = (total_count - 1) // per_page + 1

    data = db.query(Data).filter(Data.user_id == user.id).offset(offset).limit(per_page).all()

    return {
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_count": total_count,
        "data": data
    }


@app.get("/export_data")
async def export_data(user: User = Depends(get_user), db=Depends(get_db)):
    user = db.query(User).filter(User.token == user.token).first()
    data = db.query(Data).filter(Data.user_id == user.id).all()

    df_list = []
    for item in data:
        df_list.append({
            'segment': item.segment,
            'country': item.country,
            'product': item.product,
            'discount_band': item.discount_band,
            'units_sold': item.units_sold,
            'manufacturing_price': item.manufacturing_price,
            'sale_price': item.sale_price,
            'gross_sales': item.gross_sales,
            'discounts': item.discounts,
            'sales': item.sales,
            'cogs': item.cogs,
            'profit': item.profit,
            'date': item.date,
            'month_number': item.month_number,
            'month_name': item.month_name,
            'year': item.year
        })

    df = pd.DataFrame(df_list)

    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False, sheet_name="Exported Data")
    excel_file.seek(0)

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=exported_data.xlsx"}
    )

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app,host='0.0.0.0',port=5000)  