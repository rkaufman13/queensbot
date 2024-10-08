import gymnasium, collections, csv
from gymnasium import error, spaces
import tqdm
from points import get_points, convert_matrix
import numpy as np
import matplotlib.pyplot as plt



class QueensEnv(gymnasium.Env):
  metadata = {'render.modes': ['human']}
  def __init__(self, length):
    super(gymnasium.Env, self).__init__()
    self.length = length
    self.game = np.zeros(shape=(length,length))
    self.action_space = spaces.Discrete(length**2,)
  def step(self, action):
    win = False
    x = int(action/self.length)
    y = action % self.length
    self.game[y,x]=1
    reward, win, lose, info = get_points(self.game, self.length)    
    return self.game,reward,win, lose, info
  def reset(self, seed=None, options=None):
    self.game = np.zeros(shape=(self.length, self.length))
    return self.game, {}
  def render(self, mode='human', close=False):
    print(self.game)
    print(" ")  

class BlackjackAgent:
    def __init__(
        self,
        learning_rate: float,
        initial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        discount_factor: float = 0.95,
    ):
        """Initialize a Reinforcement Learning agent with an empty dictionary
        of state-action values (q_values), a learning rate and an epsilon.

        Args:
            learning_rate: The learning rate
            initial_epsilon: The initial epsilon value
            epsilon_decay: The decay for epsilon
            final_epsilon: The final epsilon value
            discount_factor: The discount factor for computing the Q-value
        """
        self.q_values = collections.defaultdict(lambda: np.zeros(env.action_space.n))

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        self.training_error = []
        

    def get_action(self, obs: tuple[np.ndarray]) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability epsilon return a random action to explore the environment
        if np.random.random() < self.epsilon:
            return env.action_space.sample()

        # with probability (1 - epsilon) act greedily (exploit)
        else:
            return int(np.argmax(self.q_values[tuple(np.ndarray.flatten(obs))]))

    def update(
        self,
        obs: tuple[np.ndarray],
        action: int,
        reward: float,
        terminated: bool,
        next_obs: tuple[np.ndarray],
    ):

        """Updates the Q-value of an action."""
        future_q_value = (not terminated) * np.max(self.q_values[tuple(np.ndarray.flatten(next_obs))])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[tuple(np.ndarray.flatten(obs))][action]
        )

        self.q_values[tuple(np.ndarray.flatten(obs))][action] = (
            self.q_values[tuple(np.ndarray.flatten(obs))][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)

learning_rate = 0.01
n_episodes = 100_000
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)  # reduce the exploration over time
final_epsilon = 0.1

agent = BlackjackAgent(
    learning_rate=learning_rate,
    initial_epsilon=start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=final_epsilon,
)

env = QueensEnv(8)

wins = 0


env = gymnasium.wrappers.RecordEpisodeStatistics(env, deque_size=n_episodes)
for episode in tqdm.tqdm(range(n_episodes)):
    obs, info = env.reset(seed=None)
    done = False

    # play one episode
    while not done:
        action = agent.get_action(obs)
        next_obs, reward, terminated, truncated, info = env.step(action)

        # update the agent
        agent.update(obs, action, reward, terminated, next_obs)

        # update if the environment is done and the current obs
        done = terminated or truncated
        obs = next_obs

    agent.decay_epsilon()

rolling_length = 500
fig, axs = plt.subplots(ncols=2, figsize=(12, 5))
axs[0].set_title("Episode rewards")
# compute and assign a rolling average of the data to provide a smoother graph
reward_moving_average = (
    np.convolve(
        np.array(env.return_queue).flatten(), np.ones(rolling_length), mode="valid"
    )
    / rolling_length
)
axs[0].plot(range(len(reward_moving_average)), reward_moving_average)
axs[1].set_title("Episode lengths")
length_moving_average = (
    np.convolve(
        np.array(env.length_queue).flatten(), np.ones(rolling_length), mode="same"
    )
    / rolling_length
)
axs[1].plot(range(len(length_moving_average)), length_moving_average)
plt.tight_layout()
plt.show()