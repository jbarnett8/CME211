import math
import os
import sys


def print_help_text():
    """
    Prints useful help text to run the program
    :return: Nothing
    """
    print('grades_file\t:\tSpecifies the input file describing raw student' +\
          ' grades')
    print('output_file\t:\tSpecifies the file to write final grades')
    print('m\t\t:\tAn integer > 1 giving the # of homework assignments')
    print('k\t\t:\tAn integer > 0 giving the # of categories in hw')
    print('w_i\t\t:\t(Optional) floats in [0,1] specifies weight of' +
          'category i that sum to 1.0 with length k')


def import_args(args):
    """
    Takes in program arguments and cleans up
    :param args: Arguments directly from the command line
    :return: Cleaned variables
    """
    arg_list = [arg.strip() for arg in args]
    if len(arg_list) < 5:
        raise RuntimeError('Not enough input arguments')

    input_file = arg_list[1]
    out_file = arg_list[2]
    m = int(arg_list[3])
    k = int(arg_list[4])

    if len(arg_list) > 5:
        w_i = [float(w) for w in arg_list[4:]]
        if len(w_i) != k:
            raise RuntimeError('Not enough weights specified')
    else:
        w_i = [1/k for i in range(k)]

    # We run through a variety of sanity checks
    for w in w_i:
        if not ((w >= 0) and (w <= 1)):
            raise RuntimeError('One or more of the weights are not within ' + \
                'interval [0,1]')

    if not math.isclose(sum(w_i), 1):
        raise RuntimeError('The sum of the weights w_i are not equal to 1.0')

    if not os.path.isfile(input_file):
        raise RuntimeError("file {} does not exist".format(input_file))

    return input_file, out_file, m, k, w_i


def ingest_data(input_file, m, k):
    """
    Takes in the cleaned input data to store values in student dictionaries
    :param input_file: The filename of the gradebook
    :param m: The number of hw's
    :param k: The number of categories
    :return: Ingested data in the form of a student dictionary
    """
    students = dict()
    with open(input_file, 'r') as f:
        for line in f:
            data = line.split()
            s_id = data[0]
            hw_d = [float(d) for d in data[1:m*k + 1]]
            exam_d = [float(d) for d in data[-2:]]
            # Check if the student already exists
            if (s_id in students.keys()):
                raise RuntimeError('Duplicate student entry in {}'.format(
                    input_file))
            # Store tuple of list of grades
            students[s_id] = (hw_d, exam_d)

    return students


def calc_grades(students, m, k, w_i):
    """
    Calculates the grades using the  weights for each hw and total exam score
    :param students: Dictionary containing student grading info
    :param m: The number of hw's
    :param k: The number of categories
    :param w_i: The weights used for each category w_k
    :return: Dictionary of students with semi-final grades
    """
    student_grades = dict()
    for s_id, grades in students.items():
        raw_hw = grades[0]
        exam = grades[1]
        # This makes a list of length w of tuples with length k
        hw = zip(*[iter(raw_hw)] * k)
        hw_grades = []
        for i, t in enumerate(hw):
            # We multpiply the cat grade by the weight and sum
            g = sum([g*w_i[j] for j, g in enumerate(t)])
            hw_grades.append((g, i))
        student_grades[s_id] = (hw_grades, 0.5*sum(exam))
    return student_grades


def calc_final(student_grades):
    """
    Caculates the final grade including the dropped score
    :param student_grades: The dictionary of semi-final grades of students
    :return: A list of students and final grades that is sorted
    """
    student_list = []
    for s_id, grades in student_grades.items():
        hw_grades = grades[0]
        dropped = min(hw_grades)
        # We add the grades, drop the lowest, then find the avg
        hw_final = sum(g for g, i in hw_grades)
        hw_final -= dropped[0]
        hw_final /= (len(hw_grades) - 1)
        final_grade = 0.5*(hw_final + grades[1])
        student_list.append((final_grade, dropped[1], s_id))
    student_list.sort(reverse=True)
    return student_list

def write_results(student_list, out_file):
    """
    Writes the results in the specified form
    :param student_list: The list from which to write
    :param out_file: The file to write to
    :return: Nothing
    """
    with open(out_file, 'w') as f:
        for g, d_i, s_id in student_list:
            f.write('{} {} {:.3f}\n'.format(s_id, d_i, g))


if __name__ == '__main__':
    try:
        in_f, out_f, m, k, w_i = import_args(sys.argv)
        students = ingest_data(in_f, m, k)
        grades = calc_grades(students, m, k, w_i)
        student_grades_list = calc_final(grades)
        write_results(student_grades_list, out_f)
    except RuntimeError as e:
        print('ERROR: {}'.format(e))
        print_help_text()
        sys.exit(2)