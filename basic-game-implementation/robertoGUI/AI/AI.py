import components.Board as Board
import random

class AI:

    def __init__(self, level: int):
        self.level = level
        self.color = "black"
        self.stones = 60
        self.white_around = None
        self.black_around = None

    def set_tables(self, board: Board):
        self.white_around = [[0 for _ in range(board.size)] for _ in range(board.size)]
        self.black_around = [[0 for _ in range(board.size)] for _ in range(board.size)]

    def update_white_around(self, board: Board, row: int, col: int):
        self.white_around[row][col] = "◯"
        directions = [(1,0), (0,1), (1,1), (-1,1)]
        for vertical, horizontal in directions:
            for i in range(1,3):
                for sign in [1, -1]:
                    new_x = row + i * vertical * sign
                    new_y = col + i * horizontal  * sign
                    if 0 <= new_y < board.size and 0 <= new_x < board.size:
                        if board.grid[new_x][new_y].state is None:
                            self.white_around[new_x][new_y] += 1

    def update_black_around(self, board: Board, row: int, col: int):
        self.black_around[row][col] = "●"
        directions = [(1,0), (0,1), (1,1), (-1,1)]
        for vertical, horizontal in directions:
            for i in range(1,3):
                for sign in [1, -1]:
                    new_x = row + i * vertical * sign
                    new_y = col + i * horizontal * sign
                    if 0 <= new_x < board.size and 0 <= new_y < board.size:
                        if board.grid[new_x][new_y].state is None:
                            self.black_around[new_x][new_y] += 1

    def evaluate_board(self, ai_color: str, board: Board) :
        """
        Calculates the value of the current board state for the AI (ai_color).
        A positive value is good for the AI, a negative value is good for the opponent.
        """
        opp_color = "white" if ai_color == "black" else "black"
        size = board.size
        total_score = 0
        
        # Directions: Horizontal, Vertical, Diagonal /, Diagonal \
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        # Scoring tables 
        # We penalize if both sides are blocked.
        # Format: (AI_count, Opp_count) -> Score
        
        # NOTE: 10000000 is a guaranteed win score (must dominate everything else)
        score_map = {
            (5, 0): 10000000, 
            (4, 0): 10000, # 4-in-a-row (strong potential win)
            (3, 0): 1000,
            (2, 0): 100,
            (1, 0): 10,
            (0, 5): -10000000, 
            (0, 4): -9000, # Threat of loss (must be slightly less than attack, but very large)
            (0, 3): -900,
            (0, 2): -90,
            (0, 1): -9,
        }

        # Iterate over all possible starting points
        for r in range(size):
            for c in range(size):
                
                # Check the 4 directions
                for dr, dc in directions:
                    
                    # Ensure the 5-square segment does not go off the board
                    if r + 4 * dr < size and c + 4 * dc < size and r + 4 * dr >= 0 and c + 4 * dc >= 0:
                        
                        segment = []
                        # Build the 5-square segment
                        for i in range(5):
                            segment.append(board.grid[r + i * dr][c + i * dc].state)

                        ai_count = segment.count(ai_color)
                        opp_count = segment.count(opp_color)
                        empty_count = segment.count(None) 

                        # If it is a relevant segment
                        if (ai_count, opp_count) in score_map:
                            score = score_map[(ai_count, opp_count)]
                            
                            # Bonus/Malus for open segments (not blocked at the ends)
                            # This is a crucial simplification
                            if empty_count > 0 : # If there is room to evolve
                                
                                # Check immediate adjacent squares for openness
                                is_open = False
                                
                                # Check the square before the segment start
                                r_prev, c_prev = r - dr, c - dc
                                if 0 <= r_prev < size and 0 <= c_prev < size and board.grid[r_prev][c_prev].state is None:
                                    is_open = True
                                
                                # Check the square after the segment end
                                r_next, c_next = r + 5 * dr, c + 5 * dc
                                if 0 <= r_next < size and 0 <= c_next < size and board.grid[r_next][c_next].state is None:
                                    is_open = True
                                
                                if is_open and (ai_count == 4 or opp_count == 4):
                                    score *= 2 
                                
                                if not is_open and ai_count < 5 and opp_count < 5:
                                    score = score // 2 # Segment is "dead" or hard to complete.
                                
                            total_score += score

        return total_score


    # In the AI class (AI.py) - Method get_best_move

    def get_best_move(self, board: Board, ai_color: str):
        """Launches the Alpha-Beta search and returns the best coordinates."""
        
        depth = 2 * self.level 
        best_score = -float('inf')
        best_move = None
        size = board.size
        
        # --- START OF OPTIMIZATION: MOVE RESTRICTION (Window Search) ---
        possible_moves = []
        is_board_empty = True
        
        # 1. Iterate over all squares to find relevant moves
        for r in range(size):
            for c in range(size):
                if board.grid[r][c].state is None: # If the square is empty
                    
                    # Check if the square is active (surrounded by pieces, using 'around' tables)
                    # NOTE: These tables MUST be updated before this call.
                    if (self.white_around and self.white_around[r][c] > 0) or \
                    (self.black_around and self.black_around[r][c] > 0):
                        
                        possible_moves.append((r, c))
                
                elif is_board_empty:
                    is_board_empty = False

        # 2. Handle start of game
        if not possible_moves:
            # If the board is empty (first move)
            if is_board_empty:
                center = size // 2
                return (center, center)
            # Else (end of game or all active squares are filled)
            else:
                return None 
                
        # --- END OF OPTIMIZATION ---

        # Quick initial scoring based on Depth 1 evaluation
        scored_moves = []
        for move in possible_moves:
            r, c = move
            board.place_stone(r, c, ai_color)
            score = self.evaluate_board(ai_color, board)
            board.grid[r][c].state = None
            scored_moves.append((score, move))
            
        # Sort best scores first (descending order)
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        
        # 3. Alpha-Beta search on the sorted moves
        print(f"AI is calculating... (Depth: {depth}, Moves considered: {len(scored_moves)})")
        
        for score, move in scored_moves:
            r, c = move
            
            # Simulate the move
            board.place_stone(r, c, ai_color)
            
            # Call Minimax (Max is implicit here, it's the AI's turn)
            score = self.minimax(board, depth - 1, -float('inf'), float('inf'), False, ai_color)
            
            # Undo the move (fundamental for search)
            board.grid[r][c].state = None
            
            if score > best_score:
                best_score = score
                best_move = move
                
        print(f"AI chose move {best_move} with expected score {best_score}")
        return best_move


    def minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing_player: bool, ai_color: str) -> int:
        """
        Minimax algorithm implementation with Alpha-Beta pruning.
        """
        opp_color = "white" if ai_color == "black" else "black"
        current_player_color = ai_color if maximizing_player else opp_color
        
        # 1. Stopping condition: depth limit or win/loss
        
        # Simplification: evaluate if maximum depth is reached
        if depth == 0:
            return self.evaluate_board(ai_color, board)

        # 2. Generate possible moves (limited to a neighborhood if possible)
        possible_moves = []
        # For a complete implementation, moves around existing pieces should be generated
        #NEED OPTIMISATION
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c].state is None:
                    possible_moves.append((r, c))

        if not possible_moves:
            return self.evaluate_board(ai_color, board) # Full board = draw / end game

        # 3. Main Minimax loop
        if maximizing_player:
            max_eval = -float('inf')
            
            # Immediate win check (winner = very high score)
            if self.check_win_at_depth(board, opp_color): # Opponent has won in the previous move
                return -100000000 - depth
                
            for move in possible_moves:
                r, c = move
                
                # Simulate
                board.place_stone(r, c, current_player_color)
                
                # Recursion
                eval = self.minimax(board, depth - 1, alpha, beta, False, ai_color)
                
                # Undo
                board.grid[r][c].state = None
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval

        else: # Minimizing player
            min_eval = float('inf')
            
            # Immediate loss check (loser = very low score)
            if self.check_win_at_depth(board, ai_color): # AI has won in the previous move
                return 100000000 + depth 

            for move in possible_moves:
                r, c = move
                
                # Simulate
                board.place_stone(r, c, current_player_color)
                
                # Recursion
                eval = self.minimax(board, depth - 1, alpha, beta, True, ai_color)
                
                # Undo
                board.grid[r][c].state = None
                
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval

    def check_win_at_depth(self, board: Board, color: str) -> bool:
        """
        Utility function to check if the current state is a win for 'color'.
        This is crucial for optimizing alpha-beta pruning.
        """
        # For Alpha-Beta, we must traverse the entire board, like in evaluate_board.
        size = board.size
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for r in range(size):
            for c in range(size):
                for dr, dc in directions:
                    if r + 4 * dr < size and c + 4 * dc < size and r + 4 * dr >= 0 and c + 4 * dc >= 0:
                        
                        count = 0
                        for i in range(5):
                            if board.grid[r + i * dr][c + i * dc].state == color:
                                count += 1
                            else:
                                break
                        if count == 5:
                            return True
        return False