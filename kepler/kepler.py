# importing every needed liberarly:
from controller import Supervisor
import math
import json

supervisor = Supervisor()

# Main variables:
time_step = 64
G = 0.001
SUN_MASS = 5
center_x, center_y = 0, 0
dt = time_step / 1000.0
step_count = 0
print_interval = 50
MAX_STEPS = 100000
per_step = 1

# setting up the file for saving data in it:
simulation_data = {
    "MERCURY" : [],
    "VENUS" : [],
    "EARTH" : [],
    "MARS" : [],
    "JUPITER" : [],
    "SATURN" : [],
    "URANUS" : [],
    "NEPTUNE" : []
}

# classes for OOP system, to control every planet:
class Planet:

    # Main planets value function, to control each plaents with different values:
    def __init__(self, name, a_value, e_value, supervisor, time_step):
        self.name = name
        self.a = a_value
        self.e = e_value
        self.robot_node = supervisor.getFromDef(self.name)
        if self.robot_node is None:
            print(f"Error: No robot with DEF '{self.name}' found.")
            exit()
        self.angle = math.pi
        self.time_step = time_step

    # Funtion for controlling the planets movement, using keplers law:
    def move(self, step_count, dt):
        r = self.a * (1 - self.e**2) / (1 + self.e * math.cos(self.angle))
        angular_speed = math.sqrt(G * SUN_MASS * self.a * (1 - self.e**2)) / (r**2)
        self.angle += angular_speed * dt
        v = math.sqrt(G * SUN_MASS * (2.0 / r - 1.0 / self.a))
        x = center_x + r * math.cos(self.angle)
        y = center_y + r * math.sin(self.angle)
        self.robot_node.getField("translation").setSFVec3f([x, y, 0])
        if step_count % print_interval == 0:
            print(f"Step: {step_count}, r={r:.3f}, v={v:.3f}, angle={math.degrees(self.angle):.1f}°")
            print(f"  Position: ({x:.3f}, {y:.3f})")
            print("-" * 40)
        if step_count % per_step == 0:
            data_collecting = {
                "step": step_count,
                "x": x,
                "y": y,
                "velocity": v,
                "radius": r,
                "angle": self.angle % (2 * math.pi)
            }
            simulation_data[self.name].append(data_collecting)

# Setting up each planet and its cordinantes:
# MERCURY:
MERCURY = Planet("MERCURY", 2.5, 0.205, supervisor, time_step)
mercury_visual = supervisor.getFromDef("MERCURY_VISUAL")

# VENUS:
VENUS = Planet("VENUS", 4, 0.007, supervisor, time_step)
venus_visual = supervisor.getFromDef("VENUS_VISUAL")

# EARTH:
EARTH = Planet("EARTH", 6, 0.017, supervisor, time_step)
earth_visual = supervisor.getFromDef("EARTH_VISUAL")

# MARS:
MARS = Planet("MARS", 8.5, 0.093, supervisor, time_step)
mars_visual = supervisor.getFromDef("MARS_VISUAL")

# JUPITER:
JUPITER = Planet("JUPITER", 15, 0.049, supervisor, time_step)
jupiter_visual = supervisor.getFromDef("JUPITER_VISUAL")

# SATURN:
SATURN = Planet("SATURN", 22, 0.057, supervisor, time_step)
saturn_visual = supervisor.getFromDef("SATURN_VISUAL")

# URANUS:
URANUS = Planet("URANUS", 30, 0.046, supervisor, time_step)
uranus_visual = supervisor.getFromDef("URANUS_VISUAL")

# NEPTUNE:
NEPTUNE = Planet("NEPTUNE", 38, 0.010, supervisor, time_step)
neptune_visual = supervisor.getFromDef("NEPTUNE_VISUAL")

# Main loop, Running all the planets in it:
while supervisor.step(time_step) != -1:
    step_count += 1
    # Move mercury:
    MERCURY.move(step_count, dt)
    mercury_visual.getField("translation").setSFVec3f([0, 0, 0.3])
    
    # Move venus:
    VENUS.move(step_count, dt)
    venus_visual.getField("translation").setSFVec3f([0, 0, 0.3])
    
    # Move earth:
    EARTH.move(step_count, dt)
    earth_visual.getField("translation").setSFVec3f([0, 0, 0.3])

    # Move mars:
    MARS.move(step_count, dt)
    mars_visual.getField("translation").setSFVec3f([0, 0, 0.3])
    
    # Move jupiter:
    JUPITER.move(step_count, dt)
    jupiter_visual.getField("translation").setSFVec3f([0, 0, 0.3])
    
    # Move saturn:
    SATURN.move(step_count, dt)
    saturn_visual.getField("translation").setSFVec3f([0, 0, 0.3])
    
    # Move uranus:
    URANUS.move(step_count, dt)
    uranus_visual.getField("translation").setSFVec3f([0, 0, 0.3])
    
    # Move neptune:
    NEPTUNE.move(step_count, dt)
    neptune_visual.getField("translation").setSFVec3f([0, 0, 0.3])

    # if step count is equal or over max steps, get out of the loop:
    if step_count >= MAX_STEPS:
        break

# Saving the data in "simulation_data.json" file every time the simulation ends:
with open("simulation_data.json", "w") as f:
    json.dump(simulation_data, f, indent=4)

print("Data saved successfully! Datas are in simulation_data.json file!")

supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE) # pause the simulation