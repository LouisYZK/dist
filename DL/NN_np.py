import numpy as np
from tqdm import tqdm

mnist = np.load('mnist_scaled.npz')
X_train, y_train, X_test, y_test = [mnist[f] for f in ['X_train', 'y_train', 
                                    'X_test', 'y_test']]
del mnist


class NeuralNetMLP():
    def __init__(self,
                 n_hidden=30,
                 l2=0,
                 epochs=100,
                 eta=0.001,
                 shuffle=True,
                 minibatch_size=10,
                 seed=None):
        self.n_hidden = n_hidden
        self.l2 = l2
        self.epochs = epochs
        self.learning_rate = eta
        self.shuffle = shuffle
        self.minibatch_size = minibatch_size
    
    def _one_hot(self, y, n_class):
        one_hot = np.zeros((n_class, y.shape[0]))
        for ind, val in enumerate(y):
            one_hot[val, ind] = 1
        return one_hot.T
    
    def _sigmod(self, z):
        return 1. / (1. + np.exp(- np.clip(z, -250, 250)))

    def _forward(self, X):
        z_h = np.dot(X, self.w_h) + self.b_h
        a_h = self._sigmod(z_h)
        z_out = np.dot(a_h, self.w_out) + self.b_out
        a_out = self._sigmod(z_out)
        return z_h, a_h, z_out, a_out

    def _compute_cost(self, y_enc, output):
        L2_term = (self.l2 * (np.sum(self.w_h ** 2.) +
                   np.sum(self.w_out ** 2.)))

        term1 = -y_enc * (np.log(output))
        term2 = (1. - y_enc) * np.log(1. - output)
        cost = np.sum(term1 - term2) + L2_term
        return cost

    def predict(self, X):
        _, _, z_out, _ = self._forward(X)
        y_pred = np.argmax(z_out, axis=1)
        return y_pred

    def fit(self, X_train, y_train, X_valid, y_valid):
        n_output = np.unique(y_train).shape[0]
        n_features = X_train.shape[1]
        
        self.w_h = np.random.normal(loc=0.0, scale=0.1,
                                    size=(n_features, self.n_hidden))
        self.b_h = np.zeros(self.n_hidden)

        self.w_out = np.random.normal(loc=0.0, scale=0.1,
                                      size=(self.n_hidden, n_output))
        self.b_out = np.zeros(n_output)

        self.eval_ = {'cost':[], 'valid_acc':[], 'train_acc': []}

        y_train_enc = self._one_hot(y_train, n_output)

        for i_epoch in tqdm(range(self.epochs)):
            inds = np.arange(X_train.shape[1])

            if self.shuffle:
                np.random.shuffle(inds)
            
            start_id = 0
            while start_id < inds.shape[0]:
                batch_inds = inds[start_id: start_id + self.minibatch_size]
                z_h, a_h, z_o, a_o = self._forward(X_train[batch_inds])

                # sigma_out:[n_samples, n_out]
                sigma_out = a_o - y_train_enc[batch_inds]
                # [n_hidden, n_out] --> [n_hidden, n_sample] dot [n_sample, n_out]
                grad_w_out = np.dot(a_h.T, sigma_out)
                grad_b_out = np.sum(sigma_out, axis=0)
                delta_w_out = (grad_w_out + self.l2 * self.w_out)
                delta_b_out = grad_b_out
                self.w_out -= self.learning_rate * delta_w_out
                self.b_out -= self.learning_rate * delta_b_out

                # sigma_h:[n_samples, n_hidden]
                sigma_h = np.dot(sigma_out, self.w_out.T) * a_h * (1 - a_h)
                # [n_features, n_hidden] --> [n_features, n_samples] dot [n_samples, n_hidden]
                grad_w_h = np.dot(X_train[batch_inds].T, sigma_h)
                grad_b_h = np.sum(sigma_h, axis=0)
                delta_w_h = (grad_w_h + self.l2 * self.w_h)
                delta_b_h = grad_b_h
                self.w_h -= self.learning_rate * delta_w_h
                self.b_h -= self.learning_rate * delta_b_h

                start_id += self.minibatch_size

            z_h, a_h, z_out, a_out = self._forward(X_train)
            
            cost = self._compute_cost(y_enc=y_train_enc,
                                      output=a_out)

            y_train_pred = self.predict(X_train)
            y_valid_pred = self.predict(X_valid)

            train_acc = ((np.sum(y_train == y_train_pred)).astype(np.float) /
                         X_train.shape[0])
            valid_acc = ((np.sum(y_valid == y_valid_pred)).astype(np.float) /
                         X_valid.shape[0])

            self.eval_['cost'].append(cost)
            self.eval_['train_acc'].append(train_acc)
            self.eval_['valid_acc'].append(valid_acc)

            print(f'epoch:{i_epoch}, train_acc:{train_acc}, val_acc:{valid_acc}...')

n_epochs = 200

from concurrent.futures import ThreadPoolExecutor
lr = [0.001, 0.005, 0.0001, 0.0005]
def train_with_lr(lr):
    nn = NeuralNetMLP(n_hidden=100, 
                      l2=0.01, 
                      epochs=n_epochs, 
                      eta=lr,
                      minibatch_size=100, 
                      shuffle=True,
                      seed=1)
    nn.fit(X_train=X_train[:55000], 
           y_train=y_train[:55000],
           X_valid=X_train[55000:],
           y_valid=y_train[55000:])
    y_test_pred = nn.predict(X_test)
    acc = (np.sum(y_test == y_test_pred)
                .astype(np.float) / X_test.shape[0])

    print('learning_rate:', lr, 'Test accuracy: %.2f%%' % (acc * 100))
    return nn.eval_, acc

import matplotlib.pyplot as plt
plt.style.use('ggplot')
with ThreadPoolExecutor(max_workers=4) as e:
    for res, acc in e.map(train_with_lr, lr):
        plt.plot(range(n_epochs), res['cost'], label=f'lr:{lr},acc:{acc}')
        plt.ylabel('Cost')
        plt.xlabel('Epochs')
    plt.savefig('./images/res.png', dpi=300)
    plt.show()




# plt.plot(range(nn.epochs), nn.eval_['train_acc'], 
#          label='training')
# plt.plot(range(nn.epochs), nn.eval_['valid_acc'], 
#          label='validation', linestyle='--')
# plt.ylabel('Accuracy')
# plt.xlabel('Epochs')
# plt.legend()
# #plt.savefig('images/12_08.png', dpi=300)
# plt.show()
