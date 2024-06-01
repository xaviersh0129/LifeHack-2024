## Beasts: Police Station Finder

## Problem Statement

Our solution addresses Theme 3 Subtheme 1: Strengthening domestic security requires exploring solutions that utilize crime data analysis and patrol route optimization. The problem statement is to design a solution that seamlessly integrates crime hotspots analysis with patrol route optimization, allowing law enforcement agencies to prioritize higher crime risk areas and shorten emergency response times.

## How Does Our Hack Answer the Problem Statement?

Our solution effectively addresses the problem statement by requiring input of the address where a crime has occurred. It then outputs the police stations that are nearest to it in terms of travel time. In situations where multiple crimes are happening simultaneously in the same area and one police station cannot handle all the incidents, our algorithm ensures efficient resource allocation. Each police station has a limit on the number of cases it can manage. If this limit is exceeded, the algorithm activates the next nearest police station to assist. This approach prevents situations where a manpower shortage at one station leads to longer emergency response times. By leveraging the Google Maps API, we optimize the route for the fastest possible response, ensuring that the emergency services arrive promptly.

## How Did We Build Our Hack?

We built our hack using Python scripts and many libraries. We also used relevant datasets available online, such as the geojson of the Singapore map, the KML file of the police stations in Singapore, and past data on the number of cases dealt by each police station from 2011 to 2021.

## Important Files in the Repository

Datasets: Contains datasets used in the project.
police-station-finder/src: Contains source code for the React app.
combine.py: Python script to combine data from KML and geojson files.
datacleaning.ipynb: Jupyter notebook for data cleaning.
server.py: Backend server script.
.env: Environment variables file.
README.md: This file.

## Usage

To use the Police Station Finder:
1 Clone the repository to your local machine.
2 Navigate to the police-station-finder directory.
3 Create a .env file in the root directory and add your Google Maps API key:
REACT_APP_GOOGLE_MAPS_API_KEY=your_api_key_here
###Replace your_api_key_here with your actual Google Maps API key.
4 Install dependencies using npm install.
5 Start the backend server using python server.py.
6 Start the React app using npm start.
7 Enter the address where the crime has occurred in the form field and submit.
8 View the top 3 closest police stations and their travel times.

## Dataset

The dataset used includes:
cleaned_crime_data.csv
FivePreventableCrimeCasesRecordedByNeighbourhoodPoliceCentreNPCAnnual.csv
new.geojson
policestations.json
singapore_with_police_stations.geojson
SingaporePoliceForceNPCBoundary.geojson
SPFBoundaries.kml
SPFEstablishments.kml

## Contributors

xavierhua0129
EyuGongYi
kziyang1207
yolotouch
