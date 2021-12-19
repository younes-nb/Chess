from src.Model.Piece import Piece
from PyQt6.QtGui import QPixmap
from src.res import resource_path


class Pawn(Piece):
    def __init__(self, x, y, team):
        super().__init__(x, y)
        self.team = team
        self.image = None
        match self.team:
            case "White":
                self.image = QPixmap(resource_path("Pieces/white-pawn.png"))
                self.type = "WPawn"
            case "Black":
                self.image = QPixmap(resource_path("Pieces/black-pawn.png"))
                self.type = "BPawn"