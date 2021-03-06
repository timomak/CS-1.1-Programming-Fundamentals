import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, initial_infected, virus):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct parameters.

        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.

        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.

        self.population = [] # List of Person objects
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.current_infected_list = []
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus.name, len(self.population), self.vacc_percentage, self.initial_infected)
        self.logger = Logger(file_name=self.file_name)
        self.newly_infected = []
        self.should_continue_running = True

    def _create_population(self):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.

        for infected_person in range(self.initial_infected):
            new_person = Person(_id=self.next_person_id, is_vaccinated= False, infection=self.virus)
            self.current_infected_list.append(new_person)
            self.total_infected += 1
            self.current_infected += 1
            self.pop_size += 1
            self.population.append(new_person)
            self.next_person_id += 1

        # print("Infected population: {}".format(len(self.current_infected_list)))
        vaccinated_population = list()
        vaccinated_population_number = (round(self.pop_size * self.vacc_percentage, 0)) - 1

        # print("Vaccinated population: {}".format(vaccinated_population_number))

        for person in range(int(vaccinated_population_number)):
            new_person = Person(_id=self.next_person_id, is_vaccinated=True)
            vaccinated_population.append(new_person)
            self.population.append(new_person)
            self.next_person_id += 1

        remaining_population = self.pop_size - (len(self.current_infected_list) + len(vaccinated_population))

        # print("Rest of population: {}".format(remaining_population))

        for person in range(remaining_population):
            new_person = Person(_id=self.next_person_id, is_vaccinated=False)
            self.population.append(new_person)
            self.next_person_id +=1



    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # TODO: Complete this helper method.  Returns a Boolean.
        infected_population = self.current_infected_list
        # [person for person in self.population if person.infection != None]
        # print("Infected population: {} current, {} loop".format(len(self.current_infected_list), len(infected_population)))

        vaccinated_population = [person for person in self.population if person.is_vaccinated == True]
        # print("Vaccinated population: {}".format(len(vaccinated_population)))

        dead_population = [person for person in self.population if person.is_alive != True]
        # print("Dead population: {}".format(len(dead_population)))

        if len(dead_population) == self.pop_size:
            # print("Stop!")
            return False
        elif len(vaccinated_population) == self.pop_size:
            # print("Stop!")
            return False
        elif len(infected_population) == self.pop_size:
            # print("Stop!")
            return False
        elif len(vaccinated_population) + len(infected_population) == self.pop_size:
            return False
        elif len(self.population) == 0:
            return False
        else:
            # print("Continue!")
            return True


    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper

        print("Starting simulation in run()")
        self._create_population()
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        print("Should similation continue? Bot: {}".format(should_continue))
        while should_continue == True and self.should_continue_running == True:

            self.time_step()
            time_step_counter += 1
            print("Time step: {}".format(time_step_counter))

            self.logger.log_time_step(time_step_counter, self.total_dead, self.newly_infected, self.total_infected)
            should_continue = self._simulation_should_continue()
        # while should_continue:
        # TODO: for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.
        # print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))

        print('The simulation has ended after {} turns.'.format(time_step_counter))

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        # TODO: Finish this method.
        counter = 0
        infected_peoples = self.current_infected_list
        print("Number of infected people before time step: {}".format(len(infected_peoples)))
        # [p for p in self.population if p.infection != None]
        # healthy_peoples = [p for p in self.population if p.infection == None]

        for infected_person in infected_peoples:
            for _ in range(5):
                healthy_people = [ p for p in self.population if p.infection == None ]

                if len(self.population) == 0:
                    print("It should stop")
                    self.should_continue_running = False
                    return
                elif len(healthy_people) == 0:
                    print('It should stop because no healthy people')
                    self.should_continue_running = False
                    return

                counter +=1
                print("Population size: ",len(self.population))
                random_person = self.get_alive_random_person_from_population_that_is_not_the_person_that_is_interacting(infected_person)
                # if random_person.is_alive == True:
                self.interaction(infected_person, random_person)
                # else:
                #     print("random_person is not alive")
        self._infect_newly_infected()
        print("Number of infected people after time step: {}".format(len(self.current_infected_list)))

    def get_alive_random_person_from_population_that_is_not_the_person_that_is_interacting(self, interacting_infected_person):
        healthy_people = [p for  p in self.population if p.infection == None and p.is_alive == True]
        # if len(self.population) == 0:
        #     self._simulation_should_continue()
        #     # stop simulation
        # elif len(healthy_people) == 0:
        #     return self._simulation_should_continue()


        random_person = random.choice(healthy_people)
        print("Ran Id",random_person._id)
        # print("random person id",random_person._id)
        # print("Is random person alive? Bot: {}".format(random_person.is_alive))
        if random_person == interacting_infected_person or random_person.is_alive == False:
            print("Random person is dead, need to look for a new one!", random_person.is_alive)
            self.get_alive_random_person_from_population_that_is_not_the_person_that_is_interacting(interacting_infected_person)
        elif random_person.is_alive == True and random_person != interacting_infected_person:
            print("random person {} is alive: {}".format(random_person._id, random_person.is_alive))
            return random_person
        else:
            self.get_alive_random_person_from_population_that_is_not_the_person_that_is_interacting(interacting_infected_person)


    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        # assert person.is_alive == True
        # assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.
        if person.infection != None:
            # random_person.did_get_infected(person)
            if random_person.did_get_infected(person) == True:
                self.newly_infected.append(random_person)
                self.current_infected_list.append(random_person)
                self.total_infected += 1
                self.logger.log_interaction(person, random_person, True)
                print('Person Got Infected')
            else:
                self.logger.log_interaction(person, random_person, False)
                print('Person did not get infected!')
        else:
            print("Person {} did not infect because he is not sick".format(person._id))

    # No need because we do that in person.py
    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for i in self.newly_infected:
            self.total_infected += 1
            self.current_infected_list.append(i)
            if i.did_survive_infection() == False:
                self.total_dead += 1
                print('Dead Pop: {}'.format(self.total_dead))
                self.population.remove(i)
            else:
                i.is_vaccinated = True

        self.newly_infected = []





if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[2])
    repro_num = float(params[3])
    mortality_rate = float(params[4])

    pop_size = int(params[0])
    vacc_percentage = float(params[1])

    if len(params) == 6:
        initial_infected = int(params[5])

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    start_logger = sim.logger.write_metadata(pop_size, vacc_percentage, virus_name, mortality_rate, repro_num)
    sim.run()

def test_create_population():
    """Tests if the population is being properly created"""
    virus = Virus("HIV", 0.8, 0.3)
    simulation = Simulation(pop_size=10, vacc_percentage=0.5, initial_infected=1, virus=virus)
    simulation._create_population()
    assert simulation.pop_size == 11
    assert len(simulation.population) == 11
    assert simulation.current_infected == 1
    assert len(simulation.current_infected_list) == 1
    assert simulation.total_infected == 1
    assert simulation.total_dead == 0

def test_simulation_should_continue():
    """Tests the simulation should continue method """
    virus = Virus("HIV", 0.8, 0.3)
    simulation = Simulation(pop_size=10, vacc_percentage=0.5, initial_infected=1, virus=virus)
    simulation._create_population()
    simulation_continues = simulation._simulation_should_continue()
    assert simulation_continues is True
    assert len(simulation.current_infected_list) == 1
    assert simulation.total_dead == 0

def test_run():
    virus = Virus("HIV", 0.8, 1)
    simulation = Simulation(pop_size=10, vacc_percentage=0.5, initial_infected=1, virus=virus)
    simulation.run()
    assert simulation.total_dead == 100

# def test_time_step():
#     """ Tests whether the time step method works"""
#     virus = Virus("HIV", 0.8, 0.3)
#     simulation = Simulation(pop_size=10, vacc_percentage=0.5, initial_infected=1, virus=virus)
#     # simulation.run()
#     simulation._create_population()
#     simulation.time_step()
#     assert simulation.pop_size == 20

def test_get_alive_random_person():
    """ Tests whether the time step method works"""
    virus = Virus("HIV", 0.8, 0.3)
    simulation = Simulation(pop_size=10, vacc_percentage=0.5, initial_infected=1, virus=virus)
    simulation._create_population()
    sick_person = simulation.current_infected_list[0]
    random_person = simulation.get_alive_random_person_from_population_that_is_not_the_person_that_is_interacting(sick_person)
    assert simulation.pop_size == 11
    assert random_person.is_alive == True

def test_interaction_infection():
    '''Tests the interaction function  '''
    virus = Virus("HIV", 0.8, 0.3)
    simulation = Simulation(pop_size=10, vacc_percentage=0.5, initial_infected=1, virus=virus)
    simulation._create_population()
    sick_person = simulation.current_infected_list[0]
    healthy_person = Person(2, False)
    simulation.interaction(sick_person, healthy_person)
    assert simulation.total_infected == 2

def test_interaction_not_infectious():
    '''Tests the interaction function  '''
    virus = Virus("HIV", 0.8, 0.3)
    simulation = Simulation(pop_size=10, vacc_percentage=0.5, initial_infected=1, virus=virus)
    simulation._create_population()
    sick_person = simulation.current_infected_list[0]
    healthy_person = Person(2, True)
    simulation.interaction(sick_person, healthy_person)
    assert simulation.total_infected == 1
