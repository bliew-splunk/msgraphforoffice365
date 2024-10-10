from flask import Flask, request, abort
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


"""
https://learn.microsoft.com/en-us/graph/api/security-emailthreatsubmission-post-emailthreats?view=graph-rest-beta&tabs=http#http-request

Sample Request

POST https://graph.microsoft.com/beta/security/threatSubmission/emailThreats
Content-type: application/json

{
  "@odata.type": "#microsoft.graph.security.emailUrlThreatSubmission",
  "category": "spam",
  "recipientEmailAddress": "tifc@contoso.com",
  "messageUrl": "https://graph.microsoft.com/beta/users/c52ce8db-3e4b-4181-93c4-7d6b6bffaf60/messages/AAMkADU3MWUxOTU0LWNlOTEt="
}

Response
HTTP/1.1 201 Created
Content-type: application/json

{
  "@odata.context": "https://graph.microsoft.com/beta/$metadata#security/threatSubmission/emailThreatSubmission/$entity",
  "@odata.type": "#microsoft.graph.security.emailUrlThreatSubmission",
  "category": "spam",
  "recipientEmailAddress": "tifc@contoso.com",
  "id": "49c5ef5b-1f65-444a-e6b9-08d772ea2059",
  "createdDateTime": "2021-10-10T03:30:18.6890937Z",
  "contentType": "email",
  "emailSubject": "This is a spam",
  "status": "succeeded",
  "source": "administrator",
  "createdBy": {
    "user": {
      "identity": "c52ce8db-3e4b-4181-93c4-7d6b6bffaf60",
      "displayName": "Ronald Admin",
      "email": "tifc@contoso.com"
    }
  },
  "result": {
    "detail": "allowedByTenant",
    "category": "notSpam",
    "userMailboxSetting": "isFromDomainInDomainSafeList,isJunkMailRuleEnabled",
    "detectedUrls": ["contoso.com"],
    "detectedFiles": [
        {
            "fileName": "test.ps1",
            "fileHash": "hash of test.ps1"
        }
    ]
  },
  "adminReview": null,
  "internetMessageId": "some-internet-message-id@contoso.com",
  "sender": "test@contoso.com",
  "senderIP": "127.0.0.1",
  "receivedDateTime": "2021-10-09T03:30:18.6890937Z",
  "originalCategory": "notSpam",
  "attackSimulationInfo": null,
  "tenantAllowOrBlockListAction": null,
  "tenantId" : "39238e87-b5ab-4ef6-a559-af54c6b07b42"
}
"""


@app.route("/<tenant>/oauth2/v2.0/token", methods=["POST"])
def serve_mock_access_token(tenant):
    app.logger.info(f"Tenant: {tenant}")
    app.logger.info(f"Form: {request.form}")
    assert "client_id" in request.form
    assert "client_secret" in request.form
    # assert "code" in request.form
    assert "scope" in request.form

    # grant_type = request.form.get("grant_type")
    # assert grant_type == "authorization_code"

    return {
        "token_type": "Bearer",
        "expires_in": 3599,
        "ext_expires_in": 3599,
        "access_token": "this is a mock access token",
    }


@app.route("/v1.0/users")
def users():
    return {"users": []}


@app.route("/beta/security/threatSubmission/emailThreats", methods=["POST"])
def create_email_threat_submission():
    payload = request.json
    app.logger.info(f"Payload: {payload}")
    if "category" in payload:
        if payload["category"] == "error":
            abort(400)

    return {
        "@odata.context": "https://graph.microsoft.com/beta/$metadata#security/threatSubmission/emailThreatSubmission/$entity",
        "@odata.type": "#microsoft.graph.security.emailUrlThreatSubmission",
        "category": "spam",
        "recipientEmailAddress": "tifc@contoso.com",
        "id": "49c5ef5b-1f65-444a-e6b9-08d772ea2059",
        "createdDateTime": "2021-10-10T03:30:18.6890937Z",
        "contentType": "email",
        "emailSubject": "This is a spam",
        "status": "succeeded",
        "source": "administrator",
        "createdBy": {
            "user": {
                "identity": "c52ce8db-3e4b-4181-93c4-7d6b6bffaf60",
                "displayName": "Ronald Admin",
                "email": "tifc@contoso.com"
            }
        },
        "result": {
            "detail": "allowedByTenant",
            "category": "notSpam",
            "userMailboxSetting": "isFromDomainInDomainSafeList,isJunkMailRuleEnabled",
            "detectedUrls": ["contoso.com"],
            "detectedFiles": [
                {
                    "fileName": "test.ps1",
                    "fileHash": "hash of test.ps1"
                }
            ]
        },
        "internetMessageId": "some-internet-message-id@contoso.com",
        "sender": "test@contoso.com",
        "senderIP": "127.0.0.1",
        "receivedDateTime": "2021-10-09T03:30:18.6890937Z",
        "originalCategory": "notSpam",
        "tenantId": "39238e87-b5ab-4ef6-a559-af54c6b07b42"
    }, 201
