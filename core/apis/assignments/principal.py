from flask import Blueprint,Flask, jsonify, make_response
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema
principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_principal_assignments(p):
    assignments = Assignment.get_graded_assignments()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def update_gra(p,incoming_payload):
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Extract 'id' and 'grade' directly from the loaded payload
    assignment_id = grade_assignment_payload.id
    grade = grade_assignment_payload.grade
    status,assignment = Assignment.update_grade(assignment_id,grade)
    if status==400:
        data= {"data":"Error"}
        return make_response(jsonify(data),400)
    else:
        assignments_dump = AssignmentSchema().dump(assignment)
        return APIResponse.respond(data=assignments_dump)

@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teacher(p):
    assignments = Teacher.get_all_teachers(p.user_id)
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


