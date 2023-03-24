from datetime import datetime
from influxdb.line_protocol import make_lines
import bspump
import logging

L = logging.getLogger(__name__)


class InfluxStringConvertProcessor(bspump.Processor):
    def __init__(self, app, pipeline, id=None, config=None):
        super().__init__(app, pipeline, id=None, config=None)


    def process(self, context, event):

        if "datetime_id" in event:
            influx_string_dict = [{
                "measurement": "table1",
                "tags": {
                    "site": event.get("site", float("NaN")),
                    "NRCellCU": event.get("NRCellCU", float("NaN"))
                },
                "time": event.get("timestamp"),
                "fields": {
                    "UE_Context_Setup_Success_Rate": float(event.get("UE_Context_Setup_Success_Rate",0.0)),
                    "Random_Access_Success_Rata": float(event.get("Random_Access_Success_Rata",0.0)),
                    "Avg_DL_MAC_Cell_Throughput_Mbps": float(event.get("Avg_DL_MAC_Cell_Throughput_Mbps",0.0)),
                    "Avg_DL_MAC_Cell_Throughput_consid_traff_Mbps": float(event.get("Avg_DL_MAC_Cell_Throughput_consid_traff_Mbps",0.0)),
                    "Avg_DL_MAC_Cell_Throughput_PDSCH_Mbps": float(event.get("Avg_DL_MAC_Cell_Throughput_PDSCH_Mbps",0.0)),
                    "Avg_DL_MAC_DRB_Throughput_Mbps": float(event.get("Avg_DL_MAC_DRB_Throughput_Mbps",0.0)),
                    "Avg_UL_MAC_Cell_Throughput_Mbps": float(event.get("Avg_UL_MAC_Cell_Throughput_Mbps",0.0)),
                    "Avg_UL_MAC_Cell_Throughput_consid_traff_Mbps": float(event.get("Avg_UL_MAC_Cell_Throughput_consid_traff_Mbps",0.0)),
                    "Avg_UL_MAC_Cell_Throughput_PUSCH_Mbps": float(event.get("Avg_UL_MAC_Cell_Throughput_PUSCH_Mbps",0.0)),
                    "AVG_UL_MAC_UE_Throughput": float(event.get("AVG_UL_MAC_UE_Throughput",0.0)),
                    "AVG_DL_MAC_UE_Throughput": float(event.get("AVG_DL_MAC_UE_Throughput",0.0)),
                    "DL_MAC_TRAFFIC_GB": float(event.get("DL_MAC_TRAFFIC_GB",0.0)),
                    "UL_MAC_TRAFFIC_GB": float(event.get("UL_MAC_TRAFFIC_GB",0.0)),
                    "CELL_AVAILABILITY": float(event.get("CELL_AVAILABILITY",0.0))
                }
            }]

            event = make_lines({'points': influx_string_dict})
            print(event)
            return event
        else:
            L.warning("datetime_id was not found in the event:", event)


    def get_timestamp(self, time):
        utc_time = datetime.strptime("{}".format(time), "%Y-%m-%d %H:%M:%S")
        epoch_time = int((utc_time - datetime(1970, 1, 1)).total_seconds() * 1000000000)
        return epoch_time
