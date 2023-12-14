import csv
import numpy as np

WIDTH_ROAD = 3.650 
WIDTH_LANE = WIDTH_ROAD/2

def check_out_of_lane(max_lane_offset):
    check = (WIDTH_ROAD/4) + (max_lane_offset)
    if check > WIDTH_LANE:
        return False 
    else:
        return True 

def get_time_sim_from_csv(csv_file):
    time_sim_column = []
    with open(csv_file, newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)

        for row in csv_reader:
            time_sim = row[0]
            time_sim_column.append(time_sim)
        time_sim_column_float = []
        for string in time_sim_column:
            try:
                float_value = float(string)
                time_sim_column_float.append(float_value)
            except ValueError:
                float_value = 0
                time_sim_column_float.append(float_value)
    time_simulation = max(time_sim_column_float)
    return time_simulation

def get_max_lane_offset_from_csv(csv_file):
    lane_offset_column = []
    with open(csv_file, newline='') as file1:
        csv_reader1 = csv.reader(file1)
        next(csv_reader1, None)
        for row in csv_reader1:
            numero_colonne = len(row)
            if numero_colonne > 8:
                laneoffset = row[8] 
                lane_offset_column.append(laneoffset)
        lane_offset_column_float = []
        for string in lane_offset_column:
            try:
                float_value = float(string)
                lane_offset_column_float.append(float_value)
            except ValueError:                
                float_value = 0
    lane_offset_column_float_absolute = [abs(valore) for valore in lane_offset_column_float]
    valore_max_lane_offset = max(lane_offset_column_float_absolute)

    if (valore_max_lane_offset*100) >= 100: #fix RdbSniffer fails
        lane_offset_column_float_absolute = sorted(lane_offset_column_float_absolute)
        valore_max_lane_offset = lane_offset_column_float_absolute[-2]
    return valore_max_lane_offset * 100 #convert to cm 
