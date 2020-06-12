## Table of contents
* [General info](#general-info)
* [What's Included](#whats-included)
* [Technologies](#technologies)
* [How to Use](#how-to-use)

## General info
This project is a suite of tools for the paper and pencil game Deadball.
	
## What's Included
On the Back End: 
* retrieveMLBRosters.py  -- Lambda function to retrieve roster from MLB database
* retrieveDeadballRoster.py (unfinished) -- retrieves prior team from DynamoDB or generates a new one from scratch

On the Front End:
* index.html & fetchRoster.js -- Displays MLB team from given year in table format
* scorecard.html & generateScorecard.js (unfinished) -- Creates print-ready scorecard from roster

## Team Data Format (JSON)
In order to make all parts interchangeable, team data should be passed in the following format:

team_name
player_count
players:

	jersey
	first_name
	last_name
	full_name


	position
	handedness
	traits
	batting_target
	walk_target


The data returned from an MLB database will have the following extra fields, which can be safely ignored:

org_id
year
players:
	id
	total_plate_appearances
	batting_average
	on_base_percentage

## Technologies
Project is written in:
* Python version: 2.7.17
* JavaScript version: 
* HTML5 

It makes use of the following AWS Services:
* S3 (static webpage hosting)
* API Gateway (MLB-to-Deadball API)
* AWS Lambda (deploying Python functions)
* DynamoDB (Coming Soon - store custom teams)
	
## How to Use
Backend elements can be tested via running them in python ("python <filename>.py")

Front-end elements can be tested with a compatible browser.

The full project can be seen at <insert S3 bucket address here>
