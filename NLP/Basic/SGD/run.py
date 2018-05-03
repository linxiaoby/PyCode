from model import *
import argparse
from sklearn import metrics
if __name__ == '__main__':
    # command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", default='mnist', type=str)        # dataset type
    parser.add_argument("-m", default='adagrad', type=str)      # train method type
    parser.add_argument("-e", default=10, type=int)     # max epochs
    parser.add_argument("-b", default=100, type=int)    # batch size
    parser.add_argument("-a", default=0.01, type=float) # learning rate
    parser.add_argument("-p", default=0.1, type=float)  # norm penalty
    args = parser.parse_args()
    DATA_TYPE = args.c                                  #dataset type
    METHOD = args.m                                     # train method type
    BATCH_SIZE = args.b                                 # batch size
    ALPHA = args.a                                      # learning rate
    MAX_EPOCHS = args.e                                 # max epochs
    LMDA = args.p                                       # norm weight

    logger.info("dataset is %s, method is %s, max epoch is %d, batch_size is %d, learning rate is %f, penalty is %f"
                % (DATA_TYPE, METHOD, MAX_EPOCHS, BATCH_SIZE, ALPHA, LMDA))

    if DATA_TYPE == 'mnist' or DATA_TYPE == 'MNIST':                                  #MNIST
        # prepare data
        logger.info("prepare mnist dataset")
        X_train, X_test, y_train, y_test = data_process(1)
        logger.info(X_train.shape)
        #train
        if METHOD == 'adagrad':                                #Adagrad
            logger.info("use Adagrad method")
            W, loss, time = adagrad_train(X_train, y_train, BATCH_SIZE, ALPHA, MAX_EPOCHS, LMDA)
        else:
            logger.info("use Momentum method")
            #Momentum
            W, loss, time = momentum_train(X_train, y_train, BATCH_SIZE, ALPHA, MAX_EPOCHS, LMDA)
        logger.info("\ntraining done!")
        logger.info("loss is %f" % loss)

        #test
        logger.info("begin to test")
        y_pred = test(X_test, y_test, W)
        accuracy = metrics.accuracy_score(y_test, y_pred)
        recall = metrics.recall_score(y_test, y_pred)
        f1 = metrics.f1_score(y_test, y_pred)
        logger.info("accuracy is %f, recall is %f, f1 value is %f" % (accuracy, recall, f1))

    elif DATA_TYPE == 'covertype' or DATA_TYPE == 'Covertype':                                                #Covertype
        # prepare data
        logger.info("prepare covertype dataset")
        X_train, X_test, y_train, y_test = data_process(2)

        # train
        if METHOD == 'adagrad':                                 # Adagrad
            logger.info("use Adagrad method")
            W, loss, loss_list = adagrad_train(X_train, y_train, BATCH_SIZE, ALPHA, MAX_EPOCHS, LMDA)
        else:
            logger.info("use Momentum method")          # Momentum
            W, loss, loss_list = momentum_train(X_train, y_train, BATCH_SIZE, ALPHA, MAX_EPOCHS, LMDA)
        logger.info("\ntraining done!")
        logger.info("loss is %f" % loss)

        # test
        logger.info("begin to test")
        y_pred = test(X_test, y_test, W)
        accuracy = metrics.accuracy_score(y_test, y_pred)
        recall = metrics.recall_score(y_test, y_pred)
        f1 = metrics.f1_score(y_test, y_pred)
        logger.info("accuracy is %f, recall is %f, f1 value is %f" % (accuracy, recall, f1))
    else:
        logger.error("dataset parameter -c is wrong!")
