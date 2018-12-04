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

        infected_population = list()

        for infected_person in range(self.initial_infected):
            new_person = Person(_id=self.next_person_id, is_vaccinated= False, infection=virus)
            self.current_infected_list.append(new_person)
            self.total_infected += 1
            self.current_infected += 1
            self.population.append(new_person)
            self.next_person_id += 1

        vaccinated_population = list()
        vaccinated_population_number = round(self.pop_size * self.vacc_percentage, 0)

        for person in range(int(vaccinated_population_number)):
            new_person = Person(_id=self.next_person_id, is_vaccinated=True)
            vaccinated_population.append(new_person)
            self.population.append(new_person)
            self.next_person_id += 1

        remaining_population = self.pop_size - (len(infected_population) + len(vaccinated_population))
        for person in range(remaining_population):
            new_person = Person(_id=self.next_person_id, is_vaccinated=False)
            self.population.append(new_person)
            self.next_person_id +=1

        # for person in self.population:
        #     if person.infection != None:
        #         print("ID: {}   is_vaccinated: {}   virus: {}".format(person._id, person.is_vaccinated, person.infection.name))
        #     else:
        #         print("ID: {}   is_vaccinated: {}   virus: {}".format(person._id, person.is_vaccinated, person.infection))


    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # TODO: Complete this helper method.  Returns a Boolean.
        infected_population = sum([person for person in self.population if person.infection != None])
        vaccinated_population = sum([person for person in self.population if person.is_vaccinated == True])
        dead_population = sum([person for person in self.population if person.is_alive == True ])


        # for person in self.population:
        #     if person.infection != None:
        #         infected_population += 1
        #     elif person.is_vaccinated:
        #         vaccinated_population += 1
        #     elif person.is_alive == False:
        #         dead_population += 1
        if dead_population == self.pop_size:
            # print("Stop!")
            return False
        elif vaccinated_population == self.pop_size:
            # print("Stop!")
            return False
        elif infected_population == self.pop_size:
            # print("Stop!")
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
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        if should_continue == True:
            time_step_counter += 1
            # Logger.log_time_step()

        # while should_continue:
        # TODO: for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.
        # print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))
        else:
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



    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

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
            random_person.did_get_infected(person)
            if random_person.did_get_infected(person) == True:
                self.newly_infected.append(random_person)
                self.logger.log_interaction(person, random_person, True)
                print('Person Got Infected')
            else:
                self.logger.log_interaction(person, random_person, False)
                print('Person did not get infected!')

    # def _infect_newly_infected(self):
    #     ''' This method should iterate through the list of ._id stored in self.newly_infected
    #     and update each Person object with the disease. '''
    #     # TODO: Call this method at the end of every time step and infect each Person.
    #     # TODO: Once you have iterated through the entire list of self.newly_infected, remember
    #     # to reset self.newly_infected back to an empty list.
    #     pass
    #


if __name__ == "__main__":
    # params = sys.argv[1:]
    # virus_name = str(params[0])
    # repro_num = float(params[1])
    # mortality_rate = float(params[2])
    #
    # pop_size = int(params[3])
    # vacc_percentage = float(params[4])
    #
    # if len(params) == 6:
    #     initial_infected = int(params[5])
    #
    # virus = Virus(name, repro_rate, mortality_rate)
    # sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)
    #
    # sim.run()
    virus = Virus("HIV", 0.8, 0.3)
    simulation = Simulation(pop_size=10, vacc_percentage=0.5, initial_infected=1, virus=virus)
    # simulation._create_population()
    # simulation.time_step()
    sick_person = Person(11, False, virus)
    healthy_person = Person(12, False)
    # healthy_person.did_get_infected(sick_person)
    simulation.interaction(sick_person, healthy_person)

def test_simulation_should_continue():
    """Tests the simulation should continue method """
    virus = Virus("HIV", 0.8, 0.3)
    simulation = Simulation(pop_size=10, vacc_percentage=0.5, initial_infected=1, virus=virus)
    simulation_continues = simulation._simulation_should_continue()
    assert simulation_continues is True


def test_interaction():
    '''Tests the interaction function  '''
    virus = Virus("HIV", 0.8, 0.3)
    simulation = Simulation(pop_size=10, vacc_percentage=0.5, initial_infected=1, virus=virus)
    sick_person = Person(11, False, virus)
    healthy_person = Person(12, False)
    simulation.interaction(sick_person, healthy_person)
