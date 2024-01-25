from heuristic import (
    ChebyshevDistance,
    DiagonalDistance,
    EuclideanDistance,
    HeuristicRelaxPath,
    ManhattanDistance,
)


HEURISTIC_CLASSES = {
    "h1": DiagonalDistance,
    "h2": ChebyshevDistance,
    "h3": ManhattanDistance,
    "h4": EuclideanDistance,
    "h5": HeuristicRelaxPath,
}


class InputHandler:
    def __init__(self):
        self.config = self.get_configuration()
        self.use_variant = self.get_search_algorithm()
        self.heuristic_type = self.get_heuristic_type(self.use_variant)

    def title(self):
        print(
            """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ~                                       ~
        ~       ____  ________ __  _________    ~
        ~      / __ \/ ____/ // / / ____/   |   ~
        ~     / /_/ / /_  / // /_/ __/ / /| |   ~
        ~    / ____/ __/ /__  __/ /___/ ___ |   ~
        ~   /_/   /_/      /_/ /_____/_/  |_|   ~
        ~                                       ~
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        )

    def get_input(
        self,
        prompt,
        conversion_func=int,
        validation_func=lambda x: True,
        error_message="Input non valido. Riprova.",
    ):
        while True:
            try:
                value = conversion_func(input(prompt))
                if validation_func(value):
                    return value
                else:
                    print(error_message)
            except ValueError:
                print(error_message)

    def get_configuration(self):
        self.title()
        config = dict()
        config["rows"] = self.get_input(
            "Inserisci il numero di righe della griglia: ",
            int,
            lambda x: x > 0,
            "Deve essere un numero positivo.",
        )
        config["cols"] = self.get_input(
            "Inserisci il numero di colonne della griglia: ",
            int,
            lambda x: x > 0,
            "Deve essere un numero positivo.",
        )
        config["traversability_ratio"] = (
            self.get_input(
                "Inserisci la percentuale di celle attraversabili (0/%-100/%): ",
                float,
                lambda x: 0 <= x <= 100,
                "Deve essere un numero tra 0 e 100.",
            )
            / 100
        )
        config["obstacle_agglomeration_ratio"] = self.get_input(
            "Inserisci il fattore di agglomerazione degli ostacoli (numero nell'intervallo [0,1]) : ",
            float,
            lambda x: 0 <= x <= 1,
            "Deve essere un numero tra 0 e 1.",
        )
        config["num_agents"] = self.get_input(
            "Inserisci il numero di agenti: ",
            int,
            lambda x: x >= 0,
            "Deve essere un numero positivo.",
        )
        config["maximum_time"] = self.get_input(
            "Inserisci il tempo massimo: ",
            int,
            lambda x: x > 0,
            "Deve essere un numero positivo.",
        )
        return config

    def get_search_algorithm(self):
        search_algorithms = ["Reach Goal", "Reach Goal variante"]
        numbered_options = [
            f"{i+1}. {option}" for i, option in enumerate(search_algorithms)
        ]
        print("\n".join(numbered_options))
        choice = self.get_input(
            "Scegli un algoritmo di ricerca: ",
            int,
            lambda x: 1 <= x <= len(numbered_options),
        )
        return choice == 2

    def get_heuristic_type(self, use_variant):
        heuristic_types = list(HEURISTIC_CLASSES)
        if use_variant:
            print("La variante di Reach Goal l'euristica del percorso rilassato")
            return heuristic_types[4]

        numbered_options = [
            f"{i+1}. {option}" for i, option in enumerate(heuristic_types[:4])
        ]
        print("\n".join(numbered_options))
        choice = self.get_input(
            "Scegli un'euristica: ", int, lambda x: 1 <= x <= len(numbered_options)
        )
        return heuristic_types[choice - 1]
