import json

from c3po.db.metadata import insert_metadata


class DataService:
    @staticmethod
    def UpdateOrCreate(data):
        try:
            json_data = json.loads(data)
            insert_metadata(json_data["facebook_post"])
            return {"success": True}, 200
        except Exception:
            return {"success": False}, 500
