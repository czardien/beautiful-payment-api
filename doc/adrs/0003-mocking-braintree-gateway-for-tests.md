# 3. Mocking Braintree Gateway for tests

Date: 2020-04-29

## Status

Accepted

## Context

When writing tests for our view functions we follow strict isolation and idempotency principles. Hence it is a common practice to mock / stub database our 3rd party connections.

When working with Braintree we can use sandboxes for development purposes and it might also be used in the context of unit tests.

However we have observed that this resulted in non-idempotent tests on the /transaction/sale endpoint when two runs might either succeed or fail depending on the payment-method-nonce attribute with error: `Unknown or expired payment-method-nonce`.

## Decision

We will be mocking Braintree connections.

## Consequences

Testing remains idempotent. Testing modules which require a connection to Braintree will be responsible for mocking the connection.
