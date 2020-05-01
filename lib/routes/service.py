from flask import Response


def status():
    return Response(response="Ok", status="200")


def metrics():
    return Response(response="Not implemented", status="501")
