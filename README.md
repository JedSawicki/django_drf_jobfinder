# Django DRF job offers scraper
Scraping job offers never was that easy! Scraping script is using 5 polish web pages for getting job offers.

### Note
Beside HTTPX this project is using selenium with undetected-chromedriver in order to pass through Cloudflare security, this solution is extending scraping time up to 7 seconds.
## Requirements:
- Python 3.11
### Libraries
- django rest framework
- concurrent for multithreading
- HTTPX and selenium for requests
- Undetected-chromedriver for passing the cloudflare bot security
- Selectolax for parsing HTML
### Setup and Usage
![scraper](https://user-images.githubusercontent.com/95547700/173223892-2f526da5-3e46-485d-9ebf-6631cadfff08.PNG)
1. Pull the project
2. Create venv inside project folder and activate it
   ```
   cd /core
   python -m venv venv
   source venv/bin/activate
   ```
3. Install requirements to your virtual-env
   ```
   pip install -r requirements.txt
   ```  
4. Create .env file in your root folder and add your secret key
   ```
   touch .env
   ```
   - Generate secret key: https://djecrety.ir/
   - edit .env file:
   ```
   SECRET_KEY={your_secret_key}
   DEBUG=True
   ```
5. Now you can run your django drf app with development server!
   ```
   python manage.py runserver
   ```

Go to http://127.0.0.1:8000/ and start searching for a dream job!
