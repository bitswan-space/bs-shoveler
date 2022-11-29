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
                "time": self.get_timestamp(event.get("datetime_id")),
                "fields": {
                    "period_duration": event.get("period_duration", float("NaN")),
                    "pmEndcSetupUeSucc": event.get("pmEndcSetupUeSucc", float("NaN")),
                    "pmEndcSetupUeAtt": event.get("pmEndcSetupUeAtt", float("NaN")),
                    "pmEndcRelUeNormal": event.get("pmEndcRelUeNormal", float("NaN")),
                    "pmEndcRelUeAbnormalMenb": event.get("pmEndcRelUeAbnormalMenb", float("NaN")),
                    "pmEndcRelUeAbnormalSgnb": event.get("pmEndcRelUeAbnormalSgnb", float("NaN")),
                    "pmEndcRelUeAbnormalMenbAct": event.get("pmEndcRelUeAbnormalMenbAct", float("NaN")),
                    "pmEndcRelUeAbnormalSgnbAct": event.get("pmEndcRelUeAbnormalSgnbAct", float("NaN")),
                    "pmEndcPSCellChangeSuccIntraSgnb": event.get("pmEndcPSCellChangeSuccIntraSgnb", float("NaN")),
                    "pmEndcPSCellChangeAttIntraSgnb": event.get("pmEndcPSCellChangeAttIntraSgnb", float("NaN")),
                    "pmEndcPSCellChangeSuccInterSgnb": event.get("pmEndcPSCellChangeSuccInterSgnb", float("NaN")),
                    "pmEndcPSCellChangeAttInterSgnb": event.get("pmEndcPSCellChangeAttInterSgnb", float("NaN")),
                    "pmUeCtxtSetupAtt": event.get("pmUeCtxtSetupAtt", float("NaN")),
                    "pmUeCtxtSetupSucc": event.get("pmUeCtxtSetupSucc", float("NaN")),
                    "pmRadioRaCbAttMsg2": event.get("pmRadioRaCbAttMsg2", float("NaN")),
                    "pmRadioRaCbSuccMsg3": event.get("pmRadioRaCbSuccMsg3", float("NaN")),
                    "pmMacVolDl": event.get("pmMacVolDl", float("NaN")),
                    "pmPdschSchedActivity": event.get("pmPdschSchedActivity", float("NaN")),
                    "pmPdschAvailTime": event.get("pmPdschAvailTime", float("NaN")),
                    "pmMacVolDlDrb": event.get("pmMacVolDlDrb", float("NaN")),
                    "pmMacTimeDlDrb": event.get("pmMacTimeDlDrb", float("NaN")),
                    "pmMacVolUl": event.get("pmMacVolUl", float("NaN")),
                    "pmPuschSchedActivity": event.get("pmPuschSchedActivity", float("NaN")),
                    "pmPuschAvailTime": event.get("pmPuschAvailTime", float("NaN")),
                    "pmMacVolUlResUe": event.get("pmMacVolUlResUe", float("NaN")),
                    "pmMacTimeUlResUe": event.get("pmMacTimeUlResUe", float("NaN")),
                    "pmCellDowntimeAuto": event.get("pmCellDowntimeAuto", float("NaN")),
                    "pmCellDowntimeMan": event.get("pmCellDowntimeMan", float("NaN"))
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
