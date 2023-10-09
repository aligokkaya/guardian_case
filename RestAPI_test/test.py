

"""1.Madde"""
# import requests

# # Token almak için POST isteği yap
# res = requests.post('http://localhost:8000/create_user/',
#     json={"username": "ali", "surname": "gkky"})

# # Yanıtı kontrol et
# if res.status_code == 200:
#     # Tokenı al
#     token = res.json().get('token')
#     print('Token:', token)
# else:
#     print('Authentication failed:', res.text)









# """Token kontrol """
# import requests

# url = 'http://127.0.0.1:8000/protected'
# headers = {
#     'Authorization': 'Bearer '+token  # tokenı buraya yerleştirin
# }

# response = requests.get(url, headers=headers)
# result = response.json()

# if response.status_code == 200:
#     print('Başarılı:', result['message'])
# else:
#     print('Hata:', result['message'])











# # """burası 2. ve 3. madde """  
# import requests

# url = "http://localhost:8000/upload"
# token2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJndWFyZGlhbiIsImV4cCI6MTcyODIyNDM2M30.TyAjx5g00t7NLgrbm05zp6WfwE6CTYLEqpFwMrY7rdU"

# file_path = "04-01-Financial Sample Data-1.xlsx"

# headers = {"Authorization": f"Bearer {token2}"}
# files = {"file": (file_path, open(file_path, "rb"))}

# params = {"token": token2}  # "token" parametresini ekleyin

# response = requests.post(url, headers=headers, files=files, params=params)

# print(response.status_code)
# print(response.json())






# """4. Madde"""

# import requests

# url = "http://localhost:8000/brut_satis/Midmarket"  # İstek atılacak endpoint URL'i
# headers = {"token": token}  # Kullanıcının tokenini headers'a ekleyin
# params = {"para_birimi": "EUR"}  # İsteğin parametreleri (isteğe bağlı)

# response = requests.get(url, headers=headers, params=params)

# if response.status_code == 200:
#     data = response.json()
#     segment = data["segment"]
#     brut_satis = data["brut_satis"]
#     para_birimi = data["para_birimi"]
#     print(f"Segment: {segment}")
#     print(f"Brüt Satış: {brut_satis} {para_birimi}")
# else:
#     print("İstek başarısız. Hata kodu:", response.status_code)
#     print("Hata mesajı:", response.text)








"""Ekle sil güncelle"""

# import requests

# base_url = "http://localhost:8000"  # API'nin temel URL'si
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJndWFyZGlhbiIsImV4cCI6MTcyODIyNDM2M30.TyAjx5g00t7NLgrbm05zp6WfwE6CTYLEqpFwMrY7rdU"  # Kullanıcı tokenı

# # Yeni bir kayıt oluşturma
# create_data_url = base_url + "/create_data"
# headers = {"token":token}
# data = {
#     "segment": "Segment 1",
#     "country": "Country 1",
#     "product": "Product 1",
#     "discount_band": "Discount Band 1",
#     "units_sold": '100',
#     "manufacturing_price": '10.5',
#     "sale_price": '15.0',
#     "gross_sales": '1500.0',
#     "discounts": '200.0',
#     "sales": '1300.0',
#     "cogs":'900.0',
#     "profit": '400.0',
#     "date": "2023-10-07",
#     "month_number": '10',
#     "month_name": "October",
#     "year": '2023'
# }

# response = requests.post(create_data_url, headers=headers, json=data)
# if response.status_code == 200:
#     result = response.json()
#     print(result["message"])
#     print(result["data"])
# else:
#     print("Kayıt oluşturma başarısız.")

# # Bir kaydı güncelleme
# data_id = 2114  # Güncellenecek kaydın ID'si
# update_data_url = base_url + f"/update_data/{data_id}"
# updated_data =  {
#     "segment": "Segment 1",
#     "country": "Country 1",
#     "product": "Product 1",
#     "discount_band": "Discount Band 1",
#     "units_sold": '100',
#     "manufacturing_price": '10.5',
#     "sale_price": '15.0',
#     "gross_sales": '1500.0',
#     "discounts": '200.0',
#     "sales": '1300.0',
#     "cogs":'900.0',
#     "profit": '400.0',
#     "date": "2023-10-07",
#     "month_number": '10',
#     "month_name": "October",
#     "year": '2023'
# }
# response = requests.put(update_data_url, headers=headers, json=data)
# if response.status_code == 200:
#     result = response.json()
#     print(result["message"])
#     print(result["data"])
# else:
#     print("Kayıt güncelleme başarısız.")

# # Bir kaydı silme
# data_id = 2114  # Silinecek kaydın ID'si
# delete_data_url = base_url + f"/delete_data/{data_id}"
# response = requests.delete(delete_data_url, headers=headers)
# if response.status_code == 200:
#     result = response.json()
#     print(result["message"])
# else:
#     print("Kayıt silme başarısız.")

# # Kayıtları listeleme
# list_data_url = base_url + "/list_data"
# response = requests.get(list_data_url, headers=headers)
# if response.status_code == 200:
#     result = response.json()
#     print("Sayfa:", result["page"])
#     print("Kayıt sayısı:", result["total_count"])
#     print("Kayıtlar:")
#     for item in result["data"]:
#         print(item)
# else:
#     print("Kayıt listeleme başarısız.")








"""Gün sonu export kaydı"""
# import requests

# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE3MjgzNDg0MTd9.bLyAM4EtmJrUQYT8kl6Jevn3FPjYP8S6RiT9C381nBo"
# url = "http://localhost:8000/export_data"
# headers = {"token": token}

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     with open("exported_data.xlsx", "wb") as file:
#         file.write(response.content)
#     print("Excel dosyası başarıyla alındı.")
# else:
#     print("Excel dosyası alınamadı. Hata kodu:", response.status_code)


