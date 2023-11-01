# Introduction

**Urban Wind Simulation** is a speckle automate function that aims to solve wind comfort levels on urban level by using computational fluid dynamics with OpenFOAM 9. The base libraries behind it is [archaea-simulation](https://pypi.org/project/archaea-simulation/) and [archaea](https://pypi.org/project/archaea/) which include interfaces to convert given geometries into CFD scenarios.

![CFD Sample Result](/img/sample_result.png)

## Key Concepts

### 1. Domain Orientation

Domain orientation should be parallel to provided wind direction to calculate effect of wind on urban correctly. Direction of the wind represents with meteorological angles designated by δ, increase clockwise from the north (y) axis. Math angles, designated by α, increase counterclockwise from the east (x) axis.

![Math & Meteo Angles](/img/math_meteo_angles.png)

### 2. Atmospheric Boundary Layer (WIP)

Wind speed info collected from weather stations with exact values for exact heights. Creating an atmospheric boundary layer from reference wind speeds and heights is a must since higher altitudes are considered.

![Atmospheric Boundary Layer](/img/abl.png)

### 3. Wind Tunnel Sizing

Wind tunnel represents the domain in which air flows in it. Automate function calculates bounding box aligned with wind direction for geometries that aim to simulate, then with this bounding box function scales domain with given function inputs. Size of the domain has a direct impact on simulation time since the size of it affects the number of volume meshes.

![Wind Tunnel Sizing](/img/wind_tunnel_sizing.png)

### 4. Parallel Computing

OpenFOAM supports parallelism through domain decomposition, which involves dividing the computational domain into smaller subdomains that can be solved concurrently. This approach allows for efficient distribution of computational work, reducing simulation times and enabling the modeling of larger and more complex problems.

## Supported Speckle Objects

- Objects.Geometry.Brep
