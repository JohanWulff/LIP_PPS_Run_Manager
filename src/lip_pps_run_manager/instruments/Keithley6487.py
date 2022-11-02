from lip_pps_run_manager.setup_manager import VISASerialDevice


class Keithley6487(VISASerialDevice):
    """
    Class for the keithley 6487 PicoAmmeter
    """

    def __init__(
        self,
        device_name: str,
        resource_string: str,
        baud_rate: int = 9600,
        data_bits: int = 8,
        flow_control: str = "none",
        parity: str = "none",
        read_termination: str = '\r',
    ):
        super().__init__(
            device_type="Keithley6487",
            device_name=device_name,
            resource_string=resource_string,
            baud_rate=baud_rate,
            data_bits=data_bits,
            flow_control=flow_control,
            parity=parity,
            read_termination=read_termination,
            stop_bits="one",
        )

        self._IDN = self._VISA_Handle.query("*IDN?")
        if "KEITHLEY INSTRUMENTS INC.,MODEL 6487" not in self._IDN:
            raise RuntimeError(f"Connected device: {self._IDN} does not seem to be a Keithley 6487 Picoammeter")

    def set_voltage(self, voltage: int):
        self._VISA_Handle.write(f"SOURCE:VOLTAGE {voltage}")

    def get_voltage(self) -> float:
        voltage = self._VISA_Handle.query_ascii_values("SOURCE:VOLTAGE?")
        return voltage

    def get_current(self) -> float:
        current = self._VISA_Handle.query_ascii_values("READ?")
        return current

    def set_current_range(self, limit: float):
        if abs(limit) > 0.0021:
            raise ValueError("Current limit has to be in the range (-21mA, 21mA).")
        self._VISA_Handle.write(f"SENSE:CURRENT:RANGE {limit}")

    def voltage_on(self):
        self._VISA_Handle.write("SOURCE:VOLTAGE:STATE ON")

    def voltage_off(self):
        self._VISA_Handle.write("SOURCE:VOLTAGE:STATE OFF")

    def configure_voltage_source(self, voltage_range: float, current_limit: float) -> bool:
        if voltage_range not in [10, 50, 500]:
            raise ValueError("Current range limit can only be set to either 10, 50 or 500")
        if current_limit not in [25e-6, 250e-6, 2.5e-3, 25e-3]:
            raise ValueError("Source current limit must be one of [25e-6, 250e-6, 2.5e-3, 25e-3].")
        if current_limit == 25e-3 and voltage_range != 10:
            raise ValueError("Cannot set current limit to 25mA if voltage range limit is not 10V")
        self._VISA_Handle.write(f"SOURCE:VOLTAGE:RANGE {voltage_range}")
        self._VISA_Handle.write(f"SOURCE:VOLTAGE:ILIMIT {current_limit}")

    def safe_shutdown(self):
        pass
