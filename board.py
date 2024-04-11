import pygame
import os


class Board:

    piece_images = {
        'P': 'w_pawn_png_512px.png',
        'N': 'w_knight_png_512px.png',
        'B': 'w_bishop_png_512px.png',
        'R': 'w_rook_png_512px.png',
        'Q': 'w_queen_png_512px.png',
        'K': 'w_king_png_512px.png',
        'p': 'b_pawn_png_512px.png',
        'n': 'b_knight_png_512px.png',
        'b': 'b_bishop_png_512px.png',
        'r': 'b_rook_png_512px.png',
        'q': 'b_queen_png_512px.png',
        'k': 'b_king_png_512px.png',
    }
    def __init__(self):
        self.initialized = False
        self.image_path = '/Users/alif/Documents/twirld/images/'

        self.black = (0, 0, 0)
        self.white = (231, 235, 202)
        self.black = (98, 134, 66)
        self.silver = (127, 127, 127)
        pygame.init()

        self.padding_top = 240
        self.evaluation_bar = 0

        self.square = 70
        self.width = (self.square * 8) + self.evaluation_bar
        self.height = (self.square * 8) + self.padding_top
        self.image_center = 20
        self.pieces = self.load_pieces()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chess Board")

        self.fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.fen = 'rnbqk1nr/pp3ppp/3bp3/2pp4/P1P5/3P1N2/1P2PPPP/RNBQKB1R w KQkq - 1 5'


    def load_pieces(self):
        _images = {}
        for piece in self.piece_images:
            img = os.path.join(self.image_path, self.piece_images[piece])
            original_img = pygame.image.load(img)
            resized_img = pygame.transform.scale(original_img, (self.square - self.image_center, self.square - self.image_center))
            _images[piece] = resized_img
        return _images


    def _draw_empty_board(self):
        for row in range(8):
            for col in range(8):
                color = self.white if (row + col) % 2 == 0 else self.black
                x = col * self.square
                y = row * self.square


                pygame.draw.rect(
                    self.screen,
                    color,
                    (x, y + (self.padding_top // 2), self.square, self.square)
                )


        # draw evaluation_bar
        pygame.draw.rect(
            self.screen,
            (255, 0, 255),
            (self.width - self.evaluation_bar, self.padding_top // 2, self.square * 8, self.square * 4)
        )

    def draw_piece(self, row, col, piece, selected=False):
        pos_x = col * self.square
        pos_y = row * self.square

        pos_x = pos_x + (self.image_center // 2)
        pos_y = pos_y + (self.image_center // 2) + (self.padding_top // 2)

        if selected:
            # Create a surface with transparency
            overlay = pygame.Surface((self.square, self.square), pygame.SRCALPHA)
            overlay.fill((229, 105, 91, 255))  # Translucent white color (adjust alpha as needed)
            self.screen.blit(overlay, (col * self.square, row * self.square + (self.padding_top // 2)))
        self.screen.blit(
            piece,
            (pos_x, pos_y)
        )


    def initial_board_matrix(self):
        _splitted_fen = self.fen.split(' ')
        pieces = _splitted_fen[0].split('/')
        board_matrix = []

        for row in pieces:
            row_list = []
            for char in row:
                if char.isdigit():
                    row_list.extend(['.'] * int(char))  # Expand numeric characters into empty squares
                else:
                    row_list.append(char)  # Add piece identifiers as is
            board_matrix.append(row_list)

        return board_matrix

    def initial_board(self):
        _splitted_fen = self.fen.split(' ')
        pieces = _splitted_fen[0].split('/')

        for row_index, row in enumerate(pieces):
            col_index = 0
            for char in row:
                if char.isdigit():
                    col_index += int(char)
                else:
                    piece = self.pieces[char]
                    self.draw_piece(row_index, col_index, piece)
                    col_index += 1

        self._board = self.initial_board_matrix()

    def run(self):

        done = False

        selected_piece = None
        while not done:
            self.screen.fill(self.silver)
            self._draw_empty_board()
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_Q:
                        done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click event
                    if event.button == 1:  # Left mouse button clicked
                        mouse_x, mouse_y = event.pos
                        # Convert mouse coordinates to board coordinates
                        clicked_col = mouse_x // self.square
                        clicked_row = (mouse_y - self.padding_top // 2) // self.square
                        # Check if the clicked square contains a piece
                        if (0 <= clicked_row < 8) and (0 <= clicked_col < 8):
                            selected_piece = (clicked_row, clicked_col)  # Store the selected piece
                            print(selected_piece, '--'*100)

            self.initial_board()
            for _row in self._board:
                print(' '.join(_row))
            print('--'*16)

            if selected_piece:
                row, col = selected_piece
                piece = self._board[row][col]
                if piece != '.':
                    self.draw_piece(row, col, self.pieces[piece], selected=True)

            pygame.display.flip()
        pygame.quit()


b = Board()
b.run()

