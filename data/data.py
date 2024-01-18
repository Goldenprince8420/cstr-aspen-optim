class StreamDataGeneratorAspenCSTR:
    def __init__(self, system):
        self.aspen = system.aspen
        self.all_streams = None
        self.all_in_streams = None
        self.all_out_streams = None
        self.all_components = None
        self.all_blocks = None
        self.all_paths = []
        self.stream_dict = {}
        self.ATMOS_TEMP = 25
        self.ATMOS_PRES = 1.033
        self.DEFAULT_VOL = 150

    def _get_flow_data(self):
        self.stream_dict = {}
        for stream in self.all_streams:
            self.stream_dict[stream] = {}
            self.stream_dict[stream]["TEMP"] = 0
            self.stream_dict[stream]["PRES"] = 0
            self.stream_dict[stream]["FLOW"] = {}
            for component in self.all_components:
                self.stream_dict[stream]["FLOW"][component] = 0

        for stream in self.all_in_streams:
            # Temperature data
            temperature_path = "\Data\Streams\{}\Input\TEMP\MIXED".format(stream)
            stream_temp_value = self.aspen.Tree.FindNode(temperature_path).Value
            if stream_temp_value is not None:
                self.stream_dict[stream]["TEMP"] = stream_temp_value
            else:
                self.stream_dict[stream]["TEMP"] = self.ATMOS_TEMP

            # Pressure Data
            pressure_path = "\Data\Streams\{}\Input\PRES\MIXED".format(stream)
            stream_pres_value = self.aspen.Tree.FindNode(pressure_path).Value
            if stream_temp_value is not None:
                self.stream_dict[stream]["PRES"] = stream_pres_value
            else:
                self.stream_dict[stream]["PRES"] = self.ATMOS_PRES

            # Flow data
            for component in self.all_components:
                component_flow_path = "\Data\Streams\{}\Input\FLOW\MIXED\{}".format(stream, component)
                component_flow_value = self.aspen.Tree.FindNode(component_flow_path).Value
                if component_flow_value is not None:
                    self.stream_dict[stream]["FLOW"][component] = component_flow_value

        for stream in self.all_out_streams:
            # Temperature data
            temperature_path = "\Data\Streams\{}\Output\TEMP_OUT\MIXED".format(stream)
            stream_temp_value = self.aspen.Tree.FindNode(temperature_path).Value
            if stream_temp_value is not None:
                self.stream_dict[stream]["TEMP"] = stream_temp_value
            else:
                self.stream_dict[stream]["TEMP"] = self.ATMOS_TEMP

            # Pressure Data
            pressure_path = "\Data\Streams\{}\Output\PRES_OUT\MIXED".format(stream)
            stream_pres_value = self.aspen.Tree.FindNode(pressure_path).Value
            if stream_temp_value is not None:
                self.stream_dict[stream]["PRES"] = stream_pres_value
            else:
                self.stream_dict[stream]["PRES"] = self.ATMOS_PRES

            # Flow data
            for component in self.all_components:
                component_flow_path = "\Data\Streams\{}\Output\MOLEFLOW\MIXED\{}".format(stream, component)
                component_flow_value = self.aspen.Tree.FindNode(component_flow_path).Value
                if component_flow_value is not None:
                    self.stream_dict[stream]["FLOW"][component] = component_flow_value

        for block in self.all_blocks:
            self.stream_dict[block] = {}
            # Temperature data
            temperature_path = "\Data\Blocks\{}\Input\TEMP".format(block)
            cstr_temp_value = self.aspen.Tree.FindNode(temperature_path).Value
            if cstr_temp_value is not None:
                self.stream_dict[block]["TEMP"] = cstr_temp_value
            else:
                self.stream_dict[block]["TEMP"] = self.ATMOS_TEMP

            # Pressure Data
            pressure_path = "\Data\Blocks\{}\Input\PRES".format(block)
            cstr_pres_value = self.aspen.Tree.FindNode(pressure_path).Value
            if cstr_temp_value is not None:
                self.stream_dict[block]["PRES"] = cstr_pres_value
            else:
                self.stream_dict[block]["PRES"] = self.ATMOS_PRES

            # Pressure Data
            vol_path = "\Data\Blocks\{}\Input\VOL".format(block)
            cstr_vol_value = self.aspen.Tree.FindNode(vol_path).Value
            if cstr_vol_value is not None:
                self.stream_dict[block]["VOL"] = cstr_vol_value
            else:
                self.stream_dict[block]["VOL"] = self.DEFAULT_VOL

    def _get_stream_information(self, tree_path):
        print(self.aspen.Tree.FindNode(tree_path).Value)

    def get(self, path):
        self._get_stream_information(tree_path=path)

    def generate(self,
                 all_streams_list,
                 all_in_streams_list,
                 all_out_streams_list,
                 all_components,
                 all_blocks):
        self.all_streams = all_streams_list
        self.all_in_streams = all_in_streams_list
        self.all_out_streams = all_out_streams_list
        self.all_components = all_components
        self.all_blocks = all_blocks
        self._get_flow_data()
        return self.stream_dict
