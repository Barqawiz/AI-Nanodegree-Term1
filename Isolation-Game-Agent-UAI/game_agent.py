"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """The heuristic value calculated as following:
    1- 70% for legal moves check (2 strategies)
    2- 15% for player one near center
    3- 15% for opponent near corner
    
    
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
   
    #raise NotImplementedError
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)

    #15% for player one near center: 3.5-(3.5-6%3)
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    playerCenter = abs(w - abs(w-(x%(game.width-1)))) + abs(h - abs(h-(y%(game.height-1))))

    #15% for opponent near corner
    oy, ox = game.get_player_location(opponent)
    oponentCorner = abs(w-(x%(game.width-1))) + abs(h-(y%(game.height-1)))

    #70% for legal mvoes check

    ownMoves = len(game.get_legal_moves(player))
    oppMoves = len(game.get_legal_moves(opponent))
    masterCheck1 = float(ownMoves - oppMoves)
    if (ownMoves >=2):
        masterCheck1 = float(ownMoves - oppMoves*2)

    if oppMoves == 0 and ownMoves > 0:
        return float("inf")
    else:
        return (playerCenter * 0.15) + (oponentCorner * 0.15) + (masterCheck1*0.7)


def custom_score_2(game, player):
    """Calculate the heuristic value of player moves - (opponent moves *2)

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)
    ownMoves = len(game.get_legal_moves(player))
    oppMoves = len(game.get_legal_moves(opponent))

    return float( ownMoves - oppMoves*2 )

def custom_score_3(game, player):
    """The heuristic value calculated as following:
    1- 70% for legal moves check (1 strategy)
    2- 15% for player one near center
    3- 15% for opponent near corner

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    #raise NotImplementedError
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)

    #20% for player one near center: 3.5-(3.5-6%3)
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    playerCenter = abs(w - abs(w-(x%(game.width-1)))) + abs(h - abs(h-(y%(game.height-1))))

    #20% for opponent near corner
    oy, ox = game.get_player_location(opponent)
    oponentCorner = abs(w-(x%(game.width-1))) + abs(h-(y%(game.height-1)));

    #60% for legal mvoes check
    ownMoves = len(game.get_legal_moves(player))
    oppMoves = len(game.get_legal_moves(opponent))
    masterCheck = float(ownMoves - oppMoves)

    if (oppMoves == 0 and ownMoves > 0):
        masterCheck = float("inf")

    return (playerCenter * 0.2) + (oponentCorner * 0.2) + (masterCheck*0.6)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        bestMove = (-1, -1)
        bestScore = float("-inf")
        legalMoves = game.get_legal_moves()

        for move in legalMoves:
            selectedScore = self.minimax_minimizer(game.forecast_move(move), depth-1)
            if (selectedScore > bestScore):
                bestScore = selectedScore
                bestMove  = move

        return bestMove

    def minimax_maximizer(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth <= 0:
            return self.score(game, self)

        bestScore = float("-inf")
        legalMoves = game.get_legal_moves()

        for move in legalMoves:
            selectedScore = self.minimax_minimizer(game.forecast_move(move), depth - 1)
            if (selectedScore > bestScore):
                bestScore = selectedScore

        return bestScore

    def minimax_minimizer(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth <= 0:
            return self.score(game, self)

        bestScore = float("inf")
        legalMoves = game.get_legal_moves()
        for move in legalMoves:
            selectedScore = self.minimax_maximizer(game.forecast_move(move), depth-1)
            if (selectedScore < bestScore):
                bestScore = selectedScore

        return bestScore


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 0
            while True:
                best_move =  self.alphabeta(game, depth)
                if game.is_loser(self):
                    break
                if game.is_winner(self):
                    break
                depth= depth+1

        except SearchTimeout as ex:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        # strategy 1: alpha is the best explored max option in my path (if found bigger/or found it then break)
        # strategy 2: beta is the best explored min option in my path  (if found lower/or found it then break)
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout((-1, -1))

        try:
            bestMove = (-1, -1)
            bestScore = float("-inf")
            legalMoves = game.get_legal_moves()

            for move in legalMoves:
                selectedScore = self.alphabeta_minimizer(game.forecast_move(move), depth - 1, alpha, beta)
                if (selectedScore >= bestScore):
                    bestScore = selectedScore
                    bestMove = move

                if (bestScore >= beta):
                    break

                alpha = max(alpha, bestScore)
        except SearchTimeout:
            raise SearchTimeout(bestMove)

        return bestMove

    def alphabeta_maximizer(self, game, depth, alpha, beta):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth <= 0:
            return self.score(game, self)

        bestScore = float("-inf")
        legalMoves = game.get_legal_moves()

        for move in legalMoves:
            selectedScore = self.alphabeta_minimizer(game.forecast_move(move), depth - 1, alpha, beta)


            if (selectedScore > bestScore):
                bestScore = selectedScore

            if (bestScore >= beta):
                return bestScore
            alpha = max(alpha, bestScore)

        return bestScore

    def alphabeta_minimizer(self, game, depth, alpha, beta):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth <= 0:
            return self.score(game, self)

        bestScore = float("inf")
        legalMoves = game.get_legal_moves()
        for move in legalMoves:
            selectedScore = self.alphabeta_maximizer(game.forecast_move(move), depth - 1, alpha, beta)
            if (selectedScore < bestScore):
                bestScore = selectedScore

            if (bestScore <= alpha):
                return bestScore
            beta = min(beta, bestScore)

        
        return bestScore