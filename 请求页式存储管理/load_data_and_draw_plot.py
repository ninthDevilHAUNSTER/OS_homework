from matplotlib import pyplot as plt
import pickle

color_map = ['r', 'b', 'y', 'g', 'darkblue', 'darkred', 'orange', 'purple', 'brown', 'pink']
alg_list = ['fifo', 'opt', 'lru', 'clock']
page_size_list = [1024, 2048, 3072, 4096, 5120, 6144, 7168, 8192]


def draw_plot(RESULT_MAT, page_size):
    index = 1
    for key, value in RESULT_MAT.items():
        X, Y = RESULT_MAT[key][0], RESULT_MAT[key][1]
        plt.plot(X, Y, label='{} alg analyze page_size {}K'.format(key, page_size // 1024), c=color_map[index - 1])
        index += 1
    plt.legend()

    plt.xlabel("4 ALG PAGE SIZE/K {}".format(page_size // 1024))
    plt.ylabel("Que ye lv")
    plt.savefig('./img/4 alg analyze with page size {}.png'.format(page_size // 1024))
    plt.show()
    print("[*] Draw {} figure Done".format(page_size))


def load_data(page_size):
    clock_dict = pickle.load(open('./data/clock-data.txt', 'rb'))
    fifo_dict = pickle.load(open('./data/fifo-data.txt', 'rb'))
    lru_dict = pickle.load(open('./data/lru-data.txt', 'rb'))
    opt_dict = pickle.load(open('./data/opt-data.txt', 'rb'))
    RESULT_MAT = {
        'clock': clock_dict[page_size],
        'fifo': fifo_dict[page_size],
        'lru': lru_dict[page_size],
        'opt': opt_dict[page_size]
    }
    draw_plot(RESULT_MAT, page_size)


if __name__ == '__main__':
    for i in page_size_list:
        load_data(i)
