#  modulo argparse in Python è utilizzato per scrivere interfacce utente a riga di comando user-friendly
import argparse
import os


# Definizione dei percorsi come costanti
OUTPUT_PATH = os.path.join("benchmarks", "report")
GENERATOR_PATH = os.path.join("benchmarks", "generators.")
PROBLEM_PATH = os.path.join("benchmarks", "problems.")

# 1. Creo un oggetto parser
__parser = argparse.ArgumentParser(
    prog="pf4ea", description="Pathfinding for an entry agent"
)

# 2. Aggiungo al parser principale un subparsers che conterrà tutti i subparser generati
__subparsers = __parser.add_subparsers(dest="command", help="sub-command help")

# 3. Aggiungo un subparser per il comando "run"
__parser_run = __subparsers.add_parser(
    "run", help="run help", formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
# 3.1. Aggiungo gli argomenti per il subparser "run"
__parser_run.add_argument(
    "-i",
    "--input",
    type=str,
    help="Input file.",
    default=PROBLEM_PATH,
)
__parser_run.add_argument(
    "-o",
    "--output",
    type=str,
    help="Output file.",
    default=OUTPUT_PATH,
)

__parser_run.add_argument(
    "-r",
    "--report",
    type=bool,
    help="Salva il report su file.",
    action=argparse.BooleanOptionalAction,
    default=False,
)

__parser_run.add_argument(
    "-v",
    "--variant",
    type=bool,
    help="Usa la variante di ReachGoal.",
    action=argparse.BooleanOptionalAction,
    default=False,
)

__parser_run.add_argument(
    "--show",
    type=bool,
    help="Mostra la soluzione graficamente.",
    action=argparse.BooleanOptionalAction,
    default=False,
)


# 4. Aggiungo un subparser per il comando "gen"
__parser_gen = __subparsers.add_parser(
    "gen", help="gen help", formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
# 4.1. Aggiungo gli argomenti per il subparser "gen"
__parser_gen.add_argument(
    "-f",
    "--file",
    type=str,
    help="Input file.",
    default=GENERATOR_PATH,
)

__parser_gen.add_argument(
    "--show",
    type=bool,
    action=argparse.BooleanOptionalAction,
    help="Mostra la soluzione graficamente.",
    default=False,
)
__parser_gen.add_argument(
    "-s",
    "--save",
    type=bool,
    help="Salva il problema generato su file.",
    action=argparse.BooleanOptionalAction,
    default=False,
)

__parser_gen.add_argument(
    "-m", 
    "--heuristic",
    type=str, 
    help="Heuristic type.",
    default = "h1"
)
__parser_gen.add_argument(
    "-v",
    "--variant",
    type=bool,
    help="Usa la variante di ReachGoal.",
    action=argparse.BooleanOptionalAction,
    default=False,
)

__parser_gen.add_argument(
    "-r",
    "--report",
    type=bool,
    help="Salva il report su file.",
    action=argparse.BooleanOptionalAction,
    default=False,
)

__parser_gen.add_argument(
    "--csv_output",
    type=bool,
    help="Salva i problemi generati e le relative soluzioni su un file di output in formato csv",
    action=argparse.BooleanOptionalAction,
    default=False,
)

# 3. Aggiungo un subparser per il comando "man"
__parser_man = __subparsers.add_parser(
    "man", help="man help", formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
__parser_man.add_argument(
    "--save",
    type=bool,
    help="Salva il problema generato su file.",
    action=argparse.BooleanOptionalAction,
    default=False,
)

__parser_man.add_argument(
    "--show",
    type=bool,
    help="Mostra la soluzione graficamente.",
    action=argparse.BooleanOptionalAction,
    default=False,
)

__parser_man.add_argument(
    "-r",
    "--report",
    type=bool,
    help="Salva il report su file.",
    action=argparse.BooleanOptionalAction,
    default=False,
)


def get_args() -> argparse.Namespace:
    """Ottiene gli argomenti dalla riga di comando.

    Restituisce:
        argparse.Namespace: gli argomenti analizzati dalla riga di comando.
    """
    args = __parser.parse_args()
    return args
