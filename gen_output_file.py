__author__ = 'caroca'


def gen_output_file(solution):
    with open('output1.txt', 'w') as f:
        for i in range(len(solution)):
            f.write(solution[i] + '\n')


if __name__ == "__main__":
    solution = [(0,0,1),(5,4,10),(2,3,12)]
    gen_output_file(solution)