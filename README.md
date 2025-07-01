# tafuta
This project aim combating the alarming issue of kidnappings in the Democratic Republic of Congo. Criminals are exploiting 
local phone numbers to extort money from victims' families, often leading to tragic outcomes, even after ransom payments. 
Our solution focuses on tracking these suspicious numbers, enabling authorities and communities to proactively prevent such crimes and save lives.

# Tafuta

Tafuta is a web-based application designed to combat the alarming issue of kidnappings in the Democratic Republic of Congo. Criminals often exploit local phone numbers to extort money from victims' families, leading to tragic outcomes even after ransom payments. This project aims to track suspicious phone numbers, enabling authorities and communities to proactively prevent such crimes and save lives.

## Features

- **Phone Number Tracking**: Track suspicious phone numbers and identify their locations using triangulation and network APIs.
- **Reporting System**: Report suspicious phone numbers to help build a database of potentially harmful numbers.
- **Dashboard**: Visualize reports and tracking data with charts and filters for better insights.
- **Map-Based Tracking**: View tracked locations on an interactive map with detailed metadata.
- **User Authentication**: Secure login and registration system for authorized users.
- **Export Data**: Export reported numbers and tracking logs as CSV files for further analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/marcelbag/tafuta.git
   cd tafuta

```
2. Install dependencies:
``` pip install -r requirements.txt ```

3. Set up the database:
```python backend/models/initialize_db.py```

4. Run the application:
``` python backend/app.py ```

5. Run the application:

Access the application at http://127.0.0.1:5000.

## Technologies used 



## Project Structure

```
/backend
  /models
      database.py
      initialize.py
      number.py
      user.py
      tafuta.db
  /routes
      track_number.py
      report_number.py
      login.py
      register.py
      report_number.py
      track_number.py
  /static
        /assets
          /icons
          /images
      /css
          styles.css
      /js
       app.js   
       dashboard.js
       report.js
       track_map.js
  /templates
      dashboard.html
      report.html
      login.html
      register.html
      index.html
/app.py
/utilis
      tringulation.py
      validation.py
```

![alt text](image.png)