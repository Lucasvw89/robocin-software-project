class Permutations:

    Calculated = False
    preComputedPermutations = {
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {}
    }


    @staticmethod
    def getAllPermutations(num_teammates, num_targets) -> tuple[tuple[int]]:
        if not Permutations.Calculated:
            Permutations.Calculated = True
            for i in range(1, 7):
                for j in range(1, i+1):
                    Permutations.preComputedPermutations[i][j] = Permutations.preComputeAllPermutations(list(range(0, i)), j)
        # print(Permutations.preComputedPermutations)
        return Permutations.preComputedPermutations[num_teammates][num_targets]


    @staticmethod
    def preComputeAllPermutations(arr: list[int], num: int) -> list[tuple[int]]:
        allPermutations: set[tuple[int]] = set()

        def heapsAlgorithm(k, array):
            if k == 1:
                curr_result = tuple(array[:num].copy())
                allPermutations.add(curr_result)
                return

            heapsAlgorithm(k-1, array)

            for i in range(k-1):
                if k % 2 == 0:
                    array[i], array[k-1] = array[k-1], array[i]
                else:
                    array[0], array[k-1] = array[k-1], array[0]

                heapsAlgorithm(k-1, array)


        heapsAlgorithm(len(arr), arr)

        return tuple(allPermutations)