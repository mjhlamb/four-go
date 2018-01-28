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

    def __str__():
        return "AI"

    def update(self, gameBoard):
        self.gameBoard = gameBoard

    def constructSearchTree(self, x, y, num, gamePaths):  # return tree
        if num > 0:
            root = Tree()
            for i in range(3):
                for j in range(3):
                    _x = i + x - 1
                    _y = j + y - 1
                    if 19 > _x >= 0 and 19 > _y >= 0 and self.gameBoard[_y][_x] == self.BLANK:
                        node = Tree()
                        _gamePaths = copy.deepcopy(gamePaths)
                        _path = [_x, _y]
                        _gamePaths.append(_path)
                        node = self.constructSearchTree(_x, _y, num - 1, _gamePaths)
                        node.parent = root
                        root.children.append(node)
            return root
        else:
            node = Tree()
            node.position.append(x)
            node.position.append(y)
            _gameBoard = copy.copy(self.gameBoard)

            if len(gamePaths) > 1:
                _gameBoard[gamePaths[0][1]][gamePaths[0][0]] = self.BLACK
                _gameBoard[gamePaths[1][1]][gamePaths[1][0]] = self.WHITE
                _gameBoard[gamePaths[0][1]][gamePaths[0][0]] = self.BLACK

            if self.checkOneLine_num(x, y, 4, _gameBoard):
                node.data = 4
            elif self.checkOneLine_num(x, y, 4, _gameBoard):
                node.data = 3
            elif self.checkOneLine_num(x, y, 4, _gameBoard):
                node.data = 2
            elif self.checkOneLine_num(x, y, 4, _gameBoard):
                node.data = 1
            else:
                node.data = 0

            return node

    def calculateTree(self, x, y):
        tree = self.constructSearchTree(x, y, 3, [])
        (alphabetaValue, alphabetaPosition) = self.alphabeta(tree, 1, -9999, 9999, True, [0, 0])
        print(alphabetaPosition)
        return alphabetaPosition

    def alphabeta(self, node, depth, alpha, beta, maximizingPlayer, position):
        if depth == 0 or node.children is None:
            return (node.data, node.position)
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
            return (v, position)
        else:
            v = 9999
            for child in node.children:
                (alphabetaValue, alphabetaPosition) = self.alphabeta(child, depth - 1, alpha, beta, True, position)
                v = min(v, alphabetaValue)
                if v == alphabetaValue:
                    position = alphabetaPosition
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return (v, position)

    def checkOneLine_num(self, x, y, num, _gameBoard):
        if self.checkOneLine(self.WHITE, x, y, self.RIGHTUP, num, _gameBoard):
            return True
        elif self.checkOneLine(self.WHITE, x, y, self.RIGHTDOWN, num, _gameBoard):
            return True
        elif self.checkOneLine(self.WHITE, x, y, self.HORIZONTAL, num, _gameBoard):
            return True
        elif self.checkOneLine(self.WHITE, x, y, self.VERTICAL, num, _gameBoard):
            return True
        else:
            return False

    def checkOneLine(self, color, x, y, dir, len, _gameBoard):  # direction = int
        flag = False
        length = 0
        localGameBoard = copy.deepcopy(_gameBoard)

        dx = 0
        dy = 0
        _x = 0
        _y = 0

        localGameBoard[y][x] = self.WHITE

        if dir == self.RIGHTUP:
            dx = 1
            dy = -1
        elif dir == self.RIGHTDOWN:
            dx = 1
            dy = 1
        elif dir == self.HORIZONTAL:
            dx = 1
            dy = 0
        elif dir == self.VERTICAL:
            dx = 0
            dy = 1

        for i in range(-len + 1, len):
            _y = y + i * dy
            _x = x + i * dx

            if 19 > _x >= 0 and 19 > _y >= 0:
                if flag:
                    if localGameBoard[_y][_x] == color:
                        length += 1
                        if length == len:
                            return True
                    else:
                        flag = False
                        length = 0
                else:
                    if localGameBoard[_y][_x] == color:
                        flag = True
                        length += 1
