import numpy as np
import math

maxsize = float('inf')

# Функція копіювання тимчасового рішення до остаточного рішення
def copyToFinal(curr_path):
    final_path[:N + 1] = curr_path[:]
    final_path[N] = curr_path[0]

# Функція знаходження ребра мінімальної вартості, що має кінець у вершині i
def firstMin(adj, i):
    min = maxsize
    for k in range(N):
        if adj[i][k] < min and i != k:
            min = adj[i][k]

    return min

# функція для знаходження другого ребра мінімальної вартості, що має кінець у вершині i
def secondMin(adj, i):
    first, second = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]

        elif (adj[i][j] <= second and
              adj[i][j] != first):
            second = adj[i][j]

    return second

# функція, яка приймає в якості аргументів:
# curr_bound -> нижня межа кореневого вузла
# curr_weight-> зберігає поточну вагу шляху
# level-> поточний рівень під час переміщення в дереві простору пошуку
# curr_path[] -> зберігає поточний шлях, яякий буде скопійовано до final_path[]
def TSPRec(adj, curr_bound, curr_weight,
           level, curr_path, visited):
    global final_res

    # базовий випадок – це коли ми досягли рівня N, що означає, що ми охопили всі вузли один раз
    if level == N:

        # перевірити, чи є ребро від останньої вершини на шляху назад до першої вершини
        if adj[curr_path[level - 1]][curr_path[0]] != 0:

            # curr_res зберігає загальну вагу отриманого нами рішення
            curr_res = curr_weight + adj[curr_path[level - 1]] \
                [curr_path[0]]
            if curr_res < final_res:
                copyToFinal(curr_path)
                final_res = curr_res
        return

    # для будь-якого іншого рівня повторити для всіх вершин, щоб рекурсивно побудувати дерево пошуку
    for i in range(N):

        # Розглянемо наступну вершину, якщо вона не та сама
        if (adj[curr_path[level - 1]][i] != 0 and
                visited[i] == False):
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]

            # Інакше обчислення curr_bound для рівня 2 з інших рівнів
            if level == 1:
                curr_bound -= ((firstMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)
            else:
                curr_bound -= ((secondMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)

            # curr_bound + curr_weight це фактична нижня межа для вузла, до якого ми прийшли.
            # Якщо поточна нижня межа < final_res, потрібно дослідити вузол далі
            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True

                # викликати TSPRec для наступного рівня
                TSPRec(adj, curr_bound, curr_weight,
                       level + 1, curr_path, visited)

            # Інакше нам доведеться обрізати вузол, скинувши всі зміни до curr_weight і curr_bound
            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp

            # Також скинути відвіданий масив
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True

# Функція визначення final_path
def TSP(adj):
    # Обчислення початкової нижньої межі для кореневого вузла за формулою 1/2 * (sum of first min + second min) для всіх вершин.
    # Також ініціалізуємо curr_path і масив visited
    curr_bound = 0
    curr_path = [-1] * (N + 1)
    visited = [False] * N

    # Обчислення початкової межі
    for i in range(N):
        curr_bound += (firstMin(adj, i) +
                       secondMin(adj, i))

    # Округлення нижньої межі до цілого числа
    curr_bound = math.ceil(curr_bound / 2)

    # Починаємо з вершини 1 тому перша вершина в curr_path[] це 0
    visited[0] = True
    curr_path[0] = 0

    # Викликаємо TSPRec для curr_weight, що дорівнює 0 і рівня 1
    TSPRec(adj, curr_bound, 0, 1, curr_path, visited)


adj = np.loadtxt('D:\l3-1.txt', dtype='i', delimiter=' ', skiprows=1)
print('Матриця графа:')
print(adj)

N = 6

# final_path[] зберігає кінцеве рішення (шлях комівояжера)
final_path = [None] * (N + 1)

# visited[] відстежує вже відвідані вузли на певному шляху
visited = [False] * N

# Зберігає кінцеву мінімальну вагу найкоротшого шляху
final_res = maxsize

TSP(adj)

print("\nМінімальна вага маршруту:", final_res)
print("Пройдений шлях: ", end=' ')
for i in reversed(range(N + 1)):
    print(final_path[i], end=' ')