# 🌊 MAGICSEAWEED

Automation script that helps me in the task of interpreting when there are waves, scraping data from multiple magicseaweed sites (with threads) from the spots at the same time.

# 🏄 steps to put this to work:

Asure you have selenium and google chrome installed on your linux machine.

1. ```git clone this repo```
2. ```cd to folder```
3. ```python -m venv venv```
4. ```source venv/bin/activate```
3. ```pip install -r requirements.txt```
4. ```asure you downloaded google chrome and chromedriver, and chromedriver its on path```
5. ```python main.py```

📝 At the end, it will generate a text file (magicseaweed.csv), where you can see all the conditions and filter them by the desired ones.
Personally, the conditions that I consider favorables are the following: The wind_state parameter, I want it to be off-shore, additionally I look that the period is higher than 7s and strength is greater than 1m and less than ~2.5.

![CSV result](static/result.png?raw=true "CSV result")

This project is still under construction

If you enjoyed this project, I will be so much pleased if you give me a star (⭐).