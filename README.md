 ###### Create python virtual environment
 ```
 python -m venv .venv
 ```

 ###### Activate python virtual environment
 ```
 source .venv/bin/activate
 ```

 ###### Install python requirements
 ```
 pip install -r requirements.txt
 ```

 ###### CD into the project
 ```
 cd xerpa_test
 ```

 ###### DB
 ```
 python manage.py makemigrations
 python manage.py migrate
 ```

 ###### Load the data from the csv into db.sqlite3
 ```
 python manage.py load_data
 ```

 ###### Run server for api testing
 ```
 python manage.py runserver
 ```

 ###### Example queries
 ```
 POST http://127.0.0.1:8000/api/enrich/
 only "petrobras" is currently a keyword, so only two of this transactions will be enriched
 {
    "transactions": [
        {
            "id": "d1c0bd75-1aee-4901-9ef9-2a7897518e16",
            "description": "PETROBRAS 11 ORTE/7 SU",
            "amount": -6999,
            "date": "2023-12-01"
        },
        {
            "id": "53ae625b-59f7-4c86-9f49-fc0d49af9043",
            "description": "PETROBRAS 9 NTE/7 ORNTE",
            "amount": -16999,
            "date": "2023-12-01"
        },
        {
            "id": "a1bc32c6-570c-4023-a017-f22b8b920c05",
            "description": "PEDIDOSYA 3D RESTAURANT",
            "amount": -16999,
            "date": "2023-12-01"
        },
        {
            "id": "cc9264b1-e149-46c4-b3fb-ebc3756b7e80",
            "description": "McDonalds Las Condes",
            "amount": -16999,
            "date": "2023-12-01"
        }
    ]
}
 ```
 ```
 POST http://localhost:8000/api/commerces/
 use the api to create a comercio and get an uuid to then create a keyword related to it
 {
  "merchant_name": "PedidosYa",
  "category": "0a634e46-79fb-4bd1-a0f7-0fda27076a1a",
  "merchant_logo": null
}
 ```
 ```
 POST http://localhost:8000/api/keywords/
 use id generated for the comercio above to set the foreign key needed for the keyword relating to commerce
 {
    "keyword": "pedidosya",
    "merchant": "uuid"
}
If the same query to the /enrich/ endpoint is called now, the PedidosYa transaction should be enriched. Repeat for McDonald's if required.
 ```

 ###### Improving points
 ```
 Keyword detection in the Transaction description can be vastly improved. Check not only the first word, or check for abreviations and other ways to relate a Transaction with commerces, categories and keywords.
 ```
