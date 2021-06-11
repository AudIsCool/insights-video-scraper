# insights-video-scraper
A small python script that scrapes and downloads videos from Insights.gg


# Requirements 
- Python 3


# Usage
The base code for fetching teams, channels and videos can be found in [graphql.py](./graphql.py), and example usage can be found in [main.py](./main.py). 

## Authentication
Insights uses cookies for authorization, primarily a session and token key, which you can find in your cookies under the name `__akshon__sessionv2` and `__akshon__token` respectively. In order to find your authentication cookies you can open your browser, go to your insights.gg dashboard, and look for those aforementioned cookies in the browser's developer console. You can find out how [here](https://www.cookieyes.com/how-to-check-cookies-on-your-website-manually)


<br>

You should store these cookies in your enviornmental variables :D

### In bash
```
export SESSION_COOKIE="YOUR_SESSION_HERE"
export TOKEN_COOKIE="YOUR_TOKEN_HERE"
``` 

or add them in your `~/.bashrc` file. 


### Windows 
You can read how [here](https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html#GUID-DD6F9982-60D5-48F6-8270-A27EC53807D0).

<br>

Click the names should be the same as above (`SESSION_COOKIE` and `TOKEN_COOKIE`), their values should be the values of `__akshon__sessionv2` and `__akshon__token` respectively.

## Running 
After that you should just be able to run the `main.py` file with python3 :D 