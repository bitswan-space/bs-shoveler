from datetime import datetime
from influxdb.line_protocol import make_lines
import bspump
import logging

L = logging.getLogger(__name__)


class InfluxStringConvertProcessor(bspump.Processor):
    """
    Converts converts event to influx string. It presumes that the format of the event will stay the same
    for all incoming events because the first event is used to prepare the influx format dictionary.

    This processor requires the following configuration parameters:
    - ignore_fields - list of fields that should be ignored
    - timestamp_name - name of the field that contains timestamp
    - site_key - name of the tag that contains site name
    - cell_key - name of the tag that contains cell name
    - measurement - name of the measurement
    """

    def __init__(self, app, pipeline, id=None, config=None):
        super().__init__(app, pipeline, id=None, config=None)
        self.first_event_processed = False
        self.event_fields = []
        self.ignore_fields = self.Config["ignore_fields"]
        self.timestamp_name = self.Config["timestamp_name"]
        self.site_key = self.Config["site_key"]
        self.cell_key = self.Config["cell_key"]
        self.measurement_name = self.Config["measurement_name"]

    def process(self, context, event):
        # called only when processing the first event
        if not self.first_event_processed:
            self.event_fields = self.get_event_fields(event)
            self.first_event_processed = True

        return self.convert_to_influx_string(event)

    # returns new event in influx string format using influxdb.line_protocol.make_lines function
    def convert_to_influx_string(self, event):
        if self.timestamp_name in event:
            influx_string_dict = {
                "measurement": "{}".format(self.measurement_name),
                "tags": {
                    self.site_key: event.get(str(self.site_key)),
                    self.cell_key: event.get(str(self.cell_key)),
                },
                "time": event.get(str(self.timestamp_name)),
                "fields": {},
            }
            # add fields obtained from the first event
            for field in self.event_fields:
                # add field to fields nested dict in influx_string_dict the value is in event[field]
                if(isinstance(event.get(field),int)):
                    influx_string_dict["fields"][field] = float(event.get(field))
                else:
                    influx_string_dict["fields"][field] = event.get(field)

            influx_string_dict = [influx_string_dict]

            event = make_lines({"points": influx_string_dict})
            return event
        else:
            L.warning(
                "timestamp_name with value",
                self.timestamp_name,
                "was not found in the event:",
                event,
            )

    # returns list of fields that are in the event
    def get_event_fields(self, event):
        keys = [i for i in event.keys()]
        for field_name in self.ignore_fields:
            if field_name in keys:
                keys.remove(field_name)
        return keys

    def get_timestamp(self, time):
        utc_time = datetime.strptime("{}".format(time), "%Y-%m-%d %H:%M:%S")
        epoch_time = int(
            (utc_time - datetime(1970, 1, 1)).total_seconds() * 1000000000
        )
        return epoch_time


class MockProcessor(InfluxStringConvertProcessor):
    def __init__(self, *args, **kwargs):
        self.Config = {}
        self.first_event_processed = False
        self.event_fields = []
        self.Config["ignore_fields"] = [
            "timestamp",
            "site",
            "cell",
            "measurement",
        ]
        self.Config["timestamp_name"] = "timestamp"
        self.Config["site_key"] = "site"
        self.Config["cell_key"] = "cell"
        self.Config["measurement"] = "measurement"
        self.timestamp_name = self.Config["timestamp_name"]
        self.site_key = self.Config["site_key"]
        self.cell_key = self.Config["cell_key"]
        self.measurement_name = self.Config["measurement"]
        self.ignore_fields = self.Config["ignore_fields"]


def test_processor():
    processor = MockProcessor(None, None)

    event = {
        "timestamp": "2019-01-01 00:00:00",
        "site": "site1",
        "cell": "cell1",
        "field1": 1,
        "field2": 2,
        "field3": 3,
        "field4": 4,
        "field5": 5,
        "field6": 6,
    }

    event2 = {
        "timestamp": "2019-01-01 00:00:00",
        "site": "site1",
        "cell": "cell1",
        "field1": 32,
        "field2": 32,
        "field3": 32,
        "field4": 32,
        "field5": 32,
        "field6": 32,
    }

    output_event = processor.process(None, event)

    assert (
        output_event
        == "measurement,cell=cell1,site=site1 field1=1.0,field2=2.0,field3=3.0,field4=4.0,field5=5.0,field6=6.0 1546300800000000000\n"
    )

    output_event2 = processor.process(None, event2)

    assert (
        output_event2
        == "measurement,cell=cell1,site=site1 field1=32.0,field2=32.0,field3=32.0,field4=32.0,field5=32.0,field6=32.0 1546300800000000000\n"
    )

    # check if new fields are not addded to the output event

    event3 = {
        "timestamp": "2019-01-01 00:00:00",
        "site": "site1",
        "cell": "cell1",
        "field1": 32,
        "field2": 32,
        "field3": 32,
        "field4": 32,
        "field5": 32,
        "field6": 32,
        "field7": 32,
    }

    output_event3 = processor.process(None, event3)

    assert (
        output_event3
        == "measurement,cell=cell1,site=site1 field1=32.0,field2=32.0,field3=32.0,field4=32.0,field5=32.0,field6=32.0 1546300800000000000\n"
    )

    event4 = {
        "timestamp": "2019-01-01 00:00:00",
        "site": "site1",
        "cell": "cell1",
        "field1": 32.0,
        "field2": 32.0,
        "field3": 32.0,
        "field4": 0,
    }

    output_event4 = processor.process(None, event4)

    assert (
        output_event4
        == "measurement,cell=cell1,site=site1 field1=32.0,field2=32.0,field3=32.0,field4=0.0 1546300800000000000\n"
    )
