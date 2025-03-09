import numpy as np
import sys

from diff_equation import Diff_Equ

import pygame
from steps_function_quit import display_events
from steps_function_quit import display_graph


from Room import Room

import Integrators
from Integrators import leap_frog

'''
class to put the hole thing together. Its main parts
are the Differential Equation, the rooms, and the method
of integration. The Integration can be done by calling
the run function. If the integration is done the results
are saved in self.y for later use for example to display
them with with the function "Show"'''

class circularwall:
    def __init__(self,center,radius):
        self.center=center
        self.radius=radius

class Simulation:
    def __init__(self, num_individuals, num_steps=500, method="leap_frog",delay=0.5, tau=0.05  ,total_time=30, v_des=1.5, room="square",
                 room_size=25,collection_radius=2,obs_rad=0.5,obs_dis=1 ,num_obs=1,obs_gap=1.8):
        self.collection_radius=collection_radius
        std_deviation = 0.07
        self.num_steps=int(total_time/tau)
        self.delay=delay
        # is late used to make the agents differ in weight and size
        variation = np.random.normal(
            loc=1, scale=std_deviation, size=(1, num_individuals))

        # Constants
        self.L = room_size  # size of square room (m)
        self.N = num_individuals  # quantity of pedestrians
        self.tau = tau  # time-step (s)
        # self.num_steps = num_steps  # number of steps for integration

        # Agent information
        # radii of pedestrians (m)
        self.radii = 0.3 * (np.ones(self.N)*variation).squeeze()
        self.v_des = v_des * np.ones(self.N)  # desired velocity (m/s)
        # mass of pedestrians (kg)
        self.m = 80 * (np.ones(self.N)*variation).squeeze()
        self.forces = None              # forces on the agents
        self.agents_escaped = None  # number of agents escaped by timesteps
        # Three dimensional array of velocity
        self.v = np.zeros((2, self.N, self.num_steps))
        self.y = np.zeros(
            (2, self.N, self.num_steps))  # Three dimensional array of place: x = coordinates, y = Agent, z=Time
        self.status = np.ones(
            (self.N, self.num_steps))  # Three dimensional array of place: x = statusif food is received, y = Agent, z=Time
        # other
        # kind of room the simulation runs in
        self.room = Room(room, room_size)
        # method used for integration
        self.method = getattr(Integrators, method)
        # initialize Differential equation
        self.diff_equ = Diff_Equ(
            self.N, self.L, self.tau, self.room, self.radii, self.m)
        self.obs_rad=obs_rad
        self.obs_dis=obs_dis
        circwalls=[]
        if num_obs==1:
            circwalls=[
            circularwall(np.array([collection_radius+self.obs_dis+obs_rad,room_size/2+0.1]),obs_rad)
        ]
        if num_obs==2:
            circwalls=[
                circularwall(np.array([collection_radius+self.obs_dis+obs_rad,room_size/2+obs_gap/2+obs_rad]),obs_rad),
                circularwall(np.array([collection_radius+self.obs_dis+obs_rad,room_size/2-obs_gap/2-obs_rad]),obs_rad)
            ]
        self.circular_Obstacles=np.array(circwalls)
        

    # function set_time, set_steps give the possiblity to late change these variable when needed
    def set_steps(self, steps):
        self.num_steps = steps

    # function to change the methode of integration if needed
    def set_methode(self, method):
        self.method = getattr(Integrators, method)

    def dont_touch(self, i, pos):  # yields false if people don't touch each other and true if they do
        for j in range(i - 1):
            if np.linalg.norm(pos - self.y[:, j, 0]) < self.radii[i]+self.radii[j]+0.32:
                return True
        for obs in self.circular_Obstacles:
            if np.linalg.norm(pos - obs.center) < self.radii[i]+obs.radius+0.32:
                return True
        return False

    # fills the spawn zone with agents with random positions
    def fill_room(self):
        spawn = self.room.get_spawn_zone()
        breath = spawn[0, 1] - spawn[0, 0]
        height = spawn[1, 1] - spawn[1, 0]
        max_len = max(breath, height)

        # checks if the area is too small for the agents to fit in
        area_people = 0
        # for i in range(self.N):
        #     area_people += 4 * self.radii[i] ** 2
        # if area_people >= 0.7 * max_len ** 2:
        #     sys.exit(
        #         'Too much people! Please change the size of the room/spawn-zone or the amount of people.')
        # checks if the agent touches another agent/wall and if so gives it a new random position in the spawn-zone
        # total = self.N
        # density = np.floor(((breath)*(height))/total)
        # cur = 0
        # cur_spawn = 0
        # for j in range(height):
        #     if (cur_spawn == total):
        #         break
        #     for i in range(breath):
        #         if (cur_spawn == total):
        #             break
        #         cur += 1
        #         if cur >= density:
        #             x = i+spawn[0, 0]
        #             y = j+spawn[1, 0]
        #             self.y[:, cur_spawn, 0] = [x, y]
        #             cur_spawn += 1
        #             cur = 0

        len_right = spawn[0, 1] - spawn[0, 0]
        len_left = spawn[1, 1] - spawn[1, 0]
        max_len = max(len_left, len_right)

        for i in range(self.N):
            # The pedestrians don't touch the wall
            x = len_right*np.random.rand() + spawn[0, 0]
            y = len_left * np.random.rand() + spawn[1, 0]
            pos = [x, y]

            # The pedestrians don't touch each other
            while self.dont_touch(i, pos):
                x = len_right * np.random.rand() + spawn[0, 0]
                y = len_left * np.random.rand() + spawn[1, 0]
                pos = [x, y]
            self.y[:, i, 0] = pos
        print("spawn done")
        self.v[:, :, 0] = self.v_des * \
            self.diff_equ.e_t(self.y[:, :, 0], self.status[:, 0])

    # calls the method of integration with the starting positions, diffequatial equation, number of steps, and delta t = tau
    def run(self):
        self.y, self.agents_escaped, self.forces, self.status,self.dead = self.method(
            self.y[:, :, 0], self.v[:, :, 0], self.diff_equ.f, self.diff_equ.e_0, self.num_steps, self.tau, self.room,sim_class=self)

    # Displayes the simulation in pygame
    def show(self,path,path_doc, wait_time, sim_size,simul):
        a=display_graph(self.agents_escaped, self.forces, self.m,self.status,path_graph=path,path_doc=path_doc)
        display_events(self.y, self.room, wait_time, self.radii,
                       sim_size, self.dead,self.status,path,simul=simul)
        return a
