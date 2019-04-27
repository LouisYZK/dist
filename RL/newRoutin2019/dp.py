import gym
import gym_gridworlds
import numpy as np


def policy_val(policy, env, GAMMA=1.0, theta=0.0001):
    V = np.zeros(env.observation_space.n)
    while True:
        delta = 0
        for s in range(env.observation_space.n):
            v = 0
            for a, action_prob in enumerate(policy[s]):
                for next_state, next_prob in enumerate(env.P[a,s]):
                    reward = env.R[a, next_state]
                    v += action_prob*next_prob*(reward + GAMMA*V[next_state])
            delta = max(delta, V[s]-v)
            V[s] = v
        if delta < theta:
            break
    return np.array(V)

def one_step_lookahead(state, V, GAMMA):
        A = np.zeros(env.action_space.n)
        for a in range(env.action_space.n):
            for next_state, prob in enumerate(env.P[a, state]):
                reward = env.R[a, next_state]
                A[a] += prob * (reward + GAMMA*V[next_state])
        return A

def policy_improvement(env, policy_eval_fun=policy_val, GAMMA=1.0):

    # 用随机策略开始
    policy = np.ones((env.observation_space.n, env.action_space.n)) / env.action_space.n

    while True:
        V = policy_eval_fun(policy, env, GAMMA)
        policy_stable = True
        for s in range(env.observation_space.n):
            chosen_a = np.argmax(policy[s])
            action_values = one_step_lookahead(s, V, GAMMA)
            best_a = np.argmax(action_values)

            # 贪心的方式更新策略
            if chosen_a != best_a:
                policy_stable = False
            policy[s] = np.eye(env.action_space.n)[best_a]

        if policy_stable:
            return policy, V

def value_iteration(env, theta=0.001, GAMMA=1.0):
    V = np.zeros(env.observation_space.n)
    while True:
        delta = 0
        for s in range(env.observation_space.n):
            A = one_step_lookahead(s, V, GAMMA)
            best_action_value = np.max(A)
            delta = max(delta, np.abs(best_action_value - V[s]))
            V[s] = best_action_value
        if delta < theta:
            break
    policy = np.zeros((env.observation_space.n, env.action_space.n))
    for s in range(env.observation_space.n):
        A = one_step_lookahead(s, V, GAMMA)
        best_action = np.argmax(A)
        policy[s, best_action] = 1.0
    return policy, V


if __name__ == '__main__':
    env = gym.make('Gridworld-v0')
    random_policy = np.ones((env.observation_space.n, env.action_space.n)) / env.action_space.n
    # print(policy_val(random_policy, env))

    print(policy_improvement(env))
    print(value_iteration(env))