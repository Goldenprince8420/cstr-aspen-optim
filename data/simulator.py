import json
import numpy as np
import sobol_seq
from tqdm import tqdm


class StreamDataSimulatorAspenNewCSTR:
    def __init__(self,
                 engine,
                 generator,
                 attributes_dict,
                 num_points):
        self.engine = engine
        self.attributes = attributes_dict
        self.generator = generator
        self.num_points = num_points
        self.all_streams = None
        self.all_in_streams = None
        self.all_out_streams = None
        self.all_components = None
        self.all_blocks = None
        self.samples_path = None
        self.save_path = None

    def _create_variable_ranges(self):
        self.variable_ranges = []
        for key in self.attributes.keys():
            if key == "FEED":  # FEED
                temp_range_s01 = tuple(self.attributes[key]["TEMP"])
                self.variable_ranges.append(temp_range_s01)

                pres_range_s01 = tuple(self.attributes[key]["PRES"])
                self.variable_ranges.append(pres_range_s01)

                ethanol_range_s01 = tuple(self.attributes[key]["FLOW"]["ETHANOL"])
                self.variable_ranges.append(ethanol_range_s01)

                acac_range_s01 = tuple(self.attributes[key]["FLOW"]["AC-AC"])
                self.variable_ranges.append(acac_range_s01)

                eth_acet_range_s01 = tuple(self.attributes[key]["FLOW"]["ETH-ACET"])
                self.variable_ranges.append(eth_acet_range_s01)

                water_range_s01 = tuple(self.attributes[key]["FLOW"]["WATER"])
                self.variable_ranges.append(water_range_s01)

            if key == "CSTR":  # CSTR
                temp_range_s01 = tuple(self.attributes[key]["TEMP"])
                self.variable_ranges.append(temp_range_s01)

                pres_range_s01 = tuple(self.attributes[key]["PRES"])
                self.variable_ranges.append(pres_range_s01)

                ethanol_range_s01 = tuple(self.attributes[key]["VOL"])
                self.variable_ranges.append(ethanol_range_s01)

        self.n_features = len(self.variable_ranges)

    def _sample_points(self):
        # Generate a Sobol sequence for n_variables
        # points = sobol_seq.i4_sobol_generate(self.n_features, self.num_points)
        points = np.random.rand(self.num_points, self.n_features)
        print(points.shape)

        # Initialize an empty array to store the samples
        self.samples = np.zeros((self.num_points, self.n_features))

        # Scale and shift the Sobol points to match the specified variable ranges
        for i in range(self.n_features):
            self.samples[:, i] = self.variable_ranges[i][0] + points[:, i] * (
                    self.variable_ranges[i][1] - self.variable_ranges[i][0])

        return self.samples

    def _configure_simulation(self):
        self.simulation_collector = {
            "1": {},
        }
        self._create_variable_ranges()
        self._sample_points()

    def _run_engine(self):
        self.engine.ReInit()
        self.engine.Engine.Run2()

    def _run_simulation(self):
        self._configure_simulation()
        i = 1

        temp_path_feed = "\Data\Streams\{}\Input\TEMP\MIXED".format("FEED")
        pres_path_feed = "\Data\Streams\{}\Input\PRES\MIXED".format("FEED")
        ethanol_path_feed = "\Data\Streams\{}\Input\FLOW\MIXED\{}".format("FEED", "ETHANOL")
        acac_path_feed = "\Data\Streams\{}\Input\FLOW\MIXED\{}".format("FEED", "AC-AC")
        eth_acet_path_feed = "\Data\Streams\{}\Input\FLOW\MIXED\{}".format("FEED", "ETH-ACET")
        water_path_feed = "\Data\Streams\{}\Input\FLOW\MIXED\{}".format("FEED", "WATER")

        cstr_temp_path = "\Data\Blocks\{}\Input\TEMP".format("CSTR1")
        cstr_pres_path = "\Data\Blocks\{}\Input\PRES".format("CSTR1")
        cstr_vol_path = "\Data\Blocks\{}\Input\VOL".format("CSTR1")

        for sample in tqdm(self.samples):
            #  FEED
            self.engine.Tree.FindNode(temp_path_feed).Value = sample[0]  # Temperature Information
            self.engine.Tree.FindNode(pres_path_feed).Value = sample[1]  # Pressure Information
            self.engine.Tree.FindNode(ethanol_path_feed).Value = sample[2]  # Ethanol
            self.engine.Tree.FindNode(acac_path_feed).Value = sample[3]  # Acetic Acid
            self.engine.Tree.FindNode(eth_acet_path_feed).Value = sample[4]  # Ethyl Acetate
            self.engine.Tree.FindNode(water_path_feed).Value = sample[5]  # Water

            self.engine.Tree.FindNode(cstr_temp_path).Value = sample[6]  # CSTR Temperature
            self.engine.Tree.FindNode(cstr_pres_path).Value = sample[7]  # CSTR Pressure
            self.engine.Tree.FindNode(cstr_vol_path).Value = sample[8]  # CSTR Volume

            #  Run the system and saving the results
            self._run_engine()
            self.simulation_result = self.generator.generate(all_streams_list=self.all_streams,
                                                             all_in_streams_list=self.all_in_streams,
                                                             all_out_streams_list=self.all_out_streams,
                                                             all_components=self.all_components,
                                                             all_blocks=self.all_blocks)
            self.simulation_collector[str(i)] = self.simulation_result
            i += 1

    def save_results(self, save_path):
        self.save_path = save_path

        # Save the dictionary to a JSON file
        with open(self.save_path, 'w') as json_file:
            json.dump(self.simulation_collector, json_file, indent=4)

    def simulate(self,
                 all_streams_list,
                 all_in_streams_list,
                 all_out_streams_list,
                 all_components,
                 all_blocks,
                 samples_path):
        self.all_streams = all_streams_list
        self.all_in_streams = all_in_streams_list
        self.all_out_streams = all_out_streams_list
        self.all_components = all_components
        self.all_blocks = all_blocks
        self.samples_path = samples_path
        self._run_simulation()
        return self.simulation_collector
