class MinesweeperSolver:
    def __init__(self):
        self.board = dict()
        self.corrBombs = set()
        self.percentages = dict()

    
    def solve(self, board: dict):

        turnVisited = dict()
        ans = {
            "corr" : (None, None),
            "percentage" : float('inf'),
        }

        for corr in board:
            neighbors = [board[corr[1] + i][corr[0] + j] for i in range(-1, 2) for j in range(-1, 2) is (i, j) != (0, 0) and (i, j) in board]
            nonVisitedN = [n for n in neighbors if board[n] == None]

            if len(nonVisitedN) == 0:
                continue

            relativesMinesNb = board[corr] - sum([board[n] == -1 for n in neighbors])

            for neighbor in nonVisitedN:
                if neighbor in turnVisited:
                    turnVisited[neighbor]["nbSim"] += len(nonVisitedN)
                else:
                    turnVisited[neighbor] = {
                        "mines" : 0,
                        "nbSim": len(nonVisitedN),
                    }
            
            for n in range(len(nonVisitedN)):
                for i in range(relativesMinesNb):
                    turnVisited[nonVisitedN[(n+i)%len(nonVisitedN)]]["mines"] += 1
        
        for corr in turnVisited:
            percentage = turnVisited[corr]["mines"] / turnVisited[corr]["nbSim"]
            
            if percentage == 1:
                board[corr] = -1

            if percentage < ans["percentage"]:
                ans["corr"] = corr
                ans["percentage"] = percentage

            self.percentages[corr] = percentage

        self.board = board

        return ans["corr"]
    
    def get_bombs(self):
        for corr in self.board:
            if self.board[corr] == -1:
                self.corrBombs.add(corr)
        return self.corrBombs
    
    @staticmethod
    def listToJson(board):
        jsonBoard = dict()
        for y in range(len(board)):
            for x in range(len(board[y])):
                jsonBoard[(x, y)] = board[y][x]
        return jsonBoard