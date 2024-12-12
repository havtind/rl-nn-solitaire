import random


class Actor:
    def __init__(self, episodes, greediness, learning_rate, discount_rate, decay_rate):
        self.greediness = greediness
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.eligibility_decay = decay_rate

        self.policy = {}
        self.eligibilities = {}
        self.greediness_increase = self.greediness / episodes


    def verify_SAP_is_known(self, state, possible_moves):
        # for each episode, this function is called
        # if the current state is not in the SAP policy then
        if state not in self.policy.keys():
            # for every possible move
            for action in possible_moves:
                # in first iteration, the state key must be added
                if state not in self.policy.keys():
                    self.policy[state] = {}
                # in the next interations, the SAP pair can be added
                self.policy[state][action] = 0


    def update_policy(self, state, action, td):
        # the gain/penalty from TD is affecting each of the previous SAPS, according to their eligibility
        # this is done for every SAP in actions performed, after each move.
        self.policy[state][action] += self.learning_rate * td * self.eligibilities[state][action]


    def refresh_eligibility(self, state, action):
        # when an action is performed, the corresponding SAP will get "fresh" a eligibility trace
        if state not in self.eligibilities.keys():
            self.eligibilities[state] = {}
        self.eligibilities[state][action] = 1

    def update_eligibility(self, state, action):
        # after each move in an episode, the eligibilities are updated with decay
        if state not in self.eligibilities.keys():
            # because nested dict, the key, i.e. the state, must be present before adding/changing SAP eligibility
            self.eligibilities[state] = {}
        # adding/updating the SAP eligibilities
        self.eligibilities[state][action] = self.discount_rate * self.eligibility_decay * self.eligibilities[state][action]

    def set_eligibilities_zero(self):
        # for every episode, the eligibility traces are set to zero, for every SAP in policy
        for state in self.eligibilities:
            for action in state:
                self.eligibilities[state][action] = 0

    def update_actor(self, performed_actions, td):
        # function is called for every round, in every episode

        # refresh eligibility for the last SAP added
        prev_state, prev_action = performed_actions[-1]
        self.refresh_eligibility(prev_state, prev_action)

        # for every previous step, the policy is updated for the SAP
        # the eligibility decay is also updated
        for state, action in performed_actions:
            self.update_policy(state, action, td)
            self.update_eligibility(state, action)

    def get_action(self,state, legal_moves, is_training):
        # If the model is running without training and a state is not discovered
        # in the training process, then this function returns a random action among possible actions
        if (not(is_training) and state not in self.policy.keys()):
            return random.choice(legal_moves)
        # a higher greediness_rate means the agent will exploit more than exploring
        if (random.uniform(0, 1) < self.greediness):
            return self.get_max_value_action(state)
        else:
        # if not, it will return a random move among the SAPs in the policy
            return random.choice(list(self.policy[state].keys()))


    def get_max_value_action(self, state):
        # returns max action among the SAPs for the given state
        return max(self.policy[state], key=(lambda action: self.policy[state][action]))


    def increase_greediness(self, episodes):
        # increases greediness linearily towards end of game.
        self.greediness += self.greediness_increase

    def set_max_greedy(self):
        # with max greediness, the agent will only exploit current policy.
        self.greediness = 1