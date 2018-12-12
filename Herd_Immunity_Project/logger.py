from person import Person
from virus import Virus

class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    # TODO: Write a test suite for this class to make sure each method is working
    # as expected.

    # PROTIP: Write your tests before you solve each function, that way you can
    # test them one by one as you write your class.

    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name,
                        mortality_rate, basic_repro_num):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!

        data_log_text = "Data for the current {0} outbreak!\nPopulation Size: {1}\nVaccination Percentage: {2}\nVirus: {0}\nVirus' Mortality Rate: {3}\nBasic Reproduction Number: {4}".format(
        virus_name, pop_size, vacc_percentage, mortality_rate, basic_repro_num)
        data_log = open(self.file_name + ".txt", "w+")
        data_log.write(data_log_text + "\n\n")
        data_log.close
        

    def log_interaction(self, person, random_person, did_infect):

        # , random_person_sick=None,
        #                     random_person_vacc=None, did_infect=None
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        if did_infect == True:
            infected = "{} infected {}.".format(
            person._id, random_person._id
            )
        elif random_person.infection != None:
            infected = "{} didn't infect {} because {} is already sick.".format(
            person._id, random_person._id)
            
        elif random_person.is_vaccinated == True:
            infected = "{} didn't infect {} because is vaccinated".format(
            person._id, random_person._id)
            

        edit_log = open(self.file_name + ".txt", "a")
        edit_log.write(infected + "\n")
        edit_log.close()


    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        if did_die_from_infection == True:
            life_status = "{} died from infection.".format(person._id)
        elif did_die_from_infection == False:
            life_status = "{} survived the infection.".format(person._id)

        edit_log = open(self.file_name + ".txt", "a")
        edit_log.write(life_status + "\n")
        edit_log.close()

    def log_time_step(self, time_step_number, total_dead, newly_infected, total_infected):
        ''' STRETCH CHALLENGE DETAILS:

        If you choose to extend this method, the format of the summary statistics logged
        are up to you.

        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.

        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        # TODO: Finish this method. This method should log when a time step ends, and a
        # new one begins.
        # NOTE: Here is an opportunity for a stretch challenge!
        log = "End of Time Step #{}. There were {} people infected. Now there is {} total people infected. The total number of deaths has rose to {}".format(time_step_number, newly_infected, total_infected, total_dead)
        with open(self.file_name, 'a') as out:
            out.write(log)

def test_write_metadata():
    new_file = Logger("test_data_log")
    new_file.write_metadata(pop_size=1, vacc_percentage=0.3, virus_name="test", mortality_rate=0.3, basic_repro_num=100)
    assert new_file.file_name is "test_data_log"

def test_log_interaction():
    virus = Virus("HIV", 0.8, 0.3)
    infected_person = Person(_id=1, is_vaccinated=False, infection=virus)
    not_vaccinated_person = Person(_id=2, is_vaccinated= True)
    new_file = Logger("test_data_log")
    new_file.log_interaction(person=infected_person, random_person=not_vaccinated_person, did_infect=False)
    assert new_file.file_name is "test_data_log"

def test_log_infection_survivor():
    virus = Virus("HIV", 0.8, 0.3)
    infected_person = Person(_id=1, is_vaccinated=False, infection=virus)
    new_file = Logger("test_data_log")
    new_file.log_infection_survival(infected_person, did_die_from_infection=True)
    assert new_file.file_name is "test_data_log"
