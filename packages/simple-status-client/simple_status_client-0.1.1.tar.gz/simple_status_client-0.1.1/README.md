# SimpleStatusClient

A helper Client library in Python for the SimpleStatus project

## Getting Started

Ensure you have pulled [SimpleStatusServer](https://github.com/bravosierra99/SimpleStatus) and are running it (preferably straight from docker)

- clone library [SimpleStatusClient](https://github.com/bravosierra99/SimpleStatusClient)
- cd SimpleStatusClient
- python -m pip install . \_(this should be the python environment in which your stasus needing code runs)
- Within the code that you wish to send statuses do the following
  - `from SimpleStatusClient import APIClient, Colors`
  - `client = APIClient("http://*server_ip*/api")` server_ip should be the ip address of your docker container
  - `client.setConfig()` -- _fill in params_
  - `client.setStatus()` -- _fill in params_

Voila, you should be able to view your status on the dashboard.

### Example Usage

`client.set_config("My Component","This is the thingamabob for our whatsamaahousit server", 0, Colors.yellow)`

- <Response [200]>

`client.set_status("My Component",Colors.green,"All systems go")`
- <Response [200]>

## Things to keep in mind
- Components are identified by ID, which is calculated by hashing the name (or by calling the base functions and providing it directly e.g. `APIClient.set_status_base`).  
  - *DUPLICATE NAMES OVERWRITE*.  
  - This is by design, if you want to update your configuration and or status you can do it without jumping through any hoops.  Simply send a new configuration or status.  That being said if you have code in multiple places using the same id... they will be stepping on each other
- This library is provided as a convience, the REST API is full accessible and you can write your own interface if you would like.  
  - I promise to keep this library up to date and working to the best of my ability.  Maybe I'll even write tests for it.