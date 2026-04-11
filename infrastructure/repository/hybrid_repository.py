# async def get_all_by_chat_id(self, chat_id: int):
#     try:
#         cursor = mongo.get_database.get_collection("messages").find({"chat_id": chat_id})
#         return await cursor.to_list(length=None)
#     except Exception as e:
#         print(f"Error getting messages by chat id: {e}")
#         raise e
