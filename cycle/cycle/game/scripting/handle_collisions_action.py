import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the cycle collides
    with the food, or the cycle collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._p1_win = False
        self._p2_win = False

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)

    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the cycle collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        #Player 1 Cycle
        cycle1 = cast.get_first_actor("cycles")
        cycle_head_1 = cycle1.get_head()
        cycle_segments_1 = cycle1.get_segments()
        
        #Player 2 Cycle
        cycle2 = cast.get_second_actor("cycles")
        cycle_head_2 = cycle2.get_head()
        cycle_segments_2 = cycle2.get_segments()

        #Player 1 Victory
        for cycle_segment_1 in cycle_segments_1:
            if cycle_head_2.get_position().equals(cycle_segment_1.get_position()):
                self._p1_win = True
                self._is_game_over = True
             
        #Player 2 Victory
        for cycle_segment_2 in cycle_segments_2:
            if cycle_head_1.get_position().equals(cycle_segment_2.get_position()):
                self._p2_win = True
                self._is_game_over = True
        
        #Stalemate: Cycles crashes against each other
        if cycle_head_2.get_position().equals(cycle_head_1.get_position()):
                self._p1_win = False
                self._p2_win = False
                self._is_game_over = True
            
        
        
    def _handle_game_over(self, cast): 
        """Shows the 'game over' message and turns the cycle and food white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            cycle1 = cast.get_first_actor("cycles")
            cycle2 = cast.get_second_actor("cycles")
            segments1 = cycle1.get_segments()
            segments2 = cycle2.get_segments()

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()

            #Message depending on who wins or if both loses
            if self._p1_win == True:
                message.set_text("Player 1 Wins!")
            elif self._p2_win == True:
                message.set_text("Player 2 Wins!")
            else:
                message.set_text("Cycles Crashed!")
            
            message.set_position(position)
            cast.add_actor("messages", message)
            
            #Loser cycles color turn to white
            if self._p1_win == True:
                for segment2 in segments2:
                    segment2.set_color(constants.WHITE)
            elif self._p2_win == True:
                for segment1 in segments1:
                    segment1.set_color(constants.WHITE)
            else:
                for segment2 in segments2:
                    segment2.set_color(constants.WHITE)
                for segment1 in segments1:
                    segment1.set_color(constants.WHITE)
                