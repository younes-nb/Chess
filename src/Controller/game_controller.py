from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel
from src.Model.bishop import Bishop
from src.Model.blank import Blank
from src.Model.king import King
from src.Model.knight import Knight
from src.Model.pawn import Pawn
from src.Model.piece import Piece
from src.Model.queen import Queen
from src.Model.rook import Rook
from src.View.game_view import GameView
from src.res import resource_path


class GameController(GameView):
    def __init__(self):
        super().__init__(self.create_pieces())
        self.selected_piece = None
        self.turn = "White"

    def create_pieces(self):
        pieces = [
            [Rook(self, 0, 0, "Black"), Knight(self, 0, 1, "Black"),
             Bishop(self, 0, 2, "Black"), Queen(self, 0, 3, "Black"),
             King(self, 0, 4, "Black"), Bishop(self, 0, 5, "Black"),
             Knight(self, 0, 6, "Black"), Rook(self, 0, 7, "Black")],
            [Pawn(self, 1, 0, "Black"), Pawn(self, 1, 1, "Black"),
             Pawn(self, 1, 2, "Black"), Pawn(self, 1, 3, "Black"),
             Pawn(self, 1, 4, "Black"), Pawn(self, 1, 5, "Black"),
             Pawn(self, 1, 6, "Black"), Pawn(self, 1, 7, "Black")],
            [Blank(self, 2, 0), Blank(self, 2, 1), Blank(self, 2, 2), Blank(self, 2, 3),
             Blank(self, 2, 4), Blank(self, 2, 5), Blank(self, 2, 6), Blank(self, 2, 7)],
            [Blank(self, 3, 0), Blank(self, 3, 1), Blank(self, 3, 2), Blank(self, 3, 3),
             Blank(self, 3, 4), Blank(self, 3, 5), Blank(self, 3, 6), Blank(self, 3, 7)],
            [Blank(self, 4, 0), Blank(self, 4, 1), Blank(self, 4, 2), Blank(self, 4, 3),
             Blank(self, 4, 4), Blank(self, 4, 5), Blank(self, 4, 6), Blank(self, 4, 7)],
            [Blank(self, 5, 0), Blank(self, 5, 1), Blank(self, 5, 2), Blank(self, 5, 3),
             Blank(self, 5, 4), Blank(self, 5, 5), Blank(self, 5, 6), Blank(self, 5, 7)],
            [Pawn(self, 6, 0, "White"), Pawn(self, 6, 1, "White"),
             Pawn(self, 6, 2, "White"), Pawn(self, 6, 3, "White"),
             Pawn(self, 6, 4, "White"), Pawn(self, 6, 5, "White"),
             Pawn(self, 6, 6, "White"), Pawn(self, 6, 7, "White")],
            [Rook(self, 7, 0, "White"), Knight(self, 7, 1, "White"),
             Bishop(self, 7, 2, "White"), Queen(self, 7, 3, "White"),
             King(self, 7, 4, "White"), Bishop(self, 7, 5, "White"),
             Knight(self, 7, 6, "White"), Rook(self, 7, 7, "White")]
        ]
        return pieces

    def set_turn_icon(self, white_turn_icon: QPixmap, black_turn_icon: QPixmap):
        self.info_white.turn_icon.setPixmap(white_turn_icon)
        self.info_black.turn_icon.setPixmap(black_turn_icon)
        self.info_white.turn_icon.update()
        self.info_black.turn_icon.update()

    def select_piece(self, piece):
        if self.turn == piece.team and piece.type != "Blank":
            if self.selected_piece and self.selected_piece != piece:
                self.selected_piece.selected = False
                self.un_paint()
                self.selected_piece.update()
            if piece.selected:
                piece.selected = False
                self.selected_piece = None
                self.un_paint()
                piece.update()
            else:
                self.selected_piece = piece
                self.selected_piece.selected = True
                self.paint()
                self.selected_piece.update()

    def change_turn(self):
        match self.turn:
            case "White":
                self.turn = "Black"
                self.info_black.turn_icon.setToolTip("It's your turn!")
                self.info_white.turn_icon.setToolTip("Wait!")
                self.set_turn_icon(QPixmap(resource_path("Icons/turn-blank.png")),
                                   QPixmap(resource_path("Icons/turn.png")))

            case "Black":
                self.turn = "White"
                self.info_white.turn_icon.setToolTip("It's your turn!")
                self.info_black.turn_icon.setToolTip("Wait!")
                self.set_turn_icon(QPixmap(resource_path("Icons/turn.png")),
                                   QPixmap(resource_path("Icons/turn-blank.png")))

    def move_piece(self, target: Piece):
        self.board.removeWidget(target)
        self.board.removeWidget(self.selected_piece)
        target.position, self.selected_piece.position = self.selected_piece.position, target.position
        self.board.addWidget(target, target.position[0], target.position[1])
        self.board.addWidget(self.selected_piece, self.selected_piece.position[0], self.selected_piece.position[1])

        self.pieces[target.position[0]][target.position[1]], self.pieces[self.selected_piece.position[0]][
            self.selected_piece.position[1]] = self.pieces[self.selected_piece.position[0]][
                                                   self.selected_piece.position[1]], self.pieces[target.position[0]][
                                                   target.position[1]]
        self.un_paint()
        self.selected_piece.selected = False
        target.update()
        self.selected_piece.update()

        if target.team != "None":
            self.capture_piece(target)
        self.check()
        self.selected_piece = None
        self.change_turn()
        self.board.update()
        self.update()

    def capture_piece(self, piece: Piece):
        blank = Blank(self, piece.position[0], piece.position[1])
        self.pieces[blank.position[0]][blank.position[1]] = blank
        self.board.removeWidget(piece)
        self.board.addWidget(blank, blank.position[0], blank.position[1])
        self.board.update()
        self.add_captured_piece_icon(piece.type)
        piece.destroy(False, False)
        piece.update()
        blank.update()

    def add_captured_piece_icon(self, piece):
        captured_label = QLabel()
        if piece[0] == 'W':
            match piece:
                case "WQueen":
                    captured_label.setPixmap(QPixmap(resource_path("Pieces/out-white-queen.png")))
                case "WBishop":
                    captured_label.setPixmap(QPixmap(resource_path("Pieces/out-white-bishop.png")))
                case "WKnight":
                    captured_label.setPixmap(QPixmap(resource_path("Pieces/out-white-knight.png")))
                case "WRook":
                    captured_label.setPixmap(QPixmap(resource_path("Pieces/out-white-rook.png")))
                case "WPawn":
                    captured_label.setPixmap(QPixmap(resource_path("Pieces/out-white-pawn.png")))

            self.info_white.captured_pieces.addWidget(captured_label, self.info_white.captured_x,
                                                      self.info_white.captured_y)
            self.info_white.captured_y += 1
            if self.info_white.captured_y > 2:
                self.info_white.captured_x += 1
                self.info_white.captured_y = 0
            self.info_white.captured_pieces.update()
        elif piece[0] == 'B':
            match piece:
                case "BQueen":
                    captured_label.setPixmap(QPixmap(resource_path("Pieces/out-black-queen.png")))
                case "BBishop":
                    captured_label.setPixmap(QPixmap(resource_path("Pieces/out-black-bishop.png")))
                case "BKnight":
                    captured_label.setPixmap(QPixmap(resource_path("Pieces/out-black-knight.png")))
                case "BRook":
                    captured_label.setPixmap(QPixmap(resource_path("Pieces/out-black-rook.png")))
                case "BPawn":
                    captured_label.setPixmap(QPixmap(resource_path("Pieces/out-black-pawn.png")))
            self.info_black.captured_pieces.addWidget(captured_label, self.info_black.captured_x,
                                                      self.info_black.captured_y)
            self.info_black.captured_y += 1
            if self.info_black.captured_y > 2:
                self.info_black.captured_x += 1
                self.info_black.captured_y = 0
            self.info_black.captured_pieces.update()

    def check(self):
        opponent_king = self.checked_king(True)
        king = self.checked_king(False)
        found_opponent_king = False
        found_king = False
        for row in self.pieces:
            if found_opponent_king:
                break
            for piece in row:
                if found_opponent_king:
                    break
                if piece.team != self.turn and piece.team != "None":
                    for movement in piece.all_moves():
                        if self.pieces[movement[0]][movement[1]].type == king.type:
                            found_king = True
                if piece.team == self.turn:
                    for movement in piece.all_moves():
                        if self.pieces[movement[0]][movement[1]].type == opponent_king.type:
                            found_opponent_king = True
                            opponent_king.is_checked = True
                            opponent_king.update()
                            break
        if not found_opponent_king:
            opponent_king.is_checked = False
            opponent_king.update()
        if not found_king:
            king.is_checked = False
            king.update()

    def checked_king(self, check):
        white_king = None
        black_king = None
        for row in self.pieces:
            for piece in row:
                if piece.type == "WKing":
                    white_king = piece
                elif piece.type == "BKing":
                    black_king = piece
        if check:
            match self.turn:
                case "White":
                    return black_king
                case "Black":
                    return white_king
        else:
            match self.turn:
                case "White":
                    return white_king
                case "Black":
                    return black_king

    def check_mate(self):
        opponent_king = self.checked_king(False)
        mate = True
        for row in self.pieces:
            if not mate:
                break
            for piece in row:
                if not mate:
                    break
                self.selected_piece = piece
                if piece.team == opponent_king.team:
                    for movement in piece.all_moves():
                        if movement_validation(movement, self.create_copy()):
                            mate = False
                            break
        self.selected_piece = None
        if mate:
            for row in self.pieces:
                for piece in row:
                    if piece.team != opponent_king.team and piece.team != "None":
                        for movement in piece.all_moves():
                            if self.pieces[movement[0]][movement[1]].type == opponent_king.type:
                                piece.checker = True
                                piece.update()
                                break

            opponent_king.is_check_mate = True
            opponent_king.update()
        return mate

    def paint(self):
        if self.selected_piece:
            movements = self.selected_piece.all_moves()
            for movement in movements:
                if movement_validation(movement, self.create_copy()):
                    if self.pieces[movement[0]][movement[1]].team != "None":
                        self.pieces[movement[0]][movement[1]].target = True
                    else:
                        self.pieces[movement[0]][movement[1]].is_painted = True
                    self.pieces[movement[0]][movement[1]].update()

    def un_paint(self):
        for i in self.pieces:
            for piece in i:
                piece.is_painted = False
                piece.target = False
                piece.update()

    def create_copy(self):
        game_copy = GameController()
        for row in self.pieces:
            for piece in row:
                x = piece.position[0]
                y = piece.position[1]
                match piece.type:
                    case "WKing":
                        game_copy.pieces[x][y] = King(game_copy, x, y, "White")
                    case "BKing":
                        game_copy.pieces[x][y] = King(game_copy, x, y, "Black")
                    case "WQueen":
                        game_copy.pieces[x][y] = Queen(game_copy, x, y, "White")
                    case "BQueen":
                        game_copy.pieces[x][y] = Queen(game_copy, x, y, "Black")
                    case "WBishop":
                        game_copy.pieces[x][y] = Bishop(game_copy, x, y, "White")
                    case "BBishop":
                        game_copy.pieces[x][y] = Bishop(game_copy, x, y, "Black")
                    case "WKnight":
                        game_copy.pieces[x][y] = Knight(game_copy, x, y, "White")
                    case "BKnight":
                        game_copy.pieces[x][y] = Knight(game_copy, x, y, "Black")
                    case "WRook":
                        game_copy.pieces[x][y] = Rook(game_copy, x, y, "White")
                    case "BRook":
                        game_copy.pieces[x][y] = Rook(game_copy, x, y, "Black")
                    case "WPawn":
                        game_copy.pieces[x][y] = Pawn(game_copy, x, y, "White")
                    case "BPawn":
                        game_copy.pieces[x][y] = Pawn(game_copy, x, y, "Black")
                    case "Blank":
                        game_copy.pieces[x][y] = Blank(game_copy, x, y)

        for row in game_copy.pieces:
            for piece in row:
                if piece.position == self.selected_piece.position:
                    game_copy.selected_piece = piece
                    break
        return game_copy


def movement_validation(movement: tuple, game_copy: GameController):
    target = game_copy.pieces[movement[0]][movement[1]]
    target.position, game_copy.selected_piece.position = game_copy.selected_piece.position, target.position
    game_copy.pieces[target.position[0]][target.position[1]], \
        game_copy.pieces[game_copy.selected_piece.position[0]][
        game_copy.selected_piece.position[1]] = game_copy.pieces[game_copy.selected_piece.position[0]][
                                                    game_copy.selected_piece.position[1]], \
                                                game_copy.pieces[target.position[0]][
                                                    target.position[1]]
    if target.team != "None":
        game_copy.pieces[target.position[0]][target.position[1]] = Blank(game_copy, target.position[0],
                                                                         target.position[1])
    king = None
    found = False
    for row in game_copy.pieces:
        if found:
            break
        for piece in row:
            if piece.team == game_copy.selected_piece.team and piece.type[1::] == "King":
                king = piece
                found = True
                break

    for row in game_copy.pieces:
        for piece in row:
            if piece.team != game_copy.selected_piece.team and piece.team != "None":
                for move in piece.all_moves():
                    if game_copy.pieces[move[0]][move[1]].type == king.type:
                        return False
    return True