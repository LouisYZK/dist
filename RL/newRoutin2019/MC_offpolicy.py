import gym
import matplotlib.pyplot as plt
from mpl_toolkits import  mplot3d
from collections import defaultdict
import numpy as np
# from MC import plottig
from util.plotting import plot_value_function
from tqdm import tqdm
def make_random_policy(nA):
    A = np.ones(nA) / nA
    def policy_fn(obs):
        return A
    return policy_fn

def make_greedy_policy(Q):
    def policy_fn(obs):
        A = np.zeros_like(Q[obs], dtype=float)
        best_action = np.argmax(Q[obs])
        A[best_action] = 1.0
        return A
    return policy_fn

def mc_control_importance_sampling(env, num_episodes, behavior_policy,
                                   discount_factor=1.0):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    C = defaultdict(lambda: np.zeros(env.action_space.n))
    target_policy = make_greedy_policy(Q)

    for i_episode in tqdm(range(num_episodes)):
        episode = []
        state = env.reset()
        for t in range(100):
            probs = behavior_policy(state)
            action = np.random.choice(np.arange(len(probs)), p=probs)
            next_state, reward, done, _ = env.step(action)
            episode.append((state, action, reward))
            if done:
                break
            state = next_state

        G = 1.0
        W = 1.0

        for state, action, reward in reversed(episode):
            G = discount_factor * G + reward
            C[state][action] += W
            Q[state][action] += (W / C[state][action]) * (G - Q[state][action])
            if action != np.argmax(target_policy(state)):
                # 这一步判断是为了更新W时不计算target_policy
                break
            W = W * 1./behavior_policy(state)[action]
        # if i_episode%100 == 0:
        #     print(f'{i_episode}/{num_episodes}.....')

    return Q, target_policy

if __name__ == "__main__":
    env = gym.make('Blackjack-v0')
    random_policy = make_random_policy(env.action_space.n)
    Q, policy = mc_control_importance_sampling(env, 50000, random_policy)

    V = defaultdict(float)
    for state, action_values in Q.items():
        best_value = np.max(action_values)
        V[state] = best_value
    # plottig(V)
    plot_value_function(V)
    pass