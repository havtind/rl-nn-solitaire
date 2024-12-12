from pegSolitaire import PegSolitaire
from critic import CriticTable
from criticANN import CriticANN
from actor import Actor

class LearningAgent:
    def __init__(self, episodes, size, type, empty_cell_pos,
                 episode_display, display_frequency, critic_type, nn_layers,
                 greediness, learning_rate, discount_rate, decay_rate ):

        self.episodes = episodes
        self.size = size
        self.critic_type = critic_type
        if critic_type == 'ann':
            if type == 'triangle':
                input_size = self.get_triangle_number(size)
            else:
                input_size = self.get_quadratic_number(size)
            self.critic = CriticANN(learning_rate, decay_rate, discount_rate, nn_layers, input_size)
        else:
            self.critic = CriticTable(learning_rate, discount_rate, decay_rate)

        self.actor = Actor(episodes, greediness, learning_rate, discount_rate, decay_rate)

        self.shape = type
        self.episode_display = episode_display
        self.display_frequency = display_frequency
        self.empty_cell_pos = empty_cell_pos


    def initialize_game(self, visualize, game_title=""):
        # starts a new game of Peg Solitaire
        peg_game = PegSolitaire(self.size, self.shape, game_title, visualize,
                                self.empty_cell_pos, display_frequency=self.display_frequency)
        return peg_game


    def run_model(self):
        peg_game = self.initialize_game(visualize=True, game_title='Spiller...')
        state = peg_game.get_state_as_bitstring()
        possible_moves = peg_game.get_possible_moves()

        peg_game.board.print_grid()
        # for the final run, the greediness is set to max, for exploiting the policy
        self.actor.set_max_greedy()

        while len(possible_moves)>0:
            # perform a move as long
            _, new_state, possible_moves = self.make_game_choice(peg_game, state, [], possible_moves, is_training=False)
            state = new_state

        pegs_remaining = peg_game.count_filled_cells()
        if pegs_remaining == 1:
            peg_game.display.update_display('Gratulerer, du vant!', last_window=True)
        else:
            peg_game.display.update_display('Du tapte!', last_window=True)


    def train_model(self):
        pegs_remaining = []

        for episode in range(self.episodes):
            print('Episode: ', episode)

            for e in self.episode_display:
                if episode == e:
                    game_title = "Episode nr: "+str(episode)
                    peg_game = self.initialize_game(visualize=True, game_title=game_title)
            if episode not in self.episode_display:
                peg_game = self.initialize_game(visualize=False)

            possible_moves = peg_game.get_possible_moves()
            state = peg_game.get_state_as_bitstring()

            # initialize eligibbilities
            if self.critic_type == 'table':
                self.actor.set_eligibilities_zero()
            else:
                self.critic.set_eligibilities_zero()

            performed_actions = []

            while (len(possible_moves)>0):
                # check if current state and SAPS are known to critic and actor
                self.actor.verify_SAP_is_known(state, possible_moves)
                self.critic.verify_state_is_known(state)

                #get move from actor and perform the move
                reward, new_state, possible_moves = \
                    self.make_game_choice(peg_game, state, performed_actions, possible_moves, is_training=True)

                # calculates temporal differencing
                td = self.critic.calculate_temporal_difference(reward, state, new_state)

                #update actor, critic and eligibilities with TD
                self.actor.update_actor(performed_actions, td)
                self.critic.update_critic(performed_actions, td)

                #peg_game.board.print_grid()
                state = new_state

            pegs_left = peg_game.count_filled_cells()
            pegs_remaining.append(pegs_left)
            # increases greediness for each episode. More exploiting of learning and less exploring
            self.actor.increase_greediness(self.episodes)
        return pegs_remaining


    def make_game_choice(self, peg_game, state, performed_actions, possible_moves, is_training):
        # get a move from the Actor based on current state and possible moves.
        action = self.actor.get_action(state, possible_moves, is_training)

        peg_pos = action[0]
        peg_direction = action[1]

        # performs the move
        peg_game.make_move(peg_pos, peg_direction)

        # get potential reward from the new state
        reward = peg_game.get_reward()

        new_state = peg_game.get_state_as_bitstring()
        possible_moves = peg_game.get_possible_moves()
        # add the previous state and move
        performed_actions.append((state, action))

        return reward, new_state, possible_moves


    def get_triangle_number(self, n):
        for i in range (n):
             n += i
        return n

    def get_quadratic_number(self, n):
        return pow(n,2)





