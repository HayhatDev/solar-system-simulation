# importing every needed liberarly:
from controller import Supervisor
import math
import json

supervisor = Supervisor()

# Main variables:
time_step = 64
epslion = 0.1
G = 0.001
dt = time_step / 1000.0
step_count = 0
print_interval = 50
MAX_STEPS = 100000
per_step = 1
threshold = 0.0000001

# Setting up the file for saving data and body masses:
simulation_data = {
    "SUN" : [],
    "MERCURY" : [],
    "VENUS" : [],
    "EARTH" : [],
    "MARS" : [],
    "JUPITER" : [],
    "SATURN" : [],
    "URANUS" : [],
    "NEPTUNE" : [],
    "COMET" : []
    }
    
masses = {
    "SUN": 5.0,
    "MERCURY": 0.000000830,
    "VENUS":   0.00001224,
    "EARTH":   0.00001502,
    "MARS":    0.000001614,
    "JUPITER": 0.004774,
    "SATURN":  0.001429,
    "URANUS":  0.0002183,
    "NEPTUNE": 0.0002576,
    "COMET": 0.0000000001
}
    
# classes for OOP system, to control every planet:
class Planet:

    # Main planets value function, to control each plaents with different values:
    def __init__(self, name, masses, a_value, e_value, supervisor, time_step, angle_degree=0.0):
        self.name = name
        self.a = a_value
        self.e = e_value
        self.mass = masses.get(self.name)
        self.robot_node = supervisor.getFromDef(self.name)
        if self.robot_node is None:
            raise RuntimeError(f"Error: No node with DEF '{self.name}' found.")

        self.translation_field = self.robot_node.getField("translation")
        if self.translation_field is None:
            raise RuntimeError(f"Error: Node '{self.name}' has no translation field.")
            
        # Radius calculation:
        radius = self.a * (1 + self.e)
        
        # Angle:
        self.angle = math.radians(angle_degree)
        
        # Velocity and Position caclulation and safety check:
        if self.a != 0.0:
            # Velocity:
            velocity = math.sqrt(G * masses.get("SUN") * ((2 / radius) - (1 / self.a)))
            self.velocity_x = -velocity * math.sin(self.angle)
            self.velocity_y =  velocity * math.cos(self.angle)
            
            # Position:
            self.x = radius * math.cos(self.angle)
            self.y = radius * math.sin(self.angle)
        else:
            self.x = 0.0
            self.y = 0.0
            self.velocity_x = 0.0
            self.velocity_y = 0.0
                   
        # Acceleration:
        self.acceleration_x = 0.0
        self.acceleration_y = 0.0
        
        self.translation_field.setSFVec3f([self.x, self.y, 0.0])
        
        self.time_step = time_step
        
    
    # Gravitational force function:
    def gravity(self, source_body):
    
        # target body gets affect by gravity force from the source body:
        target_body = self

        # calculate the distance between the bodies
        x_distance = source_body.x -  target_body.x
        y_distance = source_body.y - target_body.y
        
        # get the radius
        radius_softend = math.sqrt(x_distance**2 + y_distance**2 + epslion**2)
        
        # check if the radius is extermly small or equal to 0:
        # if so, skip the calculations:
        if radius_softend < threshold:
            return
         
        # now, calculate the acceleraion from the source body on the target:   
        acceleration = G * source_body.mass / radius_softend**2
        self.acceleration_x += acceleration * x_distance / radius_softend
        self.acceleration_y += acceleration * y_distance / radius_softend
        

# Setting up each planet and its values:
# MERCURY:
MERCURY = Planet("MERCURY", masses, 2.5, 0.205, supervisor, time_step, angle_degree=45)
mercury_visual = supervisor.getFromDef("MERCURY_VISUAL")

# VENUS:
VENUS = Planet("VENUS", masses, 4, 0.007, supervisor, time_step, angle_degree=120)
venus_visual = supervisor.getFromDef("VENUS_VISUAL")

# EARTH:
EARTH = Planet("EARTH", masses, 6, 0.017, supervisor, time_step, angle_degree=200)
earth_visual = supervisor.getFromDef("EARTH_VISUAL")

# MARS:
MARS = Planet("MARS", masses, 8.5, 0.093, supervisor, time_step, angle_degree=310)
mars_visual = supervisor.getFromDef("MARS_VISUAL")

# JUPITER:
JUPITER = Planet("JUPITER", masses, 15, 0.049, supervisor, time_step, angle_degree=15)
jupiter_visual = supervisor.getFromDef("JUPITER_VISUAL")

# SATURN:
SATURN = Planet("SATURN", masses, 22, 0.057, supervisor, time_step, angle_degree=180)
saturn_visual = supervisor.getFromDef("SATURN_VISUAL")

# URANUS:
URANUS = Planet("URANUS", masses, 30, 0.046, supervisor, time_step, angle_degree=90)
uranus_visual = supervisor.getFromDef("URANUS_VISUAL")

# NEPTUNE:
NEPTUNE = Planet("NEPTUNE", masses, 38, 0.010, supervisor, time_step, angle_degree=270)
neptune_visual = supervisor.getFromDef("NEPTUNE_VISUAL")

# COMET:
COMET = Planet("COMET", masses, 12, 0.85, supervisor, time_step, angle_degree=0)

# SUN:
SUN = Planet("SUN", masses, 0, 0, supervisor, time_step)

# all simulation bodies in one list:
planets_comet = [MERCURY, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE, COMET]
Px = sum(body.mass * body.velocity_x for body in planets_comet)
Py = sum(body.mass * body.velocity_y for body in planets_comet)
SUN.velocity_x = - Px / SUN.mass
SUN.velocity_y = - Py / SUN.mass

bodies = [MERCURY, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE, COMET, SUN]

    
# Main loop, Running all the planets in it:
while supervisor.step(time_step) != -1:
    # Set starting acceleration(x and y) to 0.0:
    for body in bodies:
        body.acceleration_x = 0.0
        body.acceleration_y = 0.0
     
    # Set Targets adn Source bodies   
    for target in bodies:
        for source in bodies:
            if target != source:
                target.gravity(source)
                
# Update body stored velocity and position with new values after the gravity force and calculations are set:
    for body in bodies:
        NewVelocity_x = body.velocity_x + (body.acceleration_x * dt)
        NewVelocity_y = body.velocity_y + (body.acceleration_y * dt)
        body.velocity_x = NewVelocity_x
        body.velocity_y = NewVelocity_y
        
        NewPosition_x = body.x + (NewVelocity_x * dt)
        NewPosition_y = body.y + (NewVelocity_y * dt)
        body.x = NewPosition_x
        body.y = NewPosition_y
        

    # Set the new position to webots object real-time position:
    for body in bodies:
        body.translation_field.setSFVec3f([body.x, body.y, 0.0])
        r = math.sqrt(body.x**2 + body.y**2)
        v = math.sqrt(body.velocity_x**2 + body.velocity_y**2)
        body.angle = math.atan2(body.y, body.x)
        
        # Print and append all needed data:
        if body.name == "SUN" and step_count % print_interval == 0:
            print(f"SUN Real Position: x = {body.x:.6f}, y = {body.y:.6f}")
        if step_count % print_interval == 0:
            print(f"Step: {step_count}, r={r:.3f}, v={v:.3f}, angle={math.degrees(body.angle):.1f}°")
            print(f"  Position: ({body.x:.3f}, {body.y:.3f})")
            print("-" * 40)
        if step_count % per_step == 0:
            data_collecting = {
               "step" : step_count,
               "x" : body.x,
               "y" : body.y,
               "velocity" : v,
               "velocity_x" : body.velocity_x,
               "velocity_y" : body.velocity_y,
               "radius" : r,
               "angle" : body.angle
            }

            simulation_data[body.name].append(data_collecting)
            
    step_count += 1

    # if step count is equal or over max steps, get out of the loop:
    if step_count >= MAX_STEPS:
        break

# Saving the data in "simulation_data.json" file every time the simulation ends:
with open("simulation_data.json", "w") as f:
    json.dump(simulation_data, f, indent=4)

print("Data saved successfully! Datas are in simulation_data.json file!")

supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE) # pause the simulation
