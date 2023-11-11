from dotenv import load_dotenv 
load_dotenv()

class Driver:   

    def __init__(self, lista_parametri):
       self.parameters = lista_parametri
       self.id_driver = 1
        
    def set_id_drivers(pop, MU, num_generations):
        for i,off in enumerate(pop):
            off.id_driver = num_generations * MU + i + 1 

    def reset_driver(self):
        self.parameters = None



