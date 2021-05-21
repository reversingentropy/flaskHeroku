from model.DatabasePool import DatabasePool

class Furniture:
    @classmethod
    def getFurnitureByCat(cls,catid):
        dbConn = DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)
        sql = "SELECT furniture.cat_id,category.cat_name,category.cat_description, furniture.dimension, furniture.images, furniture.it_id, furniture.item_code, furniture.name, furniture.price, furniture.quantity FROM furniture,category WHERE category.cat_id = furniture.cat_id = %s "
        cursor.execute(sql,(catid,))
        Furniture = cursor.fetchall()
        dbConn.close()
        return Furniture