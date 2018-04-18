from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time
import numpy as np
import tensorflow as tf

import model
from data_reader import load_data, DataReader


flags = tf.flags

# data
flags.DEFINE_string('data_dir',    'data/demo',   'data directory. Should contain train.txt/valid.txt/test.txt with input data')
flags.DEFINE_string('train_dir',   'cv',     'training directory (models and summaries are saved there periodically)')
flags.DEFINE_string('load_model',   None,    '(optional) filename of the model to load. Useful for re-starting training from a checkpoint')

# model params
flags.DEFINE_string ('model_choice',    'lstm',                         'model choice')
flags.DEFINE_string ('embedding_path',  None,                           'pretrained emebdding path')
flags.DEFINE_integer('rnn_size',        650,                            'size of LSTM internal state')
flags.DEFINE_integer('highway_layers',  2,                              'number of highway layers')
flags.DEFINE_integer('word_embed_size', 50,                             'dimensionality of word embeddings')
flags.DEFINE_string ('kernels',         '[1,2,3,4,5,6,7]',              'CNN kernel widths')
flags.DEFINE_string ('kernel_features', '[50,100,150,200,200,200,200]', 'number of features in the CNN kernel')
flags.DEFINE_integer('rnn_layers',      2,                              'number of layers in the LSTM')
flags.DEFINE_float  ('dropout',         0.5,                            'dropout. 0 = no dropout')

# optimization
flags.DEFINE_float  ('learning_rate_decay', 0.5,  'learning rate decay')
flags.DEFINE_float  ('learning_rate',       1.0,  'starting learning rate')
flags.DEFINE_float  ('decay_when',          1.0,  'decay if validation perplexity does not improve by more than this much')
flags.DEFINE_float  ('param_init',          0.05, 'initialize parameters at')
flags.DEFINE_integer('batch_size',          20,   'number of sequences to train on in parallel')
flags.DEFINE_integer('max_epochs',          25,   'number of full passes through the training data')
flags.DEFINE_float  ('max_grad_norm',       5.0,  'normalize gradients at')
flags.DEFINE_integer('max_doc_length',    15,   'max_doc_length')
flags.DEFINE_integer('max_sen_length',     50,   'maximum sentence length')

# bookkeeping
flags.DEFINE_integer('seed',           3435, 'random number generator seed')
flags.DEFINE_integer('print_every',    5,    'how often to print current loss')
flags.DEFINE_string ('EOS',            '+',  '<EOS> symbol. should be a single unused character (like +) for PTB and blank for others')

FLAGS = flags.FLAGS


def run_test(session, m, data, batch_size, num_steps):
    """Runs the model on the given data."""

    costs = 0.0
    iters = 0
    state = session.run(m.initial_state)

    for step, (x, y) in enumerate(reader.dataset_iterator(data, batch_size, num_steps)):
        cost, state = session.run([m.cost, m.final_state], {
            m.input_data: x,
            m.targets: y,
            m.initial_state: state
        })

        costs += cost
        iters += 1

    return costs / iters


def load_wordvec(embedding_path, word_vocab):
    '''loads pretrained word vectors'''

    initW = np.random.uniform(-0.25, 0.25, (word_vocab.size, FLAGS.word_embed_size))
    with open(embedding_path, "r") as f:
        for line in f:
            line = line.rstrip().split(' ')
            word, vec = line[0], line[1:]
            if word_vocab.token2index.has_key(word):
                initW[word_vocab[word]] = np.asarray([float(x) for x in vec])
    return initW


def sparse2dense(x, vocab_size):
    '''converts a sparse input to a dense representation, for computing the reconstruction loss'''

    x_dense = np.zeros([x.shape[0], x.shape[1], vocab_size], dtype=np.int32)
    for i in xrange(x.shape[0]):
        for j in xrange(x.shape[1]):
            data_idx = x[i][j]
            x_dense[i][j][data_idx] = 1
    return x_dense


def build_model(word_vocab, train):
    '''build a training or inference graph, based on the model choice'''

    my_model = None
    if train:
        pretrained_emb = None
        embedding_path = FLAGS.embedding_path
        if FLAGS.load_model is None and embedding_path != None and os.path.exists(embedding_path):
            pretrained_emb = load_wordvec(embedding_path, word_vocab)
        if FLAGS.model_choice == 'bilstm':
            my_model = model.cnn_sen_enc(
                    word_vocab_size=word_vocab.size,
                    word_embed_size=FLAGS.word_embed_size,
                    batch_size=FLAGS.batch_size,
                    num_highway_layers=FLAGS.highway_layers,
                    max_sen_length=FLAGS.max_sen_length,
                    kernels=eval(FLAGS.kernels),
                    kernel_features=eval(FLAGS.kernel_features),
                    max_doc_length=FLAGS.max_doc_length,
                    pretrained=pretrained_emb)

            my_model.update(model.bilstm_doc_enc(my_model.input_cnn,
                                           batch_size=FLAGS.batch_size,
                                           num_rnn_layers=FLAGS.rnn_layers,
                                           rnn_size=FLAGS.rnn_size,
                                           max_doc_length=FLAGS.max_doc_length,
                                           dropout=FLAGS.dropout))

            my_model.update(model.label_prediction(my_model.enc_outputs))
            my_model.update(model.self_prediction(my_model.enc_outputs, word_vocab.size))
            my_model.update(model.loss_pretrain(my_model.plogits, FLAGS.batch_size, FLAGS.max_doc_length, word_vocab.size))
            my_model.update(model.training_graph(my_model.loss * FLAGS.max_doc_length,
                    FLAGS.learning_rate, FLAGS.max_grad_norm))

        elif FLAGS.model_choice == 'lstm':
            my_model = model.cnn_sen_enc(
                    word_vocab_size=word_vocab.size,
                    word_embed_size=FLAGS.word_embed_size,
                    batch_size=FLAGS.batch_size,
                    num_highway_layers=FLAGS.highway_layers,
                    max_sen_length=FLAGS.max_sen_length,
                    kernels=eval(FLAGS.kernels),
                    kernel_features=eval(FLAGS.kernel_features),
                    max_doc_length=FLAGS.max_doc_length,
                    pretrained=pretrained_emb)

            my_model.update(model.lstm_doc_enc(my_model.input_cnn,
                                           batch_size=FLAGS.batch_size,
                                           num_rnn_layers=FLAGS.rnn_layers,
                                           rnn_size=FLAGS.rnn_size,
                                           max_doc_length=FLAGS.max_doc_length,
                                           dropout=FLAGS.dropout))

            my_model.update(model.lstm_doc_dec(my_model.input_cnn, my_model.final_enc_state,
                                           batch_size=FLAGS.batch_size,
                                           num_rnn_layers=FLAGS.rnn_layers,
                                           rnn_size=FLAGS.rnn_size,
                                           max_doc_length=FLAGS.max_doc_length,
                                           dropout=FLAGS.dropout))

            my_model.update(model.label_prediction_att(my_model.enc_outputs, my_model.dec_outputs))
            my_model.update(model.self_prediction(my_model.enc_outputs, word_vocab.size))
            my_model.update(model.loss_pretrain(my_model.plogits, FLAGS.batch_size, FLAGS.max_doc_length, word_vocab.size))

            my_model.update(model.training_graph(my_model.loss * FLAGS.max_doc_length,
                    FLAGS.learning_rate, FLAGS.max_grad_norm))

    else:
        if FLAGS.model_choice == 'bilstm':
            my_model = model.cnn_sen_enc(
                    word_vocab_size=word_vocab.size,
                    word_embed_size=FLAGS.word_embed_size,
                    batch_size=FLAGS.batch_size,
                    num_highway_layers=FLAGS.highway_layers,
                    max_sen_length=FLAGS.max_sen_length,
                    kernels=eval(FLAGS.kernels),
                    kernel_features=eval(FLAGS.kernel_features),
                    max_doc_length=FLAGS.max_doc_length)

            my_model.update(model.bilstm_doc_enc(my_model.input_cnn,
                                           batch_size=FLAGS.batch_size,
                                           num_rnn_layers=FLAGS.rnn_layers,
                                           rnn_size=FLAGS.rnn_size,
                                           max_doc_length=FLAGS.max_doc_length,
                                           dropout=FLAGS.dropout))

            my_model.update(model.self_prediction(my_model.enc_outputs, word_vocab.size))
            my_model.update(model.loss_pretrain(my_model.plogits, FLAGS.batch_size, FLAGS.max_doc_length, word_vocab.size))

        elif FLAGS.model_choice == 'lstm':
            my_model = model.cnn_sen_enc(
                    word_vocab_size=word_vocab.size,
                    word_embed_size=FLAGS.word_embed_size,
                    batch_size=FLAGS.batch_size,
                    num_highway_layers=FLAGS.highway_layers,
                    max_sen_length=FLAGS.max_sen_length,
                    kernels=eval(FLAGS.kernels),
                    kernel_features=eval(FLAGS.kernel_features),
                    max_doc_length=FLAGS.max_doc_length)

            my_model.update(model.lstm_doc_enc(my_model.input_cnn,
                                           batch_size=FLAGS.batch_size,
                                           num_rnn_layers=FLAGS.rnn_layers,
                                           rnn_size=FLAGS.rnn_size,
                                           max_doc_length=FLAGS.max_doc_length,
                                           dropout=FLAGS.dropout))

            my_model.update(model.lstm_doc_dec(my_model.input_cnn, my_model.final_enc_state,
                                           batch_size=FLAGS.batch_size,
                                           num_rnn_layers=FLAGS.rnn_layers,
                                           rnn_size=FLAGS.rnn_size,
                                           max_doc_length=FLAGS.max_doc_length,
                                           dropout=FLAGS.dropout))

            my_model.update(model.self_prediction(my_model.enc_outputs, word_vocab.size))
            my_model.update(model.loss_pretrain(my_model.plogits, FLAGS.batch_size, FLAGS.max_doc_length, word_vocab.size))
    return my_model


def main(_):
    ''' Trains model from data '''

    if not os.path.exists(FLAGS.train_dir):
        os.mkdir(FLAGS.train_dir)
        print('Created training directory', FLAGS.train_dir)

    word_vocab, word_tensors, max_doc_length, label_tensors = \
        load_data(FLAGS.data_dir, FLAGS.max_doc_length, FLAGS.max_sen_length)

    train_reader = DataReader(word_tensors['train'], label_tensors['train'],
                              FLAGS.batch_size)

    valid_reader = DataReader(word_tensors['valid'], label_tensors['valid'],
                              FLAGS.batch_size)

    test_reader = DataReader(word_tensors['test'], label_tensors['test'],
                              FLAGS.batch_size)

    print('initialized all dataset readers')

    with tf.Graph().as_default(), tf.Session() as session:

        # tensorflow seed must be inside graph
        tf.set_random_seed(FLAGS.seed)
        np.random.seed(seed=FLAGS.seed)

        ''' build training graph '''
        initializer = tf.random_uniform_initializer(-FLAGS.param_init, FLAGS.param_init)
        with tf.variable_scope("Model", initializer=initializer):
            train_model = build_model(word_vocab, train=True)

        # create saver before creating more graph nodes, so that we do not save any vars defined below
        saver = tf.train.Saver(max_to_keep=50)

        ''' build graph for validation and testing (shares parameters with the training graph!) '''
        with tf.variable_scope("Model", reuse=True):
            valid_model = build_model(word_vocab, train=False)

        if FLAGS.load_model:
            saver.restore(session, FLAGS.load_model)
            print('Loaded model from', FLAGS.load_model, 'saved at global step', train_model.global_step.eval())
        else:
            tf.global_variables_initializer().run()
            session.run(train_model.clear_word_embedding_padding)
            print('Created and initialized fresh model. Size:', model.model_size())

        summary_writer = tf.summary.FileWriter(FLAGS.train_dir, graph=session.graph)

        ''' take learning rate from CLI, not from saved graph '''
        session.run(
            tf.assign(train_model.learning_rate, FLAGS.learning_rate),
        )

        ''' training starts here '''
        best_valid_loss = None
        #rnn_state = session.run(train_model.initial_rnn_state)
        for epoch in range(FLAGS.max_epochs):

            epoch_start_time = time.time()
            avg_train_loss = 0.0
            count = 0
            for x, _ in train_reader.iter():
                y = sparse2dense(x, word_vocab.size)
                count += 1
                start_time = time.time()

                loss, _, gradient_norm, step, _ = session.run([
                    train_model.loss,
                    train_model.train_op,
                    train_model.global_norm,
                    train_model.global_step,
                    train_model.clear_word_embedding_padding
                ], {
                    train_model.input  : x,
                    train_model.targets: y,
                })

                avg_train_loss += 0.05 * (loss - avg_train_loss)

                time_elapsed = time.time() - start_time

                if count % FLAGS.print_every == 0:
                    print('%6d: %d [%5d/%5d], train_loss/perplexity = %6.8f/%6.7f secs/batch = %.4fs, grad.norm=%6.8f' % (step,
                                                            epoch, count,
                                                            train_reader.length,
                                                            loss, np.exp(loss),
                                                            time_elapsed,
                                                            gradient_norm))

            print('Epoch training time:', time.time()-epoch_start_time)

            # epoch done: time to evaluate
            avg_valid_loss = 0.0
            count = 0
            #rnn_state = session.run(valid_model.initial_rnn_state)
            for x, _ in valid_reader.iter():
                y = sparse2dense(x, word_vocab.size)
                count += 1
                start_time = time.time()

                loss = session.run(
                    valid_model.loss
                , {
                    valid_model.input  : x,
                    valid_model.targets: y,
                })

                if count % FLAGS.print_every == 0:
                    print("\t> validation loss = %6.8f, perplexity = %6.8f" % (loss, np.exp(loss)))
                avg_valid_loss += loss / valid_reader.length

            print("at the end of epoch:", epoch)
            print("train loss = %6.8f, perplexity = %6.8f" % (avg_train_loss, np.exp(avg_train_loss)))
            print("validation loss = %6.8f, perplexity = %6.8f" % (avg_valid_loss, np.exp(avg_valid_loss)))

            save_as = '%s/epoch%03d_%.4f.model' % (FLAGS.train_dir, epoch, avg_valid_loss)
            saver.save(session, save_as)
            print('Saved model', save_as)

            ''' write out summary events '''
            summary = tf.Summary(value=[
                tf.Summary.Value(tag="train_loss", simple_value=avg_train_loss),
                tf.Summary.Value(tag="valid_loss", simple_value=avg_valid_loss)
            ])
            summary_writer.add_summary(summary, step)

            ''' decide if need to decay learning rate '''
            if best_valid_loss is not None and np.exp(avg_valid_loss) > np.exp(best_valid_loss) - FLAGS.decay_when:
                print('validation perplexity did not improve enough, decay learning rate')
                current_learning_rate = session.run(train_model.learning_rate)
                print('learning rate was:', current_learning_rate)
                current_learning_rate *= FLAGS.learning_rate_decay
                if current_learning_rate < 1.e-5:
                    print('learning rate too small - stopping now')
                    break

                session.run(train_model.learning_rate.assign(current_learning_rate))
                print('new learning rate is:', current_learning_rate)
            else:
                best_valid_loss = avg_valid_loss


if __name__ == "__main__":
    tf.app.run()
