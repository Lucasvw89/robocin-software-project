from rsoccer_gym.Entities import Robot
from utils.ssl.Navigation import Navigation
from utils.Point import Point


# pathfinding completo: fazer grafo, percorrer grafo
# adicionar dijkistra, talvez A* mais pra frente
# ideia:
# 1 tracar uma linha entre robo e objetivo. 
# 2 se houver interseções com oponentes:
# 3     pegar a primeira interseção e criar dois pontos, um pra cada lado do obstaculo em relação ao robo atual:
# 4     a partir de cada um desses pontos, tracar uma linha até o objetivo,
# 5     se houver interseções nessa nova linha: reptir desde a linha 2
# 6 conectar os pontos na ordem que foram criados
# 7 deletar or pontos impossiveis de alcancar e as conexoes impossiveis de percorrer
# 8 adicionar peso as arestas de acordo com a distancia, mas talvez de acordo com o angulo tb, pq isso pode afetar a velocidade
# 9 rodar dijkstra ou A*
# sempre priorizar os pontos mais a frente pois os obstaculos podem ser móveis
# mandar o robo seguir sem freiar e sem controlar a velocidade até chegar perto do objetivo


# implementação atual incompleta
class PathFinding:

    @staticmethod   # calcular se existem interseções
    def findIntersections(
            pos: Point,
            target: Point,
            opponents: dict,
            r: float=0.18   # distancia entre dois robos ja que cada robo tem um raio de 0.09
        ) -> list[Point]:   # retorna todas as interseções

        # essa lista vai conter todos os obstaculos que estão entre o robo e o objetivo
        intersections: list[Point] = []

        # vetor do segmento de reta entre robo e target
        v = target - pos

        # um obstaculo importante é um obstaculo que está a frente do robo e mais proximo que o objetivo
        # podemos determinar se um obstaculo é importante utilizando produto interno e vetor distancia

        # queremos a interseção dessa reta com todos os obstaculos importantes na forma:
        # a * (t ** 2) + b * t + c = 0

        # e calcular se delta = b**2 - 4*a*c < 0 para todos os oponentes

        for curr_id, opponent in opponents.items():
            pos_opponent = Point(opponent.x, opponent.y)

            # usaremos esse vetor para determinar se o obstaculo é importantre ou nao
            vetor_para_o_oponente = pos_opponent - pos

            # se o obstaculo estiver atrás do robo ou estiver mais distante que o objetivo, ele nao é importante
            if vetor_para_o_oponente.length() > v.length() or vetor_para_o_oponente.dot(v) <= 0:
                continue

            # equação de interceção entre reta e circulo
            a = (v.x ** 2) + (v.y ** 2)
            b = 2 * ((pos.x - pos_opponent.x) * v.x + (pos.y - pos_opponent.y) * v.y)
            c = ((pos.x - pos_opponent.x) ** 2 + (pos.y - pos_opponent.y) ** 2) - (r**2)

            delta = (b ** 2) - 4 * a * c

            if delta >= 0:
                intersections.append(curr_id)

        return intersections



    # primeira versao do pathfinding
    # no maximo um nó intermediário, escolher o mais próximo
    def avoidObstacle(
            robot: Robot,
            target: Point,
            intersections: list[Point],
            opponents: dict
    ) -> tuple[Point, float]:
        pos = Point(robot.x, robot.y)

        # iniciar variaveis
        dist_closest_intersect = 1e9
        pos_closest_intersect = Point(0,0)

        # loop para achar interseção mais proxima
        for curr_id in intersections:
            intersection = opponents[curr_id]
            pos_intersection = Point(intersection.x, intersection.y)
            if pos.dist_to(pos_intersection) < dist_closest_intersect:
                pos_closest_intersect = pos_intersection
                dist_closest_intersect = pos.dist_to(pos_closest_intersect)

        # calcular off set do obstaculo para criar um novo ponto:
        # calcular o vetor direcionado ao objetivo:
        vector_to_target = target - pos
        # escolher um vetor perpendicular a ele e normalizar para facilitar calculos posteriores
        perpendicular_vector = Point(vector_to_target.y, -vector_to_target.x).normalize()

        # vetor direcionado a interseção com obstaculo mais proximo
        vector_to_intersect = (pos - pos_closest_intersect).normalize()

        # projetar o vector_to_intersect no vetor perpendicular
        offset = perpendicular_vector * vector_to_intersect.dot(perpendicular_vector)

        # ecalar o resultado para a distancia mais proxima possivel do obstaculo, mas mitigando a probabilidade de colisao
        offset = offset.normalize() * (0.25)

        # mandar o robo para o novo ponto
        target_velocity, target_angle_velocity = Navigation.goToPoint(
            robot,
            pos_closest_intersect + offset,     # o ponto é a posicao do obstaculo mais o offset calculado
            # controlar a velocidade se o novo ponto intermediario e o objetivo estiverem muito proximos
            control_speed=(
                (pos_closest_intersect + offset).dist_to(target) <= 0.25     # retorna verdadeiro se proximo
            )
        )

        return target_velocity, target_angle_velocity




    # implementação antiga, ainda vai ser revisada:

    # # ajuste cauteloso
    # # quando um obstaculo está proximo o suficiente do robo, o robo tenta se afastar um pouco
    # # limitado aos obstaculos importantes que estao muito proximos

    # influencias: list[Point] = []
    # for curr_id, opponent in self.opponents.items():
    #     pos_opponent = Point(opponent.x, opponent.y)
    #     influencia_atual = self.pos - pos_opponent

    #     # somente obstaculos importantes
    #     if influencia_atual.length() <= 0.20 and (pos_opponent - self.pos).dot(self.targets[self.curr_target] - self.pos) >= 0:
    #         influencias.append((influencia_atual / influencia_atual.length() ** 10) / 10)


    # adjust = Point(0, 0)
    # for i in influencias:
    #     adjust += i
    # if adjust == Point(0,0):
    #     return

    # adjust = Navigation.global_to_local_velocity(adjust.x, adjust.y, Navigation.degrees_to_radians(Geometry.normalize_angle(self.robot.theta, 0, 180)))
    # adjust = adjust.normalize() / 2

    # self.set_vel(self.next_vel + adjust)