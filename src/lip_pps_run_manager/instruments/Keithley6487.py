from lip_pps_run_manager.setup_manager import VISADevice


class Keithley6487(VISADevice):
    """
    Class for the keithley 6487 PicoAmmeter
    """

    def __init__(self, device_name: str, resource_string: str):
        super().__init__(device_type="Keithley6487", device_name=device_name, resource_string=resource_string)

    def set_voltage(self, voltage: int):
        self._VISA_Handle.write(f"SOURCE:VOLTAGE {voltage}")

    def get_voltage(self) -> float:
        voltage = self._VISA_Handle.query_ascii_values("MEASURE:VOLTAGE?")
        return voltage

    def get_current(self) -> float:
        current = self._VISA_Handle.query_ascii_values("MEASURE:CURRENT?")
        return current

    def get_cv(self) -> float:
        pass

    def set_current_range(self, limit: float) -> bool:
        if limit not in [10, 50, 500]:
            raise ValueError("Current limit can only be set to either 10, 50 or 500")
        self._VISA_Handle.write(f"SOURCE:CURRENT:RANGE {limit}")
        pass

    def set_voltage_range(self, limit: float) -> bool:
        if limit not in [10, 50, 500]:
            raise ValueError("Voltage limit can only be set to either 10, 50 or 500")
        self._VISA_Handle.write(f"SOURCE:VOLTAGE:RANGE {limit}")
        pass

    def voltage_on(self) -> bool:
        pass

    def voltage_off(self) -> bool:
        pass

    def set_source_current_limit(self, limit: float) -> bool:
        pass

    def safe_shutdowm(self):
        pass
