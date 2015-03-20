__author__ = 'caroca'

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time


def get_file():
    script_dir = os.path.dirname(__file__)  #<-- absolute dir the script is in
    abs_file_path = os.path.dirname(os.path.abspath(__file__))
    onlyfiles = [f for f in os.listdir(abs_file_path) if os.path.isfile(os.path.join(abs_file_path, f))]
    print "Introduce the number corresponding to the desired file to perform the algorithm on it :"
    count = 1
    for i in onlyfiles:
        print count, " --> ", i
        count += 1
    findex = raw_input("\nType the number and press 'Enter' : ")
    while True:
        try:
            findex = int(findex)
            if findex in range(1,count):
                break
            else:
                print findex, "is not in among the proposed numbers. Please introduce a number within the range ",
                print "[", 1, ", ", count -1, "]"
        except:
            print findex, "is not an integer. Please introduce an integer"
        findex = raw_input("\nType the number and press 'Enter' : ")
    f = onlyfiles[findex - 1]
    return os.path.join(abs_file_path, f)


def create_image_matrix(fname):
    with open(fname) as f:
        counter = 0
        for line in f:
            if counter == 0:
                size = line.split()
                size[0], size[1] = int(size[0]), int(size[1])
                print "number of rows = ", size[0], " ,  number of columns = ", size[1]
                image_matrix = np.zeros((size[0], size[1]), dtype=int)
            else:
                for i in range(size[1]):
                    if line[i] == '.':
                        image_matrix[counter-1][i] = 0
                    else:
                        image_matrix[counter-1][i] = 1
            counter += 1
    return image_matrix


def create_empty_image_matrix(fname):
    with open(fname) as f:
        for line in f:
            size = line.split()
            size[0], size[1] = int(size[0]), int(size[1])
            new_image_matrix = np.zeros((size[0], size[1]), dtype=int)
            break
    return new_image_matrix


def paint_sq_rcs(matrix, r, c, s):
    size = 2*s + 1
    for i in [x - s for x in range(size)]:
        for j in [x - s for x in range(size)]:
            matrix[r + i][c + j] = 1
    return matrix


def paint_sq_white_rcs(matrix, r, c, s):
    size = 2*s + 1
    for i in [x - s for x in range(size)]:
        for j in [x - s for x in range(size)]:
            matrix[r + i][c + j] = 0
    return matrix


def erase_cell_rc(matrix, r, c):
    matrix[r][c] = 0
    return matrix


def gen_paintsq_rcs_string(r, c, s):
    return "PAINTSQ " + str(r) + " " + str(c) + " " + str(s)


def gen_erasecell_rc_string(r, c):
    return "ERASECELL " + str(r) + " " + str(c)


def plot_image(img):
    plt.imshow(img, cmap=cm.Greys, interpolation='none')
    plt.show()


def first_solution(matrix, maxS):
    shape = matrix.shape
    temp_matrix = np.zeros((shape[0], shape[1]), dtype=int)
    for s in range(maxS):
        size = 2*s + 1
        coords_init = [0 + s, 0 + s]
        coords = coords_init[:]
        Fmax = shape[0]/size
        Cmax = shape[1]/size
        for i in range(Fmax):
            for j in range(Cmax):
                index = [coords[0] - s, coords[0] + s, coords[1] - s, coords[1] + s]
                if s == 0:
                    blacks = matrix[coords[0], coords[1]]
                    if blacks == 1:
                        temp_matrix[coords[0], coords[1]] = size
                else:
                    blacks = sum(sum(matrix[index[0]: index[1], index[2]: index[3]]))
                    if blacks > ((size**2)/2 + 1):
                        temp_matrix[index[0]: index[1], index[2]: index[3]] = 0
                        temp_matrix[coords[0], coords[1]] = size
                coords = [coords[0], coords[1] + size]
            coords = [coords[0] + size, coords_init[1]]
    # plot_image(temp_matrix)
    return temp_matrix


def get_values_index(ls, value):
    indices = []
    while np.amax(ls) == value:
        ind = np.argmax(ls)
        indices.append(ind)
        ls[ind] = 0
    return indices


def second_solution(matrix, sMax):
    copy_matrix = matrix[:]
    sh = copy_matrix.shape
    weighed_matrix = np.zeros(sh, dtype=int)
    for s in range(sMax, sMax-1, -1):
        while True:
            blacks_matrix = second_solution_iteration(copy_matrix, s)
            max_value = int(np.amax(blacks_matrix))
            print max_value, (2*s+1)**2
            if max_value == (2*s + 1)**2:
                indices = np.where(blacks_matrix == blacks_matrix.argmax())
                print indices
                copy_matrix = paint_sq_white_rcs(copy_matrix, indices[0][0], indices[1][0], s)
                weighed_matrix[indices[0][0], indices[1][0]] = s
                print indices[0][i], indices[1][i], s
            else:
                break
    plot_image(weighed_matrix)


def second_solution_iteration(matrix, s):
    shape = matrix.shape
    # size = 2*s + 1
    coords_init = [0 + s, 0 + s]
    coords = coords_init[:]
    Fmax = shape[0]-2*s
    Cmax = shape[1]-2*s
    blacks_matrix = np.zeros(shape)  # np.zeros((shape[0] - 2*s, shape[1] - 2*s))
    for i in range(Fmax):
        for j in range(Cmax):
            index = [coords[0] - s, coords[0] + s, coords[1] - s, coords[1] + s]
            if s == 0:
                blacks = matrix[coords[0], coords[1]]
                if blacks == 1:
                    blacks_matrix[coords[0], coords[1]] = 1
            else:
                blacks_matrix[coords[0], coords[1]] = sum(sum(matrix[index[0]: index[1] + 1, index[2]: index[3] + 1]))
            coords = [coords[0], coords[1] + 1]
        coords = [coords[0] + 1, coords_init[1]]
    return blacks_matrix


def write_commands(image_matrix, temp_matrix):
    shape = image_matrix.shape
    cnt = 0
    with open('output1.txt', 'w') as f:
        for i in range(shape[0]):
            for j in range(shape[1]):
                if temp_matrix[i, j] != 0:
                    f.write(gen_paintsq_rcs_string(i, j, (temp_matrix[i, j] - 1)/2) + '\n')
                    cnt += 1
    aux_matrix = image_matrix - paint_image("output1.txt", shape)
    with open('output2.txt', 'w') as f:
        for i in range(shape[0]):
            for j in range(shape[1]):
                if aux_matrix[i, j] < 0:
                    f.write(gen_erasecell_rc_string(i, j) + '\n')
                    cnt += 1
                elif aux_matrix[i, j] > 0:
                    f.write(gen_paintsq_rcs_string(i, j, 0) + '\n')
                    cnt += 1
    with open('output1.txt', 'r') as f:
        data1 = f.read()
    with open('output2.txt', 'r') as f:
        data2 = f.read()
    with open('output.txt', 'w') as f:
        f.write(str(cnt) + '\n' + data1 + data2)
    os.remove("output1.txt")
    os.remove("output2.txt")
    print "number of commands = ", cnt


def paint_image(fname, shape):
    matrix = np.zeros(shape)
    with open(fname) as f:
        for line in f:
            my_str_list = line.split()
            if my_str_list.__len__() == 4:
                paint_sq_rcs(matrix, int(my_str_list[1]), int(my_str_list[2]), int(my_str_list[3]))
            elif my_str_list.__len__() == 3:
                erase_cell_rc(matrix, int(my_str_list[1]), int(my_str_list[2]))
    return matrix


if __name__ == "__main__":
    fname = get_file()
    image_matrix = create_image_matrix(fname)
    # plot_image(image_matrix)
    new_image_matrix = create_empty_image_matrix(fname)
    second_solution(image_matrix, 20)
    # temp_matrix = first_solution(image_matrix, 20)
    # write_commands(image_matrix, temp_matrix)
    # painted_matrix = paint_image("output.txt", image_matrix.shape)
    # f, axarr = plt.subplots(2)
    # axarr[0].imshow(image_matrix, cmap=cm.Greys, interpolation='none')
    # axarr[0].set_title('Original image')
    # axarr[1].imshow(painted_matrix, cmap=cm.Greys, interpolation='none')
    # axarr[1].set_title('Painted image')
    # plt.show()