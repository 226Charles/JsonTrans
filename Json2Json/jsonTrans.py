import json
import math
import os

rec_path = "./enterprise/rectangle/Test-0008-100_jpg_Label.json"
tag_rec_path = "./TransResult/RecTransResult.json"
poly_path = "./enterprise/polygon/Test-0008-100_jpg_Label.json"
tag_poly_path = "./TransResult/PolyTransResult.json"
elps_path = "./enterprise/ellispe/Test-0008-100_jpg_Label.json"
tag_elps_path = "./TransResult/EllispeTransResult.json"
meas_path = "./enterprise/measure/Test-0008-100_jpg_Label.json"
tag_meas_path = "./TransResult/MeasureTransResult.json"
curve_path = "./enterprise/curve/Test-0008-100_jpg_Label.json"
tag_curve_path = "./TransResult/CurveTransResult.json"

# 递归遍历JSON数据并输出键值对
def traverse_json(data, prefix=""):
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            traverse_json(value, new_prefix)
    else:
        print(f"{prefix}: {data}")

#寻找特定值
def extract_value(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            result = extract_value(value, target_key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = extract_value(item, target_key)
            if result is not None:
                return result

def calc_angle(cos_value,sin_value):

    sin_value = -sin_value
    
    # 计算角度
    angle = math.atan2(sin_value, cos_value)

    # # 将弧度转换为角度
    angle_deg = math.degrees(angle)

    return angle_deg


def Rec_JSON_TRANS(rec_path, tag_rec_path):

    # 读取JSON文件
    with open(rec_path, 'r') as file:
        data = json.load(file)

    result_data = {
        extract_value(data, 'Name'): [
            {
                "diagnosis": [],
                "imageClass": [],
                "lesion": []
            }
        ]
    }

    result_lesions = result_data[extract_value(data, 'Name')][0]["lesion"]
    box = data["Models"]["BoundingBoxLabelModel"]
    width = data["FileInfo"]["Width"]
    height = data["FileInfo"]["Height"]
    depth = data["FileInfo"]["Depth"]

    for i, item in enumerate(box):
        new_lesion = {
                        "color": "#347caf",
                        "handles": {
                            "end": {
                                "x": item["p1"][0],
                                "y": item["p1"][1],
                                "active": False,
                                "moving": False,
                                "highlight": True
                            },
                            "start": {
                                "x": item["p2"][0],
                                "y": item["p2"][1],
                                "active": False,
                                "highlight": True
                            },
                            "textBox": {
                                "x": None ,
                                "y": None,
                                "active": False,
                                "hasMoved": False,
                                "boundingBox": {
                                    "top": None,
                                    "left": None,
                                    "width": width,
                                    "height": height
                                },
                                "hasBoundingBox": True,
                                "drawnIndependently": True,
                                "movesIndependently": False,
                                "allowedOutsideImage": True
                            },
                            "centerPoint": {
                                "x": (item["p1"][0] + item["p2"][0]) / 2,
                                "y": (item["p2"][0] + item["p2"][1]) / 2,
                                "z": depth
                            },
                            "initialRotation": calc_angle(item["RotateMatrix"][0],item["RotateMatrix"][1])
                        },
                        "toolType": "RectangleRoi",
                        "extra": {
                            "color": "#347caf",
                            "label": None,
                            "labelContent": {},
                            "nodeType": "check",
                            "lesionNumber": "1",
                            "instanceNumber": "1"
                        }
                    }
        result_lesions.append(new_lesion)

    json_data = json.dumps(result_data, indent=4)
    with open(tag_rec_path, 'w') as f:
        f.write(json_data)

def Poly_JSON_TRANS(poly_path, tag_poly_path):

    with open(poly_path, 'r') as file:
        data = json.load(file)

    result_data = {
        extract_value(data, 'Name'): [
            {
                "diagnosis": [],
                "imageClass": [],
                "lesion": []  
            }
        ]
    }

    result_lesions = result_data[extract_value(data, 'Name')][0]["lesion"]
    box = data["Polys"]
    width = data["FileInfo"]["Width"]
    height = data["FileInfo"]["Height"]
    depth = data["FileInfo"]["Depth"]

    for i, item in enumerate(box):
        new_lesion = {
                        "color": "#347caf",
                        "handles": {
                            "points": [],
                            "textBox": {
                                "x": None,
                                "y": None,
                                "active": False,
                                "hasMoved": False,
                                "boundingBox": {
                                    "top": None,
                                    "left": None,
                                    "width": width,
                                    "height": height
                                },
                                "hasBoundingBox": True,
                                "drawnIndependently": True,
                                "movesIndependently": False,
                                "allowedOutsideImage": True
                            },
                            "centerPoint": {
                                "x": 0,
                                "y": 0,
                                "z": 0
                            },
                            "invalidHandlePlacement": False
                        },
                        "toolType": "FreehandRoi",
                        "extra": {
                            "color": "#347caf",
                            "label": None,
                            "labelContent": {},
                            "nodeType": "check",
                            "lesionNumber": "1",
                            "instanceNumber": "1"
                        }
                }
        
        points = item["Shapes"][0]["Points"]

        firstx = 0
        firsty = 0
        lens = len(points)

        centerx = 0
        centery = 0
        centerz = 0

        for j, temp in enumerate(points):

            centerx += temp["Pos"][0]
            centery += temp["Pos"][1]
            centerz += temp["Pos"][2]

            if j == 0:
                firstx = temp["Pos"][0]
                firsty = temp["Pos"][1]
            if j != lens-1:
                temppoint = {
                                "x": temp["Pos"][0],
                                "y": temp["Pos"][1],
                                "lines": [
                                    {
                                        "x": points[j+1]["Pos"][0],
                                        "y": points[j+1]["Pos"][1]
                                    }
                                ],
                                "active": True,
                                "highlight": True
                            }
                new_lesion["handles"]["points"].append(temppoint)
            else:
                temppoint = {
                                "x": temp["Pos"][0],
                                "y": temp["Pos"][1],
                                "lines": [
                                    {
                                        "x": firstx,
                                        "y":firsty
                                    }
                                ],
                                "active": True,
                                "highlight": True
                            }
                new_lesion["handles"]["points"].append(temppoint)

        new_lesion["handles"]["centerPoint"]["x"] = centerx / lens
        new_lesion["handles"]["centerPoint"]["y"] = centery / lens
        new_lesion["handles"]["centerPoint"]["z"] = centerz / lens

        result_lesions.append(new_lesion)

    json_data = json.dumps(result_data, indent=4)
    with open(tag_poly_path, 'w') as f:
        f.write(json_data)

def Ellipse_JSON_TRANS(elps_path,tag_elps_path):
    # 读取JSON文件
    with open(elps_path, 'r') as file:
        data = json.load(file)

    result_data = {
        extract_value(data, 'Name'): [
            {
                "diagnosis": [],
                "imageClass": [],
                "lesion": []
            }
        ]
    }

    result_lesions = result_data[extract_value(data, 'Name')][0]["lesion"]
    box = data["Models"]["EllipseModel"]
    width = data["FileInfo"]["Width"]
    height = data["FileInfo"]["Height"]
    depth = data["FileInfo"]["Depth"]

    for i, item in enumerate(box):
        new_lesion = {
                        "color": "#347caf",
                        "handles": {
                            "end": {
                                "x": item["Center"][0] + item["MajorAxis"]/2,
                                "y": item["Center"][1] + item["MinorAxis"]/2,
                                "active": False,
                                "moving": False,
                                "highlight": True
                            },
                            "start": {
                                "x": item["Center"][0] - item["MajorAxis"]/2,
                                "y": item["Center"][1] - item["MinorAxis"]/2,
                                "active": False,
                                "highlight": True
                            },
                            "textBox": {
                                "x": None ,
                                "y": None,
                                "active": False,
                                "hasMoved": False,
                                "boundingBox": {
                                    "top": None,
                                    "left": None,
                                    "width": width,
                                    "height": height
                                },
                                "hasBoundingBox": True,
                                "drawnIndependently": True,
                                "movesIndependently": False,
                                "allowedOutsideImage": True
                            },
                            "centerPoint": {
                                "x": item["Center"][0],
                                "y": item["Center"][1],
                                "z": depth
                            },
                            "initialRotation": "0"
                        },
                        "toolType": "EllipticalRoi",
                        "extra": {
                            "color": "#347caf",
                            "label": None,
                            "labelContent": {},
                            "nodeType": "check",
                            "lesionNumber": "1",
                            "instanceNumber": "1"
                        }
                    }
        result_lesions.append(new_lesion)

    json_data = json.dumps(result_data, indent=4)
    with open(tag_elps_path, 'w') as f:
        f.write(json_data)

def Measure_JSON_TRANS(meas_path,tag_meas_path):
     # 读取JSON文件
    with open(meas_path, 'r') as file:
        data = json.load(file)

    result_data = {
        extract_value(data, 'Name'): [
            {
                "diagnosis": [],
                "imageClass": [],
                "lesion": []
            }
        ]
    }

    result_lesions = result_data[extract_value(data, 'Name')][0]["lesion"]
    box = data["Models"]["MeasureModel"]
    width = data["FileInfo"]["Width"]
    height = data["FileInfo"]["Height"]
    depth = data["FileInfo"]["Depth"]

    for i, item in enumerate(box):
        new_lesion = {
                        "color": "#347caf",
                        "handles": {
                            "end": {
                                "x": item["Pos"]["p1"][0],
                                "y": item["Pos"]["p1"][1],
                                "active": False,
                                "moving": False,
                                "highlight": True
                            },
                            "start": {
                                "x": item["Pos"]["p2"][0],
                                "y": item["Pos"]["p2"][1],
                                "active": False,
                                "highlight": True
                            },
                            "textBox": {
                                "x": None ,
                                "y": None,
                                "active": False,
                                "hasMoved": False,
                                "boundingBox": {
                                    "top": None,
                                    "left": None,
                                    "width": width,
                                    "height": height
                                },
                                "hasBoundingBox": True,
                                "drawnIndependently": True,
                                "movesIndependently": False,
                                "allowedOutsideImage": True
                            },
                            "centerPoint": {
                                "x": (item["Pos"]["p1"][0]+item["Pos"]["p2"][0])/2,
                                "y": (item["Pos"]["p1"][1]+item["Pos"]["p2"][1])/2,
                                "z": depth
                            }
                        },
                        "toolType": "Length",
                        "extra": {
                            "color": "#347caf",
                            "label": None,
                            "labelContent": {},
                            "nodeType": "check",
                            "lesionNumber": "1",
                            "instanceNumber": "1"
                        }
                    }
        result_lesions.append(new_lesion)

    json_data = json.dumps(result_data, indent=4)
    with open(tag_meas_path, 'w') as f:
        f.write(json_data)

def Curve_JSON_TRANS(curve_path,tag_curve_path):
    with open(curve_path, 'r') as file:
        data = json.load(file)

    result_data = {
        extract_value(data, 'Name'): [
            {
                "diagnosis": [],
                "imageClass": [],
                "lesion": []  
            }
        ]
    }

    result_lesions = result_data[extract_value(data, 'Name')][0]["lesion"]
    box = data["Curves"]
    width = data["FileInfo"]["Width"]
    height = data["FileInfo"]["Height"]
    depth = data["FileInfo"]["Depth"]

    for i, item in enumerate(box):
        new_lesion = {
                        "color": "#347caf",
                        "handles": {
                            "points": [],
                            "textBox": {
                                "x": None,
                                "y": None,
                                "active": False,
                                "hasMoved": False,
                                "boundingBox": {
                                    "top": None,
                                    "left": None,
                                    "width": width,
                                    "height": height
                                },
                                "hasBoundingBox": True,
                                "drawnIndependently": True,
                                "movesIndependently": False,
                                "allowedOutsideImage": True
                            },
                            "centerPoint": {
                                "x": 0,
                                "y": 0,
                                "z": 0
                            },
                            "invalidHandlePlacement": False
                        },
                        "toolType": "CurveTool",
                        "extra": {
                            "color": "#347caf",
                            "label": None,
                            "labelContent": {},
                            "nodeType": "check",
                            "lesionNumber": "1",
                            "instanceNumber": "1"
                        }
                }
        
        points = item["Shapes"][0]["Points"]

        firstx = 0
        firsty = 0
        lens = len(points)

        centerx = 0
        centery = 0
        centerz = 0

        for j, temp in enumerate(points):

            centerx += temp["Pos"][0]
            centery += temp["Pos"][1]
            centerz += temp["Pos"][2]

            if j == 0:
                firstx = temp["Pos"][0]
                firsty = temp["Pos"][1]
            if j != lens-1:
                temppoint = {
                                "x": temp["Pos"][0],
                                "y": temp["Pos"][1],
                                "lines": [
                                    {
                                        "x": points[j+1]["Pos"][0],
                                        "y": points[j+1]["Pos"][1]
                                    }
                                ],
                                "active": True,
                                "highlight": True
                            }
                new_lesion["handles"]["points"].append(temppoint)
            else:
                temppoint = {
                                "x": temp["Pos"][0],
                                "y": temp["Pos"][1],
                                "lines": [
                                    {
                                        "x": firstx,
                                        "y":firsty
                                    }
                                ],
                                "active": True,
                                "highlight": True
                            }
                new_lesion["handles"]["points"].append(temppoint)

        new_lesion["handles"]["centerPoint"]["x"] = centerx / lens
        new_lesion["handles"]["centerPoint"]["y"] = centery / lens
        new_lesion["handles"]["centerPoint"]["z"] = centerz / lens

        result_lesions.append(new_lesion)

    json_data = json.dumps(result_data, indent=4)
    with open(tag_curve_path, 'w') as f:
        f.write(json_data)

if __name__ == '__main__':

    Rec_JSON_TRANS(rec_path=rec_path, tag_rec_path=tag_rec_path)
    Poly_JSON_TRANS(poly_path=poly_path,tag_poly_path=tag_poly_path)
    Ellipse_JSON_TRANS(elps_path=elps_path,tag_elps_path=tag_elps_path)
    Measure_JSON_TRANS(meas_path=meas_path,tag_meas_path=tag_meas_path)
    Curve_JSON_TRANS(curve_path=curve_path,tag_curve_path=tag_curve_path)