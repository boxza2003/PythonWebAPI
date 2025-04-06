from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

app = FastAPI()
#uvicorn main:app --reload 
#--reload: 當程式碼改變時 server 會自動重啟，只會於開發時使用

class Device(BaseModel):
    idno: str
    name: str
    data: str

class Rtn(BaseModel):
    code: int
    info: str
    data: Optional[Any] = None

class DeviceQuery(BaseModel):
    idno: str

device_db: Dict[str, Device] = {}

device_db = {
    "123A": Device(idno="123A", name="電磁閥A", data="資料1"),
    "123B": Device(idno="123B", name="電磁閥B", data="資料2"),
    "123C": Device(idno="123C", name="電磁閥C", data="資料3")
}

@app.get("/getDevices", response_model=Rtn)
def get_devices():
    return Rtn(code=0, info="", data=device_db)


@app.get("/getDevice/{idno}", response_model=Rtn)
def get_device(idno: str):
    try:
        if idno not in device_db:
            #raise HTTPException(status_code=404, detail=f"找不到 idno={idno}")
            return Rtn(code=1, info=f"查無idno={idno}資料")        
        return Rtn(code=0, info="", data=device_db[idno])    
    except Exception as e:
        return Rtn(code=99, info=str(e))
    

#用json傳入值話，需改成post
@app.post("/qryDevice", response_model=Rtn)
def qry_device(qry: DeviceQuery):
    try:
        if qry.idno not in device_db:
            return Rtn(code=1, info=f"查無idno={qry.idno}資料")    
        return Rtn(code=0, info="", data=device_db[qry.idno])
    except Exception as e:
        return Rtn(code=99, info=str(e))


@app.post("/addDevice", response_model=Rtn)
def add_device(device: Device):
    try:
        if device.idno in device_db:
            #raise HTTPException(status_code=404, detail=f"idno={device.idno}已存在，無法新增")
            return Rtn(code=2, info=f"idno={device.idno}已存在，無法新增")        
        device_db[device.idno] = device
        return Rtn(code=0, info="")
    except Exception as e:
        return Rtn(code=99, info=str(e))


@app.put("/updDevice", response_model=Rtn)
def upd_device(device: Device):
    try:
        if device.idno not in device_db:            
            return Rtn(code=3, info=f"查無idno={device.idno}資料，無法更新")        
        device_db[device.idno] = device
        return Rtn(code=0, info="")    
    except Exception as e:
        return Rtn(code=99, info=str(e))


@app.delete("/delDevice", response_model=Rtn)
def del_device(device: Device):
    try:
        if device.idno not in device_db:
            return Rtn(code=4, info=f"查無idno={device.idno}資料，無法刪除")        
        del device_db[device.idno]
        return Rtn(code=0, info="")
    except Exception as e:
        return Rtn(code=99, info=str(e))
    