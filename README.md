
```
provide-client-params.lambda.ListFunctions
before-parameter-build.lambda.ListFunctions
before-call.lambda.ListFunctions
request-created.lambda.ListFunctions
choose-signer.lambda.ListFunctions
before-sign.lambda.ListFunctions
before-send.lambda.ListFunctions
response-received.lambda.ListFunctions
needs-retry.lambda.ListFunctions
after-call.lambda.ListFunctions
```

```
kwargs.event_name = 'response-received.*.*'
# OR
kwargs.event_name = 'after-call.lambda.ListFunctions'

# want
kwargs.prased_response.ResponseMetadata.RequestId
kwargs.prased_response.ResponseMetadata.HTTPStatusCode


```
