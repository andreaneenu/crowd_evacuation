from Simulation_class import Simulation
import os
import time
from pathlib import Path
import numpy as np
# we have modified this code from the github repository: https://github.com/fschur/Evacuation-Bottleneck/tree/master
# we have changed 

'''
There are different adjustments you can make to the Simulation.

room:
There are different rooms to choose from:
    -"square": a standart square room with one exit
    -"long_room": a standart rectangle room with one exit
    -"long_room_v2": a rectangle room with two exits. Half of the agents will go to each exit
    -"edu_11", "edu_1", "edu_room": square rooms with one exit and different walls inside the room

You can choose the number of agents in the simulation with "num_individuals".

"num_steps" is the duraten the simulation will runn (recommended:1000)

"method" is the method of integration. You should use leap_frog even though it will often explode
since more relaible methods of integration like ode45 and monto carlo take a lot a computational power.
'''
# calls the simulation with 3 agents, 1000 timesteps, and the leap_frog methode
# for integration and the standart square room


# for nthsample in range(1, 101):        
#     for OBS_dis in range(12,23,2):
#         path = "C:\\Yash\\IITD\\sem 8\\crowd_data_final 2obs OBS_dis" + \
#                 "\\OBS_dis" + str(OBS_dis/10.0)
#         start_time = time.time()
#         print("OBS_dis=",OBS_dis/10.0, " sample=", nthsample)
#         sim = Simulation(num_individuals=40, total_time=18,collection_radius=2,
#                             tau=0.02, method="leap_frog", room_size=11, room="square", num_obs=2,obs_rad=1.5,obs_gap=2,obs_dis=float(OBS_dis/10.0))
#         sim.fill_room()                 # fills the spawn zone with random people
#         sim.run()                       # runs the simulation
#         path_obj = Path(path)
#         if not path_obj.exists():
#             try:
#                 path_obj.mkdir(parents=True, exist_ok=True)
#                 print(f"Directories '{path}' created successfully")
#             except Exception as e:
#                 print(f"Error creating directories '{path}': {e}")
#         else:
#             print(f"Directories '{path}' already exist")
#         path_To_Save = path + "\\"+str(nthsample)+"thsample"
#         # displays the solutions to the simulations in pygame with
#         tmp=sim.show(path=path_To_Save, path_doc=path,
#                     wait_time=30, sim_size=800, simul=sim)
#         end_time = time.time()
#         total_time = end_time - start_time
#         print(f"Elapsed time: {total_time:.6f} seconds")


# for nthsample in range(1, 45):        
#     for OBS_dis in range(-3,2,2):
#         path = "C:\\Yash\\IITD\\sem 8\\crowd_data_final 2obs OBS_dis" + \
#                 "\\OBS_dis" + str(OBS_dis/10.0)
#         start_time = time.time()
#         print("OBS_dis=",OBS_dis/10.0, " sample=", nthsample)
#         sim = Simulation(num_individuals=40, total_time=18,collection_radius=2,
#                             tau=0.02, method="leap_frog", room_size=11, room="square", num_obs=2,obs_rad=1.5,obs_gap=2,obs_dis=float(OBS_dis/10.0))
#         sim.fill_room()                 # fills the spawn zone with random people
#         sim.run()                       # runs the simulation
#         path_obj = Path(path)
#         if not path_obj.exists():
#             try:
#                 path_obj.mkdir(parents=True, exist_ok=True)
#                 print(f"Directories '{path}' created successfully")
#             except Exception as e:
#                 print(f"Error creating directories '{path}': {e}")
#         else:
#             print(f"Directories '{path}' already exist")
#         path_To_Save = path + "\\"+str(nthsample)+"thsample"
#         # displays the solutions to the simulations in pygame with
#         tmp=sim.show(path=path_To_Save, path_doc=path,
#                     wait_time=30, sim_size=800, simul=sim)
#         end_time = time.time()
#         total_time = end_time - start_time
#         print(f"Elapsed time: {total_time:.6f} seconds")
        


# for nthsample in range(1, 101):
#     for OBS_Gap in range(5,8):
#         path = "C:\\Yash\\IITD\\sem 8\\crowd_data_final 2obs OBS_Gap" + \
#                 "\\OBS_Gap" + str(float(OBS_Gap/10.0))
#         start_time = time.time()
#         print("OBS_Gap=",OBS_Gap/10.0, " sample=", nthsample)
#         sim = Simulation(num_individuals=40, total_time=18,collection_radius=2,
#                         tau=0.02, method="leap_frog", room_size=11, room="square", num_obs=2,obs_rad=1.5,obs_gap=float(OBS_Gap/10.0),obs_dis=1.2)
#         sim.fill_room()                 # fills the spawn zone with random people
#         sim.run()                       # runs the simulation
#         path_obj = Path(path)
#         if not path_obj.exists():
#             try:
#                 path_obj.mkdir(parents=True, exist_ok=True)
#                 print(f"Directories '{path}' created successfully")
#             except Exception as e:
#                 print(f"Error creating directories '{path}': {e}")
#         else:
#             print(f"Directories '{path}' already exist")
#         path_To_Save = path + "\\"+str(nthsample)+"thsample"
#         # displays the solutions to the simulations in pygame with
#         tmp=sim.show(path=path_To_Save, path_doc=path,
#                 wait_time=30, sim_size=800, simul=sim)
#         end_time = time.time()
#         total_time = end_time - start_time
#         print(f"Elapsed time: {total_time:.6f} seconds")

# for nthsample in range(1, 63):
#     for OBS_Rad in range(15,27, 1):
#         path = "C:\\Yash\\IITD\\sem 8\\crowd_data_final 2obs OBS_Rad" + \
#                 "\\OBS_Rad" + str(float(OBS_Rad/10.0))
#         start_time = time.time()
#         print("OBS_Rad=",OBS_Rad/10.0, " sample=", nthsample)
#         sim = Simulation(num_individuals=40, total_time=18,collection_radius=2,
#                         tau=0.02, method="leap_frog", room_size=11, room="square", num_obs=2,obs_rad=float(OBS_Rad/10.0),obs_gap=2,obs_dis=1.2)
#         sim.fill_room()                 # fills the spawn zone with random people
#         sim.run()                       # runs the simulation
#         path_obj = Path(path)
#         if not path_obj.exists():
#             try:
#                 path_obj.mkdir(parents=True, exist_ok=True)
#                 print(f"Directories '{path}' created successfully")
#             except Exception as e:
#                 print(f"Error creating directories '{path}': {e}")
#         else:
#             print(f"Directories '{path}' already exist")
#         path_To_Save = path + "\\"+str(nthsample)+"thsample"
#         # displays the solutions to the simulations in pygame with
#         tmp=sim.show(path=path_To_Save, path_doc=path,
#                 wait_time=30, sim_size=800, simul=sim)
#         end_time = time.time()
#         total_time = end_time - start_time
#         print(f"Elapsed time: {total_time:.6f} seconds")


start_time = time.time()

sim = Simulation(num_individuals=40, total_time=24,
                 tau=0.02, method="leap_frog", room_size=11, room="square",num_obs=2,obs_rad=1.2,obs_gap=2.2,obs_dis=0.5)
sim.fill_room()                 # fills the spawn zone with random people
sim.run()                       # runs the simulation
path="C:\Yash\IITD\sem 8\crowd_data\exp"
end_time = time.time()

total_time = end_time - start_time
print(f"Elapsed time: {total_time:.6f} seconds")
sim.show(path=path,path_doc=path, wait_time=30, sim_size=800, simul=sim)
