# Final report: Particle swarm network simulation

| | |
|-|-|
| **Course**     | Modeling Abstractions for Embedded/Networked Systems (CSE5309) |
| **Instructor** | Fei Miao
| **Date**       | Spring 2022
| **Student**    | Lynn Pepin
| **NetID**      | tmp13009, 2079724
| **Due:**       | May 7th

# Basic functionality

The goal is to simulate a discrete-time network wireless physical-level mesh network. The network has $N$ particles in a swarm communicating over $k$ channels.

This simulation is implemented using Python3, numpy, and PyGame[^pygame], the latter of which is used for rendering the simulation.

[^pygame]: https://www.pygame.org/


# Appendix A: Particle movement patterns

The $N$ particles are spawned at random at radius $\mathcal{N}(\mu=100,\sigma=10)$ and angle $\mathcal{U}(2\pi)$ from center. The particles do not collide with one another and obey basic Newtonian physics.

The particles move according to a system of differential equations:

$$\frac{d\theta}{dt} = \frac{\pi}{r^2}$$

$$\frac{dr}{dt} = \frac{(100 - x)^3}{100000}$$



# Appendix B: Table of notation

|||
|-|-|
| $(r, \theta)$ | Polar coordinates in (meters, radians)
| (x, y)      | Cartesian coordinates, in meters
| $n \in N$   | Node index
| $k \in K$   | Channel index
| $t$         | Time in seconds
| $\Delta t$  | Simulation timestep


The goal of this system is to simulate the physical layer of a wireless mesh network in order to measure its raw throughput. The network is composed of $N$ nodes, operating as a swarm

This system simulates the motion of $N$ massless particles, communicating over a wireless system with $K$ channels

<!-- # Appendix A: Signals and bits

We want to simulate a raw wireless physical layer and measure the throughput in bits. This means no error-correction. We use a simplified formula for loss:[^pathloss]

$$L = 20 \log_{10}\left(4\pi d \lambda^{-1}\right)$$

where $d$ is in meters and $\lambda = 6\cdot10^{9}\text{Hz} = 6\text{GHz}$.

[^pathloss]: Path loss details are succinctly explained at https://en.wikipedia.org/wiki/Path_loss

Signal attenuation is roughly modeled by $I = e^{-a\cdot d}$, where $I$ is the signal intensity ratio, $a$ is a coefficient, and $d$ is distance (in meters for our purpose). We use this intenisty, $I$ (which ranges from 1 to 0) as the probability a single bit is lost to noise.

There are *very very many* constants one needs to derive or source, many of which are not open knowledge as 6GHz WiFi is very new. Relevant constants include 6GHz background noise levels and attenuation rate through different mediums. 

 We assume an attenuation of roughly 50 dB per meter (https://www.extremenetworks.com/extreme-networks-blog/how-far-will-wi-fi-6e-travel-in-6-ghz/, https://www.nctatechnicalpapers.com/Paper/2019/2019-the-promise-of-wifi-in-the-6-ghz-band/download). This means --->

