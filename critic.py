import random

class CriticTable:
    def __init__(self, learning_rate, discount_rate, decay_rate):
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.eligibility_decay = decay_rate
        self.values = {}
        self.eligibilities = {}


    def verify_state_is_known(self, state):
        if state not in self.values.keys():
            self.values[state] = random.uniform(0, 0.2)

    def refresh_eligibility(self, state):
        # for the most recent state, eligibility is refreshed
        self.eligibilities[state] = 1

    def update_eligibility(self, state):
        # after each move in an episode, the eligibilities for a state are updated with decay
        self.eligibilities[state] = self.discount_rate * self.eligibility_decay * self.eligibilities[state]

    def set_eligibilities_zero(self):
        # resetting eligibilities before each episode
        for state in self.eligibilities:
            self.eligibilities[state] = 0

    def update_critic(self, performed_actions, td):
        # function is called for every round, in every episode

        # refresh eligibility for the most recent state
        prev_state, action = performed_actions[-1]
        self.refresh_eligibility(prev_state)

        # for every previous state, the state values and eligibilities are updated.
        for state, action in performed_actions:
            self.update_state_value(state, td)
            self.update_eligibility(state)

    def update_state_value(self, state, td):
        # the gain/penalty from TD is affecting each of the previous states, according to their eligibility
        # this is done for every state in actions performed, after each move.
        self.values[state] += self.learning_rate * td * self.eligibilities[state]

    def calculate_temporal_difference(self, reward, state, successor_state):
        # verifying that the state is known, since a new move was just made
        if (successor_state not in self.values.keys()):
            self.verify_state_is_known(successor_state)
        # calculates TD
        return reward + self.discount_rate * self.values[successor_state] - self.values[state]