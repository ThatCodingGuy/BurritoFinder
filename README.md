# BurritoFinder

This app offers a way to find food trucks near you on the map. It gets the information from https://data.sfgov.org/resource/rqzj-sfat.json, does some parsing on it, and offers it up on a RESTful API. This app also consumes that API with a single page app that makes heavy use of google maps.


#Installation
To install, clone the repo.
Then, set up a virtualenv using requirements.txt and python3.5
To run the backend tests:
```
nosetests
```

To run the server:
```
python server.py
```

#Technology stack
This project is built using python3 and flask for the backend.
For the front end, JQuery and BackBone.js were used, as well as google maps.

It was my first time using flask and BackBone.js, as well as my first time building a single page app.


#Design/Architecture(Backend) :
In the backend, I used a fairly standard MVC architecture. Since the controllers are few and thin for now, they are directly in the server.py file. 

As for the model, I decided to abstract the FoodTruck service behind an interface. To add new services, you simply have to implement the interface for the new service and register it's listener in the FoodTruckManager.

No persistence is currently used, but a caching layer for the 3rd party services would be a logical next step. Currently, every request the server receives creates another request for every 3rd party service we're integrated with. Ideally, we'd cache those results and only refresh them once in a while(every day?) to keep response times low.

#Design/Architecture(Frontend) :
As it was my first time building a single page application from scratch, there was a steep learning curve. I tried to keep the views and models seperated, but they're still a bit too coupled. 

Since I didn't have time to build an elegant solution surrounding loading only the pins nears you as you move the map, the frontend currently polls all food trucks near you with a very large radius. This is clearly non-optimal, but since the dataset is quite small for now, no noticeable slowdowns should occur.

#Quality:
To ensure software quality, I built unit tests for the model layer of the flask backend. The controller layer being quite thin, building tests for it isn't currently the biggest bang for my buck.

My current front end code is too coupled for tests, so the current priority is refactoring that to be testable. 
