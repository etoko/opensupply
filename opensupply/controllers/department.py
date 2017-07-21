
import transaction

from sqlalchemy import desc

from opensupply.models import DBSession, Department
from opensupply.controllers import ApiController
from opensupply.models import User


class DepartmentController(ApiController):
    """
    Class controls all CRUD operations on the Deparmtent model instances
    """
    id = 0;
    name = None
    created_by = None
    created_date = None
    modified_by = None
    modified_on = None
    items = {}

    def set_attributes(self, j_department):
        self.id = int(j_department.pop("department.id"))
        self.name = j_department.pop("department.name")
        #self.created_by = j_department.pop("department.created_by")
        #self.created_on = j_department.pop("department.created_on")
        #self.modified_by = j_department.pop("department.modified_by")
        #self.modified_on = j_department.pop("department.modified_on")
        #self.items = j_department.pop("department.items")

    def _valid(j_department):
        """
        Checks the validity of the dictionary to determine whether it is valid
        "enough" to be used to create or update a Department instance
        """
        try:
            department_id = j_department.pop("department.id")
            return department_id >=-1

        except KeyError as err:
            print(err)
            return False
        return False
    
    def _set_department(self, department):
        #user = User.get_by_username(self.modified_by)
        department.name = self.name
        #department.created_by = user.id
        #department.modified_by = user.id
        #department.modified_on = self.modified_on
        #department.items = self.items
        
        return department

    def _to_json(self, department):
        """
        Jsonify the sql alchemy query result. Skips attr starting with "_"
        """
        if department is None:
            #pass
            print("None Department")

        j_department = {"name": department.name, "id": department.id}
        
        return j_department

    def save(self, j_department):
        """
        Function creates and updates a Department instance
        """
        self.set_attributes(dict(j_department))
        department = self._set_department(Department(self.name))
        
        def _create(department):
            with transaction.manager:
                DBSession.add(department)
                department = transaction.commit()

        def _update(department):
            department = self.get(self.id)
            print("DEPARTMENT ID: " + str(self.id))
            
            with transaction.manager:
                department = DBSession.query(Department).get(self.id)
                department.name = self.name
                department = DBSession.merge(department)
                transaction.commit()

        _create(department) if self.id == -1 else _update(department) 
        return self._to_json(department)

    def get(self, *args, **kwargs):
        department_id = 0
        if len(args):
            department_id = args[0] 
            return self._to_json(DBSession.query(Department).\
                get(int(department_id)))
        elif kwargs:
             try:
                 if kwargs['FIRST']:
                     return self._to_json(DBSession.query(Department).order_by(\
                         Department.id).first())
             except KeyError as err:
                 #Return last because first failed!
                 return self._to_json(DBSession.query(Department).order_by( \
                     desc(Department.id)).first())
        elif not len(args) and not len(kwargs):
            return DBSession.query(Department).\
              filter(Department.voided == False).all()

        return False
#            print("Department is: ", department_id)
#            try:
#                department_id = kwargs.pop("department.id")
#                print "department_id from get:", department_id
#                return DBSession.query(Department).get(int(department_id)).first()
#            except KeyError as err:
#                print err
#                #return DBSession.query(Department).all()
#            return None

    def delete(self, j_department):
        self.set_attributes(j_department)
        department = self.get(self.id)
        department.voided = True
     
        with transaction.manager:
            DBSession.merge(department)
            transaction.commit()

