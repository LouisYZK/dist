import gym
import gym_gridworlds
import itertools
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
import plotting
from TD_windy_grid import sarsa

def make_epsilon_greedy_policy(Q, epsilon, nA):
    def policy_fun(obs):
        A = np.ones(nA, dtype=float) * epsilon / nA
        best_action = np.argmax(Q[obs])
        A[best_action] += (1.0 - epsilon)
        return A
    return policy_fun


def q_learning(env, num_episodes, discount_factor=1.0, alpha=0.5, epsilon=0.1):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    stats = plotting.EpisodeStats(episode_lengths=np.zeros(num_episodes),
                                  episode_rewards=np.zeros(num_episodes),
                                  methods="q-learning")
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

            td_target = reward + discount_factor*np.max(Q[next_state])
            td_error = td_target - Q[state][action]
            Q[state][action] += alpha * td_error

            if done:
                break
            state = next_state
            action = next_action
    return Q, stats

def n_step_sarsa(env, num_episodes, discount_factor=1.0, alpha=0.5, epsilon=0.1, n=5):
    """
        args:
            n: definite the n-step
    """
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    stats = plotting.EpisodeStats(episode_lengths=np.zeros(num_episodes),
                                  episode_rewards=np.zeros(num_episodes),
                                  methods="n_step_sarsa")
    policy = make_epsilon_greedy_policy(Q, epsilon, env.action_space.n)

    for i_episode in tqdm(range(num_episodes)):
        state = env.reset()
        action_prob = policy(state)
        action = np.random.choice(np.arange(env.action_space.n),
                                            p=action_prob)

        state_store = []
        action_store = []
        reward_store = []
        T = 100000
        for t in itertools.count():
            if t < T:
                next_state, reward, done, _ = env.step(action)
                state_store.append(next_state)
                reward_store.append(reward)
                stats.episode_rewards[i_episode] += reward
                stats.episode_lengths[i_episode] = t
                if done:
                    T = t + 1
                    action_store.append(action)
                else:
                    next_action_prob = policy(next_state)
                    next_action = np.random.choice(np.arange(env.action_space.n),
                                                   p=next_action_prob)
                    action_store.append(next_action)

                    state = next_state
                    action = next_action
            tao = t - n + 1
            if tao >= 0:
                G = 1.0
                for i in range(tao+1, min(tao+n, T)):
                    G += (discount_factor ** (i-tao-1))*reward_store[i]
                if tao + n < T:
                    G += (discount_factor ** n) * Q[state_store[tao+n-1]][action_store[tao+n-1]]
                Q[state_store[tao]][action_store[tao]] += alpha*(G - Q[state_store[tao]][action_store[tao]])
            if tao == T - 1:
                break
    return Q, stats




if __name__ == "__main__":
    env = gym.make('Cliff-v0')
    Q, stats = q_learning(env, 100)
    Q, stats1 = sarsa(env, 100)
    # Q, stats2 = sarsa(env, 1000, exp=True)
    # plotting.plot_episode_n_stats(stats, stats1, stats2)
    Q, stats3 = n_step_sarsa(env, 100, n=50)
    plotting.plot_episode_n_stats(stats3, stats1, stats)