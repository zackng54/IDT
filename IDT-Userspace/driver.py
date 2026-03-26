from train import *
from infer import *
from utils import *

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

def run_infer (infer, n_infer, chkpt, timer):
    """
    Driver for running infer.

    :param infer: Infer class instance
    :param chkpt: checkpoint to be restored
    :param timer: Timer class instance
    """

    logging.info("Infer start.") 
    timer.start()
    
    infer.reset(chkpt)

    for itr in range(n_infer):
        infer.infer()

    Experience.write()
    Experience.reset()

    logging.info("Infer end.") 
    timer.end()
    timer.print()


def run_train (train, timer):
    """
    Driver for running train.

    :param train: Train class instance
    :param timer: Timer class instance
    :return: saved checkpoint file
    """

    logging.info("Train start.")

    timer.start()
    chkpt = train.train()
    
    logging.info("Train end.")
    timer.end()
    timer.print()

    return chkpt


def driver (n_iter):
    """
    Driver.

    Invoke this method to run.
    Infer and train is invoked repeatedly.

    :param n_iter: Number of iterations to be runned.
    """

    # Set demotion path
    ConfigNodes.set_demotion_path()

    # chkpt = "./pre-trained/checkpoint"
    # import os
    # # chkpt = "./pre-trained/checkpoint"
    # chkpt = "./pre-trained/checkpoint/algorithm_state"

    # # if not os.path.isfile(chkpt + ".tune_metadata"):
    # #     logging.warning("No checkpoint found, will generate one after first train pass")
    # #     # chkpt = None  # signal to skip restore on first infer
    # #     chkpt = "./pre-trained/checkpoint/algorithm_state"
    # if not os.path.isfile(chkpt + ".tune_metadata"):
    #       logging.warning("No checkpoint found, will generate one after first train pass")
    #       chkpt = None 

    Action.__init__()
    State.__init__()

    # infer = Infer(chkpt)
    # infer = Infer(chkpt if chkpt is not None else "./pre-trained/checkpoint/algorithm_state")

    train = Train()
    timer = Timer()

    logging.info("Generating initial checkpoint via pre-training...")
    chkpt = run_train(train, timer)

    #n_infer = 32
    infer = Infer(chkpt)
    n_infer = 4

    for itr in range(n_iter):
        run_infer(infer, n_infer, chkpt, timer)
        chkpt = run_train(train, timer)

    del train
    del infer


if __name__ == "__main__":
    logging.info("Driver start.\n")

    driver(n_iter=16384) # set to rung long time
    
    logging.info("Driver end.\n")
