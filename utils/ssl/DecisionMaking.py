from utils.Point import Point
from utils.Permutations import Permutations


# a ideia final é adicionar um algoritmo de min max que escolhe os alvos de forma a minimizar a maior distancia entre um robo e seu target
def list_lt(    # list less than
        list1: list[float],
        list2: list[float]
    ) -> bool:

    list1.sort(reverse=True)
    list2.sort(reverse=True)
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            continue
        elif list1[i] < list2[i]:
            return True
        else: return False



class DecisionMaking:

    decided = False
    finalDecision = []
    num_targets = -1

    @staticmethod
    def chooseTarget(curr_id: int, targets: list[Point], teammates: dict):
        chosen_target = -1  # sem target ainda
        if len(targets) != DecisionMaking.num_targets:
            DecisionMaking.decided = False

        if not DecisionMaking.decided:
            # indices de atribuição de robo para target
            # exemplo de funcionamento [1, 3, 2, 0, 5, 4] -> o robo com id 1 vai para o tagret 0, o robo com id 3, vai para o target 1 e assim por diante...
            all_attributions = Permutations.getAllPermutations(len(teammates.keys()), len(targets))

            fastest_attribution = -1
            min_list_dist = [1e9] * len(targets)
            for idx, attribution in enumerate(all_attributions):
                distances = [
                    targets[target_id].dist_to(Point(teammates[robot_id].x, teammates[robot_id].y))
                    for target_id, robot_id in enumerate(attribution)
                ]
                if list_lt(distances, min_list_dist):
                    fastest_attribution = idx
                    min_list_dist = distances

            DecisionMaking.decided = True
            DecisionMaking.finalDecision = all_attributions[fastest_attribution]
            DecisionMaking.num_targets = len(targets)


        for target_id, robot_id in enumerate(DecisionMaking.finalDecision):
            if robot_id == curr_id:
                chosen_target = target_id

        return chosen_target