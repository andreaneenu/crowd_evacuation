import numpy as np
import pygame
import matplotlib.pyplot as plt
from pygame_screen_record import ScreenRecorder

# example positions for test purposes
movement_data = np.random.randint(20, 700, (2, 5, 5))
objects_pos = np.random.randint(100, 700, (2, 10))


def display_events(movement_data, room, wait_time, radii, sim_size, dead, status, path,simul):
    """This function takes as input:
    movement_data: matrix with shape (x, y, z). x=2 are the number coordinates, 
    y is the number of individuals and z is the number of timesteps.
    room: instanz of the class room. We need it to draw the walls.
    radii: The radii of the individuals.
    sim_size: The size of the image on the screen later
    The function draws a map for each timestep of the room with each individuals in it.
    The code is built in the library 'pygame'"""

    # colors
    background_color = (170, 170, 170)  # grey
    destination_color = (0, 128, 0)               # green
    object_color = (0, 0, 0)  # black
    blue = (0, 0, 250)
    black = (0, 0, 0)
    orange=(255,110,0)
    lavender=(230,230,250)
    red=(250, 0, 0)

    # variable for initializing pygame
    # the ratio (size of image) / (size of actual room)
    normalizer = int(sim_size/room.get_room_size())
    map_size = (room.get_room_size()*normalizer + 100,  # size of the map
                room.get_room_size()*normalizer + 100)  # plus a little free space
    wait_time = wait_time  # time that the simultation waits between each timestep
    wait_time_after_sim = 1  # waittime after simulation
    movement_data_dim = movement_data.shape
    # number of indiciduals in the simulation
    num_persons = movement_data_dim[1]
    num_time_iterations = movement_data_dim[2]  # number of timesteps
    num_walls = room.get_num_walls()  # number of walls

    pygame.init()  # initialize the intanz
    simulate = False  # variable to indicate if the simulation is running
    # create a new object of type Font(filename, size)
    font = pygame.font.Font(None, 32)
    worldmap = pygame.display.set_mode(map_size)

    recorder = ScreenRecorder(9)  # pass your desired fps
    recorder.start_rec()  # start recording

    while True:
        # # start simulation if any key is pressed and quits pygame if told so
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         simulate = True
        #     elif event.type == pygame.QUIT:
        #         pygame.quit()
        simulate = True
        worldmap.fill(0)
        # This creates a new surface with text already drawn onto it
        text = font.render(
            'Press any key to start the simulation', True, (255, 255, 255))
        # printing the text starting with a 'distance' of (100,100) from top left
        worldmap.blit(text, (100, 100))
        pygame.display.update()

        if simulate == True:
            # print the map for each timestep
            for t in range(num_time_iterations):
                # quit the simulation if told so
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                # initialize the map with background color
                worldmap.fill(background_color)

                # draw each peron for timestep t
                for person in range(num_persons):
                    if (status[person, t]) == 1:
                        pygame.draw.circle(worldmap, red,
                                           ((normalizer*movement_data[0, person, t] + 50).astype(int),
                                            (normalizer*movement_data[1, person, t] + 50).astype(int)),
                                           int(normalizer * radii[person]), 0)
                    elif (status[person, t]) == 2:
                        pygame.draw.circle(worldmap, blue,
                                           ((normalizer*movement_data[0, person, t] + 50).astype(int),
                                            (normalizer*movement_data[1, person, t] + 50).astype(int)),
                                           int(normalizer * radii[person]), 0)
                    elif (status[person, t]) == 3:
                        pygame.draw.circle(worldmap, orange,
                                           ((normalizer*movement_data[0, person, t] + 50).astype(int),
                                            (normalizer*movement_data[1, person, t] + 50).astype(int)),
                                           int(normalizer * radii[person]), 0)
                    elif (status[person, t]) == 4:
                        pygame.draw.circle(worldmap, lavender,
                                           ((normalizer*movement_data[0, person, t] + 50).astype(int),
                                            (normalizer*movement_data[1, person, t] + 50).astype(int)),
                                           int(normalizer * radii[person]), 0)
                    else:
                        pygame.draw.circle(worldmap, black,
                                           ((normalizer*movement_data[0, person, t] + 50).astype(int),
                                            (normalizer*movement_data[1, person, t] + 50).astype(int)),
                                           int(normalizer * radii[person]), 0)

                # draw each object for timestep t
                for wall in range(num_walls):
                    pygame.draw.lines(worldmap, object_color, True,
                                      normalizer*room.get_wall(wall) + 50, 2)
                    
                
                # draw the obstacle 
                for obs in simul.circular_Obstacles:
                    pygame.draw.circle(worldmap, object_color,
                                       ((normalizer * obs.center[0] + 50).astype(int),
                                        (normalizer * obs.center[1] + 50).astype(int)),
                                       obs.radius*normalizer, 2)
                
                    
                # draw the destination of the agents in green
                for des in room.get_destination():
                    pygame.draw.circle(worldmap, destination_color,
                                       ((normalizer * des[0] + 50).astype(int),
                                        (normalizer * des[1] + 50).astype(int)),
                                       simul.collection_radius*normalizer, 2)
                # prints additional information on the screen
                strf = "Number of People dead: " + \
                    str(int(dead[t]))
                text = font.render(strf, True, (255, 255, 255))
                # printing the text starting with a 'distance' of (10,10) from top left
                worldmap.blit(text, (10, 10))

                strd = "Number of People: " + str(num_persons)
                textd = font.render(strd, True, (255, 255, 255))
                # printing the text starting with a 'distance' of (400,10) from top left
                worldmap.blit(textd, (400, 10))

                # update the map
                pygame.display.update()
                # wait for a while before drawing new positions
                pygame.time.wait(wait_time)
            simulate = False
            text = font.render('SIMULATION FINISHED', True, (255, 255, 255))
            worldmap.blit(text, (100, 100))
            pygame.display.update()
            pygame.time.wait(wait_time_after_sim)

            # Uncomment to exit function instead of going back to the loop
            recorder.stop_rec()  # stop recording
            # saves the last recording
            recorder.save_recording(path+"recording.mp4")
            pygame.quit()
            return

# run a test with random inputs
# display_events(movement_data, objects_pos)


def display_graph(agents_escaped, acceleration, mass, status, path_graph,path_doc):
    '''Drawn 3 graphs related to the simullation. The first one is
    the number of people who escaped the room at each timestep.
    The secound one is the number of people which experience a force higher than "tol" 
    and therfore died.
    The third one shows the forces one random agents experienceses.
    '''

    tol = 6000       # force at which the people die (in Newton)

    _, num_persons, num_steps = np.shape(acceleration)
    forces_new = np.zeros((num_persons, num_steps - 1))
    num_dead = np.zeros(num_steps - 1)
    status_dead = np.zeros(num_persons)
    totaldead = 0

    # get force by multiplying the acceleration with the mass

    for t in range(num_steps - 1):
        for person in range(num_persons):
            if status_dead[person] == 1:
                continue
            if status[person, t] == 0:
                totaldead += 1
                status_dead[person] = 1
        num_dead[t] = totaldead
    print("total dead=", totaldead)
    with open(path_doc+"death.txt", 'a') as file:
        file.write(str(totaldead) + '\n')
    f = plt.figure(figsize=(10, 10))
    f.subplots_adjust(hspace=0.3)

    f1 = f.add_subplot(2, 1, 1)
    f1.plot(range(len(agents_escaped)), agents_escaped, 'g')
    f1.set_ylabel("num escaped")
    f1.set_xlabel("timestep")
    f1.set_title("Food collection")

    f2 = f.add_subplot(2, 1, 2)
    f2.plot(range(num_steps - 1), num_dead, 'r')
    f2.set_ylabel("num dead")
    f2.set_xlabel("timestep")

    # f3 = f.add_subplot(3, 1, 3)
    # chosen_agent = int(num_persons/2)
    # f3.plot(range(num_steps - 1), forces_new[chosen_agent, :], 'b')
    # f3.set_ylabel("forces on agent")
    # f3.set_xlabel("timestep")
    save_path = path_graph+" graph"
    if save_path is not None:
        plt.savefig(save_path)
    plt.close(f)
    return totaldead
