from Tree import *
import copy


class Ai:
    gameBoard = []
    BLACK = "black"
    WHITE = "white"
    BLANK = "*"

    VERTICAL = 0
    HORIZONTAL = 1
    RIGHTDOWN = 2
    RIGHTUP = 3

    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        print("AI is now constructed")

    def __str__(self):
        return "AI"

    def update(self, gameBoard):
        self.gameBoard = gameBoard

    def constructSearchTree(self, x, y, num, gamePaths):  # return tree
        if num > 0:
            root = Tree()
            for k in range(19):
                for l in range(19):
                    if self.gameBoard[l][k] != self.BLANK:
                        for i in range(3):
                            for j in range(3):
                                _x = i + k - 1
                                _y = j + l - 1
                                if 19 > _x >= 0 and 19 > _y >= 0 and self.gameBoard[_y][_x] == self.BLANK:
                                    _gamePaths = copy.deepcopy(gamePaths)
                                    _path = [_x, _y]
                                    _gamePaths.append(_path)
                                    node = self.constructSearchTree(_x, _y, num - 1, _gamePaths)
                                    node.parent = root
                                    root.children.append(node)
            return root
        else:
            node = Tree()
            node.position.append(gamePaths[0][0])
            node.position.append(gamePaths[0][1])
            _gameBoard = copy.deepcopy(self.gameBoard)

            if len(gamePaths) > 1:
                _gameBoard[gamePaths[0][1]][gamePaths[0][0]] = self.WHITE
                _gameBoard[gamePaths[1][1]][gamePaths[1][0]] = self.BLACK

            if self.checkOneLine_num(x, y, 4, self.WHITE, _gameBoard):
                node.data = 10
            elif not self.checkOneLine_num(x, y, 3, self.BLACK, _gameBoard):
                if self.checkOneLine_num(x, y, 3, self.WHITE, _gameBoard):
                    node.data = 3
                elif self.checkOneLine_num(x, y, 2, self.WHITE, _gameBoard):
                    node.data = 2
                elif self.checkOneLine_num(x, y, 1, self.WHITE, _gameBoard):
                    node.data = 1
                else:
                    node.data = 0
            elif self.checkOneLine_num(x, y, 3, self.BLACK, _gameBoard):
                node.data = -1
            elif self.checkOneLine_num(x, y, 4, self.BLACK, _gameBoard):
                node.data = -10

            return node

    def calculate_data(self, gameBoard):
        pass

    def calculateTree(self, x, y):
        tree = self.constructSearchTree(x, y, 2, [])
        (alphabetaValue, alphabetaPosition) = self.alphabeta(tree, 2, -9999, 9999, True, [0, 0])
        print(alphabetaPosition)
        return alphabetaPosition

    def alphabeta(self, node, depth, alpha, beta, maximizingPlayer, position):
        if depth == 0 or node.children is None:
            return node.data, node.position
        if maximizingPlayer:
            v = -9999
            for child in node.children:
                (alphabetaValue, alphabetaPosition) = self.alphabeta(child, depth - 1, alpha, beta, False, position)
                if alphabetaValue is not None:
                    v = max(v, alphabetaValue)
                if v == alphabetaValue:
                    position = alphabetaPosition
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return v, position
        else:
            v = 9999
            for child in node.children:
                (alphabetaValue, alphabetaPosition) = self.alphabeta(child, depth - 1, alpha, beta, True, position)
                if alphabetaValue is not None:
                    v = min(v, alphabetaValue)
                if v == alphabetaValue:
                    position = alphabetaPosition
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return v, position

    def checkOneLine_num(self, x, y, num, color, _gameBoard):
        if self.checkOneLine(color, x, y, self.RIGHTUP, num, _gameBoard):
            return True
        elif self.checkOneLine(color, x, y, self.RIGHTDOWN, num, _gameBoard):
            return True
        elif self.checkOneLine(color, x, y, self.HORIZONTAL, num, _gameBoard):
            return True
        elif self.checkOneLine(color, x, y, self.VERTICAL, num, _gameBoard):
            return True
        else:
            return False

    def checkOneLine(self, color, x, y, direction, length_num, _gameBoard):  # direction = int
        flag = False
        length = 0
        localGameBoard = _gameBoard

        dx = 0
        dy = 0

        if direction == self.RIGHTUP:
            dx = 1
            dy = -1
        elif direction == self.RIGHTDOWN:
            dx = 1
            dy = 1
        elif direction == self.HORIZONTAL:
            dx = 1
            dy = 0
        elif direction == self.VERTICAL:
            dx = 0
            dy = 1

        for i in range(-length_num + 1, length_num):
            _y = y + i * dy
            _x = x + i * dx

            if 19 > _x >= 0 and 19 > _y >= 0:
                if flag:
                    if localGameBoard[_y][_x] == color:
                        length += 1
                        if length == length_num:
                            return True
                    else:
                        flag = False
                        length = 0
                else:
                    if localGameBoard[_y][_x] == color:
                        flag = True
                        length += 1
