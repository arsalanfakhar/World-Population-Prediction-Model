# World-Population-Prediction-Model
**Population growth** is known as one of the **driving forces** behind environmental problems, because the growing population demands more and more (non-renewable) resources for its own application.  

Population in the world is currently (2020) growing at a rate of around **1.05%** per year (down from 1.08% in 2019, 1.10% in 2018, and 1.12% in 2017). The current average population increase is estimated at **81 million people per year**.

## How our model works ?
Growth is usually thought of as a linear process: an increase by a constant amount over a period of time. But in reality it is a quadratic relationship rather than being linear and depends mainly on two parameters:

 - Alpha: Difference between birth rate and death rate in %per . Generally there is a direct relation between net growth and this.
 - Beta: Resources available in percent .Generally there is a inverse 		   relationship.

So when we tested different models we found out that net growth mainly depends on the above two parameters. Then we verified the results by comparing it with four of the most popular agencies and their prediction

 1. United States Census Bureau(UN)
 2. United Nations Department of Economic and Social Affairs
 3. Maddison
 4. Worldometers

Our prediction was close enough to the actual results. But it can be improved with more parameters.
## Description of parameters
Our Api or models requires you to send the following parameters:

 - Starting year : The year you want to start simulation from.
 - Starting population: The population of starting year which is given in billions.
 - Ending year:  The year you want to end the simulation.
 - Alpha: Default value is 0.025.
 - Beta: Defualt value is -0.018.

**Note:** The default values of alpha and beta were calculated by running simulation more than 1000 times and the best value was chosen for the model.
 # API Description
 We have hosted the API on heroku and the end point are:
 

 - [https://populationpredictorapp.herokuapp.com/test]
 This API returns just Hello world its made for testing purpose and is a GET API.
 - [https://populationpredictorapp.herokuapp.com/predict]
 It is a POST API which takes in json in the following format:
 ***Eg:***
 {"start_year":"2000",
	"end_year":"2100",
	"start_pop":"2.557629e+09",
	"alpha":"0.025",
	"beta":"-0.0018"
}

