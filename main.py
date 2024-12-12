

from learningAgent import LearningAgent
import matplotlib.pyplot as plt
import torch

def main():
    try:


        agent = LearningAgent(episodes=300,
                              size=6,
                              type='triangle',  # 'diamond' or 'triangle'
                              empty_cell_pos=[],  # list of tuples: (x,y)
                              episode_display=[5],  # list of episodes to be displayed
                              display_frequency=0.4,  # number of seconds between frames
                              critic_type='table',  # 'table' or 'ann'
                              nn_layers=[10, 50, 30, 10],
                              greediness=0.6,
                              learning_rate=0.1,
                              discount_rate=0.95,
                              decay_rate=0.95
                              )


        """
        agent = LearningAgent(episodes=200,
                              size=5,
                              type='triangle',  # 'diamond' or 'triangle'
                              empty_cell_pos=[],  # list of tuples: (x,y)
                              episode_display=[],  # list of episodes to be displayed
                              display_frequency=0.4,  # number of seconds between frames
                              critic_type='ant',  # 'table' or 'ann'
                              nn_layers=[7,3,2],
                              greediness=0.6,
                              learning_rate=0.01,
                              discount_rate=0.95,
                              decay_rate=0.95
                              )
        """

        """
        agent = LearningAgent(episodes=200,
                              size=4,
                              type='diamond',  # 'diamond' or 'triangle'
                              empty_cell_pos=[],  # list of tuples: (x,y)
                              episode_display=[],  # list of episodes to be displayed
                              display_frequency=0.4,  # number of seconds between frames
                              critic_type='table',  # 'table' or 'ann'
                              nn_layers=[7, 3, 2],
                              greediness=0.6,
                              learning_rate=0.01,
                              discount_rate=0.95,
                              decay_rate=0.95
                              )

        """
        """
        agent = LearningAgent(episodes=25,
                              size=8,
                              type='triangle',  # 'diamond' or 'triangle'
                              empty_cell_pos=[(0,0),(1,0),(2,0)],  # list of tuples: (x,y)
                              episode_display=[],  # list of episodes to be displayed
                              display_frequency=0.4,  # number of seconds between frames
                              critic_type='ant',  # 'table' or 'ann'
                              nn_layers=[25, 15],
                              greediness=0.6,
                              learning_rate=0.01,
                              discount_rate=0.95,
                              decay_rate=0.95
                              )
        """


        pegs_remaining = agent.train_model()
        #print(pegs_remaining)

        # plot performance of training

        plt.plot(pegs_remaining)
        plt.ylabel('Number of pegs remaining')
        plt.xlabel('Episode number')
        plt.show()


        # run the model with max greedy policy and without training
        agent.run_model()


    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()


