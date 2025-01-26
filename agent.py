from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent

from utils.Point import Point
from utils.ssl.Navigation import Navigation
from utils.ssl.PathFinding import PathFinding
from utils.ssl.DecisionMaking import DecisionMaking


class ExampleAgent(BaseAgent):

    curr_target: int = -1

    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)

    def decision(self):
        if len(self.targets) == 0:
            return

        self.curr_target = DecisionMaking.chooseTarget(
            curr_id=self.id,
            targets=self.targets,
            teammates=self.teammates
        )

        return



    def post_decision(self):
        # se nenhum target for selecionado, nao fazer nada
        if self.curr_target == -1:
            return

        # ir direto ao target caso nao hajam colisoes, ou outros problemas
        target_velocity, target_angle_velocity = Navigation.goToPoint(
            self.robot,
            self.targets[self.curr_target]
        )

        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)


        # procurar interseções
        intersecoes: list[Point] = PathFinding.findIntersections(
            pos = self.pos,
            target=self.targets[self.curr_target],
            opponents = self.opponents
        )


        # se nao existir nenhuma interseção, ignorar
        if len(intersecoes) == 0:
            return


        # mandar o robo desviar do obstáculo
        target_velocity, target_angle_velocity = PathFinding.avoidObstacle(
            robot=self.robot,
            target=self.targets[self.curr_target],
            intersections=intersecoes,
            opponents=self.opponents
        )

        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)


        return
