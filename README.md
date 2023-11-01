# Introduction

**Urban Wind Simulation** is a speckle automate function that aims to solve wind comfort levels on urban level by using computational fluid dynamics with OpenFOAM 9. The base libraries behind it is [archaea-simulation](https://pypi.org/project/archaea-simulation/) and [archaea](https://pypi.org/project/archaea/) which include interfaces to convert given geometries into CFD scenarios.

![CFD Sample Result](/img/sample_result.png)

## Inputs

1. Wind Direction

Direction of the wind represents with meteorological angles designated by δ, increase clockwise from the north (y) axis. Math angles, designated by α, increase counterclockwise from the east (x) axis.

![Math & Meteo Angles](/img/math_meteo_angles.png)

2. Wind Speed

Wind speed info collected from weather stations with exact values for exact heights. Creating atmospheric boundary layer from reference wind speeds and heights is a must since higher altitudes are considered. 

![Atmospheric Boundary Layer](/img/abl.png)

3. Reference Wind Speed Height (TODO)

Reference wind speed height helps to create atmospheric boundary layer for urban wind simulations.

5. Wind Tunnel Sizing

Wind tunnel represents with domain which air flows in it. Automate function calculates bounding box aligned with wind direction for geometries that aiming to simulate, then with this bounding box function scales domain with given function inputs.

![Wind Tunnel Sizing](/img/wind_tunnel_sizing.png)

4. Number of CPUs

Number of cores to run parallelly.

## Supported Speckle Objects

- Objects.Geometry.Brep
