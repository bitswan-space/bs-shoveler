from datetime import datetime
from influxdb.line_protocol import make_lines
import bspump


class InfluxStringConvertProcessor(bspump.Processor):
    def __init__(self, app, pipeline, id=None, config=None):
        super().__init__(app, pipeline, id=None, config=None)

    def process(self, context, event):
        if "datetime_id" in event:
            new_event = [{
                "measurement": "ran",
                "tags": {
                    "eutrancell": event.get("eutrancell",float("NaN")),
                    "site": event.get("site",float("NaN"))
                },
                "time": self.get_timestamp(event),
                "fields": {
                    "data_volume_DL_GB": event.get("data_volume_DL_GB",float("NaN")),
                    "data_volume_UL_GB": event.get("data_volume_UL_GB",float("NaN")),
                    "data_thrg_DL_AVG_Mbps": event.get("data_thrg_DL_AVG_Mbps",float("NaN")),
                    "data_thrg_UL_AVG_Mbps": event.get("data_thrg_UL_AVG_Mbps",float("NaN")),
                    "data_thrg_active_UE_DL_Mbps": event.get("data_thrg_active_UE_DL_Mbps",float("NaN")),
                    "data_thrg_active_UE_UL_Mbps": event.get("data_thrg_active_UE_UL_Mbps",float("NaN")),
                    "RRC_connected_UE": event.get("RRC_connected_UE",float("NaN")),
                    "LTE_PRB_DL_Average_Usage": event.get("LTE_PRB_DL_Average_Usage",float("NaN")),
                    "LTE_PRB_DL_Max_Usage": event.get("LTE_PRB_DL_Max_Usage",float("NaN")),
                    "LTE_Ue_Active_DL_avg": event.get("LTE_Ue_Active_DL_avg",float("NaN")),
                    "LTE_Ue_Active_UL_avg": event.get("LTE_Ue_Active_UL_avg",float("NaN")),
                    "LTE_Ue_Active_DL_avg_time": event.get("LTE_Ue_Active_DL_avg_time",float("NaN")), 
                    "LTE_Ue_Active_DL_avgQCIall": event.get("LTE_Ue_Active_DL_avgQCIall",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI1_Percentage": event.get("LTE_Ue_Active_DL_avgQCI1_Percentage",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI5_Percentage": event.get("LTE_Ue_Active_DL_avgQCI5_Percentage",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI6_Percentage": event.get("LTE_Ue_Active_DL_avgQCI6_Percentage",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI7_Percentage": event.get("LTE_Ue_Active_DL_avgQCI7_Percentage",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI8_Percentage": event.get("LTE_Ue_Active_DL_avgQCI8_Percentage",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI9_Percentage": event.get("LTE_Ue_Active_DL_avgQCI9_Percentage",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI192_Percentage": event.get("LTE_Ue_Active_DL_avgQCI192_Percentage",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI1": event.get("LTE_Ue_Active_DL_avgQCI1",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI5": event.get("LTE_Ue_Active_DL_avgQCI5",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI6": event.get("LTE_Ue_Active_DL_avgQCI6",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI7": event.get("LTE_Ue_Active_DL_avgQCI7",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI8": event.get("LTE_Ue_Active_DL_avgQCI8",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI9": event.get("LTE_Ue_Active_DL_avgQCI9",float("NaN")),
                    "LTE_Ue_Active_DL_avgQCI192": event.get("LTE_Ue_Active_DL_avgQCI192",float("NaN")),
                    "LTE_PRB_DL_Percentage_usage" : event.get("LTE_PRB_DL_Percentage_usage",float("NaN")),
                    "LTE_PRB_UL_Average_Usage" : event.get("LTE_PRB_UL_Average_Usage",float("NaN")),
                    "LTE_PRB_UL_Percentage_usage" : event.get("LTE_PRB_UL_Percentage_usage",float("NaN")),
                    "LTE_QCI_Data_volume_DL_SUM" : event.get("LTE_QCI_Data_volume_DL_SUM",float("NaN")),
                    "LTE_QCI_Data_volume_UL_SUM" : event.get("LTE_QCI_Data_volume_UL_SUM",float("NaN")),
                    "pmPdcpVolDlDrbQci1": event.get("pmPdcpVolDlDrbQci1",float("NaN")),
                    "pmPdcpVolDlDrbQci5": event.get("pmPdcpVolDlDrbQci5",float("NaN")),
                    "pmPdcpVolDlDrbQci6": event.get("pmPdcpVolDlDrbQci6",float("NaN")),
                    "pmPdcpVolDlDrbQci7": event.get("pmPdcpVolDlDrbQci7",float("NaN")),
                    "pmPdcpVolDlDrbQci8": event.get("pmPdcpVolDlDrbQci8",float("NaN")),
                    "pmPdcpVolDlDrbQci9": event.get("pmPdcpVolDlDrbQci9",float("NaN")),
                    "pmPdcpVolDlDrbQci192": event.get("pmPdcpVolDlDrbQci192",float("NaN")),
                    "pmPdcpVolUlDrbQci1": event.get("pmPdcpVolUlDrbQci1",float("NaN")),
                    "pmPdcpVolUlDrbQci5": event.get("pmPdcpVolUlDrbQci5",float("NaN")),
                    "pmPdcpVolUlDrbQci6": event.get("pmPdcpVolUlDrbQci6",float("NaN")),
                    "pmPdcpVolUlDrbQci7": event.get("pmPdcpVolUlDrbQci7",float("NaN")),
                    "pmPdcpVolUlDrbQci8": event.get("pmPdcpVolUlDrbQci8",float("NaN")),
                    "pmPdcpVolUlDrbQci9": event.get("pmPdcpVolUlDrbQci9",float("NaN")),
                    "pmPdcpVolUlDrbQci192": event.get("pmPdcpVolUlDrbQci192",float("NaN")),
                    "pmActiveUeDlMax": event.get("pmActiveUeDlMax",float("NaN")),
                    "pmActiveUeUlMax": event.get("pmActiveUeUlMax",float("NaN")),
                    "LTE_PRB_1TTI_DL_AVAILABLE": event.get("LTE_PRB_1TTI_DL_AVAILABLE",float("NaN")),
                    "LTE_PRB_1TTI_UL_AVAILABLE": event.get("LTE_PRB_1TTI_UL_AVAILABLE",float("NaN"))}
            }]
            
            event = make_lines({'points': new_event})
            return event



    def get_timestamp(self,event):
        utc_time = datetime.strptime("{}".format(event.get("datetime_id")),"%Y-%m-%d %H:%M:%S")
        epoch_time = int((utc_time - datetime(1970,1,1)).total_seconds() * 1000000000)
        return epoch_time