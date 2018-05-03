if __name__ == '__main__':
    mni_mom_001 = []
    with open("0_mni_mom_0.1.txt") as f:
    # with open("mni_mom_0.01.txt") as f:
        lines = f.read().split('\n')
        for line in lines:
            if ": loss is " in line:
                loss = line.split('loss is ')[1]
                mni_mom_001.append(float(loss))
    print(mni_mom_001, len(mni_mom_001))
    mni_mom_001 = mni_mom_001[0:50]

    mni_mom_01 = []
    with open("mni_mom_0.01.txt") as f:
        lines = f.read().split('\n')
        for line in lines:
            if ": loss is " in line:
                loss = line.split('loss is ')[1]
                mni_mom_01.append(float(loss))

    mni_mom_01 = mni_mom_01[0:50]
    print(len(mni_mom_01))
    print(mni_mom_01)

    import numpy as np

    import matplotlib.pyplot as plt

    # evenly sampled time at 200ms intervals
    x = np.linspace(0, 50, 50)
    y1 = mni_mom_01
    y2 = mni_mom_001

    sub_axix = filter(lambda x: x % 200 == 0, x)
    plt.title('Loss Changes')
    plt.plot(x, y1, color='red', label='MNIST_Momentum_0.1')
    plt.plot(x, y2, color='blue', label='MNIST_Momentum_0.01')
    plt.legend()  # 显示图例

    plt.xlabel('epoches')
    plt.ylabel('loss')
    plt.show()
