from pyvisa.constants import ControlFlow
from pyvisa.constants import Parity
from pyvisa.constants import StopBits


class DeviceBase:
    """This is the base class for implementing a device for an experimental setup"""

    _type = None
    _name = None

    def __init__(self, device_name: str, device_type: str):
        self._type = device_type
        self._name = device_name

    def safe_shutdown(self):
        raise RuntimeError("The device type {} has not had its safe shutdown set...".format(self._type))


class VISASerialDevice(DeviceBase):
    """This is the base class for implementing a device for an experimental setup which communicates with the VISA interface"""

    _VISA_ResourceManager = None
    _VISA_Handle = None
    _resource_string = None

    def __init__(
        self,
        device_type: str,
        device_name: str,
        resource_string: str,
        baud_rate: int = 9600,
        data_bits: int = 8,
        flow_control: str = "none",
        parity: str = "none",
        stop_bits: str = "one",
        read_termination: str = '\r',
    ):
        super().__init__(device_name=device_name, device_type=device_type)
        self._resource_string = resource_string

        from .instruments import get_VISA_ResourceManager

        self._VISA_ResourceManager = get_VISA_ResourceManager()
        if data_bits not in (7, 8):
            raise ValueError(f"baud_rate set to {data_bits}, should be 7 or 8")

        if flow_control not in ControlFlow.__members__.keys():
            raise ValueError(f"{flow_control} not a valid argument string for {ControlFlow.__module___}")
        if parity not in Parity.__members__.keys():
            raise ValueError(f"{parity} not a valid argument string for {Parity.__module___}")
        if stop_bits not in StopBits.__members__.keys():
            raise ValueError(f"{stop_bits} not a valid argument string for {StopBits.__module___}")
        flow_control = getattr(ControlFlow, flow_control)
        parity = getattr(Parity, parity)
        stop_bits = getattr(StopBits, stop_bits)

        self._VISA_Handle = self._VISA_ResourceManager.open_resource(
            resource_string,
            flow_control=flow_control,
            parity=parity,
            stop_bits=stop_bits,
            baud_rate=baud_rate,
            read_termination=read_termination,
        )


class SetupManager:
    """This class holds details about the experimental setup (particularly useful for device configuration)"""

    _devices = {}

    def __init__(self):
        pass
