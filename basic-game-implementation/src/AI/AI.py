import random

class AI:

    def __init__(self, level: int, color: str):
        self.level = level
        self.color = color
        self.stones = 60
        #table de transposition pour la mémorisation
        #cle: Signature du plateau -> Valeur: {score, depth, flag}
        self.transposition_table = {} 
    

    def get_board_signature(self, board):
        """create a tuple of the state of the board for memorisation."""
        # On suppose que board.grid contient des objets avec un attribut .state
        return tuple(tuple(cell.state for cell in row) for row in board.grid)

    def get_relevant_moves(self, board):
        """get all the relevant moves that are one square away from a not empty square """
        possible_moves = []
        is_board_empty = True
        size = board.size
        # Directions: 8 voisins
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for r in range(size):
            for c in range(size):
                if board.grid[r][c].state is None:
                    # neighbor verification
                    has_neighbor = False
                    # look for a neighbor, if one is found, 
                    # than the square is relevant
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < size and 0 <= nc < size:
                            if board.grid[nr][nc].state is not None:
                                has_neighbor = True
                                is_board_empty = False
                                break
                    
                    if has_neighbor:
                        possible_moves.append((r, c))
                else:
                    is_board_empty = False

        # in case of empty board, place it at the center
        if not possible_moves and is_board_empty:
            return [(size // 2, size // 2)]
            
        return possible_moves

    def check_win_move(self, board, r, c, color):
        """
        check for the win at (r,c) coordinates
        """
        size = board.size
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # Horiz, Vert, Diag \, Diag /

        for dr, dc in directions:
            count = 1 # Actual pion counts already for one
            
            # Scan positive direction 
            for i in range(1, 5):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < size and 0 <= nc < size and board.grid[nr][nc].state == color:
                    count += 1
                else:
                    break
            
            # Scan negative direction opposée
            for i in range(1, 5):
                nr, nc = r - i * dr, c - i * dc
                if 0 <= nr < size and 0 <= nc < size and board.grid[nr][nc].state == color:
                    count += 1
                else:
                    break
            
            if count >= 5:
                return True
        return False

    def get_best_move(self, board, ai_color):
        """Start Alpha-Beta and return best coordinates."""
        # depth according to difficulty
        # easy = 1
        # medium = 2
        # hard = 3
        depth =  self.level 
        best_score = -float('inf')
        best_move = None
        opp_color = "white" if ai_color == "black" else "black"
        # check for instant win
        winning_move = self.find_immediate_threat(board, ai_color)
        if winning_move:
            print(f"Insta-Win found at {winning_move}")
            return winning_move
            
        # check for instant lose and block it
        blocking_move = self.find_immediate_threat(board, opp_color)
        if blocking_move:
            print(f"Forced block found at {blocking_move}")
            return blocking_move



        
        # 1. get all relevant moves (empty squares next to not empty square)
        possible_moves = self.get_relevant_moves(board)

        if not possible_moves:
            return None
        


        # 2. set a score for each board with a relevant move tested
        scored_moves = []
        for move in possible_moves:
            r, c = move
            board.place_stone(r, c, ai_color)
            score = self.evaluate_board(ai_color, board)
            board.grid[r][c].state = None
            scored_moves.append((score, move))
            
        #put the best score at first in the list to optimise the elagage
        scored_moves.sort(key=lambda x: x[0], reverse=True)

        
        print(f"AI calculating... (Depth: {depth}, Moves: {len(scored_moves)})")
        
        # 3.main loop with Minimax
        alpha = -float('inf')
        beta = float('inf')

        for score, move in scored_moves:
            r, c = move
            
            # test
            board.place_stone(r, c, ai_color)
            
            # recursive
            score = self.minimax(board, depth - 1, alpha, beta, False, ai_color)
            
            # delete tested pion
            board.grid[r][c].state = None
            
            if score > best_score:
                best_score = score
                best_move = move
            
            # update alpha
            alpha = max(alpha, best_score)
                
        print(f"AI chose {best_move} (Score: {best_score})")
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player, ai_color) -> int:
        """
        Algorithm Alpha-Beta with Mémorisation and Window Search.
        """
        # 0. look if board is memorised
        board_signature = self.get_board_signature(board)
        if board_signature in self.transposition_table:
            entry = self.transposition_table[board_signature]
            # On utilise le résultat stocké si la profondeur de recherche était suffisante
            # we use the result if the depth was enought
            if entry['depth'] >= depth:
                if entry['flag'] == 'exact':
                    return entry['score']
                elif entry['flag'] == 'lowerbound':
                    alpha = max(alpha, entry['score'])
                elif entry['flag'] == 'upperbound':
                    beta = min(beta, entry['score'])
                if alpha >= beta:
                    return entry['score']

        opp_color = "white" if ai_color == "black" else "black"
        current_player_color = ai_color if maximizing_player else opp_color
        
        # save alpha/beta for mémorisation
        alpha_original = alpha
        beta_original = beta

        # 1. stop condition : max depth reached
        if depth == 0:
            return self.evaluate_board(ai_color, board)

        # 2. moves generation (Optimisation Window Search)
        possible_moves = self.get_relevant_moves(board)
        
        if not possible_moves:
            return self.evaluate_board(ai_color, board)

        # 3. loop Minimax
        if maximizing_player:
            max_eval = -float('inf')
            
            for move in possible_moves:
                r, c = move
                
                # test
                board.place_stone(r, c, current_player_color)
                
                # chech for instant win (Optimisation check_win_move)
                if self.check_win_move(board, r, c, current_player_color):
                    eval = 100000000 + depth # we rather have a quick win than a long
                    board.grid[r][c].state = None
                    return eval # instant return to gain time

                # recursive
                eval = self.minimax(board, depth - 1, alpha, beta, False, ai_color)
                
                # delete tested pion
                board.grid[r][c].state = None
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            
            final_score = max_eval

        else: # Minimizing player
            min_eval = float('inf')
            
            for move in possible_moves:
                r, c = move
                
                # test
                board.place_stone(r, c, current_player_color)
                
                # check for instant lose
                if self.check_win_move(board, r, c, current_player_color):
                    eval = -100000000 - depth 
                    board.grid[r][c].state = None
                    return eval

                # recursive
                eval = self.minimax(board, depth - 1, alpha, beta, True, ai_color)
                
                # delete tested pion
                board.grid[r][c].state = None
                
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            
            final_score = min_eval

        # 4. memorizing
        flag = 'exact'
        if final_score <= alpha_original:
            flag = 'upperbound'
        elif final_score >= beta_original:
            flag = 'lowerbound'
        
        self.transposition_table[board_signature] = {
            'score': final_score,
            'depth': depth,
            'flag': flag
        }

        return final_score

    def evaluate_board(self, ai_color: str, board) :
        """
        set a score for the actual board
        """
        opp_color = "white" if ai_color == "black" else "black"
        size = board.size
        total_score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        score_map = {
            (5, 0): 10000000, 
            (4, 0): 10000, 
            (3, 0): 1000,
            (2, 0): 100,
            (1, 0): 10,
            (0, 5): -10000000, 
            (0, 4): -9000, 
            (0, 3): -900,
            (0, 2): -90,
            (0, 1): -9,
        }

        for r in range(size):
            for c in range(size):
                # we launch the eval if not on a empty square
                if board.grid[r][c].state is None:
                    continue

                for dr, dc in directions:
                    if r + 4 * dr < size and c + 4 * dc < size and r + 4 * dr >= 0 and c + 4 * dc >= 0:
                        segment = []
                        for i in range(5):
                            segment.append(board.grid[r + i * dr][c + i * dc].state)

                        ai_count = segment.count(ai_color)
                        opp_count = segment.count(opp_color)
                        empty_count = segment.count(None) 

                        if (ai_count, opp_count) in score_map:
                            score = score_map[(ai_count, opp_count)]
                            
                            # open segment gestions
                            if empty_count > 0:
                                is_open = False
                                # Case before
                                r_prev, c_prev = r - dr, c - dc
                                if 0 <= r_prev < size and 0 <= c_prev < size and board.grid[r_prev][c_prev].state is None:
                                    is_open = True
                                # Case after
                                r_next, c_next = r + 5 * dr, c + 5 * dc
                                if 0 <= r_next < size and 0 <= c_next < size and board.grid[r_next][c_next].state is None:
                                    is_open = True
                                
                                if is_open and (ai_count == 4 or opp_count == 4):
                                    score *= 2 
                                if not is_open and ai_count < 5 and opp_count < 5:
                                    score = score // 2 
                            
                            total_score += score

        return total_score

    def find_immediate_threat(self, board, color):
        """
        check if 'color' can win in one move
        used to check instant wins and loses
        """
        # we use get_relevant_moves to check only the possible win moves
        moves = self.get_relevant_moves(board)
        
        for r, c in moves:
            # test
            board.grid[r][c].state = color 
            
            # check if win
            if self.check_win_move(board, r, c, color):
                board.grid[r][c].state = None # delete tested pion
                return (r, c)
            
            board.grid[r][c].state = None # delete tested pion
            
        return None