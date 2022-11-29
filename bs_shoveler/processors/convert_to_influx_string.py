from datetime import datetime
from influxdb.line_protocol import make_lines
import bspump
import logging

L = logging.getLogger(__name__)


class InfluxStringConvertProcessor(bspump.Processor):
    def __init__(self, app, pipeline, id=None, config=None):
        super().__init__(app, pipeline, id=None, config=None)
        # self.first_event_processed = 0
        # self.event_fields = []
        # self.ignore_fields = ["eutrancell", "site"]

    def process(self, context, event):
        # called only when processing the first event
        # if (not self.first_event_processed):
        #     self.event_fields = self.get_event_fields(event)
        #     self.first_event_processed = 1

        if "datetime_id" in event:
            influx_string_dict = {
                "measurement": "ran",
                "tags": {
                    "eutrancell": event.get("eutrancell", float("NaN")),
                    "NRCellCU": event.get("NRCellCU", float("NaN"))
                },
                "time": event.get("timestamp"),
                "fields": {
                    "UE_Context_Setup_Success_Rate": event.get("UE_Context_Setup_Success_Rate"),
                    "Random_Access_Success_Rata": event.get("Random_Access_Success_Rata"),
                    "Avg_DL_MAC_Cell_Throughput_Mbps": event.get("Avg_DL_MAC_Cell_Throughput_Mbps"),
                    "Avg_DL_MAC_Cell_Throughput_consid_traff_Mbps": event.get("Avg_DL_MAC_Cell_Throughput_consid_traff_Mbps"),
                    "Avg_DL_MAC_Cell_Throughput_PDSCH_Mbps": event.get("Avg_DL_MAC_Cell_Throughput_PDSCH_Mbps"),
                    "Avg_DL_MAC_DRB_Throughput_Mbps": event.get("Avg_DL_MAC_DRB_Throughput_Mbps"),
                    "Avg_UL_MAC_Cell_Throughput_Mbps": event.get("Avg_UL_MAC_Cell_Throughput_Mbps"),
                    "Avg_UL_MAC_Cell_Throughput_consid_traff_Mbps": event.get("Avg_UL_MAC_Cell_Throughput_consid_traff_Mbps"),
                    "Avg_UL_MAC_Cell_Throughput_PUSCH_Mbps": event.get("Avg_UL_MAC_Cell_Throughput_PUSCH_Mbps"),
                    "AVG_UL_MAC_UE_Throughput": event.get("AVG_UL_MAC_UE_Throughput"),
                    "AVG_DL_MAC_UE_Throughput": event.get("AVG_DL_MAC_UE_Throughput"),
                    "DL_MAC_TRAFFIC_GB": event.get("DL_MAC_TRAFFIC_GB"),
                    "UL_MAC_TRAFFIC_GB": event.get("UL_MAC_TRAFFIC_GB"),
                    "CELL_AVAILABILITY": event.get("CELL_AVAILABILITY")
                }
            }

            for field in self.event_fields:
                influx_string_dict = influx_string_dict["fields"][field] = event[field]
            influx_string_dict = [influx_string_dict]
            event = make_lines({'points': influx_string_dict})
            print(event)
            return event
        else:
            L.warning("datetime_id was not found in the event:", event)

    # returns list of fields from event
    # def get_event_fields(self, event):
    #     keys = []
    #     if (event is dict):
    #         keys = [i for i in self.event_fields.keys()]
    #         keys.remove("site")
    #         keys.remove("eutrancell")
    #     else:
    #         L.warning("in function get_events_fields something else than dict was passed as the parameters. Nothings happens")
    #     return keys

    def get_timestamp(self, time):
        utc_time = datetime.strptime("{}".format(time), "%Y-%m-%d %H:%M:%S")
        epoch_time = int((utc_time - datetime(1970, 1, 1)).total_seconds() * 1000000000)
        return epoch_time
