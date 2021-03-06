import os
import argparse
from parse_reddit_data import parse_reddit_data
from utils import pp_output, load_model_parameters
from RNN import RNN

def train(vocab_size, state_size, bptt_truncate, model_path, data_path,
         num_epochs, learning_rate, model_dir):
    # create an RNN, if possible load pre-existing model parameters
    if model_path:
        model_parameters = load_model_parameters(model_path)
        model = RNN(vocab_size, state_size, bptt_truncate, model_parameters)
    else:
        model = RNN(vocab_size, state_size, bptt_truncate)

    # construct datasets
    training_data, validation_data, test_data = \
    parse_reddit_data(vocab_size, data_path)

    # train the model
    model.sgd(training_data, num_epochs, learning_rate, validation_data,
              test_data, model_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--vocab_size', type=int, default=1000,
                      help='the size of the model\'s vocabulary')
    parser.add_argument('--state_size', type=int, default=100,
                      help='the size of the model\'s state')
    parser.add_argument('--bptt_truncate', type=int, default=3,
                      help='number of timesteps until bptt truncation')
    parser.add_argument('--model_path', type=str,
                      help='the relative path to saved model parameters')
    parser.add_argument('--data_path', type=str,
                      default='data/reddit_data/reddit-comments.csv',
                      help='the path to the training/validation/test data')
    parser.add_argument('--num_epochs', type=int, default=10,
                      help='the number of training epochs')
    parser.add_argument('--learning_rate', type=float, default=0.05,
                      help='the learning rate')
    parser.add_argument('--model_dir', type=str, default=None,
                      help='the path to a directory to save models to')
    args = parser.parse_args()
    train(args.vocab_size,
         args.state_size,
         args.bptt_truncate,
         args.model_path,
         args.data_path,
         args.num_epochs,
         args.learning_rate,
         args.model_dir)
