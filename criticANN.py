import torch

class CriticANN:
    def __init__(
        self,
        learning_rate,
        decay_rate,
        discount_rate,
        nn_layers,
        input_size
    ):
        self.learning_rate = learning_rate
        self.eligibility_decay = decay_rate
        self.discount_rate = discount_rate

        self.eligibilities = {}

        self.model = self.initialize_pytorch(nn_layers, input_size)

        # uses Stochastic gradient descent as optimizer
        self.optimizer = torch.optim.SGD(self.model.parameters(), self.learning_rate, 0.85)

    # Initializes new neural network
    def initialize_pytorch(self, hidden_nn_layers, input_size):

        ## in pytorch, neural networks are constructed with the torch.nn package
        model = torch.nn.Sequential()

        layers = hidden_nn_layers.copy()
        layers.insert(0, input_size)
        layers.append(1)

        #  The input layer, combined with sigmoid activation function
        # input_size is number of in features, number of out features is equal to the next hidden layer
        model.add_module('input', torch.nn.Linear(input_size, layers[1]))
        model.add_module('sigmoid_input', torch.nn.ReLU())

        # the hidden layers
        for i, layer in enumerate(hidden_nn_layers):
            model.add_module(f'layer{i}', torch.nn.Linear(layer, layers[i+2]))
            model.add_module(f'sigmoid{i}', torch.nn.ReLU())

        # the output layer
        model.add_module('output_layer', torch.nn.Linear(1, 1))
        model.add_module('sigmoid_output', torch.nn.Sigmoid())

        return model


    def update_values(self, temporal_diff):
        for i, layer in enumerate(self.model.parameters()):
            for j, node_weights in enumerate(layer):
                node_weights = node_weights + self.learning_rate * temporal_diff
                # updates weights on all nodes in all layers

            # the optimizer iterates over all the gradient calculated by backpropagation(backward)
            # and uses the stored gradient to update state values
            self.optimizer.step()
            self.optimizer.zero_grad()


    def update_critic(self, performed_actions, temporal_diff):
        # function is called for every move in every episode

        # calculates loss
        loss = self.get_loss(temporal_diff)

        # backpropagates the error, loss, and
        # computes loss gradients with respect to the parameters in loss function
        loss.backward()

        for _ in performed_actions:
            # for all previous actions, the values are updated based on TD.
            self.update_values(temporal_diff)


    def calculate_temporal_difference(self, reward, previous_state, current_state):
        # calculated for every action in every episode
        td = reward + (self.discount_rate * self.get_state_value(current_state)) \
                    - self.get_state_value(previous_state)
        return td


    # represent loss as mean squared error of TD
    def get_loss(self, temp_diff):
        return pow(temp_diff, 2)

    def get_state_value(self, state):
        # transform state string to a tensor
        char_list = [char for char in state]
        float_list = list(map(float, char_list))
        tensor = torch.Tensor(float_list)
        # gives tensor as input to model, which returns the corresponding value
        return self.model(tensor)


    def set_eligibilities_zero(self):
        pass

    def verify_state_is_known(self, board_state):
        pass

    def update_eligibilities(self):
        pass


