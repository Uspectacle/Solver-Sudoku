import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
from time import time
from tqdm import tqdm

softmaxIteration = 1000

def open_sudoku(name = None):
    names = [f for f in listdir("savedSudoku") if isfile(join("savedSudoku", f))]
    if not len(names):
        raise ValueError('No Sudoku available.')
    if name not in names:
        name = np.random.choice(names)
    return np.load(join("savedSudoku", name), allow_pickle=True)


##### TRUE WAY OF DOING THINGS #####
# https://www.askpython.com/python/examples/sudoku-solver-in-python

M = 9

def compatible(grid, row, col, num):
    for x in range(9):
        if grid[row, x] == num:
            return False
    for x in range(9):
        if grid[x, col] == num:
            return False
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow, j + startCol] == num:
                return False
    return True

num_tread = 0
def easyWay(grid, row = 0, col = 0):
    global num_tread
    num_tread += 1
    if not num_tread % 100000:
        print(num_tread)
    if (row == M - 1 and col == M):
        return True
    if col == M:
        row += 1
        col = 0
    if grid[row, col] > 0:
        return easyWay(grid, row, col + 1)
    for num in range(1, M + 1, 1): 
        if compatible(grid, row, col, num):
            grid[row, col] = num
            if easyWay(grid, row, col + 1):
                return True
        grid[row, col] = 0
    return False
 
##### TRUE WAY OF DOING THINGS ##### 


def get_solution(sudoku):
    out = np.copy(sudoku)
    if easyWay(out):
        return out
    else:
        print("ERROR: No solution foud the easy way")
        return sudoku



def build_prob(sudoku):
    prob = np.ones(sudoku.shape + (9,)) * 1/9
    for d in range(1, 9+1):
        prob[sudoku == d] = np.zeros(9)
        prob[sudoku == d, d-1] = 1.
    return prob



def show(prob):
    show = []
    for rowidx in range(prob.shape[0]):
        show.append(prob[rowidx, :, :3])
        show.append(prob[rowidx, :, 3:6])
        show.append(prob[rowidx, :, 6:])
    show = np.array(show).reshape(len(show), -1)
    im = plt.imshow(show, cmap='hot', interpolation='none', vmin=0, vmax=1, aspect='equal')
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, 9*3, 3*3))
    ax.set_yticks(np.arange(-.5, 9*3, 3*3))

    # Minor ticks
    ax.set_xticks(np.arange(-.5, 9*3, 1*3), minor=True)
    ax.set_yticks(np.arange(-.5, 9*3, 1*3), minor=True)

    # Gridlines based on minor ticks
    ax.grid(which='minor', color='w', linestyle='-', linewidth=1)
    ax.grid(which='major', color='w', linestyle='-', linewidth=3)

    plt.xticks(color='w')
    plt.yticks(color='w')

    plt.savefig('result.png')
    plt.close()
    return


def normalize_row(prob):
    prob /= np.sum(prob, axis=0, keepdims=True)
    return prob
    
def normalize_col(prob):
    prob /= np.sum(prob, axis=1, keepdims=True)
    return prob

def normalize_box(prob):
    sum_box = np.empty_like(prob)
    for rowidx in range(9):
        rowbox = (rowidx//3)*3
        for colidx in range(9):
            colbox = (colidx//3)*3
            box = prob[rowbox:rowbox+3, colbox:colbox+3]
            sum_box[rowidx, colidx] = np.sum(box, axis=(0, 1))
    prob /= sum_box
    return prob

def normalize_cell(prob):
    prob /= np.sum(prob, axis=2, keepdims=True)
    return prob

def normalize_cycle(prob):
    prob = normalize_row(prob)
    prob = normalize_cell(prob)
    prob = normalize_col(prob)
    prob = normalize_cell(prob)
    prob = normalize_box(prob)
    prob = normalize_cell(prob)
    return prob



def is_solved(sudoku):
    for idx in range(9):
        for digit in range(1, 9+1):
            if digit not in sudoku[idx, :]:
                return False
            if digit not in sudoku[:, idx]:
                return False
            row = (idx // 3) * 3
            col = (idx % 3) * 3
            if digit not in sudoku[row : row + 3 , col : col + 3]:
                return False
    return True



def entropy(prob):
    return np.mean(np.log2(prob[prob>0])*prob[prob>0])

def score(prob, solution):
    true_prob = build_prob(solution)
    score_matrix = (prob-true_prob)**2
    return 1 - np.mean(score_matrix[solution > 0])



def fill_max(prob):
    return build_prob(np.argmax(prob, axis=2)+1)



def progress(lists, names):
    fig, axs = plt.subplots(len(lists), figsize=[12, 2*len(lists)])
    for idxdata, datas in enumerate(lists):
        axs[idxdata].plot(np.abs(datas), 'b')
        # axs[idxdata].plot(datas, 'lavender')
        axs[idxdata].set_title(names[idxdata], size=7)
        axs[idxdata].get_xaxis().set_visible(False)
        axs[idxdata].set_yscale('log')

        # axs[idxdata].set_yscale(size = 7)
    axs[-1].get_xaxis().set_visible(True)
    plt.savefig('progress.png')
    plt.close()
    return



def main():
    sudoku = open_sudoku()
    print('Sudoku opened')
    print(sudoku)

    startTime = time()
    solution = get_solution(sudoku)
    print(f'Solution computed in {time()-startTime:.2e} s')
    print(solution)

    prob = build_prob(sudoku)
    print('Probability initialized')

    entropy_list = []
    score_list = []
    score_fill_list = []
    entropy_gain_list = []
    score_gain_list = []
    score_fill_gain_list = []

    startTime = time()
    for n in tqdm(range(10**7)):
        prob = normalize_cycle(prob)
        if not n % softmaxIteration:
            prob = np.exp(prob)-1 # softmax
            prob = normalize_cell(prob)
        entropy_list.append(entropy(prob))
        score_list.append(score(prob, solution))
        score_fill_list.append(score(fill_max(prob), solution))
        entropy_gain_list.append(entropy_list[n-1]-entropy_list[n])
        score_gain_list.append(score_list[n-1]-score_list[n])
        score_fill_gain_list.append(score_fill_list[n-1]-score_fill_list[n])
        if not n % 100:
            progress([entropy_list, entropy_gain_list, score_list, score_gain_list, score_fill_list, score_fill_gain_list],
                ['Entropy', 'Entropy per step', 'Score', 'Score per step', 'Score fill', 'Score fill per step'])
            show(prob)
        if is_solved(np.argmax(prob, axis=2)+1):
            print(f"Solved in {n} steps, in {time()-startTime:.2e} s !!!")
            break
    progress([entropy_list, entropy_gain_list, score_list, score_gain_list, score_fill_list, score_fill_gain_list],
            ['Entropy', 'Entropy per step', 'Score', 'Score per step', 'Score fill', 'Score fill per step'])
    show(prob)
    print('proposition:')
    print(np.argmax(prob, axis=2)+1)
    print('error ?')
    print(np.argmax(prob, axis=2)+1-solution)
    is_solved(fill_max(prob))
    return

if __name__ == "__main__":
    main()