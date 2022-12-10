# 🌊 MAGICSEAWEED

Automation script that helps me in the task of interpreting when there are waves, scraping data from multiple magicseaweed sites (with threads) from the spots at the same time.

# 🏄 steps to put this to work:

Asure you have selenium and google chrome installed on your linux machine.

1. ```git clone this repo```
2. ```cd to folder```
3. ```python -m venv venv```
4. ```source venv/bin/activate```
5. ```pip install -r requirements.txt```
6. ```streamlit run main.py```


Personally, the conditions that I consider favorables are the following: The wind_state parameter, I want it to be off-shore, additionally I look that the period is higher than 7s and strength is greater than 1m and less than ~2.5.

This project is still under construction

If you enjoyed this project, I will be so much pleased if you give me a star (⭐).