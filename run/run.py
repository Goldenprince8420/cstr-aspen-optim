import json
from system.aspenplusconnector import ASPENConnector
from data.data import StreamDataGeneratorAspenCSTR
from data.simulator import StreamDataSimulatorAspenNewCSTR
from run.utils import create_save_folders, get_save_paths


class Runner:
    def __init__(self, args):
        self.args = args

    def _extract_arguments(self):
        runner_path_arg = self.args.runner_path
        f_runner = open(runner_path_arg, "r")
        runner_config = json.load(f_runner)

        self.input_config_path = runner_config["inputs"]
        self.output_config_path = runner_config["outputs"]
        self.config_path = runner_config["configs"]
        self.attributes_path = runner_config["attributes"]

        f_inputs = open(self.input_config_path, "r")
        self.input_config = json.load(f_inputs)

        f_outputs = open(self.output_config_path, "r")
        self.output_config = json.load(f_outputs)

        f_config = open(self.config_path, "r")
        self.config = json.load(f_config)

        self.do_save = self.args.do_save

    def _connect_system(self):
        self.system = ASPENConnector(self.input_config["flowsheet_path"])
        self.system.connect()

    def _load_attributes(self):
        with open(self.attributes_path, 'r') as json_file:
            self.attributes_dict = json.load(json_file)

    def _load_data_generator(self):
        self.generator = StreamDataGeneratorAspenCSTR(system=self.system)

    def get_stream_info(self, val_path):
        self.generator.get(path=val_path)

    def generate_data(self):
        # self.system.aspen.Reinit()
        self.system.aspen.Engine.Run2()
        self.streams_data = self.generator.generate(all_streams_list=self.input_config["streams"],
                                                    all_in_streams_list=self.input_config["in_streams"],
                                                    all_out_streams_list=self.input_config["out_streams"],
                                                    all_components=self.input_config["all_components"],
                                                    all_blocks=self.input_config["all_blocks"])
        return self.streams_data

    def _define_simulator(self):
        self.simulator = StreamDataSimulatorAspenNewCSTR(engine=self.system.aspen,
                                                         generator=self.generator,
                                                         attributes_dict=self.attributes_dict,
                                                         num_points=int(self.config["num_points"]))

    def _run_simulator(self):
        self.simulator.simulate(all_streams_list=self.input_config["streams"],
                                all_in_streams_list=self.input_config["in_streams"],
                                all_out_streams_list=self.input_config["out_streams"],
                                all_components=self.input_config["all_components"],
                                all_blocks=self.input_config["all_blocks"],
                                samples_path = self.input_config["samples_file"])

    def _save_results(self):
        create_save_folders(output_path=self.output_config)
        self.save_paths = get_save_paths(output_path=self.output_config)
        self.simulator.save_results(save_path=self.save_paths["simulation_save_path"])

    def run(self):
        self._extract_arguments()
        self._connect_system()
        self._load_attributes()
        self._load_data_generator()
        self._define_simulator()
        self._run_simulator()
        if self.do_save:
            self._save_results()
        # self.system.aspen.Quit()
