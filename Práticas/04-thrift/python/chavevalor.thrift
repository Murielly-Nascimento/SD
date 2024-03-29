namespace java chavevalor
namespace py chavevalor

exception KeyNotFound {
   1:i64 time,
   2:i32 key
}

service ChaveValor
{
    string getKV(1:i32 key) throws (1:KeyNotFound knf),
    bool setKV(1:i32 key, 2:string value),
    void delKV(1:i32 key)
}  

