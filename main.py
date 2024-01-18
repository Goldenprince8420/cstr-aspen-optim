import warnings
import random

import numpy as np

from run.run import Runner
from run.utils import parse_args

warnings.filterwarnings('ignore')

# random.seed(42)
# np.random.seed(42)

if __name__ == "__main__":
    parsed = parse_args()
    runner = Runner(parsed)
    runner.run()
    # stream_path = "\Data\Streams\PROD\Output\MASSFLOW3\WATER"
    # runner.get_stream_info(val_path=stream_path)
    # streams_data = runner.generate_data()
    # print(streams_data)
