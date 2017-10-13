__author__ = 'Nhuy'

"""
Compute exon accuracy: accuracy, recall, precision
Parameters: (true_file/predicted_file): string, file names of true and predicted
Returns: prints out accuracy, recall, precision rounded to 3 decimal points
"""
def exon_accuracy(true_file, predicted_file):

    # open files and save sequences
    true_seq = open(true_file, 'r').read().splitlines()
    predicted_seq = open(predicted_file, 'r').read().splitlines()

    # initialize 3 measures
    total_accuracy_num = 0
    total_recall_num = 0
    total_precision_num = 0

    total_accuracy_denom = 0
    total_recall_denom = 0
    total_precision_denom = 0

    # loop through sequences aggregating counts
    for i in range(len(true_seq)):

        # obtain the true and predicted sequence
        true = true_seq[i]
        predicted = predicted_seq[i]

        # loop through individual bases
        loop_param = range(len(true))

        # compute accuracy
        all_pos = [predicted[i] == true[i] for i in loop_param]
        total_accuracy_num += sum(all_pos)
        total_accuracy_denom += len(all_pos)

        # compute recall
        all_true_exon = [predicted[i] == true[i] for i in loop_param if true[i].isupper()]
        total_recall_num += sum(all_true_exon)
        total_recall_denom += len(all_true_exon)

        # compute precision
        all_predicted_exon = [predicted[i] == true[i] for i in loop_param if predicted[i].isupper()]
        total_precision_num += sum(all_predicted_exon)
        total_precision_denom += len(all_predicted_exon)

    # print results rounded to 3 decimal points
    accuracy = total_accuracy_num / float(total_accuracy_denom)
    recall = total_recall_num / float(total_recall_denom)
    precision = total_precision_num / float(total_precision_denom)

    print('%.3f' % round(accuracy, 3))
    print('%.3f' % round(recall, 3))
    print('%.3f' % round(precision, 3))
