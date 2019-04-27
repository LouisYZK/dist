import gym
import matplotlib.pyplot as plt
from mpl_toolkits import  mplot3d
from collections import defaultdict
import numpy as np
import math
from plotting import plot_value_function

# env = gym.make('Blackjack-v0')
"""
env.observation_space: Tuple(Discrete(32), Discrete(11), Discrete(2))
第一个是当前player的点数和，第二个是当前庄家的明牌，第三个是player是否拥有ACE(可以当做1或11)；

env.action_space: (0,1) 1表示player hit,摸牌； 0表示stop;
player stop后 庄家揭示明牌并持续抽牌到点数不大于17，之后与player的点数对比，比较出(lose, draw, win);

"""

def mc_prediction(policy, env, num_episodes, discount_factor=1.0):

    # 三个字典形成state-->value的映射
    V = defaultdict(float)
    sum_rewards = defaultdict(float)
    sum_count = defaultdict(float)

    for i_episode in range(1, num_episodes+1):
        episode = []
        state = env.reset()
        # 按每个episode的最大长度与环境交互
        for t in range(100):
            action = policy(state)
            next_state, reward, done, _ = env.step(action)
            episode.append((state, action, reward))
            if done:
                break
            state = next_state
        state_seen = set([item[0] for item in episode])
        for state in state_seen:
            index_generator = (index for index, item in enumerate(episode) if item[0]==state)
            state_firstseen_ind = next(index_generator)
            first_seen_state_episode = episode[state_firstseen_ind:]
            G = sum([item[2]*(discount_factor**i) for i, item in enumerate(first_seen_state_episode)])
            sum_rewards[state] += G
            sum_count[state] += 1.0
            V[state] = sum_rewards[state] / sum_count[state]

        if i_episode%1000 == 0:
            print(f'{i_episode}/{num_episodes}...')
    return V

def sample_policy(obs):
    """
    一个简单的测试策略
    """
    score, declare_score, ace = obs
    return 0 if score>=20 else 1

def make_epsilon_greedy_policy(Q, epsilon, nA):
    def policy_fn(obs):
        A = np.ones(nA, dtype=float) * epsilon / nA
        best_action = np.argmax(Q[obs])
        A[best_action] += (1.0 - epsilon)
        return A
    return policy_fn

def mc_control_epsilon_greedy(env, num_episodes,
                              discount_factor=1.0,
                              epsilon=0.1):
    # Q(s,a) {'state': {'action1':'value',...'action':'value'}}
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    sum_rewards = defaultdict(float)
    sum_count = defaultdict(float)

    policy = make_epsilon_greedy_policy(Q, epsilon, env.action_space.n)

    for i_episode in range(num_episodes):
        episode = []
        state = env.reset()
        for t in range(100):
            prob = policy(state)
            action = np.random.choice(np.arange(len(prob)),
                                      p=prob)
            next_state, reward, done, _ = env.step(action)
            episode.append((state, action, reward))
            if done:
                break
            state = next_state

        sa_in_episode = set([(item[0], item[1])for item in episode])

        for state, action in sa_in_episode:
            sa_pair = (state, action)
            index_generator = (ind for ind, item in enumerate(episode) if item[0]==state and item[1]==action)
            sa_first_ind = next(index_generator)
            sa_episode = episode[sa_first_ind:]

            G = sum([item[2]*(discount_factor**ind) for ind, item in enumerate(sa_episode)])
            sum_rewards[sa_pair] += G
            sum_count[sa_pair] += 1.0

            Q[state][action] = sum_rewards[sa_pair] / sum_count[sa_pair]

        if i_episode%1000 == 0:
            print(f'{i_episode}/{num_episodes}....')

    return Q, policy

def plottig(V):
    """
    绘图函数
    Input: values dict{state(score, declare_score, ace) -> value}
    Output: 2 plots contains ace usable and unusable
    """
    fig = plt.figure()
    ax = plt.axes(projection = '3d')
    data = np.hstack([np.array(list(V.keys())),
                      np.array(list(V.values())).reshape(-1,1)])
    data_ace = data[data[:,2]==1]
    data_noace = data[data[:,2]==0]
    # ax.plot_surface(data_ace[:,0], data_ace[:,1],
    #                 data_ace[:,3].reshape(-1,1), rstride=1,
    #                 cstride=1, cmap='viridis',
    #                 edgecolor='none')
    ax.scatter3D(data[:,0], data[:,1], data[:,3], c=data[:,2])
    ax.set_xlabel('player score')
    ax.set_ylabel('declare score')
    ax.set_zlabel('value')
    # plt.colorbar()
    plt.show()

def importance_sampling():
    """利用IM原理对一个已知的正态分布模型进行采样
    """
    def p(x):
    #standard normal
        mu=0
        sigma=1
        return 1/(math.pi*2)**0.5/sigma*np.exp(-(x-mu)**2/2/sigma**2)

    #uniform proposal distribution on [-4,4]
    def q(x): #uniform
        return np.array([0.125 for i in range(len(x))])

    #draw N samples that conform to q(x), and then draw M from then that approximately conform to p(x)
    N=100000
    M=1000
    x = (np.random.rand(N)-0.5)*8
    w_x = p(x)/q(x)
    w_x = w_x/sum(w_x)
    w_xc = np.cumsum(w_x) #used for uniform quantile inverse
    # resample from x with replacement with probability of w_x
    X=np.array([])
    for i in range(M):
        u = np.random.rand()
        X = np.hstack((X,x[w_xc>u][0]))

    x = np.linspace(-4,4,500)
    plt.plot(x,p(x))
    plt.hist(X,bins=100,normed=True)
    plt.title('Sampling Importance Resampling')
    plt.show()

if __name__ == '__main__':
    policy = sample_policy
    env = gym.make('Blackjack-v0')
    # V = mc_prediction(policy, env, num_episodes=80000)
    # plottig(V)
    Q, policy = mc_control_epsilon_greedy(env, num_episodes=100000, epsilon=0.1)
    V = defaultdict(float)
    for state, action in Q.items():
        action_value = np.max(action)
        V[state] = action_value
    plot_value_function(V)
    # importance_sampling()
    pass