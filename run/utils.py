import argparse
import os


def parse_args():
    print("Parsing the Arguments..")
    parser = argparse.ArgumentParser(description='Running the system')
    parser.add_argument("--do_parse", type=int, required=True)
    parser.add_argument("--runner_path", type=str)
    parser.add_argument("--do_save", type=int)
    args = parser.parse_args()
    return args


def create_save_folders(output_path):
    base_dir = output_path["base_dir"]
    date_dir = output_path["date_dir"]
    run_dir = output_path["run_dir"]
    plots_dir = output_path["plots_dir"]
    model_dir = output_path["model_dir"]
    checkpoints_dir = output_path["checkpoints_dir"]

    run_path = os.path.join(base_dir, date_dir, run_dir)
    plots_path = os.path.join(base_dir, date_dir, run_dir, plots_dir)
    model_path = os.path.join(base_dir, date_dir, run_dir, model_dir)
    checkpoints_path = os.path.join(base_dir, date_dir, run_dir, checkpoints_dir)

    if os.path.exists(run_path):
        pass
    else:
        os.makedirs(run_path)

    if os.path.exists(plots_path):
        pass
    else:
        os.makedirs(plots_path)

    if os.path.exists(model_path):
        pass
    else:
        os.makedirs(model_path)

    if os.path.exists(checkpoints_path):
        pass
    else:
        os.makedirs(checkpoints_path)


def get_save_paths(output_path):
    base_dir = output_path["base_dir"]
    date_dir = output_path["date_dir"]
    run_dir = output_path["run_dir"]
    plots_dir = output_path["plots_dir"]
    model_dir = output_path["model_dir"]
    checkpoints_dir = output_path["checkpoints_dir"]

    plots_path = os.path.join(base_dir, date_dir, run_dir, plots_dir)
    model_path = os.path.join(base_dir, date_dir, run_dir, model_dir)
    checkpoints_path = os.path.join(base_dir, date_dir, run_dir, checkpoints_dir)
    results_arr_path = os.path.join(base_dir, date_dir, run_dir, "results_array.npz")
    simulation_save_path = os.path.join(base_dir, date_dir, run_dir, output_path["simulation_save_file"])

    paths_dir = {
        "plots_path": plots_path,
        "model_path": model_path,
        "checkpoints_path": checkpoints_path,
        "result_array_save_path": results_arr_path,
        "simulation_save_path": simulation_save_path
    }
    return paths_dir
