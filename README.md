# Django DRF job offers scraper
Scraping job offers never was that easy! Scraping script is using 5 polish web pages for getting job offers.
![scraper](https://user-images.githubusercontent.com/95547700/173223892-2f526da5-3e46-485d-9ebf-6631cadfff08.PNG)

### Note
Beside HTTPX this project is using selenium with undetected-chromedriver in order to pass through Cloudflare security, this solution is extending scraping time up to 7 seconds.
## Requirements:
- Python 3.11
- Docker
- Docker-Compose 
### Libraries
- django rest framework
- concurrent for multithreading
- HTTPX and selenium for requests
- Undetected-chromedriver for passing the cloudflare bot security
- Selectolax for parsing HTML
### Setup and Usage - Docker Compose method

1. Pull the project
2. Edit .env.dev file in your root folder and add your secret key
   - Generate secret key: https://djecrety.ir/
   - edit .env.dev file:
   ```
   DEBUG=1
   SECRET_KEY={your_secret_key}
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   ```
3. Build and run docker compose:
   ```
   cd /core
   sudo docker-compose up --build -d
   ```
   Now the container will be builded, prepared for use and started in the background, default name is 'django-drf'
   ```
   > sudo docker ps
   CONTAINER ID   IMAGE      COMMAND           CREATED          STATUS          PORTS         NAMES
   <>             core_web   "python manage.py ru…"                                           django-drf

   > sudo docker-compose ps
   Name                 Command               State                    Ports                  
   ----------------------------------------------------------------------------------------------
   django-drf           python manage.py ...  Up                       0.0.0.0:8000->8000/tcp,:::8000->8000/tcp
   ```
4. Go to http://127.0.0.1:8000/ and start searching for a dream job!


### OUTDATED

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
