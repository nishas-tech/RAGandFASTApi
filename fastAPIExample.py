from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from qa_answer_with_rag import get_llm_response

app=FastAPI()

class Todo(BaseModel):
    text:str = None
    title: str = None
    is_done:bool=False


items=[]

@app.get("/")
def root():
    return {"message":"Hello World from FastAPI"}

@app.get("/items")
def list_items(limit:int=10):
    return items[0:limit]

@app.get("/items/{item_id}",response_model=Todo)
def get_item(item_id:int) -> Todo:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404,detail=f"Item {item_id} not found")

@app.get("/items/item/{item_name}")
def get_itemname(item_name:str):
    # for item in items:
    #     if item.title == item_name:
    #         return item
    return item_name
    #raise HTTPException(status_code=404,detail=f"Item {item_name} not found")

@app.put("/items/{item_id}/{item_name}")
def update_item(item_id:int,item_name:str):
        if item_id < len(items):
            items[item_id].text=item_name
            return items[item_id]
        else:
            raise HTTPException(status_code=404,detail=f"Item {item_name} not found")


@app.post("/items",response_model=list[Todo])
def create_item(item:Todo):
    items.append(item)
    return items

@app.post("/ask")
def ask_question(question: str):
    try:
        response = get_llm_response(question)
        return {"question": question, "answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))