from src.Model.Piece import Piece
from PyQt6.QtGui import QPixmap
from src.res import resource_path


class Queen(Piece):
    def __init__(self, x, y, team):
        super().__init__(x, y)
        self.team = team
        self.image = None
        match self.team:
            case "White":
                self.image = QPixmap(resource_path("Pieces/white-queen.png"))
                self.type = "WQueen"
            case "Black":
                self.image = QPixmap(resource_path("Pieces/black-queen.png"))
                self.type = "BQueen"