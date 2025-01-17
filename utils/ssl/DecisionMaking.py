from utils.Point import Point

# a ideia final é adicionar um algoritmo de min max que escolhe os alvos de forma a minimizar a maior distancia entre um robo e seu target

class DecisionMaking:
    @staticmethod
    def chooseTarget(curr_id: int, targets: list[Point], teammates: dict):
        # Implementação atual:
        # Cada target vai escolher um robo, o mais próximo.

        chosen_target = -1  # sem target ainda

        # cada robo nao pode ser escolhido por mais de um alvo, entao utilizamos esse set para registrar os robos escolhidos
        teammates_selected: set[int] = set()
        # iterar por cada target
        for target_id, target in enumerate(targets):
            targets_closest_teammate_id = -1
            targets_closest_teammate_dist = 1e9

            # cada target vai iterar por cada robo
            for teammate_id, teammate in teammates.items():
                if teammate_id in teammates_selected:
                    continue    # se ja foi selecionado, ignora

                # achar o mais proximo
                if targets_closest_teammate_id == -1 or target.dist_to(teammate) < targets_closest_teammate_dist:
                    targets_closest_teammate_id = teammate_id
                    targets_closest_teammate_dist = target.dist_to(teammate)

            # se o robo realizando a conta for escolhido por um target, ir para esse target
            if targets_closest_teammate_id == curr_id and curr_id not in teammates_selected:
                chosen_target = target_id
            teammates_selected.add(targets_closest_teammate_id)

        return chosen_target