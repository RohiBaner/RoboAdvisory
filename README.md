# RoboAdvisory
MSBD6000E-FinTechProject-WIP

# SWIPE ADVISORY - Robo-Advisory App for India

**WIP**

## Getting Started

### Prerequisites

What things you need to install the software and how to install them

```
import json
import os
import requests
import pandas as pd
import pickle
import flask
import flask_bootstrap
```

### Installing
Most of the libraries will come automatically with Anaconda. Flask needs to be installed separately by the following:
```
pip install flask
pip install flask_bootstrap
```

## To Run
```
python Final.py
```

# How does this work?
API keys are being used from AlphaVantage to get real-time stock prices. Using these, this app can perform the following tasks:
- Advice you to buy particular stocks depending on your risk tolerance.
- Get conversion rates between both digital currencies and crypto currencies
- Balance and maintain your portfolio

# Target Audience

Age Groups and their preferences (based on our research):
•	23 – 33
¬	Emergency Fund
¬	Tax Save
¬	Purchase Goals

•	33- 50
¬	Emergency Fund
¬	Tax Save
¬	Wealth
¬	Children
¬	Retirement

•	50 – 70
¬	Retirement
¬	Children 
¬	Wealth

**Note**: Children category for 33-70 age group includes: education and wedding of their children

# Goal Setting Interface
Interface parameters for goal setting:
- Initial Investment
- Time span
- Monthly contribution
- Goal Amount

Example:
**For Tax Savings (23 to 50 Age Group Preference)**
Investing in Tax Saver Mutual Funds (in India) can help people save taxes and help in gaining higher returns. Interface can include taxable income and then suggest the suitable mutual funds for tax saving. 
le income and then suggest the suitable mutual funds for tax saving.

## Screenshots
Tutorial when you start the app: ![alt text](https://i.ibb.co/gRqYMYW/Screen-Shot-2019-03-30-at-15-46-27.png) <br/>
Goals available: ![alt text](https://i.ibb.co/QJ9nvxS/Screen-Shot-2019-03-30-at-15-54-21.png) <br/>

# Technology Architecture 
- Hosting
- Technology stack

# References
- https://www.ey.com/Publication/vwLUAssets/ey-the-evolution-of-robo-advisors-and-advisor-2-model/$FILE/ey-the-evolution-of-robo-advisors-and-advisor-2-model.pdf
- https://www2.deloitte.com/content/dam/Deloitte/de/Documents/financial-services/Robo-Advisory-in-Wealth-Management.pdf
- https://www.doughroller.net/investing/how-robo-advisors-make-money/
- https://www.idc.com/getdoc.jsp?containerId=AP43074317
- https://www2.deloitte.com/content/dam/Deloitte/sg/Documents/financial-services/sea-fsi-robo-advisers-asia-pacific.pdf
- https://www.accenture.com/_acnmedia/PDF-2/Accenture-Wealth-Management-Rise-of-Robo-Advice.pdf

## Future Work
- Adding wallet management system
- Financial advice ChatBot
- Adding human interaction system
