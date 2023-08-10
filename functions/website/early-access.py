from vecul.utils import table, MySchema, make_response, context as logger
from marshmallow import ValidationError, fields


class InputSchema(MySchema):
    email = fields.Email(required=True)
    name = fields.String(required=True)


def lambda_handler(event, _):
    status_code = 400
    resp = {"error": True, "success": False, "data": ""}
    try:
        payload = InputSchema().loads(event["body"])
        item = {"pk": "early_access", "sk": payload["email"], "name": payload["name"]}
        table.put_item(Item=item)
        status_code = 200
        resp["error"], resp["success"] = False, True
        resp["message"] = "Your information has been received successfully. Thank you!"
    except ValueError as e:
        logger.error(e)
        resp["message"] = str(e)
    except ValidationError as e:
        logger.error(e)
        resp["message"] = e.messages
    except Exception as e:
        logger.error(e)
        status_code = 500

    return make_response(status_code, resp)
