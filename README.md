# IndieHedge

## Authors: Zack Boner, Konrad Siebor, Harsh Padhye

### Submission for HooHacks 2021

## Inspiration
We were inspired towards this project by the recent massive rise and subsequent massive fall of the $GME stock. We noticed a massive number of retail investors taking on a substantial amount of financial risk; many of them unaware of the potential consequences. Without the vast knowledge and capital to properly mitigate risk like a hedge fund manager, retail investors are liable to the volatility and whims of the week's "hot stock". We wanted to develop an applet that would encourage users to safely diversify and secure their investments.  Our goal is to retain the thrill of short term trading with small- and mid-cap companies, all while abstracting away the details behind risk analysis.

## What it does
We built a system that takes in a retail investor's most recent stock purchase, coupled with their own indications of how risky they thought their purchase was and how risky they'd like to be in the future, and recommends two sets of stocks. IndieHedge queries a user's recent retail investment and their perceived risk. Based on how much additional risk they are willing to take, IndieHedge suggests alternative small- and mid-cap stocks to diversify the user's portfolio and hedge their original bet.

## How we built it
Using data from Charles Schwab's US Small and Mid Cap Index Fund and the Yahoo Financials API, we built an unsupervised machine learning algorithm to classify stocks into risk categories. When a user submits their stock, we use our pretrained algorithm to classify it into a risk category. Our recommendation algorithm then examines the user's desired future risk and recommends a menagerie of stocks which fall into that risk category. We also examine the delta between the user's perceived risk when purchasing the stock and the risk we measure to recommend risk management tools and good portfolio practices to the user.

## Challenges we ran into
The primary challenge we faced was the difficulty, surprisingly, in obtaining relevant data to our project. Most existing stock data has global trends, price/volume statistics, and market share statistics, but very few data sources have pre-determined risk scores. We sourced most of our stock data from a 2-hour long session of API queries to the Yahoo Financial API. Another major challenge we faced was rapid deployment of a web app to Heroku. We are not very experienced web developers, and we faced a wide variety of niche bugs associated with Heroku's Procfiles that took us precious hours to debug. 

## Accomplishments that we're proud of
We are extremely proud of the fact that we managed to take a project from stark beginning to a strong finale in a 24 hour time period. We are proud of our strong integration of our frontend web app and our backend data science and machine learning tools. Both sides of the project were developed in a way that our frontend and backend merged seamlessly. We are also proud of the fact that we, the authors, do not have substantial experience or knowledge in the finance field, but were still able to deliver what we believe to be a useful and powerful tool for other inexperienced financiers to stay safe.

## What we learned
All three of us came into this project with marginal knowledge of the finance field, and we came out with a much better understanding of many financial terms and best practices. We learned, in the course of recommending ways to mitigate risk, how to mitigate risk ourselves, and we all feel more confident in our own decisions to (or not to) invest. We also learned on the fly how to use flask to build web apps fast, and also how to integrate a machine learning model into a flask app (it was much easier than expected). We also learned on the fly how to turn a prototype website and backend into a mostly functional web application.

## What's next for IndieHedge
In the future, IndieHedge would like to expand to suggest both derivatives and securities, recommending ways to leverage investments by balancing stocks and options. We would also like to import a user's entire purchasing history and current portfolio in making smarter decisions for that particular user. From the user's portfolio, we would investigate broader risk trends of that user's buying history to get a better idea of the type of investor we're dealing with. We'd love to port this to a mobile application to be aligned with the type of platforms that retail investors expect. It should be stressed that we wish to remain a tool for retail investors to enjoy investing.
