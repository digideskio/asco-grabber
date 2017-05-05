from ..core.application import Application


def put_application_instance_into_context(application: Application, context):
    context.obj = application


def extract_application_instance_from_context(context) -> Application:
    return context.obj
