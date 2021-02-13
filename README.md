# Transit Bus Simulation
 
 ## Overview 
 
The goal of this repository is to create a side-by-side comparison of transit buses with combustion engines with those that are electric to advise policy in Mexico City.
 
Obtaining all the data was completed without any on-vehicle sensors. The process started by obtaining the shapefile route of each transit bus in Mexico City. These were then projected into a different coordinate refrence system to make them easier to work with [`CRS Projection`]. Then, elevation for points across the route were queried to calculate the gradient [`Gradient Querying`]. Next, traffic and speed data were utilized to create a speed profile of the area during different seasons and times of the day [`Speed Querying`]. This profile and the gradient data were then spatially joined and used to create a complete drive cycle with a one second resolution [`Cycle Generation`]. Finally, using these drive cycles along with bus specifications, a simulation software named FASTSim was employed to predict the difference in energy consumption profiles of electric and combustion engine along these routes [`Simulation`].
 
 ## Data Sources
 
 The data used in this project comes from the following sources:
 * Bus Route Shapefiles [add source]
 * Waze Speed Data [https://wazeopedia.waze.com/wiki/USA/Traffic_data]
 
 The software used in the project can be found here:
 * Google Maps Elevation API [https://developers.google.com/maps/documentation/elevation]
 * FASTSim [https://www.nrel.gov/transportation/fastsim.html]
 

 
 
