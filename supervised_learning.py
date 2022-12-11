import matplotlib.pyplot as plt

from torch.utils.data import DataLoader
from rlcard.agents.dqn_agent import EstimatorNetwork
from dataset import *


class HumanModel:
    """
    MLP classifier for Poker actions. Utilizes the EstimatorNetwork class
    from the RLCard DQN:
    https://github.com/datamllab/rlcard/blob/master/rlcard/agents/dqn_agent.py
    """

    def __init__(self, num_actions=2, state_shape=None, mlp_layers=None):
        super(HumanModel, self).__init__()

        self.num_actions = num_actions
        self.state_shape = state_shape
        self.mlp_layers = mlp_layers

        self.model = EstimatorNetwork(num_actions,
                                      state_shape,
                                      mlp_layers)
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        print(self.device)

        trainset = PokerHandDataset('./RLPoker/dataset/train_hands.json')
        validset = PokerHandDataset('./RLPoker/dataset/valid_hands.json')
        testset = PokerHandDataset('./RLPoker/dataset/test_hands.json')

        self.train_loader = DataLoader(trainset, batch_size=64, shuffle=True)
        self.valid_loader = DataLoader(validset, batch_size=64, shuffle=True)
        self.test_loader = DataLoader(testset, batch_size=32, shuffle=True)

    def train(self):
        if self.device.type == "cuda":
            total_mem = torch.cuda.get_device_properties(0).total_memory
        else:
            total_mem = 0

        epochs = 100
        learning_rate = 0.001

        self.model.to(self.device)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        criterion = torch.nn.CrossEntropyLoss()

        # Recording the loss
        train_loss = []
        val_loss = []
        val_acc = []

        for i in range(epochs):
            running_train_loss = 0.0
            for j, data in enumerate(self.train_loader):
                x, y = data

                if self.device.type == "cuda":
                    x = x.to(self.device)
                    y = y.to(self.device)

                optimizer.zero_grad()
                output = self.model(x)
                loss = criterion(output, y)
                loss.backward()
                optimizer.step()

                if self.device.type == "cuda":
                    loss = loss.cpu()

                running_train_loss += np.mean(loss.data.numpy())

            running_train_loss /= self.train_loader.__len__()
            train_loss.append(running_train_loss)

            # validate
            running_val_loss = 0.0
            running_val_acc = 0.0
            with torch.no_grad():
                for _, data in enumerate(self.valid_loader):
                    x, y = data
                    if self.device.type == "cuda":
                        x = x.to(self.device)
                        y = y.to(self.device)
                    output = self.model(x)
                    loss = criterion(output, y)

                    if self.device.type == "cuda":
                        loss = loss.cpu()

                    running_val_loss += np.mean(loss.data.numpy())

                    for l in range(len(x)):
                        pred = torch.nn.functional.softmax(output[l], dim=0)
                        if torch.argmax(pred) == y[l]:
                            running_val_acc += 1

                running_val_acc /= len(self.valid_loader.dataset.y)
                running_val_loss /= self.valid_loader.__len__()
                if len(val_loss) != 0 and np.mean(running_val_loss) < min(val_loss):
                    torch.save(self.model.state_dict(), 'best.sav')
                val_loss.append(running_val_loss)
                val_acc.append(running_val_acc)

            # check GPU memory if necessary
            if self.device.type == "cuda":
                alloc_mem = torch.cuda.memory_allocated(0)
            else:
                alloc_mem = 0

            # print out
            print(
                f"Epoch [{i + 1}]: Training Loss: {running_train_loss} "
                f"Validation Loss: {running_val_loss} "
                f"Accuracy: {running_val_acc}" + (
                    f" Allocated/Total GPU memory: {alloc_mem}/{total_mem}"
                    if self.device.type == "cuda" else ""
                ))

        plt.subplot(2, 1, 1)
        plt.plot(train_loss, '-o')
        plt.plot(val_loss, '-o')
        plt.legend(['train', 'val'], loc='upper left')
        plt.xlabel('iteration')
        plt.ylabel('loss')

        plt.subplot(2, 1, 2)
        plt.plot(val_acc, '-o')

        plt.legend(['train', 'val'], loc='upper left')
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.show()

    def test(self):
        self.model.load_state_dict(torch.load('best'))
        self.model.eval()

        t_acc = []
        with torch.no_grad():
            # only one item in the iterator
            # Add more batches if your device couldn't handle the computation
            for _, data in enumerate(self.test_loader):
                x, y = data
                x = x.to(self.device)
                y = y.to(self.device)
                y_hat = self.model(x)

                if self.device.type == "cuda":
                    y = y.to("cpu")
                    y_hat = y_hat.to("cpu")
                acc = np.average(y.numpy() == np.argmax(y_hat.numpy(), axis=1))
                t_acc.append(acc.item())
        print(f"Test accuracy: {np.average(t_acc)}")
