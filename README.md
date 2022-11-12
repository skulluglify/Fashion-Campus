# Fashion-Campus
Final Project Startup Campus Track BE x AI
API requirement : https://docs.google.com/presentation/d/1e5XoOiWgGf6WTeNXdpfNdMN9_R_Q9FftgHjzigaCoYo/edit?usp=share_link
Project Progress : https://docs.google.com/spreadsheets/d/1whBKn8omWPQhWK7Q97opmVig0BBWrpyZ_74Cfddj_k4/edit?usp=sharing

### RULES
- Master **NO PUSH NO MERGE**
- Development **NO PUSH** (just merge request)
- Only use "SELECT/ INSERT/ UPDATE/ DELETE" on **run_query**
- Don't touch/ use file schema.py

## Python Version
```
python3 --version
```
Must 'Python 3.8.10'

## Create Virtual Enviroment
```
python3 -m venv venv
```

## Active venv
```
source venv/bin/activate
```

## Install Requirements
```
pip install -r req.txt
sudo apt install make
```

## Run Server
```
/Fashion-Campus$ make run
```

## Run Tester
```
/Fashion-Campus$ make tester
```

# STATUS ENDPOINT & TESTER
- [x] Endpoint
:ballot_box_with_check: Tester

UNIVERSAL
- [x] Get Image

HOME
- [x] Get Banner
- [ ] Get Category :ballot_box_with_check:

AUTHENTICATION
- [x] Sign-up :ballot_box_with_check:
- [x] Sign-in :ballot_box_with_check:

PRODUCT LIST
- [ ] Get Product List
- [ ] Get Category
- [ ] Search Product by Image

PRODUCT DETAIL PAGE
- [x] Get Product Details
- [ ] Add to Cart

CART
- [ ] Get User’s Carts
- [ ] Get User’s Shipping Address
- [x] Get Shipping Price
- [x] Create Order
- [ ] Delete Cart Item

PROFILE PAGE
- [x] User Details
- [x] Change Shipping Address
- [x] Top-up Balance
- [x] Get User Balance
- [x] Get User Shipping Address
- [ ] User Orders

ADMIN PAGE
- [x] Get Orders
- [ ] Get Product List
- [x] Create Product :ballot_box_with_check:
- [ ] Update Product :ballot_box_with_check:
- [ ] Delete Product :ballot_box_with_check:
- [ ] Get Category :ballot_box_with_check:
- [x] Create Category :ballot_box_with_check:
- [x] Update Category :ballot_box_with_check:
- [ ] Delete Category :ballot_box_with_check:
- [ ] Get Total Sales
