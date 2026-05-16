# ArtVault

## Installation & Running the Project

Install required packages:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start development server:

```bash
python manage.py runserver
```

Open in browser:

```text
http://127.0.0.1:8000/
```

## Extra requirements implemented:
- Share artwork link via Artwork details page
- View current highest bid
- Seller functionality:
  - User can create a seller profile
  - Seller can list new artwork for sale
  - Seller has sales and bid overview 
  - Seller has overview of their listed artworks 
  - Seller gets notified of new bids for their artwork
- Buyer gets notified when bid is accepted
- Users can message sellers and messages can be replied to
- Users can save artwork to favorites

## Demo Accounts

### Buyer Account
- Username: test_buyer
- Password: SomethingSecure2

### Seller Account
- Username: testuser_signup_1
- Password: Testpassword123

### Admin Account
- Username: alexia
- Password: gottpassword

