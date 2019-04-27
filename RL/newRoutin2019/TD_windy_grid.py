import gym
import gym_gridworlds
import itertools
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
import plotting

def make_epsilon_greedy_policy(Q, epsilon, nA):
    def policy_fun(obs):
        A = np.ones(nA, dtype=float) * epsilon / nA
        best_action = np.argmax(Q[obs])
        A[best_action] += (1.0 - epsilon)
        return A
    return policy_fun

def sarsa(env, num_episodes, discount_factor=1.0 ,alpha=0.5, epsilon=0.1, exp=False):
    """
        Args:
            env: environment
            num_episodes
            discount_factor: gamma in the updated equ
            alpha: learning_rate
            epsilon: the prob of exploray
            exp: whether use Expected SARSA or not
    """
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    method = "Expected SARSAR" if exp else "SARSA"
    stats = plotting.EpisodeStats(episode_lengths=np.zeros(num_episodes),
                                  episode_rewards=np.zeros(num_episodes),
                                  methods=method)
    policy = make_epsilon_greedy_policy(Q, epsilon, env.action_space.n)


    for i_episode in tqdm(range(num_episodes)):
        state = env.reset()
        action_prob = policy(state)
        action = np.random.choice(np.arange(env.action_space.n),
                                            p=action_prob)
        for t in itertools.count():
            next_state, reward, done, _ = env.step(action)
            next_action_prob = policy(next_state)
            next_action = np.random.choice(np.arange(env.action_space.n),
                                           p=next_action_prob)
            stats.episode_rewards[i_episode] += reward
            stats.episode_lengths[i_episode] = t
            if exp:
                # use expected sarsa!
                td_target = reward + discount_factor * np.dot(Q[next_state], next_action_prob)
                td_error = td_target - Q[state][action]
                Q[state][action] += alpha * td_error
            else:
                td_target = reward + discount_factor*Q[next_state][next_action]
                td_error = td_target - Q[state][action]
                Q[state][action] += alpha * td_error

            if done:
                break
            action = next_action
            state = next_state
    return Q, stats

if __name__ == "__main__":
    env = gym.make('WindyGridworld-v0')
    Q, stats1 = sarsa(env, 1000)
    Q, stats2 = sarsa(env, 1000, exp=True)
    plotting.plot_episode_n_stats(stats1,stats2)